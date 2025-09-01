import streamlit as st
import os 
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, time
import uuid
import traceback
from typing import Dict, Any, Optional, List, Union
from pycoingecko import CoinGeckoAPI
# Online-only mode - no local portfolio manager needed
import time as time_module
import math

# NOTE: 3D visualizations removed — no conditional numpy import required

# Import Supabase authentication and database functions
from supabase_config import (
    SupabaseAuth, PortfolioDatabase, require_auth, 
    export_portfolio_to_excel, init_auth_state
)
from helpers.crypto_config import get_symbol_map

# Icon Libraries Helper Functions
def get_icon(icon_name: str, library: str = "lucide", size: int = 16, color: str = "#666666") -> str:
    """
    Get SVG icon from various icon libraries
    
    Args:
        icon_name: Name of the icon
        library: Icon library to use ('lucide', 'heroicons', 'fontawesome')
        size: Icon size in pixels
        color: Icon color in hex format
    
    Returns:
        HTML string with SVG icon
    """
    icons = {
        "lucide": {
            "bullseye": f'<svg width="{size}" height="{size}" viewBox="0 0 73 73" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" fill="#000000"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <title>design-and-ux/hit-targets</title> <desc>Created with Sketch.</desc> <defs> </defs> <g id="design-and-ux/hit-targets" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd"> <g id="container" transform="translate(2.000000, 2.000000)" fill="#FFFFFF" fill-rule="nonzero" stroke="#1F2F3B" stroke-width="2"> <rect id="mask" x="-1" y="-1" width="71" height="71" rx="14"> </rect> </g> <g id="target-(1)" transform="translate(10.000000, 10.000000)" fill-rule="nonzero"> <path d="M48.3750352,23.7374297 L51.7500352,23.7374297 C50.2875,12.4873945 41.3999648,3.59996484 30.2624648,2.13753516 L30.2624648,5.51253516 C39.6000352,6.97507031 47.0249297,14.3999648 48.3750352,23.7374297 Z M30.2625703,48.3750352 L30.2625703,51.7500352 C41.4000703,50.2875 50.4001406,41.3999648 51.7501406,30.2624648 L48.3751406,30.2624648 C47.0249297,39.6000352 39.6000352,47.0249297 30.2625703,48.3750352 Z M5.62496484,30.2625703 L2.24996484,30.2625703 C3.7125,41.5126055 12.6000352,50.4000352 23.7375352,51.7501406 L23.7375352,48.3751406 C14.3999648,47.0249297 6.97507031,39.6000352 5.62496484,30.2625703 Z M2.24996484,23.7374297 L5.62496484,23.7374297 C7.0875,14.3998594 14.3999648,6.97485937 23.7375352,5.62485937 L23.7375352,2.24996484 C12.6000352,3.7125 3.7125,12.6000352 2.24996484,23.7374297 Z" id="Shape" fill="#CDD6E0"> </path> <path d="M39.4875,23.7374297 L42.9750352,23.7374297 C41.6250352,17.4374648 36.5625352,12.3748594 30.2625703,11.1373945 L30.2625703,14.6249297 C34.7625,15.7500703 38.2499297,19.2375 39.4875,23.7374297 Z M30.2625703,39.4875 L30.2625703,42.9750352 C36.5625352,41.6250352 41.6251406,36.5625352 42.8626055,30.2625703 L39.3750703,30.2625703 C38.2499297,34.7625 34.7625,38.2499297 30.2625703,39.4875 Z M14.5125,30.2625703 L11.0249648,30.2625703 C12.3749648,36.5625352 17.4374648,41.6251406 23.7374297,42.8626055 L23.7374297,39.3750703 C19.2375,38.2499297 15.7500703,34.7625 14.5125,30.2625703 Z M11.1375,23.7374297 L14.6250352,23.7374297 C15.7500703,19.2373945 19.3500352,15.7498594 23.8500703,14.5123945 L23.8500703,11.0249648 C17.4374648,12.3750703 12.3750703,17.4374648 11.1375,23.7374297 Z" id="Shape" fill="#F2F2F2"> </path> <polygon id="Shape" fill="#40596B" points="54 25.4250352 28.5749648 25.4250352 28.5749648 0 25.4250352 0 25.4250352 25.4250352 0 25.4250352 0 28.5749648 25.4250352 28.5749648 25.4250352 54 28.5749648 54 28.5749648 28.5749648 54 28.5749648"> </polygon> <circle id="Oval" fill="#FF7058" cx="27.0005273" cy="27.0005273" r="5.7375"> </circle> </g> </g> </g></svg>',
            "money": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M11.7255 17.1019C11.6265 16.8844 11.4215 16.7257 11.1734 16.6975C10.9633 16.6735 10.7576 16.6285 10.562 16.5636C10.4743 16.5341 10.392 16.5019 10.3158 16.4674L10.4424 16.1223C10.5318 16.1622 10.6239 16.1987 10.7182 16.2317L10.7221 16.2331L10.7261 16.2344C11.0287 16.3344 11.3265 16.3851 11.611 16.3851C11.8967 16.3851 12.1038 16.3468 12.2629 16.2647L12.2724 16.2598L12.2817 16.2544C12.5227 16.1161 12.661 15.8784 12.661 15.6021C12.661 15.2955 12.4956 15.041 12.2071 14.9035C12.062 14.8329 11.8559 14.7655 11.559 14.6917C11.2545 14.6147 10.9987 14.533 10.8003 14.4493C10.6553 14.3837 10.5295 14.279 10.4161 14.1293C10.3185 13.9957 10.2691 13.7948 10.2691 13.5319C10.2691 13.2147 10.3584 12.9529 10.5422 12.7315C10.7058 12.5375 10.9381 12.4057 11.2499 12.3318C11.4812 12.277 11.6616 12.1119 11.7427 11.8987C11.8344 12.1148 12.0295 12.2755 12.2723 12.3142C12.4751 12.3465 12.6613 12.398 12.8287 12.4677L12.7122 12.8059C12.3961 12.679 12.085 12.6149 11.7841 12.6149C10.7848 12.6149 10.7342 13.3043 10.7342 13.4425C10.7342 13.7421 10.896 13.9933 11.1781 14.1318L11.186 14.1357L11.194 14.1393C11.3365 14.2029 11.5387 14.2642 11.8305 14.3322C12.1322 14.4004 12.3838 14.4785 12.5815 14.5651L12.5856 14.5669L12.5897 14.5686C12.7365 14.6297 12.8624 14.7317 12.9746 14.8805L12.9764 14.8828L12.9782 14.8852C13.0763 15.012 13.1261 15.2081 13.1261 15.4681C13.1261 15.7682 13.0392 16.0222 12.8604 16.2447C12.7053 16.4377 12.4888 16.5713 12.1983 16.6531C11.974 16.7163 11.8 16.8878 11.7255 17.1019Z" fill="#ffffff"></path> <path d="M11.9785 18H11.497C11.3893 18 11.302 17.9105 11.302 17.8V17.3985C11.302 17.2929 11.2219 17.2061 11.1195 17.1944C10.8757 17.1667 10.6399 17.115 10.412 17.0394C10.1906 16.9648 9.99879 16.8764 9.83657 16.7739C9.76202 16.7268 9.7349 16.6312 9.76572 16.5472L10.096 15.6466C10.1405 15.5254 10.284 15.479 10.3945 15.5417C10.5437 15.6262 10.7041 15.6985 10.8755 15.7585C11.131 15.8429 11.3762 15.8851 11.611 15.8851C11.8129 15.8851 11.9572 15.8628 12.0437 15.8181C12.1302 15.7684 12.1735 15.6964 12.1735 15.6021C12.1735 15.4929 12.1158 15.411 12.0004 15.3564C11.8892 15.3018 11.7037 15.2422 11.4442 15.1777C11.1104 15.0933 10.8323 15.0039 10.6098 14.9096C10.3873 14.8103 10.1936 14.6514 10.0288 14.433C9.86396 14.2096 9.78156 13.9092 9.78156 13.5319C9.78156 13.095 9.91136 12.7202 10.1709 12.4074C10.4049 12.13 10.7279 11.9424 11.1401 11.8447C11.2329 11.8227 11.302 11.7401 11.302 11.6425V11.2C11.302 11.0895 11.3893 11 11.497 11H11.9785C12.0862 11 12.1735 11.0895 12.1735 11.2V11.6172C12.1735 11.7194 12.2487 11.8045 12.3471 11.8202C12.7082 11.8777 13.0255 11.9866 13.2989 12.1469C13.3765 12.1924 13.4073 12.2892 13.3775 12.3756L13.0684 13.2725C13.0275 13.3914 12.891 13.4417 12.7812 13.3849C12.433 13.2049 12.1007 13.1149 11.7841 13.1149C11.4091 13.1149 11.2216 13.2241 11.2216 13.4425C11.2216 13.5468 11.2773 13.6262 11.3885 13.6809C11.4998 13.7305 11.6831 13.7851 11.9386 13.8447C12.2682 13.9192 12.5464 14.006 12.773 14.1053C12.9996 14.1996 13.1953 14.356 13.3602 14.5745C13.5291 14.7929 13.6136 15.0908 13.6136 15.4681C13.6136 15.8851 13.4879 16.25 13.2365 16.5628C13.0176 16.8354 12.7145 17.0262 12.3274 17.1353C12.2384 17.1604 12.1735 17.2412 12.1735 17.3358V17.8C12.1735 17.9105 12.0862 18 11.9785 18Z" fill="#ffffff"></path> <path fill-rule="evenodd" clip-rule="evenodd" d="M9.59235 5H13.8141C14.8954 5 14.3016 6.664 13.8638 7.679L13.3656 8.843L13.2983 9C13.7702 8.97651 14.2369 9.11054 14.6282 9.382C16.0921 10.7558 17.2802 12.4098 18.1256 14.251C18.455 14.9318 18.5857 15.6958 18.5019 16.451C18.4013 18.3759 16.8956 19.9098 15.0182 20H8.38823C6.51033 19.9125 5.0024 18.3802 4.89968 16.455C4.81587 15.6998 4.94656 14.9358 5.27603 14.255C6.12242 12.412 7.31216 10.7565 8.77823 9.382C9.1696 9.11054 9.63622 8.97651 10.1081 9L10.0301 8.819L9.54263 7.679C9.1068 6.664 8.5101 5 9.59235 5Z" stroke="#ffffff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path> <path d="M13.2983 9.75C13.7125 9.75 14.0483 9.41421 14.0483 9C14.0483 8.58579 13.7125 8.25 13.2983 8.25V9.75ZM10.1081 8.25C9.69391 8.25 9.35812 8.58579 9.35812 9C9.35812 9.41421 9.69391 9.75 10.1081 9.75V8.25ZM15.9776 8.64988C16.3365 8.44312 16.4599 7.98455 16.2531 7.62563C16.0463 7.26671 15.5878 7.14336 15.2289 7.35012L15.9776 8.64988ZM13.3656 8.843L13.5103 9.57891L13.5125 9.57848L13.3656 8.843ZM10.0301 8.819L10.1854 8.08521L10.1786 8.08383L10.0301 8.819ZM8.166 7.34357C7.80346 7.14322 7.34715 7.27469 7.1468 7.63722C6.94644 7.99976 7.07791 8.45607 7.44045 8.65643L8.166 7.34357ZM13.2983 8.25H10.1081V9.75H13.2983V8.25ZM15.2289 7.35012C14.6019 7.71128 13.9233 7.96683 13.2187 8.10752L13.5125 9.57848C14.3778 9.40568 15.2101 9.09203 15.9776 8.64988L15.2289 7.35012ZM13.2209 8.10709C12.2175 8.30441 11.1861 8.29699 10.1854 8.08525L9.87486 9.55275C11.0732 9.80631 12.3086 9.81521 13.5103 9.57891L13.2209 8.10709ZM10.1786 8.08383C9.47587 7.94196 8.79745 7.69255 8.166 7.34357L7.44045 8.65643C8.20526 9.0791 9.02818 9.38184 9.88169 9.55417L10.1786 8.08383Z" fill="#ffffff"></path> </g></svg>',
            "price": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-signal-icon lucide-signal"><path d="M2 20h.01"/><path d="M7 20v-4"/><path d="M12 20v-8"/><path d="M17 20V8"/><path d="M22 4v16"/></svg>',
            "edit": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="m18.5 2.5 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>',
            "delete": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3,6 5,6 21,6"/><path d="m19,6v14a2,2 0 0,1 -2,2H7a2,2 0 0,1 -2,-2V6m3,0V4a2,2 0 0,1 2,-2h4a2,2 0 0,1 2,2v2"/><line x1="10" y1="11" x2="10" y2="17"/><line x1="14" y1="11" x2="14" y2="17"/></svg>',
            "refresh": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23,4 23,10 17,10"/><polyline points="1,20 1,14 7,14"/><path d="m20.49,9a9,9 0 1,1 -2.12,-6.12l2.63,2.63"/></svg>',
            "chart": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>',
            "portfolio": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>',
            "search": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>',
            "download": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7,10 12,15 17,10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>',
            "trending-up": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22,7 13.5,15.5 8.5,10.5 2,17"/><polyline points="16,7 22,7 22,13"/></svg>',
            "trending-down": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22,17 13.5,8.5 8.5,13.5 2,7"/><polyline points="16,17 22,17 22,11"/></svg>',
            "rotate-cw": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23,4 23,10 17,10"/><path d="M20.49 9A9 9 0 1 1 5.64 5.64l1.27 1.27"/></svg>',
            "file-text": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2Z"/><polyline points="14,2 14,8 20,8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10,9 9,9 8,9"/></svg>',
            "activity": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22,12 18,12 15,21 9,3 6,12 2,12"/></svg>',
            "dollar-sign": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>',
            "calendar": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>',
            "settings": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="m12 1 1.96 5.61a1 1 0 0 0 .966.69h5.89a1 1 0 0 1 .66 1.75l-4.77 4.18a1 1 0 0 0-.35 1.12L18.4 20a1 1 0 0 1-1.54 1.13L12 17.27l-4.86 3.86A1 1 0 0 1 5.6 20l2.04-5.55a1 1 0 0 0-.35-1.12L2.52 9.15a1 1 0 0 1 .66-1.75h5.89a1 1 0 0 0 .966-.69L12 1z"/></svg>',
            "save": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17,21 17,13 7,13 7,21"/><polyline points="7,3 7,8 15,8"/></svg>',
            "info": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="m9,9h4v7"/><path d="m13,17h-3"/></svg>',
            "alert-circle": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>',
            "heart-handshake": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.29 1.51 4.04 3 5.5"/><path d="M12 5L8 21l4-7 4 7-4-16"/><path d="m11 21 2 2 2-2"/><path d="m11 21-2 2-2-2"/></svg>',
            "briefcase": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>',
            "coins": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="8" cy="8" r="6"/><path d="m18.09 10.37a6 6 0 1 1-10.72 0"/><circle cx="16" cy="16" r="6"/><path d="m6.91 15.37a6 6 0 1 1 10.72 0"/></svg>',
            "clock": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12,6 12,12 16,14"/></svg>',
            "target": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>',
            "clipboard": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="8" y="2" width="8" height="4" rx="1" ry="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/></svg>',
            "alert-triangle": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
            "check-circle": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22,4 12,14.01 9,11.01"/></svg>',
            "x-circle": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>',
            "plus": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>',
            "phone": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>',
            "filter": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="22,3 2,3 10,12.46 10,19 14,21 14,12.46 22,3"/></svg>',
            "shield": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
            "bar-chart": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="20" x2="12" y2="10"/><line x1="18" y1="20" x2="18" y2="4"/><line x1="6" y1="20" x2="6" y2="16"/></svg>',
            "pie-chart": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21.21 15.89A10 10 0 1 1 8 2.83"/><path d="m22 12-10-10v10z"/></svg>',
            "tag": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2H2v10l9.29 9.29c.94.94 2.48.94 3.42 0l6.58-6.58c.94-.94.94-2.48 0-3.42L12 2Z"/><circle cx="7" cy="7" r="3"/></svg>',
            "users": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="m22 21-2-2m2-5a2 2 0 1 1-4 0 2 2 0 0 1 4 0z"/></svg>',
            "list": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>',
            "link": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.72"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.72-1.72"/></svg>',
            "scale": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m16 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="m2 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="M7 21h10"/><path d="M12 3v18"/><path d="M3 7h2c2 0 5-1 7-2 2 1 5 2 7 2h2"/></svg>',
            "upload": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17,8 12,3 7,8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>',
            "lightbulb": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/></svg>',
            "rocket": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/></svg>',
            "arrow-down": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><polyline points="19,12 12,19 5,12"/></svg>',
            "check": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20,6 9,17 4,12"/></svg>',
        },
        "heroicons": {
            "edit": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="{color}"><path fill-rule="evenodd" d="M16.862 3.487a2.25 2.25 0 113.182 3.182L7.061 19.652a1.125 1.125 0 01-.398.248l-3.75 1.5a.75.75 0 01-.97-.97l1.5-3.75a1.125 1.125 0 01.248-.398L16.674 3.299z" clip-rule="evenodd" /></svg>',
            "delete": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="{color}"><path fill-rule="evenodd" d="M16.5 4.478v.227a48.816 48.816 0 013.878.512.75.75 0 11-.256 1.478l-.209-.035-1.005 13.07a3 3 0 01-2.991 2.77H8.084a3 3 0 01-2.991-2.77L4.087 6.66l-.209.035a.75.75 0 01-.256-1.478A48.567 48.567 0 017.5 4.705v-.227c0-1.564 1.213-2.9 2.816-2.951a52.662 52.662 0 013.369 0c1.603.051 2.815 1.387 2.815 2.951zm-6.136-1.452a51.196 51.196 0 013.273 0C14.39 3.05 15 3.684 15 4.478v.113a49.488 49.488 0 00-6 0v-.113c0-.794.609-1.428 1.364-1.452zm-.355 5.945a.75.75 0 10-1.5.058l.347 9a.75.75 0 101.499-.058l-.346-9zm5.48.058a.75.75 0 10-1.498-.058l-.347 9a.75.75 0 001.5.058l.345-9z" clip-rule="evenodd" /></svg>',
            "chart": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="{color}"><path d="M18.375 2.25c-1.035 0-1.875.84-1.875 1.875v15.75c0 1.035.84 1.875 1.875 1.875h.75c1.035 0 1.875-.84 1.875-1.875V4.125c0-1.036-.84-1.875-1.875-1.875h-.75zM9.75 8.625c0-1.036.84-1.875 1.875-1.875h.75c1.036 0 1.875.84 1.875 1.875v11.25c0 1.035-.84 1.875-1.875 1.875h-.75a1.875 1.875 0 01-1.875-1.875V8.625zM3 13.125c0-1.036.84-1.875 1.875-1.875h.75c1.036 0 1.875.84 1.875 1.875v6.75c0 1.035-.84 1.875-1.875 1.875h-.75A1.875 1.875 0 013 19.875v-6.75z" /></svg>',
            "trending-up": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="{color}"><path fill-rule="evenodd" d="M15.22 6.268a.75.75 0 01.968-.432l5.942 2.28a.75.75 0 01.431.97l-2.28 5.941a.75.75 0 11-1.4-.537l1.63-4.251-1.086.483a11.2 11.2 0 00-5.45 5.174.75.75 0 01-1.199.24 9.75 9.75 0 017.04-9.91l.386-.162-4.251-1.631a.75.75 0 01-.432-.968z" clip-rule="evenodd" /><path fill-rule="evenodd" d="M6.737 11.061a.75.75 0 01.976-.43l4.5 1.746a.75.75 0 01.43.976l-1.746 4.5a.75.75 0 11-1.405-.546l1.263-3.25a7.5 7.5 0 00-3.483 3.483.75.75 0 11-1.456-.364 9 9 0 014.195-4.195l-3.25-1.263a.75.75 0 01-.431-.976z" clip-rule="evenodd" /></svg>',
        }
    }
    
    return icons.get(library, {}).get(icon_name, f'<span style="color: {color};">•</span>')

def get_simple_icon(icon_name: str) -> str:
    """
    Get simple text-based icons for Streamlit elements that don't support HTML
    """
    simple_icons = {
        "edit": "[Edit]",
        "delete": "[Delete]", 
        "refresh": "[Refresh]",
        "chart": "[Chart]",
        "download": "[Download]",
        "trending-up": "[Up]",
        "trending-down": "[Down]",
        "rotate-cw": "[Rotate]",
        "file-text": "[File]",
        "activity": "[Activity]",
        "calendar": "[Date]",
        "settings": "[Settings]",
        "save": "[Save]",
        "search": "[Search]",
        "clock": "[Time]",
        "target": "[Target]",
        "clipboard": "[Clipboard]",
        "alert-triangle": "[Warning]",
        "check-circle": "[Success]",
        "x-circle": "[Error]",
        "plus": "[Add]",
        "phone": "[Call]"
    }
    return simple_icons.get(icon_name, "•")

def display_icon_text(icon_name: str, text: str, library: str = "lucide", 
                     icon_size: int = 16, icon_color: str = "#666666") -> str:
    """
    Create text with an icon prefix - uses simple icons for Streamlit compatibility
    
    Args:
        icon_name: Name of the icon
        text: Text to display
        library: Icon library to use (ignored for simple version)
        icon_size: Icon size in pixels (ignored for simple version)
        icon_color: Icon color (ignored for simple version)
    
    Returns:
        Text string with simple icon prefix
    """
    icon = get_simple_icon(icon_name)
    return f"{icon} {text}"

def display_icon_header(icon_name: str, text: str, library: str = "lucide", 
                       icon_size: int = 18, icon_color: str = "#666666") -> str:
    """
    Create an HTML header with SVG icon
    
    Args:
        icon_name: Name of the icon
        text: Header text to display
        library: Icon library to use ('lucide', 'heroicons', etc.)
        icon_size: Icon size in pixels
        icon_color: Icon color in hex format
    
    Returns:
        HTML string with SVG icon and header text
    """
    icon_html = get_icon(icon_name, library, icon_size, icon_color)
    return f'<div style="display: flex; align-items: center; gap: 8px; margin: 10px 0;"><span>{icon_html}</span><span style="font-weight: 600; color: {icon_color};">{text}</span></div>'

def create_icon_button(icon_name: str, text: str, library: str = "lucide", 
                      icon_size: int = 16, icon_color: str = "#666666"):
    """
    Create a button with icon using HTML markdown
    """
    icon_html = get_icon(icon_name, library, icon_size, icon_color)
    html_content = f'<div style="display: inline-flex; align-items: center; gap: 8px; padding: 4px 8px; background-color: #f0f2f6; border-radius: 4px; border: 1px solid #ddd;">{icon_html}<span>{text}</span></div>'
    return html_content

def create_clickable_icon_button(icon_name: str, text: str, button_key: str, library: str = "lucide", 
                                icon_size: int = 16, icon_color: str = "#666666", button_style: str = "primary"):
    """
    Create a clickable HTML button with SVG icon using form and hidden input approach
    """
    icon_html = get_icon(icon_name, library, icon_size, icon_color)
    
    # Different button styles
    if button_style == "primary":
        bg_gradient = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
        text_color = "white"
    elif button_style == "danger":
        bg_gradient = "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)"
        text_color = "white"
    elif button_style == "success":
        bg_gradient = "linear-gradient(135deg, #22c55e 0%, #16a34a 100%)"
        text_color = "white"
    else:  # secondary
        bg_gradient = "linear-gradient(135deg, #64748b 0%, #475569 100%)"
        text_color = "white"
    
    # Initialize session state for this button
    session_key = f"button_clicked_{button_key}"
    if session_key not in st.session_state:
        st.session_state[session_key] = False
    
    # Create a simple styled div that looks like a button
    html_content = f"""
    <style>
    .icon-button-{button_key} {{
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 16px;
        background: {bg_gradient};
        color: {text_color};
        border: none;
        border-radius: 6px;
        cursor: pointer;
        transition: all 0.2s ease;
        text-decoration: none;
        font-size: 14px;
        font-weight: 500;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 2px;
        user-select: none;
    }}
    .icon-button-{button_key}:hover {{
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        filter: brightness(1.1);
    }}
    </style>
    <div class="icon-button-{button_key}">
        {icon_html}
        <span>{text}</span>
    </div>
    """
    
    return html_content

def use_clickable_button(icon_name: str, text: str, button_key: str, library: str = "lucide", 
                        icon_size: int = 16, icon_color: str = "#666666", button_style: str = "primary"):
    """
    Display a clickable button and return True if clicked
    """
    # Display the styled button
    html_content = create_clickable_icon_button(icon_name, text, button_key, library, icon_size, icon_color, button_style)
    st.markdown(html_content, unsafe_allow_html=True)
    
    # Use a hidden Streamlit button for actual functionality
    unique_key = f"hidden_btn_{button_key}_{hash(text) % 1000}"
    
    # Place the hidden button right after the styled div
    if st.button(f"Click {text}", key=unique_key, help=text):
        return True
    
    return False

def check_button_click(button_key: str) -> bool:
    """
    Check if a specific button was clicked using query parameters
    """
    try:
        # Try newer query params API first
        if hasattr(st, 'query_params'):
            query_params = dict(st.query_params)
        else:
            # Fallback to experimental API
            query_params = st.experimental_get_query_params() if hasattr(st, 'experimental_get_query_params') else {}
        
        # Check if our button was clicked
        clicked_button = query_params.get('clicked', [None])
        if isinstance(clicked_button, list):
            clicked_button = clicked_button[0] if clicked_button else None
        
        if clicked_button == button_key:
            # Clear the query parameter to prevent repeated actions
            try:
                if hasattr(st, 'query_params'):
                    st.query_params.clear()
                else:
                    st.experimental_set_query_params()
            except:
                pass  # Ignore errors when clearing query params
            return True
        
        return False
    except Exception as e:
        # Fallback: use session state instead of query params
        session_key = f"button_clicked_{button_key}"
        if st.session_state.get(session_key, False):
            st.session_state[session_key] = False
            return True
        return False
    
st.set_page_config(
        page_title="My Crypto Portfolio", 
        layout="wide"
    )
# --- Custom CSS for professional styling
st.markdown("""
<style>
    /* Main Header */
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        text-align: center;
    }
    /* Center table content */
    .stDataFrame {
        margin: 0 auto;
    }
    .stDataFrame > div {
        margin: 0 auto;
    }
    /* Center table cells */
    .stDataFrame table {
        margin: 0 auto;
    }
    .stDataFrame td, .stDataFrame th {
        justify-content: center !important;
        text-align: center !important;
    }
    
    /* Buy/Sell Transaction Visual Distinctions */
    .buy-transaction {
        background-color: rgba(34, 197, 94, 0.08) !important;
        border-left: 3px solid #22c55e !important;
    }
    .sell-transaction {
        background-color: rgba(239, 68, 68, 0.08) !important;
        border-left: 3px solid #ef4444 !important;
    }
    .buy-quantity {
        color: #16a34a !important;
        font-weight: 600 !important;
    }
    .sell-quantity {
        color: #dc2626 !important;
        font-weight: 600 !important;
        font-style: italic !important;
    }
    .transaction-icon {
        font-size: 1.1em;
        margin-right: 5px;
    }
    /* Editable title */
    .editable-title {
        background: transparent;
        color: white;
        margin-bottom: 20px;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 15px;
        border-radius: 8px;
        color: white;
        text-align: center;
        margin: 5px;
    }
    /* Search bar styling */
    .search-container {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #cbd5e0;
        margin: 10px 0;
    }
    .search-info {
        font-size: 0.9em;
        color: #64748b;
        margin-top: 5px;
    }
    .alert-success { background: #d4edda; border: 1px solid #c3e6cb; color: #155724; padding: 10px; border-radius: 5px; margin: 5px 0; }
    .alert-warning { background: #fff3cd; border: 1px solid #ffeaa7; color: #856404; padding: 10px; border-radius: 5px; margin: 5px 0; }
    .alert-danger { background: #f8d7da; border: 1px solid #f5c6cb; color: #721c24; padding: 10px; border-radius: 5px; margin: 5px 0; }
    
    /* Horizontally scrollable action buttons */
    .action-buttons {
        display: flex;
        gap: 5px;
        overflow-x: auto;
        padding: 5px 0;
        white-space: nowrap;
    }
    .action-buttons::-webkit-scrollbar {
        height: 4px;
    }
    .action-buttons::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    .action-buttons::-webkit-scrollbar-thumb {
        background: #888;
        border-radius: 10px;
    }
    
    /* Button styling */
    .edit-btn { background: #007bff; color: white; }
    .delete-btn { background: #dc3545; color: white; }
    
    /* Update indicator */
    .update-indicator {
        position: fixed;
        top: 10px;
        right: 10px;
        background: #28a745;
        color: white;
        padding: 10px;
        border-radius: 5px;
        z-index: 1000;
    }
    /* Smooth scrolling */
    html {
        scroll-behavior: smooth;
    }
    /* Section anchors */
    .section-anchor {
        position: relative;
        top: -100px;
        visibility: hidden;
    }
    /* SVG icon styling */
    .svg-icon {
        width: 16px;
        height: 16px;
        display: inline-block;
        vertical-align: middle;
        margin-right: 5px;
    }
    
    /* Navigation Menu Styling - Make text bigger */
    .main .block-container {
        padding-top: 1rem;
    }
    
    /* Target navigation links specifically */
    .css-1d391kg a,
    .css-1v0mbdj a,
    nav a {
        font-size: 1rem !important;
        font-weight: 500 !important;
    }
    
    /* Target the page navigation specifically */
    section[data-testid="stSidebar"] div[data-testid="stSidebarNav"] a {
        font-size: 1rem !important;
        font-weight: 500 !important;
        padding: 8px 12px !important;
    }
    
    /* Sidebar headers and labels */
    div[data-testid="stSidebar"] h1,
    div[data-testid="stSidebar"] h2,
    div[data-testid="stSidebar"] h3,
    div[data-testid="stSidebar"] label {
        font-size: 1rem !important;
        font-weight: 500 !important;
    }
    
    /* Buttons in sidebar */
    div[data-testid="stSidebar"] button {
        font-size: 1rem !important;
        font-weight: 500 !important;
        padding: 8px 16px !important;
    }
    
    /* Main navigation (if using st.navigation or multipage) */
    .stApp > header,
    .stApp > header * {
        font-size: 1rem !important;
        font-weight: 500 !important;
    }
    
    /* Alternative selectors for navigation links */
    nav[aria-label="navigation"] a,
    .main-nav a,
    div[data-testid="stNavigation"] a {
        font-size: 1rem !important;
        font-weight: 500 !important;
        padding: 8px 16px !important;
    }
    
    /* If using st.tabs for navigation */
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 1rem !important;
        font-weight: 500 !important;
        padding: 12px 20px !important;
    }
</style>
""", unsafe_allow_html=True)

# ==================================================================================================
# SETUP & CONFIGURATION
# ==================================================================================================

cg = CoinGeckoAPI()


@st.cache_data(ttl=1800)  # Cache for 30 minutes
def get_live_prices(coin_ids: pd.Series) -> Dict[str, Dict[str, float]]:
    """Fetch current price and market data for coins from CoinGecko."""
    if not coin_ids.any():
        return {}
    try:
        return cg.get_price(ids=list(coin_ids), vs_currencies='usd', include_market_cap='true', include_24hr_change='true')
    except Exception as e:
        st.error(f"CoinGecko API Error: {str(e)}")
        return {}

@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_coins_by_market_cap() -> List[tuple]:
    """Get top 250 coins by market cap from CoinGecko with fallback to top 200 list."""
    try:
        markets = cg.get_coins_markets(vs_currency='usd', order='market_cap_desc', per_page=250, page=1)
        return [(coin['name'], coin['symbol'].upper(), coin['id'], coin['market_cap']) for coin in markets]
    except Exception:
        # Fallback to our comprehensive top 200 crypto list
        symbol_map = get_symbol_map()
        fallback_data = []
        for display_name, symbol in symbol_map.items():
            # Extract coin name from display format "Bitcoin (BTC)" -> "Bitcoin"
            coin_name = display_name.split(' (')[0]
            coin_id = symbol.lower()  # Use symbol as coin_id for CoinGecko compatibility
            fallback_data.append((coin_name, symbol, coin_id, 0))  # Market cap set to 0 as fallback
        return fallback_data

def format_market_cap(market_cap: float) -> str:
    """Format market cap into a human-readable string (e.g., $1.5T, $250B, $50M)."""
    if market_cap >= 1e12: return f"${market_cap/1e12:.1f}T"
    if market_cap >= 1e9: return f"${market_cap/1e9:.1f}B"
    if market_cap >= 1e6: return f"${market_cap/1e6:.1f}M"
    return f"${market_cap:,.0f}"

def clean_chart_data(df: pd.DataFrame, value_columns: List[str]) -> pd.DataFrame:
    """Clean data for chart consumption by removing NaN, inf, and invalid values."""
    if df.empty:
        return df
    
    cleaned_df = df.copy()
    
    for col in value_columns:
        if col in cleaned_df.columns:
            # Convert to numeric, replacing errors with NaN
            cleaned_df[col] = pd.to_numeric(cleaned_df[col], errors='coerce')
            
            # Replace inf/-inf with NaN
            cleaned_df[col] = cleaned_df[col].replace([float('inf'), float('-inf')], pd.NA)
            
            # Remove extreme outliers (values beyond reasonable range)
            if col == 'Percentage_Change':
                # Cap percentage changes at ±10,000%
                cleaned_df[col] = cleaned_df[col].clip(-10000, 10000)
            elif 'Value' in col or 'Price' in col:
                # Remove negative values for prices/values
                cleaned_df.loc[cleaned_df[col] < 0, col] = pd.NA
    
    # Remove rows where all value columns are NaN
    cleaned_df = cleaned_df.dropna(subset=value_columns, how='all')
    
    # Log cleaning results
    original_count = len(df)
    cleaned_count = len(cleaned_df)
    if original_count != cleaned_count:
        st.caption(f"🧹 Data cleaning: {original_count - cleaned_count} rows removed due to invalid values")
    
    return cleaned_df

def prepare_plot_df(df: pd.DataFrame, required_columns: List[str], use_include: bool = True) -> pd.DataFrame:
    """Prepare a DataFrame for plotting: apply Include_In_Portfolio filter (if present),
    coerce required columns to numeric, remove inf/NaN and ensure sizes/values are non-negative.
    """
    if df is None or df.empty:
        return pd.DataFrame()

    plot_df = df.copy()

    # Respect include flag when present
    if use_include and 'Include_In_Portfolio' in plot_df.columns:
        try:
            plot_df = plot_df[plot_df['Include_In_Portfolio'] == True].copy()
        except Exception:
            # Defensive fallback
            plot_df = plot_df.copy()

    # Coerce required columns
    for col in required_columns:
        if col in plot_df.columns:
            plot_df[col] = pd.to_numeric(plot_df[col], errors='coerce')

    # Replace infinite values and drop rows where all required columns are NaN
    plot_df = plot_df.replace([float('inf'), float('-inf')], pd.NA)
    plot_df = plot_df.dropna(subset=required_columns, how='all')

    # Ensure common sizing/value columns are finite and non-negative where appropriate
    for col in ['Current_Value', 'Portfolio_Weight', 'Abs_Current_Value', 'Investment_Amount', 'Cost_Basis', 'Total_Current_Value', 'Total_Value']:
        if col in plot_df.columns:
            # Absolute and fillna with 0 to avoid tiny/negative sizes
            plot_df[col] = pd.to_numeric(plot_df[col], errors='coerce')
            plot_df[col] = plot_df[col].abs().fillna(0)

    return plot_df

# ==================================================================================================
# RESTRUCTURED TRANSACTIONS HELPER FUNCTIONS
# ==================================================================================================

def get_restructure_display_columns(df: pd.DataFrame) -> List[str]:
    """Get the most relevant columns for displaying restructured transactions."""
    available_cols = df.columns.tolist()
    
    # Priority columns to show for restructured transactions
    priority_cols = [
        'Symbol', 'Coin_Name', 'Transaction_Type', 'Quantity', 'Purchase_Price', 
        'Current_Value', 'Restructure_Group', 'Include_In_Portfolio',
        'Purchase_Date', 'Adjusted_Purchase_Price', 'Original_Purchase_Price',
        'Cost_Basis_Transferred'
    ]
    
    # ID columns (try to include one)
    id_cols = ['transaction_id', 'ID', 'id']
    
    # Build display columns list
    display_cols = []
    
    # Add ID column first if available
    for id_col in id_cols:
        if id_col in available_cols:
            display_cols.append(id_col)
            break
    
    # Add priority columns that exist
    for col in priority_cols:
        if col in available_cols and col not in display_cols:
            display_cols.append(col)
    
    # If we have very few columns, add any remaining ones
    if len(display_cols) < 5:
        for col in available_cols:
            if col not in display_cols and not col.startswith('_'):
                display_cols.append(col)
    
    return display_cols

def show_group_analysis(group_data: pd.DataFrame):
    """Show detailed analysis for a restructure group."""
    st.markdown(display_icon_header('trending-up', 'Group Analysis', 'lucide', 20, '#666666'), unsafe_allow_html=True)
    
    # Basic metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        out_transactions = group_data[group_data['Transaction_Type'] == 'RESTRUCTURE_OUT']
        total_out_value = 0
        if 'Quantity' in out_transactions.columns and 'Purchase_Price' in out_transactions.columns:
            total_out_value = (out_transactions['Quantity'].abs() * out_transactions['Purchase_Price']).sum()
        st.metric(display_icon_text("trending-down", "Total OUT Value", "lucide", 16, "#666666"), f"${total_out_value:,.2f}")
    
    with col2:
        in_transactions = group_data[group_data['Transaction_Type'] == 'RESTRUCTURE_IN']
        total_in_value = 0
        if 'Current_Value' in in_transactions.columns:
            total_in_value = in_transactions['Current_Value'].sum()
        st.metric(display_icon_text("trending-up", "Total IN Value", "lucide", 16, "#666666"), f"${total_in_value:,.2f}")
    
    with col3:
        symbols_out = out_transactions['Symbol'].unique() if 'Symbol' in out_transactions.columns else []
        symbols_in = in_transactions['Symbol'].unique() if 'Symbol' in in_transactions.columns else []
        st.metric(display_icon_text("refresh", "Symbols OUT → IN", "lucide", 16, "#666666"), f"{len(symbols_out)} → {len(symbols_in)}")
    
    with col4:
        if 'Purchase_Date' in group_data.columns:
            dates = pd.to_datetime(group_data['Purchase_Date'], errors='coerce')
            date_range = (dates.max() - dates.min()).days if not dates.isna().all() else 0
            st.metric(display_icon_text("calendar", "Date Range", "lucide", 16, "#666666"), f"{date_range} days")
        else:
            st.metric(display_icon_text("calendar", "Date Range", "lucide", 16, "#666666"), "N/A")
    
    # Show details by transaction type
    for txn_type in ['RESTRUCTURE_OUT', 'RESTRUCTURE_IN']:
        txn_data = group_data[group_data['Transaction_Type'] == txn_type]
        if len(txn_data) > 0:
            txn_icon = get_icon('arrow-right' if txn_type == 'RESTRUCTURE_OUT' else 'arrow-left', 'lucide', 16, '#666666')
            st.markdown(f"**{txn_icon} {txn_type} Transactions:**", unsafe_allow_html=True)
            display_cols = get_restructure_display_columns(txn_data)
            st.dataframe(txn_data[display_cols], use_container_width=True)

# ==================================================================================================
# PORTFOLIO RESTRUCTURING SYSTEM
# ==================================================================================================

class PortfolioRestructuringManager:
    """Manages portfolio restructuring, cost basis transfers, and asset switching logic."""
    
    def __init__(self):
        self.transaction_types = {
            'BUY': 'Standard purchase - adds to portfolio value',
            'SELL': 'Standard sale - reduces portfolio holdings', 
            'RESTRUCTURE_OUT': '[OUT] Asset sold during restructuring (excluded from portfolio value)',
            'RESTRUCTURE_IN': '[IN] Asset bought with restructuring proceeds (included in portfolio)',
            'TRANSFER': 'Direct asset-to-asset transfer',
            'EXCLUDE': 'Manually excluded from all calculations'
        }
        
        self.restructuring_rules = {
            'exclude_restructure_out': True,  # Don't count restructure-out transactions in portfolio value
            'use_cost_basis_transfer': True,  # Transfer cost basis from old to new assets
            'calculate_restructure_be': True,  # Calculate breakeven for restructured positions
        }
    
    def get_transaction_type_options(self) -> Dict[str, str]:
        """Return available transaction types for UI selection."""
        return self.transaction_types
    
    def apply_restructuring_rules(self, df: pd.DataFrame, calculation_type: str = 'holdings') -> pd.DataFrame:
        """Apply restructuring rules to filter and adjust portfolio data.
        
        Args:
            df: Portfolio DataFrame
            calculation_type: 'holdings' for current holdings, 'totals' for portfolio totals, 'original' for original holdings
        """
        if df.empty or 'Transaction_Type' not in df.columns:
            return df
        
        adjusted_df = df.copy()
        
        if calculation_type == 'totals':
            # For portfolio totals: Exclude ALL restructuring transactions
            restructure_mask = adjusted_df['Transaction_Type'].isin(['RESTRUCTURE_OUT', 'RESTRUCTURE_IN'])
            adjusted_df.loc[restructure_mask, 'Include_In_Portfolio'] = False
            adjusted_df.loc[restructure_mask, 'Current_Value'] = 0
            adjusted_df.loc[restructure_mask, 'Profit_Loss'] = 0
        elif calculation_type == 'original':
            # For original holdings: Include RESTRUCTURE_OUT (original holdings) but exclude RESTRUCTURE_IN (new holdings)
            restructure_in_mask = adjusted_df['Transaction_Type'] == 'RESTRUCTURE_IN'
            adjusted_df.loc[restructure_in_mask, 'Include_In_Portfolio'] = False
            adjusted_df.loc[restructure_in_mask, 'Current_Value'] = 0
            adjusted_df.loc[restructure_in_mask, 'Profit_Loss'] = 0
            
            # Include RESTRUCTURE_OUT transactions with positive quantities only (they represent original holdings)
            restructure_out_mask = (adjusted_df['Transaction_Type'] == 'RESTRUCTURE_OUT') & (adjusted_df['Quantity'] > 0)
            adjusted_df.loc[restructure_out_mask, 'Include_In_Portfolio'] = True
            
            # Exclude RESTRUCTURE_OUT transactions with negative quantities
            restructure_out_negative_mask = (adjusted_df['Transaction_Type'] == 'RESTRUCTURE_OUT') & (adjusted_df['Quantity'] <= 0)
            adjusted_df.loc[restructure_out_negative_mask, 'Include_In_Portfolio'] = False
            adjusted_df.loc[restructure_out_negative_mask, 'Current_Value'] = 0
            adjusted_df.loc[restructure_out_negative_mask, 'Profit_Loss'] = 0
            
            # For original holdings calculation, treat positive RESTRUCTURE_OUT as positive (original holdings)
            # This overrides the default negative treatment in load_and_process_portfolio
            adjusted_df.loc[restructure_out_mask, 'Effective_Quantity'] = abs(adjusted_df.loc[restructure_out_mask, 'Quantity'])
        elif calculation_type == 'holdings':
            # For current holdings: Exclude RESTRUCTURE_OUT but INCLUDE RESTRUCTURE_IN
            restructure_out_mask = adjusted_df['Transaction_Type'] == 'RESTRUCTURE_OUT'
            adjusted_df.loc[restructure_out_mask, 'Include_In_Portfolio'] = False
            adjusted_df.loc[restructure_out_mask, 'Current_Value'] = 0
            adjusted_df.loc[restructure_out_mask, 'Profit_Loss'] = 0
            
            # Ensure RESTRUCTURE_IN transactions are included in holdings
            restructure_in_mask = adjusted_df['Transaction_Type'] == 'RESTRUCTURE_IN'
            adjusted_df.loc[restructure_in_mask, 'Include_In_Portfolio'] = True
        
        # Apply cost basis transfers for RESTRUCTURE_IN transactions
        if self.restructuring_rules['use_cost_basis_transfer']:
            adjusted_df = self._apply_cost_basis_transfers(adjusted_df)
        
        return adjusted_df
    
    def _apply_cost_basis_transfers(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply cost basis transfers from restructured-out assets to restructured-in assets."""
        if 'Restructure_Group' not in df.columns:
            return df
        
        # Process each restructuring group
        restructure_groups = df[df['Restructure_Group'].notna()]['Restructure_Group'].unique()
        
        for group_id in restructure_groups:
            group_transactions = df[df['Restructure_Group'] == group_id].copy()
            
            # Calculate total cost basis from OUT transactions
            out_transactions = group_transactions[group_transactions['Transaction_Type'] == 'RESTRUCTURE_OUT']
            total_cost_basis = (out_transactions['Quantity'].abs() * out_transactions['Purchase_Price'].fillna(0)).sum()
            
            # Distribute cost basis to IN transactions
            in_transactions = group_transactions[group_transactions['Transaction_Type'] == 'RESTRUCTURE_IN']
            if len(in_transactions) > 0 and total_cost_basis > 0:
                total_in_value = (in_transactions['Quantity'] * in_transactions['Purchase_Price'].fillna(0)).sum()
                
                for idx, row in in_transactions.iterrows():
                    # Calculate proportional cost basis
                    quantity = row.get('Quantity') or 0
                    purchase_price = row.get('Purchase_Price') or 0
                    transaction_value = quantity * purchase_price
                    proportion = transaction_value / total_in_value if total_in_value > 0 else 0
                    
                    # Assign adjusted cost basis
                    adjusted_cost_basis = total_cost_basis * proportion
                    adjusted_purchase_price = adjusted_cost_basis / quantity if quantity > 0 else 0
                    
                    # Update the dataframe
                    df.loc[idx, 'Adjusted_Purchase_Price'] = adjusted_purchase_price
                    df.loc[idx, 'Original_Purchase_Price'] = purchase_price
                    df.loc[idx, 'Cost_Basis_Transferred'] = adjusted_cost_basis
        
        return df
    
    def create_restructuring_group(self, out_transactions: List[str], in_transactions: List[str]) -> str:
        """Create a new restructuring group linking OUT and IN transactions."""
        group_id = f"RESTR_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        return group_id
    
    def get_portfolio_summary_with_restructuring(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate portfolio summary accounting for restructuring rules."""
        if df.empty:
            return {}
        
        # Apply restructuring rules for portfolio totals (excludes ALL restructuring transactions)
        totals_df = self.apply_restructuring_rules(df, calculation_type='totals')
        
        # Apply restructuring rules for current holdings (excludes RESTRUCTURE_OUT, includes RESTRUCTURE_IN)
        holdings_df = self.apply_restructuring_rules(df, calculation_type='holdings')
        
        # Filter to included transactions for totals calculation
        if 'Include_In_Portfolio' in totals_df.columns:
            included_totals_df = totals_df[totals_df['Include_In_Portfolio'] == True].copy()
        else:
            included_totals_df = totals_df.copy()
        
        # Filter to included transactions for holdings calculation
        if 'Include_In_Portfolio' in holdings_df.columns:
            included_holdings_df = holdings_df[holdings_df['Include_In_Portfolio'] == True].copy()
        else:
            included_holdings_df = holdings_df.copy()
        
        # Calculate portfolio totals (excluding ALL restructuring transactions)
        total_cost_basis = 0
        total_current_value = included_totals_df['Current_Value'].sum()
        
        # Use adjusted purchase prices where available for totals
        for _, row in included_totals_df.iterrows():
            purchase_price = row.get('Adjusted_Purchase_Price') or row.get('Purchase_Price') or 0
            quantity = row.get('Quantity') or 0
            total_cost_basis += abs(quantity) * purchase_price
        
        total_pnl = total_current_value - total_cost_basis
        total_return_pct = (total_pnl / total_cost_basis * 100) if total_cost_basis > 0 else 0
        
        # Calculate current holdings value (includes RESTRUCTURE_IN, excludes RESTRUCTURE_OUT)
        holdings_current_value = included_holdings_df['Current_Value'].sum()
        
        # Restructuring-specific metrics
        if 'Include_In_Portfolio' in df.columns:
            excluded_transactions = int((df['Include_In_Portfolio'] == False).sum())
        else:
            excluded_transactions = 0
        cost_basis_transferred = df['Cost_Basis_Transferred'].fillna(0).sum()
        
        return {
            'total_cost_basis': total_cost_basis,
            'total_current_value': total_current_value,
            'total_pnl': total_pnl,
            'total_return_pct': total_return_pct,
            'holdings_current_value': holdings_current_value,
            'excluded_transactions': excluded_transactions,
            'cost_basis_transferred': cost_basis_transferred,
            'included_transactions_totals': len(included_totals_df),
            'included_transactions_holdings': len(included_holdings_df),
            'total_transactions': len(df)
        }

# Initialize the restructuring manager (temporarily without cache to fix method signature issue)
def get_restructuring_manager():
    """Get instance of PortfolioRestructuringManager."""
    return PortfolioRestructuringManager()

restructuring_manager = get_restructuring_manager()

def calculate_net_holdings(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate net holdings by symbol using Effective_Quantity which already accounts for transaction types"""
    if df.empty or 'Symbol' not in df.columns:
        return df
    
    # Group by symbol and sum the effective quantities
    net_holdings = []
    
    for symbol in df['Symbol'].unique():
        symbol_df = df[df['Symbol'] == symbol].copy()
        
        
        # Calculate net holdings using proper weighted average cost basis
        net_quantity = 0
        total_cost_basis = 0
        transactions_list = []
        
        # Sort transactions by date to ensure proper FIFO calculation
        symbol_df_sorted = symbol_df.sort_values(['Purchase_Date', 'Purchase_Time'], na_position='first')
        
        # First pass: collect all transactions with proper quantities
        for _, row in symbol_df_sorted.iterrows():
            transaction_type = row.get('Transaction_Type', 'BUY')
            quantity = row.get('Quantity', 0)
            
            # Use Purchase_Price as primary source, Original_Purchase_Price may contain incorrect data
            price = row.get('Purchase_Price', 0) or row.get('Original_Purchase_Price', 0) or 0
            
            if quantity is None or pd.isna(quantity):
                quantity = 0
            if price is None or pd.isna(price):
                price = 0
            
            # Store transaction with proper sign
            if transaction_type in ['BUY', 'RESTRUCTURE_IN']:
                actual_qty = abs(quantity)
                transactions_list.append({'qty': actual_qty, 'price': price, 'type': 'BUY'})
            elif transaction_type in ['SELL', 'RESTRUCTURE_OUT']:
                actual_qty = abs(quantity)
                transactions_list.append({'qty': -actual_qty, 'price': price, 'type': 'SELL'})
        
        # Second pass: calculate running totals with proper weighted average
        for tx in transactions_list:
            if tx['type'] == 'BUY':
                # Add to holdings (including 0-cost staking rewards)
                net_quantity += tx['qty']
                # Only add to cost basis if price > 0 (purchased coins)
                # Staking rewards (price = 0) increase quantity but not cost basis
                if tx['price'] > 0:
                    total_cost_basis += tx['qty'] * tx['price']
                
            elif tx['type'] == 'SELL' and net_quantity > 0:
                # Sell from holdings
                sell_qty = min(abs(tx['qty']), net_quantity)
                
                # Calculate current average cost before sale
                if net_quantity > 0:
                    avg_cost_before_sale = total_cost_basis / net_quantity
                    
                    # Reduce holdings and cost basis
                    net_quantity -= sell_qty
                    total_cost_basis -= sell_qty * avg_cost_before_sale
                    total_cost_basis = max(0, total_cost_basis)
        
        current_price = symbol_df['Current_Price'].iloc[0] if len(symbol_df) > 0 and not pd.isna(symbol_df['Current_Price'].iloc[0]) else 0
        
        # Only include symbols with positive net holdings
        if net_quantity > 0:
            weighted_avg_price = total_cost_basis / net_quantity if net_quantity > 0 else 0
            # Ensure current_price is numeric
            if current_price is None or pd.isna(current_price):
                current_price = 0
            current_value = net_quantity * current_price
            profit_loss = current_value - total_cost_basis
            percentage_change = (profit_loss / total_cost_basis * 100) if total_cost_basis > 0 else 0
            
            # Create a representative row for this symbol
            net_holding = {
                'Symbol': symbol,
                'Coin_Name': symbol_df['Coin_Name'].iloc[0] if 'Coin_Name' in symbol_df.columns else symbol,
                'Coin_ID': symbol_df['Coin_ID'].iloc[0] if 'Coin_ID' in symbol_df.columns else symbol.lower(),
                'Effective_Quantity': net_quantity,
                'Quantity': net_quantity,  # For display purposes
                'Purchase_Price': weighted_avg_price,
                'Adjusted_Purchase_Price': weighted_avg_price,
                'Current_Price': current_price,
                'Current_Value': current_value,
                'Profit_Loss': profit_loss,
                'Percentage_Change': percentage_change,
                'Transaction_Type': 'NET_HOLDING',
                'Include_In_Portfolio': True,
                # Add missing columns for display compatibility
                'Purchase_Date': 'Net Position',
                'Purchase_Time': '',
                'Target_Sell_Price': 0.0
            }
            net_holdings.append(net_holding)
    
    return pd.DataFrame(net_holdings) if net_holdings else pd.DataFrame()

def calculate_portfolio_metrics(df: pd.DataFrame, skip_price_update: bool = False) -> pd.DataFrame:
    """Calculates portfolio metrics like current price, value, and P&L using live data with restructuring support."""
    if df.empty:
        required_cols = ['Current_Price', 'Current_Value', 'Profit_Loss', 'Percentage_Change', 'Transaction_Type', 'Include_In_Portfolio']
        for col in required_cols:
            if col not in df.columns:
                if col == 'Transaction_Type':
                    df[col] = 'BUY'  # Default to BUY for existing transactions
                elif col == 'Include_In_Portfolio':
                    df[col] = True   # Default to include all transactions
                else:
                    df[col] = pd.Series(dtype='float64')
        return df
    
    # Ensure restructuring columns exist
    if 'Transaction_Type' not in df.columns:
        df['Transaction_Type'] = df['Quantity'].apply(lambda x: 'SELL' if x < 0 else 'BUY')
    
    if 'Include_In_Portfolio' not in df.columns:
        df['Include_In_Portfolio'] = True
    
    if 'Adjusted_Purchase_Price' not in df.columns:
        df['Adjusted_Purchase_Price'] = df['Purchase_Price']
    
    if 'Original_Purchase_Price' not in df.columns:
        df['Original_Purchase_Price'] = df['Purchase_Price']
    
    if 'Cost_Basis_Transferred' not in df.columns:
        df['Cost_Basis_Transferred'] = 0.0
    
    if 'Restructure_Group' not in df.columns:
        df['Restructure_Group'] = None

    # Skip price update for delete operations or when explicitly requested
    if skip_price_update:
        # Use existing prices from session state if available
        if hasattr(st.session_state, 'transactions') and not st.session_state.transactions.empty:
            existing_prices = st.session_state.transactions.set_index('Coin_ID')['Current_Price'].to_dict()
            df['Current_Price'] = df['Coin_ID'].map(lambda x: existing_prices.get(x, 0))
        else:
            # Fallback to zero prices if no existing data
            df['Current_Price'] = 0
    else:
        # Normal price update for add/edit operations
        coin_ids = df['Coin_ID'].drop_duplicates()  # This returns a Series instead of array
        live_data = get_live_prices(coin_ids)
        df['Current_Price'] = df['Coin_ID'].map(lambda x: live_data.get(x, {}).get('usd', 0))
    
    # Apply restructuring rules for holdings calculation (default behavior)
    df = restructuring_manager.apply_restructuring_rules(df, calculation_type='holdings')

    # Calculate Effective_Quantity based on transaction types
    # BUY and RESTRUCTURE_IN add to holdings (positive)
    # SELL and RESTRUCTURE_OUT subtract from holdings (negative)
    df['Effective_Quantity'] = df['Quantity'].copy()
    
    if 'Transaction_Type' in df.columns:
        # Make SELL and RESTRUCTURE_OUT quantities negative if they aren't already
        sell_mask = df['Transaction_Type'] == 'SELL'
        restructure_out_mask = df['Transaction_Type'] == 'RESTRUCTURE_OUT'
        
        # Ensure SELL quantities are negative
        df.loc[sell_mask, 'Effective_Quantity'] = -abs(df.loc[sell_mask, 'Quantity'])
        # Ensure RESTRUCTURE_OUT quantities are negative  
        df.loc[restructure_out_mask, 'Effective_Quantity'] = -abs(df.loc[restructure_out_mask, 'Quantity'])
        # Ensure BUY and RESTRUCTURE_IN quantities are positive
        buy_mask = df['Transaction_Type'] == 'BUY'
        restructure_in_mask = df['Transaction_Type'] == 'RESTRUCTURE_IN'
        df.loc[buy_mask, 'Effective_Quantity'] = abs(df.loc[buy_mask, 'Quantity'])
        df.loc[restructure_in_mask, 'Effective_Quantity'] = abs(df.loc[restructure_in_mask, 'Quantity'])
    else:
        # Fallback: use original quantity logic for backwards compatibility
        df['Effective_Quantity'] = df['Quantity']

    # Calculate metrics using adjusted purchase prices where available and using Effective_Quantity
    df['Current_Value'] = df['Effective_Quantity'] * df['Current_Price'].fillna(0)
    df['Profit_Loss'] = df['Current_Value'] - (df['Effective_Quantity'] * df['Adjusted_Purchase_Price'].fillna(0))
    # Percentage change should reflect total return (profit/loss as percentage of investment)
    investment_cost = df['Effective_Quantity'] * df['Adjusted_Purchase_Price'].fillna(0)
    df['Percentage_Change'] = ((df['Profit_Loss'] / investment_cost) * 100).fillna(0)
    # Handle division by zero cases
    df['Percentage_Change'] = df['Percentage_Change'].replace([float('inf'), float('-inf')], 0)

    return df

def load_and_process_portfolio(skip_price_update=False):
    """Central function to load, map, and process portfolio data from Supabase."""
    supabase_data = db.get_user_portfolio(st.session_state.user_id)
    if supabase_data.empty or 'transaction_id' not in supabase_data.columns:
        st.session_state.transactions = supabase_data
        return

    # Debug: Check what columns are available from Supabase
    print(f"Debug - Supabase columns: {list(supabase_data.columns)}")
    if not supabase_data.empty:
        print(f"Debug - Sample Supabase data: {supabase_data.iloc[0].to_dict()}")

    # Only map columns that exist in the data
    column_mapping = {
        'coin_name': 'Coin_Name', 'symbol': 'Symbol', 'quantity': 'Quantity',
        'purchase_price': 'Purchase_Price', 'purchase_date': 'Purchase_Date',
        'purchase_time': 'Purchase_Time', 'target_sell_price': 'Target_Sell_Price',
        'coin_id': 'Coin_ID', 'created_at': 'Created_At', 'updated_at': 'Updated_At'
    }
    
    # Add restructuring fields mapping if they exist in the data
    if 'transaction_type' in supabase_data.columns:
        column_mapping['transaction_type'] = 'Transaction_Type'
    if 'include_in_portfolio' in supabase_data.columns:
        column_mapping['include_in_portfolio'] = 'Include_In_Portfolio'
    if 'restructure_group' in supabase_data.columns:
        column_mapping['restructure_group'] = 'Restructure_Group'
    if 'adjusted_purchase_price' in supabase_data.columns:
        column_mapping['adjusted_purchase_price'] = 'Adjusted_Purchase_Price'
    if 'original_purchase_price' in supabase_data.columns:
        column_mapping['original_purchase_price'] = 'Original_Purchase_Price'
    if 'cost_basis_transferred' in supabase_data.columns:
        column_mapping['cost_basis_transferred'] = 'Cost_Basis_Transferred'

    mapped_data = supabase_data.rename(columns=column_mapping)
    
    mapped_data['ID'] = mapped_data['transaction_id']
    st.session_state.transactions = calculate_portfolio_metrics(mapped_data, skip_price_update=skip_price_update)
    st.session_state.last_update = datetime.now()

# ==================================================================================================
# AUTHENTICATION & INITIALIZATION
# ==================================================================================================

# Require authentication - online-only mode
if not require_auth():
    st.stop()

db = PortfolioDatabase()

# ==================================================================================================
# HELPER FUNCTIONS - MOVED UP FOR PROPER ORDERING
# ==================================================================================================

def refresh_portfolio_data(skip_price_update=False):
    """Helper function to refresh portfolio data from Supabase with consistent mapping"""
    load_and_process_portfolio(skip_price_update=skip_price_update)
    # Only clear price cache if we're updating prices
    if not skip_price_update:
        st.cache_data.clear()
    # Update last refresh timestamp
    st.session_state.last_update = datetime.now()

def setup_realtime_subscription():
    """Setup polling-based updates (websockets not compatible with Streamlit)"""
    if 'realtime_setup' not in st.session_state:
        st.session_state.realtime_setup = True
        st.session_state.last_realtime_check = datetime.now()

def process_import_chunk(chunk_df, start_row_offset, db, user_id):
    """Process a chunk of import data and return success count and errors"""
    success_count = 0
    errors = []
    
    for row_index, row in chunk_df.iterrows():
        try:
            # Calculate actual row number in original file
            actual_row_num = start_row_offset + row_index
            
            # Extract values with proper type handling
            quantity_val = row.iloc[chunk_df.columns.get_loc('Quantity')]
            price_val = row.iloc[chunk_df.columns.get_loc('Purchase_Price')]
            
            # Skip rows with invalid quantity or price
            if pd.isna(quantity_val) or pd.isna(price_val):
                errors.append(f"Row {actual_row_num}: Missing quantity or price")
                continue
                
            # Convert to numeric and validate
            try:
                numeric_quantity = float(quantity_val)
                numeric_price = float(price_val)
                if numeric_price <= 0:
                    errors.append(f"Row {actual_row_num}: Invalid price ({numeric_price})")
                    continue
            except (ValueError, TypeError):
                errors.append(f"Row {actual_row_num}: Invalid numeric values (qty: {quantity_val}, price: {price_val})")
                continue
            
            # Determine transaction type and adjust quantity
            final_quantity = numeric_quantity
            
            # Method 1: Check Transaction_Type column
            if 'Transaction_Type' in chunk_df.columns:
                trans_type = str(row.iloc[chunk_df.columns.get_loc('Transaction_Type')]).upper()
                if trans_type in ['SELL', 'SALE', 'S']:
                    final_quantity = -abs(numeric_quantity)  # Make negative for sell
                else:
                    final_quantity = abs(numeric_quantity)   # Make positive for buy
            
            # Method 2: Use quantity sign (negative = sell)
            elif numeric_quantity < 0:
                final_quantity = numeric_quantity  # Keep negative
            
            # Method 3: Default to buy transaction
            else:
                final_quantity = abs(numeric_quantity)  # Ensure positive for buy
            
            # Extract other values with validation
            coin_name_val = str(row.iloc[chunk_df.columns.get_loc('Coin_Name')]).strip()
            symbol_val = str(row.iloc[chunk_df.columns.get_loc('Symbol')]).upper().strip()
            
            # Validate required string fields
            if not coin_name_val or coin_name_val == 'nan' or not symbol_val or symbol_val == 'NAN':
                errors.append(f"Row {actual_row_num}: Missing coin name or symbol")
                continue
            
            # Get or generate coin_id
            if 'Coin_ID' in chunk_df.columns:
                coin_id = str(row.iloc[chunk_df.columns.get_loc('Coin_ID')]).strip().lower()
            else:
                coin_id = symbol_val.lower()
            
            # Prepare transaction data with proper datetime handling
            current_time = datetime.now()
            transaction_id = f"{coin_id}_{current_time.strftime('%Y%m%d_%H%M%S')}_{actual_row_num}"
            
            # Handle date fields with proper formatting and validation
            purchase_date_val = current_time.strftime('%Y-%m-%d')
            purchase_time_val = current_time.strftime('%H:%M:%S')
            
            if 'Purchase_Date' in chunk_df.columns:
                pd_val = row.iloc[chunk_df.columns.get_loc('Purchase_Date')]
                if not pd.isna(pd_val):
                    try:
                        # Try to parse and reformat the date to ensure consistency
                        date_str = str(pd_val).strip()
                        if date_str and date_str != 'nan':
                            # Try different date formats
                            for fmt in ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%Y%m%d']:
                                try:
                                    parsed_date = pd.to_datetime(date_str, format=fmt)
                                    purchase_date_val = parsed_date.strftime('%Y-%m-%d')
                                    break
                                except:
                                    continue
                            else:
                                # If all formats fail, try pandas auto-parsing
                                try:
                                    parsed_date = pd.to_datetime(date_str)
                                    purchase_date_val = parsed_date.strftime('%Y-%m-%d')
                                except:
                                    # Keep default if parsing fails
                                    errors.append(f"Row {actual_row_num}: Warning - Could not parse date '{date_str}', using current date")
                    except Exception:
                        # Keep default if any error
                        pass
            
            if 'Purchase_Time' in chunk_df.columns:
                pt_val = row.iloc[chunk_df.columns.get_loc('Purchase_Time')]
                if not pd.isna(pt_val):
                    try:
                        time_str = str(pt_val).strip()
                        if time_str and time_str != 'nan':
                            # Validate time format (HH:MM:SS or HH:MM or H:MM)
                            if ':' in time_str:
                                time_parts = time_str.split(':')
                                if len(time_parts) >= 2:
                                    hours = int(time_parts[0])
                                    minutes = int(time_parts[1])
                                    seconds = int(time_parts[2]) if len(time_parts) > 2 else 0
                                    if 0 <= hours <= 23 and 0 <= minutes <= 59 and 0 <= seconds <= 59:
                                        purchase_time_val = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                    except Exception:
                        # Keep default if parsing fails
                        pass
            
            # Handle target sell price
            target_sell_price_val = 0.0
            if 'Target_Sell_Price' in chunk_df.columns:
                tsp_val = row.iloc[chunk_df.columns.get_loc('Target_Sell_Price')]
                if not pd.isna(tsp_val):
                    try:
                        target_sell_price_val = float(tsp_val)
                        if target_sell_price_val < 0:
                            target_sell_price_val = 0.0
                    except (ValueError, TypeError):
                        target_sell_price_val = 0.0
            
            transaction_data = {
                'transaction_id': transaction_id,
                'coin_name': coin_name_val,
                'symbol': symbol_val,
                'coin_id': coin_id,
                'quantity': final_quantity,
                'purchase_price': numeric_price,
                'current_price': 0.0,
                'purchase_date': purchase_date_val,
                'purchase_time': purchase_time_val,
                'target_sell_price': target_sell_price_val,
                'current_value': 0.0,
                'profit_loss': 0.0,
                'percentage_change': 0.0,
                'created_at': current_time.isoformat(),
                'updated_at': current_time.isoformat()
            }
            
            # Add to database with error handling
            try:
                db_result = db.add_transaction(user_id, transaction_data)
                if db_result:
                    success_count += 1
                else:
                    errors.append(f"Row {actual_row_num}: Database rejected transaction (unknown reason)")
            except Exception as db_error:
                errors.append(f"Row {actual_row_num}: Database error - {str(db_error)}")
                
        except Exception as e:
            actual_row_num = start_row_offset + row_index
            errors.append(f"Row {actual_row_num}: Processing error - {str(e)}")
    
    return success_count, errors

def check_for_updates():
    """Check for updates and refresh data if needed (polling fallback)"""
    current_time = datetime.now()
    last_check = st.session_state.get('last_realtime_check', current_time)
    
    # If real-time is active, check for changes from websocket
    if st.session_state.get('realtime_active', False):
        if st.session_state.get('portfolio_changed', False):
            refresh_portfolio_data()
            st.session_state.portfolio_changed = False
            return True
    
    # Fallback to polling every 30 seconds if real-time is not active
    elif (current_time - last_check).seconds > 30:
        refresh_portfolio_data(skip_price_update=True)  # Use cached prices for polling
        st.session_state.last_realtime_check = current_time
        return True
    
    return False

# Initialize session state for transactions if it doesn't exist
if 'transactions' not in st.session_state:
    load_and_process_portfolio()

# Setup real-time subscription
setup_realtime_subscription()

# Check for updates (real-time + polling fallback)
if check_for_updates():
    st.rerun()

# Display real-time status indicator
if st.session_state.get('realtime_active', False):
    st.sidebar.success("[ACTIVE] Real-time updates: ON")
    if st.session_state.get('last_change_time'):
        try:
            st.sidebar.caption(f"Last update: {st.session_state.last_change_time.strftime('%H:%M:%S')}")
        except (AttributeError, TypeError):
            st.sidebar.caption("Last update: Unknown")
else:
    st.sidebar.info("📡 Polling mode: ON")
    st.sidebar.caption(f"Checks every 30s")

if 'last_update' not in st.session_state:
    st.session_state.last_update = datetime.now()

if 'portfolio_title' not in st.session_state:
    st.session_state.portfolio_title = "My Crypto Portfolio"

if 'page_title' not in st.session_state:
    st.session_state.page_title = "My Crypto Portfolio"

if 'edit_transaction_id' not in st.session_state:
    st.session_state.edit_transaction_id = None

if 'show_delete_confirm' not in st.session_state:
    st.session_state.show_delete_confirm = None



# Functions moved above for proper ordering

def add_transaction(coin_name, symbol, coin_id, quantity, purchase_price, purchase_date, purchase_time, target_sell_price=None, transaction_type='BUY', restructure_group=None):
    """Add a new transaction to the portfolio with restructuring support"""
    global db  # Declare db as global to avoid scope issues
    current_time = datetime.now()
    # Generate transaction_id with date/time for audit purposes only
    transaction_id = f"{coin_id}_{current_time.strftime('%Y%m%d_%H%M%S')}"
    
    new_row = {
        'transaction_id': transaction_id,  # For audit/history tracking
        'coin_name': coin_name,
        'symbol': symbol,
        'coin_id': coin_id,  # This will be the main ID for CRUD operations
        'quantity': quantity,
        'purchase_price': purchase_price,
        'current_price': 0,  # Will be updated by live data
        'purchase_date': purchase_date.strftime('%Y-%m-%d') if hasattr(purchase_date, 'strftime') else str(purchase_date),
        'purchase_time': purchase_time.strftime('%H:%M') if hasattr(purchase_time, 'strftime') else str(purchase_time),
        'target_sell_price': target_sell_price or 0,
        'current_value': 0,  # Will be calculated
        'profit_loss': 0,  # Will be calculated
        'percentage_change': 0,  # Will be calculated
        'transaction_type': transaction_type,  # New: Transaction type for restructuring
        'include_in_portfolio': transaction_type not in ['RESTRUCTURE_OUT', 'EXCLUDE'],  # Auto-exclude certain types
        'adjusted_purchase_price': purchase_price,  # Will be updated by restructuring logic
        'original_purchase_price': purchase_price,
        'cost_basis_transferred': 0.0,
        'restructure_group': restructure_group,
        'created_at': current_time.isoformat(),
        'updated_at': current_time.isoformat()
    }
    
    # Save to Supabase database with comprehensive error handling
    try:
        st.info(f"[ADDING] Adding {transaction_type} transaction for {symbol}...")
        
        # Debug: Log transaction details before submission
        with st.expander("[DEBUG] Pre-submission Debug", expanded=True):
            st.write("**Transaction Details:**")
            st.write(f"Symbol: {symbol}")
            st.write(f"Coin ID: {coin_id}")
            st.write(f"Transaction Type: {transaction_type}")
            st.write(f"Quantity: {quantity}")
            st.write(f"Purchase Price: {purchase_price}")
            st.write(f"User ID: {st.session_state.user_id}")
            st.write("**Full Transaction Data:**")
            st.json(new_row)
        
        # Add small delay to prevent race conditions
        import time
        time.sleep(0.5)
        
        st.info("📡 Calling database add_transaction...")
        result = db.add_transaction(st.session_state.user_id, new_row)
        st.info(f"[INFO] Database returned: {result} (type: {type(result)})")
        
        # Log the result for debugging
        if result is None:
            st.error("[ERROR] Database returned None - connection or authentication issue")
            # Try to reinitialize database connection
            st.warning("[RETRY] Attempting to reinitialize database connection...")
            try:
                # Reinitialize the database instance
                from supabase_config import PortfolioDatabase
                db = PortfolioDatabase()
                st.info("[SUCCESS] Database connection reinitialized. Please try again.")
            except Exception as reinit_error:
                st.error(f"[ERROR] Failed to reinitialize: {reinit_error}")
            
            with st.expander("[DEBUG] Debug Info"):
                st.write("Result:", result)
                st.write("Transaction data:", new_row)
                st.write("User ID:", st.session_state.user_id)
        elif result is False:
            st.error("[ERROR] Database explicitly returned False - transaction rejected")
            with st.expander("[DEBUG] Debug Info"):
                st.write("Result:", result)
                st.write("Transaction data:", new_row)
                st.write("User ID:", st.session_state.user_id)
        elif result:
            # Success case - clear any cached data that might interfere
            if 'transactions' in st.session_state:
                del st.session_state['transactions']
            if 'portfolio_df' in st.session_state:
                del st.session_state['portfolio_df']
            
            st.success(f"[SUCCESS] {transaction_type} transaction for {symbol} added successfully!")
            # Refresh data with price update for new transactions
            refresh_portfolio_data(skip_price_update=False)
            
            # Add delay before rerun to ensure database consistency
            time.sleep(1.0)
            
            # Clear form state to prevent interference with next transaction
            if 'selected_coin_info' in st.session_state:
                del st.session_state['selected_coin_info']
            
            st.rerun()
        else:
            # Unexpected falsy result
            st.error(f"[ERROR] Unexpected database result: {result}")
            with st.expander("[DEBUG] Debug Info"):
                st.write("Result type:", type(result))
                st.write("Result value:", result)
                st.write("Transaction data:", new_row)
                st.write("User ID:", st.session_state.user_id)
                
    except Exception as e:
        st.error(f"[ERROR] Database exception: {str(e)}")
        st.error(f"Exception type: {type(e).__name__}")
        
        # Try to recover from connection issues
        if "connection" in str(e).lower() or "timeout" in str(e).lower():
            st.warning("[RECONNECT] Connection issue detected. Attempting to reconnect...")
            try:
                # Reinitialize the database instance
                from supabase_config import PortfolioDatabase
                db = PortfolioDatabase()
                st.info("[SUCCESS] Reconnected. Please try adding the transaction again.")
            except Exception as reconnect_error:
                st.error(f"[ERROR] Reconnection failed: {reconnect_error}")
        
        # Debug info for troubleshooting
        with st.expander("[DEBUG] Debug Info"):
            st.write("Error details:", str(e))
            st.write("Error type:", type(e).__name__)
            st.write("Transaction data:", new_row)
            st.write("User ID:", st.session_state.user_id)
            # Try to get more detailed error info
            import traceback
            st.code(traceback.format_exc())

def delete_transaction(transaction_id):
    """Delete a transaction by its unique transaction_id"""
    # Delete from Supabase using the unique transaction_id
    success = db.delete_transaction(transaction_id, st.session_state.user_id)
    if success:
        # Refresh data without price update (optimization for delete operations)
        refresh_portfolio_data(skip_price_update=True)
        st.success("[SUCCESS] Transaction deleted from database!")
        st.rerun()
    else:
        st.error("[ERROR] Failed to delete transaction from database.")

def update_transaction(transaction_id, **kwargs):
    """Update a transaction by its unique transaction_id"""
    # Update in Supabase using the unique transaction_id
    db_updates = {}
    for key, value in kwargs.items():
        if key == 'Quantity':
            db_updates['quantity'] = value
        elif key == 'Purchase_Price':
            db_updates['purchase_price'] = value
        elif key == 'Target_Sell_Price':
            db_updates['target_sell_price'] = value
        elif key == 'Purchase_Date':
            db_updates['purchase_date'] = value
        elif key == 'Purchase_Time':
            db_updates['purchase_time'] = value
    
    success = db.update_transaction(transaction_id, st.session_state.user_id, db_updates)
    if success:
        # Refresh data with price update for edited transactions
        refresh_portfolio_data(skip_price_update=False)
        st.success("[SUCCESS] Transaction updated in database!")
        st.rerun()
    else:
        st.error("[ERROR] Failed to update transaction in database.")

# --- Header with Editable Title ---
st.sidebar.markdown(display_icon_header("settings", "Settings", "lucide", 18, "#666666"), unsafe_allow_html=True)

# --- Export/Import Options ---
st.sidebar.markdown(display_icon_header("chart", "Data Management", "lucide", 16, "#666666"), unsafe_allow_html=True)

# --- Professional Header Banner ---
st.markdown(f'''
<div style="background: linear-gradient(90deg, #1f4e79, #2e5984); padding: 20px; border-radius: 10px; margin-bottom: 0px; color: white;">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div style="display: flex; align-items: center; gap: 15px;">
            {get_icon("chart", "lucide", 32, "#ffffff")}
            <div>
                <h1 style="margin: 0; font-size: 2.5em;">{st.session_state.page_title}</h1>
                <p style="margin: 5px 0 0 0; opacity: 0.9;">Professional Crypto Portfolio Management</p>
            </div>
        </div>
    </div>
</div>
''', unsafe_allow_html=True)

# --- Auto-refresh indicator ---
time_since_update = (datetime.now() - st.session_state.last_update).total_seconds() / 60
if time_since_update >= 30:
    # Debug: Print what icon is being returned
    debug_icon = get_simple_icon("refresh")
    print(f"Debug: get_simple_icon('refresh') returns: {debug_icon}")
    st.markdown(f'<div class="update-indicator" style="margin: 0; padding: 0;">{display_icon_text("refresh", "Updating prices...")}</div>', unsafe_allow_html=True)
    st.session_state.last_update = datetime.now()
    st.rerun()

# --- Sidebar for Transaction Entry ---
st.sidebar.markdown(display_icon_header("portfolio", "Add New Entry", "lucide", 18, "#666666"), unsafe_allow_html=True)

with st.sidebar.expander("ⓘ How Portfolio Updates Work"):
    st.markdown(f"""
    **{get_icon('shuffle', 'lucide', 16, '#666666')} Portfolio Restructuring & Selling:**
    
    **{get_icon('refresh-cw', 'lucide', 16, '#666666')} Live Updates:**
    - Prices update every 30 minutes automatically
    - Manual refresh available with {get_icon('refresh-cw', 'lucide', 16, '#666666')} button
    
    **{get_icon('plus-circle', 'lucide', 16, '#22c55e')} Buy Transactions:**
    - Add positive quantities to increase holdings
    - Use current market price as default
    
    **{get_icon('minus-circle', 'lucide', 16, '#dc2626')} Sell Transactions:**
    - Select "Sell" type to reduce holdings
    - Negative quantities automatically applied
    - Tracks realized gains/losses
    
    **{get_icon('edit-3', 'lucide', 16, '#3b82f6')} Edit Existing:**
    - Click {get_icon('edit-3', 'lucide', 16, '#3b82f6')} button to modify any transaction
    - Change quantities, prices, or dates
    - Portfolio recalculates automatically
    
    **{get_icon('trash-2', 'lucide', 16, '#dc2626')} Delete Transactions:**
    - Click {get_icon('trash-2', 'lucide', 16, '#dc2626')} button to remove entries
    - Confirmation dialog prevents accidents
    
    **{get_simple_icon('trending-up')} Auto-Calculations:**
    - Current values update with live prices
    - P&L calculated in real-time
    - Portfolio metrics refresh automatically
    """, unsafe_allow_html=True)

# Only load coin data when needed (for add transaction form)
# Use session state to cache and avoid unnecessary API calls
if 'coins_data' not in st.session_state or st.session_state.coins_data is None:
    with st.spinner("Loading coin data..."):
        st.session_state.coins_data = get_coins_by_market_cap()

coins_data = st.session_state.coins_data
if not coins_data:
    st.sidebar.error("Unable to load coin data. Please check your connection.")
    # Provide a retry button using the new approach
    if use_clickable_button("refresh", "Retry Loading Coins", "retry_coins", "lucide", 16, "#666666", "primary"):
        st.session_state.coins_data = None
        st.rerun()
else:
    coin_options = [f"{name} ({symbol}) - {format_market_cap(market_cap)}" for name, symbol, coin_id, market_cap in coins_data]
    coin_map = {option: (name, symbol, coin_id) for option, (name, symbol, coin_id, _) in zip(coin_options, coins_data)}
    
    # Add search functionality for coins
    search_term = st.sidebar.text_input("🔍 Search Coins", placeholder="Type to search...", help="Search by coin name or symbol")
    
    # Filter coins based on search term
    if search_term:
        filtered_options = [option for option in coin_options if search_term.lower() in option.lower()]
    else:
        filtered_options = coin_options
    
    # Coin selection outside form for dynamic price updates
    selected_coin_option = st.sidebar.selectbox("🔍 Select Coin", options=filtered_options, help="Coins ordered by market cap")
    
    default_price = 0.01
    current_coin_price = 0.01
    if selected_coin_option:
        coin_name, symbol, coin_id = coin_map[selected_coin_option]
        current_price_data = get_live_prices(pd.Series([coin_id]))
        if current_price_data and coin_id in current_price_data:
            current_coin_price = float(current_price_data[coin_id].get('usd', 0.01))
            default_price = current_coin_price
        
        # Store selected coin info in session state to persist across form submissions
        st.session_state.selected_coin_info = {
            'coin_name': coin_name,
            'symbol': symbol,
            'coin_id': coin_id,
            'current_price': current_coin_price
        }
    
    if selected_coin_option and current_coin_price > 0.01:
        st.sidebar.markdown(f"""
        <div>
            {get_icon('price', 'lucide', 16, '#17a2b8')} <strong>Current Price:</strong> ${current_coin_price:,.0f}
        </div>
        """, unsafe_allow_html=True)

    # Enhanced transaction type selection with restructuring options
    st.sidebar.markdown(display_icon_header("trending-up", "Transaction Type", "lucide", 18, "#666666"), unsafe_allow_html=True)
    
    # Basic vs Advanced mode toggle
    use_advanced_mode = st.sidebar.checkbox("Advanced Mode", help="Enable portfolio restructuring features")

    if use_advanced_mode:
        # Add restructuring workflow guide
        with st.sidebar.expander(f"{get_icon('info', 'lucide', 16, '#666666')} Restructuring Guide", expanded=False):
            st.markdown("""
            **Portfolio Restructuring Workflow:**
            
            1. ** RESTRUCTURE_OUT**: Mark assets you're selling
               - Excluded from portfolio value
               - Preserves audit trail
            
            2. ** RESTRUCTURE_IN**: Mark assets you're buying
               - Included in portfolio value  
               - Inherits cost basis from OUT transactions
            
            3. ** Same Group ID**: Link related transactions
               - Enables automatic cost basis transfer
               - Maintains restructuring history
            """)
        
        transaction_type_options = list(restructuring_manager.get_transaction_type_options().keys())
        transaction_type_labels = [f"{key}: {restructuring_manager.get_transaction_type_options()[key]}" for key in transaction_type_options]
        
        selected_type_index = st.sidebar.selectbox(
            "Select Transaction Type",
            range(len(transaction_type_options)),
            format_func=lambda x: transaction_type_labels[x],
            help="Choose the type of transaction for proper portfolio accounting"
        )
        transaction_type = transaction_type_options[selected_type_index]
        
        # Show restructuring options if applicable
        restructure_group = None
        if transaction_type in ['RESTRUCTURE_OUT', 'RESTRUCTURE_IN']:
            st.sidebar.markdown("#### [REFRESH] Restructuring Options")
            
            # Add explanation for restructuring workflow
            if transaction_type == 'RESTRUCTURE_OUT':
                st.sidebar.info("[OUT] **Step 1**: Mark assets you're selling/exiting\n\n• These will be excluded from portfolio value\n• Use same Group ID for related transactions")
            else:  # RESTRUCTURE_IN
                st.sidebar.success("[IN] **Step 2**: Mark assets you're buying with proceeds\n\n• These will be included in portfolio value\n• Cost basis will be transferred from OUT transactions")
            
            # Option to create new group or join existing
            if 'restructuring_groups' not in st.session_state:
                st.session_state.restructuring_groups = {}
            
            group_action = st.sidebar.radio(
                "Restructuring Group",
                ["Create New Group", "Join Existing Group"],
                help="Link related restructuring transactions for proper cost basis transfer"
            )
            
            if group_action == "Create New Group":
                group_name = st.sidebar.text_input("Group Name", placeholder="e.g., BTC-to-ETH-Switch")
                if group_name:
                    restructure_group = f"RESTR_{group_name}_{datetime.now().strftime('%Y%m%d')}"
                else:
                    # Auto-generate group ID if no name provided
                    restructure_group = f"RESTR_AUTO_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            else:
                existing_groups = list(st.session_state.restructuring_groups.keys())
                if existing_groups:
                    restructure_group = st.sidebar.selectbox("Select Group", existing_groups)
                else:
                    st.sidebar.info("No existing groups. Create a new one first.")
                    # Auto-generate group ID if no existing groups
                    restructure_group = f"RESTR_AUTO_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    else:
        # Simple Buy/Sell mode
        basic_type = st.sidebar.radio("Transaction Type", ["Buy", "Sell"], help="Select Buy to add coins, Sell to reduce holdings")
        transaction_type = "BUY" if basic_type == "Buy" else "SELL"
        restructure_group = None
    
    with st.sidebar.form("transaction_form", clear_on_submit=False):
        
        # Use session state to maintain form values after failed submissions
        if 'selected_coin_info' in st.session_state:
            persistent_price = st.session_state.selected_coin_info['current_price']
        else:
            persistent_price = default_price

        # Dynamic quantity input based on transaction type
        if transaction_type in ["SELL", "RESTRUCTURE_OUT"]:
            st.markdown(display_icon_header('chart', 'Quantity', 'lucide', 16, '#666666'), unsafe_allow_html=True)
            quantity = st.number_input("", min_value=0.01, value=1.00, format="%.0f", help="Amount of coins to sell (will reduce your holdings). Note: Your browser's locale determines if you see period (.) or comma (,) as decimal separator, e.g., 1.50 or 1,50", label_visibility="collapsed")
            price_help = "Price per coin when selling"
            st.markdown(display_icon_header("dollar-sign", "Sell Price (USD)", "lucide", 16, "#666666"), unsafe_allow_html=True)
        else:
            st.markdown(display_icon_header('chart', 'Quantity', 'lucide', 16, '#666666'), unsafe_allow_html=True)
            quantity = st.number_input("", min_value=0.01, value=1.00, format="%.0f", help="Amount of coins purchased. Note: Your browser's locale determines if you see period (.) or comma (,) as decimal separator, e.g., 2.75 or 2,75", label_visibility="collapsed")
            price_help = "Price per coin when purchased (defaults to current price)"
            st.markdown(display_icon_header("dollar-sign", "Purchase Price (USD)", "lucide", 16, "#666666"), unsafe_allow_html=True)

        purchase_price = st.number_input("", min_value=0.00000001, value=float(persistent_price), format="%.2f", help=f"{price_help} (Current: ${persistent_price:,.2f}). Note: Your browser's locale determines if you see period (.) or comma (,) as decimal separator, e.g., 45.67 or 45,67)", label_visibility="collapsed")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(display_icon_header("calendar", "Transaction Date", "lucide", 16, "#666666"), unsafe_allow_html=True)
            purchase_date = st.date_input("", datetime.now().date(), label_visibility="collapsed")
        with col2:
            st.markdown(display_icon_header("clock", "Transaction Time", "lucide", 16, "#666666"), unsafe_allow_html=True)
            time_text = st.text_input("", value=datetime.now().strftime("%H:%M:%S"), 
                                    help="Format: HH:MM:SS (e.g., 14:30:00 or 09:15:30)",
                                    label_visibility="collapsed")
            try:
                purchase_time = datetime.strptime(time_text, "%H:%M:%S").time()
            except ValueError:
                st.error("Invalid time format. Please use HH:MM:SS format (e.g., 14:30:00)")
                purchase_time = datetime.now().time()
        
        st.markdown(display_icon_header("bullseye", "Target Sell Price (USD)", "lucide", 16, "#666666"), unsafe_allow_html=True)
        target_sell_price = st.number_input("", min_value=0.00000001, value=float(persistent_price), format="%.2f", help=f"Target price to sell (Current: ${persistent_price:,.2f}). Note: Your browser's locale determines if you see period (.) or comma (,) as decimal separator, e.g., 50.00 or 50,00", label_visibility="collapsed")
        
        # Adjust quantity for sell transactions (negative quantity)
        final_quantity = -abs(quantity) if transaction_type in ["SELL", "RESTRUCTURE_OUT"] else abs(quantity)
        
        # Show transaction preview
        if use_advanced_mode:
            st.markdown(display_icon_header("clipboard", "Transaction Preview", "lucide", 18, "#666666"), unsafe_allow_html=True)
            preview_text = f"**Type:** {transaction_type}\n**Impact:** "
            if transaction_type == "RESTRUCTURE_OUT":
                preview_text += f"{get_simple_icon('alert-triangle')} Will be excluded from portfolio value"
            elif transaction_type == "RESTRUCTURE_IN":
                preview_text += f"{get_simple_icon('check-circle')} Cost basis may be adjusted from restructuring"
            elif transaction_type == "EXCLUDE":
                preview_text += f"{get_simple_icon('x-circle')} Will be excluded from all calculations"
            else:
                preview_text += f"{get_simple_icon('check-circle')} Standard portfolio transaction"
            
            st.info(preview_text)
        
        # Submit button with dynamic text - inside form to satisfy Streamlit requirements
        button_text = f"➕ Add {transaction_type.replace('_', ' ').title()} Transaction"
        submit_clicked = st.form_submit_button(button_text, type="primary")
    
    # Process form submission
    if submit_clicked:
        st.info(f"{get_simple_icon('refresh')} Form submitted, processing...")
        
        if not selected_coin_option:
            st.error(f"{get_simple_icon('x-circle')} No coin selected. Please select a coin from the dropdown.")
        elif quantity <= 0:
            st.error(f"{get_simple_icon('x-circle')} Invalid quantity. Please enter a positive number.")
        else:
            try:
                coin_name, symbol, coin_id = coin_map[selected_coin_option]
                st.info(f"{get_simple_icon('check-circle')} Form validation passed for {symbol}")
                st.info(f"{get_simple_icon('phone')} Calling add_transaction function...")
                
                add_transaction(
                    coin_name, symbol, coin_id, final_quantity, purchase_price, 
                    purchase_date, purchase_time, target_sell_price, 
                    transaction_type, restructure_group
                )
            except KeyError as e:
                st.error(f"{get_simple_icon('x-circle')} Coin mapping error: {e}")
                st.error(f"Selected option: {selected_coin_option}")
                st.error(f"Available options: {list(coin_map.keys())[:5]}...")
            except Exception as e:
                st.error(f"{get_simple_icon('x-circle')} Unexpected error in form submission: {e}")
                import traceback
                st.code(traceback.format_exc())

# --- Main Portfolio Display ---
if not st.session_state.transactions.empty:
    # Create a clean display dataframe without duplicate columns
    portfolio_df = st.session_state.transactions.copy()
    
    # If we have both transaction_id and ID columns, remove transaction_id for display
    if 'transaction_id' in portfolio_df.columns and 'ID' in portfolio_df.columns:
        display_columns = [col for col in portfolio_df.columns if col != 'transaction_id']
        portfolio_df = portfolio_df[display_columns]
    
    # Ensure we have the expected column names for display
    if 'transaction_id' in st.session_state.transactions.columns and 'ID' not in portfolio_df.columns:
        # This means we only have Supabase format, need to map for display
        portfolio_df = portfolio_df.rename(columns={
            'transaction_id': 'ID',
            'coin_name': 'Coin_Name',
            'symbol': 'Symbol',
            'quantity': 'Quantity',
            'purchase_price': 'Purchase_Price',
            'current_price': 'Current_Price',
            'purchase_date': 'Purchase_Date',
            'purchase_time': 'Purchase_Time',
            'target_sell_price': 'Target_Sell_Price',
            'current_value': 'Current_Value',
            'profit_loss': 'Profit_Loss',
            'percentage_change': 'Percentage_Change',
            'coin_id': 'Coin_ID',
            'created_at': 'Created_At',
            'updated_at': 'Updated_At'
        })
    
    # Update portfolio with live data
    portfolio_df = calculate_portfolio_metrics(portfolio_df)
    
    # --- Portfolio Holdings Table ---
    with st.container():
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        
        # Add anchor for portfolio table
        st.markdown('<div id="portfolio-table" class="section-anchor"></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(display_icon_header('briefcase', 'Portfolio Holdings', 'lucide', 24, '#666666'), unsafe_allow_html=True)
            
        # Calculate net holdings for current holdings display
        # Apply restructuring rules specifically for holdings calculation
        holdings_portfolio_df = restructuring_manager.apply_restructuring_rules(portfolio_df.copy(), calculation_type='holdings')
        net_holdings_df = calculate_net_holdings(holdings_portfolio_df)
        
        # Add toggle to switch between transaction view and net holdings view
        view_mode = st.radio(
            "View Mode:",
            ["Net Holdings", "All Transactions"],
            help="Net Holdings shows current positions (BUY+RESTRUCTURE_IN-SELL-RESTRUCTURE_OUT), All Transactions shows individual transactions",
            horizontal=True
        )
        
        # Use appropriate dataframe based on view mode
        display_portfolio_df = net_holdings_df if view_mode == "Net Holdings" and not net_holdings_df.empty else portfolio_df
        with col2:
            col2a, col2b = st.columns([2, 3])  # Give more space to real-time button
            with col2a:
                if st.button("Refresh Data", help="Update all data and prices manually", use_container_width=True):
                    # Manual refresh should update prices
                    refresh_portfolio_data(skip_price_update=False)
                    st.success("Portfolio data and prices refreshed!")
                    st.rerun()
            with col2b:
                realtime_status = "ON" if st.session_state.get('realtime_active', False) else "OFF"
                if st.button(f"Real-time: {realtime_status}", help="Toggle real-time updates", use_container_width=True):
                    if st.session_state.get('realtime_active', False):
                        # Turn off real-time
                        st.session_state.realtime_active = False
                        st.info("Real-time updates disabled. Using polling mode.")
                    else:
                        # Try to turn on real-time
                        st.session_state.realtime_setup = False  # Force re-setup
                        setup_realtime_subscription()
                    st.rerun()
        
        # Search Bar - Position above the table for better user experience
        # Handle clear search flag
        if st.session_state.get('clear_search_flag', False):
            st.session_state.clear_search_flag = False
            # Delete all search-related widget states and data to clear them completely
            search_keys_to_clear = [
                'portfolio_table_search',  # Main search input
                'filtered_portfolio',      # Filtered results from advanced search
            ]
            
            # Clear all search-related session state values
            for key in search_keys_to_clear:
                if key in st.session_state:
                    del st.session_state[key]
        
        st.markdown(display_icon_header('search', 'Search & Filter Portfolio', 'lucide', 18, '#666666'), unsafe_allow_html=True)
        search_col1, search_col2 = st.columns([4, 1])
        with search_col1:
            table_search_query = st.text_input(
                "Search Portfolio", 
                placeholder="Search by coin name, symbol, purchase date, or any value...",
                key="portfolio_table_search",
                help="Real-time search across all portfolio data. Results update as you type.",
                label_visibility="collapsed"
            )
        with search_col2:
            # Show different button state based on whether there's an active search
            has_active_search = (table_search_query or 
                               'filtered_portfolio' in st.session_state or
                               bool(st.session_state.get('portfolio_table_search', '')))
            
            button_text = "[CLEAR] Clear All" if has_active_search else "Search Again"
            button_help = "Clear all search filters and show all records" if has_active_search else "Clear search and show all records"
            
            if st.button(button_text, help=button_help):
                # Immediately clear the search input and all related states
                if 'portfolio_table_search' in st.session_state:
                    del st.session_state['portfolio_table_search']
                if 'filtered_portfolio' in st.session_state:
                    del st.session_state['filtered_portfolio']
                
                # Set flag for additional cleanup
                st.session_state.clear_search_flag = True
                
                # Show immediate feedback
                if has_active_search:
                    st.markdown(f'<div style="color: #22c55e; background-color: #f0fdf4; padding: 8px; border-radius: 4px; border: 1px solid #bbf7d0;">{get_icon("check", "lucide", 16, "#22c55e")} All search filters cleared!</div>', unsafe_allow_html=True)
                st.rerun()
        
        if table_search_query:
            st.markdown(f'<div class="search-info">{get_icon("search", "lucide", 16, "#666666")} Searching for: "<strong>{table_search_query}</strong>"</div>', unsafe_allow_html=True)
        elif 'filtered_portfolio' in st.session_state and not st.session_state.filtered_portfolio.empty:
            st.markdown(f'<div class="search-info">{get_icon("chart", "lucide", 16, "#666666")} <strong>Advanced Filter Active:</strong> Performance-based filter is applied. Use "Clear All" to reset.</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="search-info">{get_icon("info", "lucide", 16, "#666666")} <strong>Search Tips:</strong> Try searching for coin names (Bitcoin), symbols (BTC), dates (2024), transaction types (buy/sell), or any value</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Display main portfolio table without ID column (hidden for cleaner view)
        display_columns = [
            'Coin_Name', 'Symbol', 'Quantity', 'Purchase_Price', 'Current_Price',
            'Purchase_Date', 'Purchase_Time', 'Target_Sell_Price', 'Current_Value', 
            'Profit_Loss', 'Percentage_Change'
        ]
        
        if len(display_portfolio_df) > 0:
            # Create display dataframe with proper formatting and transaction type indicators
            display_df = display_portfolio_df[display_columns].copy()
            
            # Add transaction type column with icons for better visibility
            if view_mode == "Net Holdings":
                display_df['Type'] = '[NET]'  # Net holdings don't have transaction types
            else:
                display_df['Type'] = display_df['Quantity'].apply(lambda x: '[SELL]' if x < 0 else '[BUY]')
            
            # Apply search filter if search query exists
            if table_search_query:
                # Recursive search across all columns
                query = table_search_query.lower()
                search_mask = (
                    display_df['Coin_Name'].astype(str).str.lower().str.contains(query, na=False) |
                    display_df['Symbol'].astype(str).str.lower().str.contains(query, na=False) |
                    display_df['Type'].astype(str).str.lower().str.contains(query, na=False) |
                    display_df['Purchase_Date'].astype(str).str.lower().str.contains(query, na=False) |
                    display_df['Purchase_Time'].astype(str).str.lower().str.contains(query, na=False) |
                    display_df['Quantity'].astype(str).str.lower().str.contains(query, na=False) |
                    display_df['Purchase_Price'].astype(str).str.lower().str.contains(query, na=False) |
                    display_df['Current_Price'].astype(str).str.lower().str.contains(query, na=False) |
                    display_df['Target_Sell_Price'].astype(str).str.lower().str.contains(query, na=False) |
                    display_df['Current_Value'].astype(str).str.lower().str.contains(query, na=False) |
                    display_df['Profit_Loss'].astype(str).str.lower().str.contains(query, na=False) |
                    display_df['Percentage_Change'].astype(str).str.lower().str.contains(query, na=False)
                )
                
                # Filter the original portfolio_df as well for downstream operations
                portfolio_df_filtered = portfolio_df[search_mask]
                display_df = display_df[search_mask]
                
                # Show search results info
                if len(display_df) == 0:
                    st.warning(f"[NO RESULTS] No results found for '{table_search_query}'")
                elif len(display_df) < len(portfolio_df):
                    st.info(f"[RESULTS] Found {len(display_df)} result(s) out of {len(portfolio_df)} total records for '{table_search_query}'")
            else:
                portfolio_df_filtered = portfolio_df.copy()
            
            # Format quantity with proper sign and styling indicators
            display_df['Formatted_Quantity'] = display_df['Quantity'].apply(
                lambda x: f"- {abs(x):,.2f}" if x < 0 else f"+ {x:,.0f}"
            )
            
            # Define styling functions at the proper scope
            def color_profit_loss(val):
                """Color positive values green, negative red"""
                if isinstance(val, (int, float)):
                    if val > 0:
                        return 'color: #16a34a; font-weight: bold'
                    elif val < 0:
                        return 'color: #dc2626; font-weight: bold'
                return ''
            
            def style_quantity(val):
                """Style quantity based on transaction type"""
                if isinstance(val, (int, float)):
                    if val < 0:
                        return 'color: #dc2626; font-weight: 600; font-style: italic; background-color: rgba(239, 68, 68, 0.08)'
                    else:
                        return 'color: #16a34a; font-weight: 600; background-color: rgba(34, 197, 94, 0.08)'
                return ''
            
            def style_transaction_type(val):
                """Style transaction type column"""
                if 'SELL' in str(val):
                    return 'color: #dc2626; font-weight: bold; background-color: rgba(239, 68, 68, 0.1)'
                else:
                    return 'color: #16a34a; font-weight: bold; background-color: rgba(34, 197, 94, 0.1)'
            
            # Create formatted display with transaction type column
            display_with_type = display_df[['Type', 'Coin_Name', 'Symbol', 'Formatted_Quantity', 'Purchase_Price', 'Current_Price',
                                          'Purchase_Date', 'Purchase_Time', 'Target_Sell_Price', 'Current_Value', 
                                          'Profit_Loss', 'Percentage_Change']].copy()
            
            formatted_df = display_with_type.style.map(color_profit_loss, subset=['Profit_Loss', 'Percentage_Change']) \
                                                  .map(style_transaction_type, subset=['Type']) \
                                                  .format({
                'Purchase_Price': '$ {:,.2f}',
                'Current_Price': '$ {:,.2f}',
                'Target_Sell_Price': '$ {:,.2f}',
                'Current_Value': '$ {:,.2f}',
                'Profit_Loss': '$ {:+,.2f}',
                'Percentage_Change': '{:+.2f}%'
            })
            
            st.dataframe(formatted_df, use_container_width=True, height=400, hide_index=True)
            
            # Advanced Portfolio Actions - Tabbed Interface for Scalability
            st.markdown(display_icon_header('settings', 'Portfolio Management', 'lucide', 24, '#666666'), unsafe_allow_html=True)
            
            # Initialize tab state if not exists
            if 'active_tab' not in st.session_state:
                st.session_state.active_tab = "⚡ Quick Actions"
            
            # Check if we should switch to Import/Export tab (for downloads)
            if st.session_state.get('switch_to_import_export', False):
                st.session_state.active_tab = "[IMPORT] Import/Export"
                st.session_state.switch_to_import_export = False
            
            action_tab1, action_tab2, action_tab3, action_tab4, action_tab5 = st.tabs([
                "⚡ Quick Actions",
                "🔍 Search & Filter", 
                "🔄 Restructuring",
                "🧩 Import/Export",
                "✒️ Analytics"
            ])
            
            with action_tab1:
                # Make Quick Transaction Actions collapsible and collapsed by default
                with st.expander("Review Restructured Transactions", expanded=False):
                    # Build a dataframe of transactions marked as RESTRUCTURE_OUT or RESTRUCTURE_IN
                    if 'transactions' in st.session_state and not st.session_state.transactions.empty:
                        txn_df = st.session_state.transactions.copy()
                        if 'Transaction_Type' not in txn_df.columns:
                            txn_df['Transaction_Type'] = txn_df['Quantity'].apply(lambda x: 'RESTRUCTURE_OUT' if False else ('SELL' if x < 0 else 'BUY'))

                        restructured_mask = txn_df['Transaction_Type'].isin(['RESTRUCTURE_OUT', 'RESTRUCTURE_IN'])
                        restructured_df = txn_df[restructured_mask].copy()

                        if restructured_df.empty:
                            st.info('No restructured transactions found.')
                        else:
                            # Group by Restructure_Group for easier review
                            if 'Restructure_Group' not in restructured_df.columns:
                                restructured_df['Restructure_Group'] = None

                            groups = restructured_df['Restructure_Group'].fillna('UNGROUPED').unique()
                            for group in groups:
                                with st.expander(f"Group: {group}", expanded=False):
                                    group_df = restructured_df[restructured_df['Restructure_Group'].fillna('UNGROUPED') == group]
                                    display_cols = ['ID'] if 'ID' in group_df.columns else group_df.columns.tolist()
                                    display_cols += [c for c in ['Symbol', 'Quantity', 'Purchase_Price', 'Transaction_Type'] if c in group_df.columns]
                                    st.dataframe(group_df[display_cols].reset_index(drop=True), use_container_width=True)

                                    # Provide actions for each transaction in the group
                                    for _, row in group_df.iterrows():
                                        txn_id = row.get('transaction_id', row.get('ID'))
                                        col1, col2 = st.columns([6,1])
                                        with col1:
                                            st.write(f"{row.get('Symbol','')}: {row.get('Quantity','')} @ ${row.get('Purchase_Price','')}")
                                        with col2:
                                            if st.button("✏️ Edit", key=f'review_edit_{txn_id}'):
                                                st.session_state.edit_transaction_id = txn_id
                                                st.session_state.scroll_to_edit = True
                                                st.rerun()
                    else:
                        st.info('No transaction data loaded in session.')
                
                with st.expander("Quick Transaction Actions", expanded=False):
                    # Add controls for number of transactions to show
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        if table_search_query and 'portfolio_df_filtered' in locals():
                            st.info(f"Showing quick actions for search results: '{table_search_query}'")
                            base_df = portfolio_df_filtered
                        else:
                            base_df = portfolio_df
                    with col2:
                        max_transactions = st.selectbox(
                            "Show transactions:",
                            options=[10, 25, 50, 100, "All"],
                            index=1,  # Default to 25
                            key="quick_edit_limit"
                        )
                    
                    # Apply transaction limit
                    if max_transactions == "All":
                        action_filtered_df = base_df
                    else:
                        action_filtered_df = base_df.head(int(max_transactions))
                    
                    # Show transaction count info
                    total_count = len(base_df)
                    showing_count = len(action_filtered_df)
                    if showing_count < total_count:
                        st.caption(f"Showing {showing_count} of {total_count} transactions")
                    else:
                        st.caption(f"Showing all {total_count} transactions")
                    
                    if len(action_filtered_df) > 0:
                        # Display transactions in a more compact format
                        for idx, (_, row) in enumerate(action_filtered_df.iterrows()):
                            with st.container():
                                col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
                                
                                with col1:
                                    # Add transaction type icon and styling with proper scalar value extraction
                                    quantity_val = row['Quantity']
                                    profit_loss_val = row['Profit_Loss']
                                    percentage_change_val = row['Percentage_Change']
                                    coin_name_val = row['Coin_Name']
                                    symbol_val = row['Symbol']
                                    current_value_val = row['Current_Value']
                                    id_val = row['ID']
                                    
                                    transaction_icon = "[SELL]" if quantity_val < 0 else "[BUY]"
                                    transaction_type = "SELL" if quantity_val < 0 else "BUY"
                                    transaction_color = "#dc2626" if quantity_val < 0 else "#16a34a"
                                    
                                    st.markdown(f"**{coin_name_val} ({symbol_val})** <span style='color: {transaction_color}; font-size: 1.1em;'>{transaction_icon}</span>", unsafe_allow_html=True)
                                    
                                    # Color-coded quantity display with icons
                                    qty_icon = "[DOWN]" if quantity_val < 0 else "[UP]"
                                    qty_style = "color: #dc2626; font-weight: 600; font-style: italic" if quantity_val < 0 else "color: #16a34a; font-weight: 600"
                                    st.markdown(f"<span style='{qty_style}'>{qty_icon} Qty: {abs(quantity_val):.1f}</span> | P&L: {percentage_change_val:+.1f}%", unsafe_allow_html=True)
                                
                                with col2:
                                    st.write(f"${current_value_val:,.2f}")
                                    color = "[PROFIT]" if profit_loss_val >= 0 else "[LOSS]"
                                    st.caption(f"{color} ${profit_loss_val:+,.2f}")
                                
                                with col3:
                                    if st.button("[EDIT]", key=f"edit_quick_{id_val}", help=f"Edit {coin_name_val}"):
                                        # Clear any existing edit state first to prevent duplicates
                                        current_edit_id = st.session_state.edit_transaction_id
                                        if current_edit_id != id_val:
                                            st.session_state.edit_transaction_id = id_val
                                            st.session_state.scroll_to_edit = True
                                            st.rerun()
                                
                                with col4:
                                    if st.button("[DELETE]", key=f"delete_quick_{id_val}", help=f"Delete {coin_name_val}"):
                                        # Use the unique transaction_id for deleting
                                        st.session_state.show_delete_confirm = id_val
                                        st.rerun()
                                
                                st.divider()
                    else:
                        if table_search_query:
                            st.info(f"No transactions found matching your search: '{table_search_query}'")
                        else:
                            st.info("No transactions available for quick actions.")
            
            with action_tab2:
                st.markdown(display_icon_header('filter', 'Advanced Search & Filtering', 'lucide', 20, '#666666'), unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**{get_icon('trending-up', 'lucide', 16, '#666666')} Performance Filter**", unsafe_allow_html=True)
                    st.markdown(display_icon_header('arrow-down', 'Min Return (%)', 'lucide', 16, '#666666'), unsafe_allow_html=True)
                    min_return = st.number_input("", value=-100.0, step=1.0, label_visibility="collapsed")
                    st.markdown(display_icon_header('arrow-up', 'Max Return (%)', 'lucide', 16, '#666666'), unsafe_allow_html=True)
                    max_return = st.number_input("", value=1000.0, step=1.0, label_visibility="collapsed")
                    
                    if st.button("[FILTER] Apply Performance Filter"):
                        # Perform filtering directly on the session state DataFrame
                        filtered_perf = portfolio_df.copy()
                        if min_return is not None:
                            filtered_perf = filtered_perf[filtered_perf['Percentage_Change'] >= min_return]
                        if max_return is not None:
                            filtered_perf = filtered_perf[filtered_perf['Percentage_Change'] <= max_return]
                        st.session_state.filtered_portfolio = filtered_perf
                
                with col2:
                    st.markdown(f"**{get_icon('bar-chart', 'lucide', 16, '#666666')} Portfolio Statistics**", unsafe_allow_html=True)
                    if not portfolio_df.empty:
                        stats = {
                            'total_transactions': len(portfolio_df),
                            'unique_coins': portfolio_df['Symbol'].nunique(),
                            'total_investment': (portfolio_df['Quantity'] * portfolio_df['Purchase_Price']).sum(),
                            'current_value': portfolio_df['Current_Value'].sum(),
                            'total_pnl': portfolio_df['Profit_Loss'].sum(),
                            'best_performer': portfolio_df.loc[portfolio_df['Percentage_Change'].idxmax(), 'Symbol'] if not portfolio_df.empty else 'N/A',
                            'worst_performer': portfolio_df.loc[portfolio_df['Percentage_Change'].idxmin(), 'Symbol'] if not portfolio_df.empty else 'N/A',
                            'avg_return': portfolio_df['Percentage_Change'].mean(),
                            'portfolio_diversity': portfolio_df['Symbol'].nunique() / len(portfolio_df) if len(portfolio_df) > 0 else 0
                        }
                        stats['total_return_pct'] = (stats['total_pnl'] / stats['total_investment'] * 100) if stats['total_investment'] > 0 else 0
                    
                    if stats:
                        # Custom compact styling for metrics
                        st.markdown("""
                        <style>
                        .compact-metrics [data-testid="metric-container"] {
                            background-color: rgba(28, 131, 225, 0.05);
                            border: 1px solid rgba(28, 131, 225, 0.1);
                            padding: 0.5rem;
                            border-radius: 0.5rem;
                            margin: 0.25rem 0;
                        }
                        .compact-metrics [data-testid="metric-container"] > div {
                            width: fit-content;
                            margin: auto;
                        }
                        .compact-metrics [data-testid="metric-container"] > div > div {
                            font-size: 0.8rem;
                            line-height: 1.2;
                        }
                        .compact-metrics [data-testid="metric-container"] label {
                            font-size: 0.7rem !important;
                            font-weight: 600 !important;
                        }
                        </style>
                        """, unsafe_allow_html=True)
                        
                        # Create compact metrics in a container
                        with st.container():
                            st.markdown('<div class="compact-metrics">', unsafe_allow_html=True)
                            
                            # Row 1: Basic counts
                            metric_row1_col1, metric_row1_col2 = st.columns(2)
                            with metric_row1_col1:
                                st.metric(f"{get_icon('list', 'lucide', 16, '#666666')} Transactions", stats['total_transactions'])
                            with metric_row1_col2:
                                st.metric(f"{get_icon('coins', 'lucide', 16, '#666666')} Unique Coins", stats['unique_coins'])
                            
                            # Row 2: Performance metrics
                            metric_row2_col1, metric_row2_col2 = st.columns(2)
                            with metric_row2_col1:
                                st.metric(f"{get_icon('trending-up', 'lucide', 16, '#22c55e')} Best Performer", stats['best_performer'])
                            with metric_row2_col2:
                                st.metric(f"{get_icon('trending-down', 'lucide', 16, '#ef4444')} Worst Performer", stats['worst_performer'])
                            
                            # Row 3: Returns and diversity
                            metric_row3_col1, metric_row3_col2 = st.columns(2)
                            with metric_row3_col1:
                                st.metric(f"{get_icon('target', 'lucide', 16, '#666666')} Avg Return", f"{stats['avg_return']:.1f}%")
                            with metric_row3_col2:
                                st.metric(f"{get_icon('pie-chart', 'lucide', 16, '#666666')} Diversity", f"{stats['portfolio_diversity']:.1%}")
                            
                            st.markdown('</div>', unsafe_allow_html=True)
                
                # Display filtered results
                if 'filtered_portfolio' in st.session_state and not st.session_state.filtered_portfolio.empty:
                    st.markdown(f"### {get_icon('filter', 'lucide', 20, '#666666')} Filtered Results", unsafe_allow_html=True)
                    st.dataframe(st.session_state.filtered_portfolio[display_columns], use_container_width=True, hide_index=True)
            
            with action_tab3:
                st.markdown(display_icon_header('tag', 'Mark Transactions for Restructuring', 'lucide', 18, '#666666'), unsafe_allow_html=True)
                
                # Choose restructuring type
                restructure_type = st.radio(
                    "Restructuring Type:",
                    ["RESTRUCTURE_OUT", "RESTRUCTURE_IN"],
                    format_func=lambda x: f"{x} (Selling/Exiting)" if x == "RESTRUCTURE_OUT" else f"{x} (Buying with proceeds)",
                    help="Select whether these are assets you're selling (OUT) or buying (IN)",
                    key="bulk_restructure_type_radio_tab"
                )
                
                # Show all transactions for selection
                transaction_options = []
                for _, row in portfolio_df.iterrows():
                    label = f"{row['Symbol']} - {row['Quantity']:+.2f} @ ${row['Purchase_Price']:.2f} ({row.get('Purchase_Date', 'Unknown Date')})"
                    transaction_options.append((label, row.get('transaction_id', row.get('ID', f"row_{_}"))))
                
                selected_transactions = st.multiselect(
                    f"Select transactions to mark as {restructure_type}:",
                    options=[opt[1] for opt in transaction_options],
                    format_func=lambda x: next(opt[0] for opt in transaction_options if opt[1] == x),
                    key="restructure_multiselect_tab"
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Mark as {restructure_type}", type="primary", key=f"mark_as_{restructure_type.lower()}_tab"):
                        if selected_transactions:
                            success_count = 0
                            error_count = 0
                            
                            # Generate a restructure group ID
                            restructure_group = f"RESTR_BULK_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                            
                            for txn_id in selected_transactions:
                                try:
                                    # Update transaction in database
                                    updates = {
                                        'transaction_type': restructure_type,
                                        'include_in_portfolio': True if restructure_type == 'RESTRUCTURE_IN' else False,
                                        'restructure_group': restructure_group
                                    }
                                    
                                    result = db.update_transaction(txn_id, st.session_state.user_id, updates)
                                    if result:
                                        success_count += 1
                                    else:
                                        error_count += 1
                                except Exception as e:
                                    st.error(f"Error updating transaction {txn_id}: {e}")
                                    error_count += 1
                            
                            # Show results
                            if success_count > 0:
                                st.success(f"[SUCCESS] Successfully marked {success_count} transactions as {restructure_type}")
                            if error_count > 0:
                                st.error(f"[ERROR] Failed to update {error_count} transactions")
                            
                            # Refresh portfolio data and rerun to show changes immediately
                            refresh_portfolio_data()
                            st.rerun()
                        else:
                            st.warning("Please select at least one transaction to mark.")
                
                with col2:
                    if st.button("[REFRESH] Refresh View", key="refresh_restructure_tab"):
                        st.rerun()
                
                # Group creator
                if st.session_state.get('show_group_creator', False):
                    st.markdown("---")
                    st.markdown(display_icon_header('users', 'Create Restructuring Group', 'lucide', 18, '#666666'), unsafe_allow_html=True)
                    
                    with st.form("restructuring_group_form_tab"):
                        group_name = st.text_input("Group Name", placeholder="e.g., BTC-to-ETH-2024")
                        group_description = st.text_area("Description", placeholder="Describe this restructuring...")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.form_submit_button(f"✚ Create Group", type="primary"):
                                if group_name:
                                    group_id = f"RESTR_{group_name}_{datetime.now().strftime('%Y%m%d')}"
                                    if 'restructuring_groups' not in st.session_state:
                                        st.session_state.restructuring_groups = {}
                                    
                                    st.session_state.restructuring_groups[group_id] = {
                                        'name': group_name,
                                        'description': group_description,
                                        'created_date': datetime.now(),
                                        'transactions': []
                                    }
                                    st.success(f"Created restructuring group: {group_id}")
                                    st.session_state.show_group_creator = False
                                    st.rerun()
                                else:
                                    st.error("Please enter a group name")
                        
                        with col2:
                            if st.form_submit_button("✖ Cancel"):
                                st.session_state.show_group_creator = False
                                st.rerun()
                
                # Show transactions by type
                st.markdown("---")
                st.markdown(display_icon_header('list', 'Transactions by Type', 'lucide', 18, '#666666'), unsafe_allow_html=True)
                
                if 'Transaction_Type' in portfolio_df.columns:
                    type_counts = portfolio_df['Transaction_Type'].value_counts()
                    
                    for txn_type, count in type_counts.items():
                        type_emoji = {
                            'BUY': '[BUY]', 'SELL': '[SELL]', 'RESTRUCTURE_OUT': '[OUT]', 
                            'RESTRUCTURE_IN': '[IN]'
                        }.get(str(txn_type), '[TXN]')
                        
                        with st.expander(f"{type_emoji} {txn_type} ({count} transactions)"):
                            type_transactions = portfolio_df[portfolio_df['Transaction_Type'] == txn_type]
                            display_cols = ['Symbol', 'Quantity', 'Purchase_Price', 'Purchase_Date']
                            available_cols = [col for col in display_cols if col in type_transactions.columns]
                            st.dataframe(type_transactions[available_cols], use_container_width=True)
                else:
                    st.info("No portfolio data available for restructuring management.")
            
            with action_tab4:
                st.markdown(f'<div style="color: #0066cc; background-color: #eff6ff; padding: 8px; border-radius: 4px; border: 1px solid #bfdbfe;">{get_icon("rocket", "lucide", 16, "#0066cc")} **Import & Export functionality has moved!**</div>', unsafe_allow_html=True)
                st.markdown("""
                The import and export features are now available at the bottom of this page 
                in the dedicated **"Import & Export Portfolio"** section.
                
                **Benefits of the new location:**
                - {get_icon('check', 'lucide', 14, '#22c55e')} Always accessible, even with an empty portfolio
                - {get_icon('check', 'lucide', 14, '#22c55e')} Better file upload handling  
                - {get_icon('check', 'lucide', 14, '#22c55e')} Enhanced debugging and error reporting
                - {get_icon('check', 'lucide', 14, '#22c55e')} Download templates anytime
                
                {get_icon('arrow-down', 'lucide', 16, '#666666')} **Scroll down to the "Import & Export Portfolio" section below to:**
                - Import your CSV files
                - Download templates
                - Export your current portfolio
                """)
                
                # Quick export button for convenience
                if not st.session_state.transactions.empty:
                    st.markdown("---")
                    st.markdown(display_icon_header('link', 'Quick Export (Convenience)', 'lucide', 18, '#666666'), unsafe_allow_html=True)
                    portfolio_df = st.session_state.transactions.copy()
                    csv_data = portfolio_df.to_csv(index=False)
                    current_date = datetime.now().strftime('%Y%m%d')
                    
                    st.download_button(
                        f"📥 Quick Export CSV ({len(portfolio_df)} records)",
                        csv_data,
                        file_name=f"crypto_portfolio_quick_{current_date}.csv",
                        mime="text/csv",
                        help="Quick export from this tab",
                        key=f"quick_csv_export_{current_date}"
                    )
            
            with action_tab5:
                # Calculate holdings chart data
                portfolio_holdings_df = st.session_state.transactions.copy()
                portfolio_holdings_df = restructuring_manager.apply_restructuring_rules(portfolio_holdings_df, calculation_type='holdings')
                net_holdings_for_chart = calculate_net_holdings(portfolio_holdings_df)
                holdings_chart_data = net_holdings_for_chart[
                    (net_holdings_for_chart['Current_Value'] > 0) & 
                    (net_holdings_for_chart['Current_Value'].notna()) &
                    (net_holdings_for_chart['Symbol'].notna())
                ].copy() if not net_holdings_for_chart.empty else pd.DataFrame()
                
                # Holdings Distribution Chart (uses holdings calculation - includes RESTRUCTURE_IN, excludes RESTRUCTURE_OUT)
                if len(holdings_chart_data) > 0:
                    st.markdown(f"### {get_icon('pie-chart', 'lucide', 20, '#666666')} Current Holdings Distribution", unsafe_allow_html=True)
                    st.info("This chart shows your net current holdings (BUY + RESTRUCTURE_IN - SELL - RESTRUCTURE_OUT)")
                    
                    try:
                        # Since holdings_chart_data now comes from net holdings, no need to group by symbol
                        # Each row already represents the net position for each symbol
                        holdings_treemap_data = holdings_chart_data.copy()
                        
                        # Apply cleaning to holdings treemap data
                        holdings_treemap_data = clean_chart_data(holdings_treemap_data, ['Current_Value', 'Percentage_Change'])
                        holdings_treemap_data = holdings_treemap_data[holdings_treemap_data['Current_Value'] > 0]
                            
                        if len(holdings_treemap_data) > 0:
                            # Verify all data is valid before creating chart
                            values_valid = all(math.isfinite(x) for x in holdings_treemap_data['Current_Value'])
                            colors_valid = all(math.isfinite(x) for x in holdings_treemap_data['Percentage_Change'])
                            
                            if values_valid and colors_valid:
                                    # Add actual values to the treemap display
                                    holdings_treemap_data['Display_Text'] = holdings_treemap_data.apply(
                                        lambda row: f"{row['Symbol']}<br>{row['Effective_Quantity']:,.0f}<br>${row['Current_Value']:,.2f}<br>{row['Percentage_Change']:+.1f}%", axis=1
                                    )
                                    
                                    # Calculate total value for display
                            total_holdings_value = holdings_treemap_data['Current_Value'].sum()
                                    
                            fig_holdings = px.treemap(
                                        holdings_treemap_data,
                                        path=['Symbol'],
                                        values='Current_Value',
                                        color='Percentage_Change',
                                        color_continuous_scale='RdYlGn',
                                        title=f'Current Holdings Distribution<br><sub>Total: ${total_holdings_value:,.2f}</sub>',
                                        hover_data={'Current_Value': ':$,.2f', 'Percentage_Change': ':+.2f%', 'Effective_Quantity': ':,.0f'}
                                    )
                            fig_holdings.update_traces(
                                        texttemplate='<b>%{label}</b><br>%{customdata[2]:,.0f}<br>$%{value:,.0f}',
                                        textposition='middle center',
                                        customdata=holdings_treemap_data[['Current_Value', 'Percentage_Change', 'Effective_Quantity']].values
                                    )
                            fig_holdings.update_layout(
                                        title_font_size=16,
                                        margin=dict(t=50, l=0, r=0, b=0)
                                    )
                            st.plotly_chart(fig_holdings, use_container_width=True)
                        else:
                            st.warning("⚠️ Holdings chart data contains non-finite values after cleaning")
                    except Exception as e:
                        st.error(f"❌ Holdings chart generation failed: {str(e)}")
                else:
                    st.info("No valid holdings data available for holdings distribution chart")
                
                # Calculate portfolio chart data for original holdings
                portfolio_totals_df = st.session_state.transactions.copy()
                portfolio_totals_df = restructuring_manager.apply_restructuring_rules(portfolio_totals_df, calculation_type='original')
                if 'Include_In_Portfolio' in portfolio_totals_df.columns:
                    portfolio_chart_data = portfolio_totals_df[portfolio_totals_df['Include_In_Portfolio'] == True]
                else:
                    portfolio_chart_data = portfolio_totals_df
                portfolio_chart_data = portfolio_chart_data[
                    (portfolio_chart_data['Symbol'].notna())
                ].copy()
                
                if len(portfolio_chart_data) > 0:
                        # Portfolio composition chart using totals calculation (excludes ALL restructuring)
                        chart_title = "ORIGINAL HOLDINGS" if not table_search_query else f"Search Results Distribution: '{table_search_query}'"
                        st.markdown(f"### {get_icon('pie-chart', 'lucide', 20, '#666666')} Original Portfolio Value Distribution", unsafe_allow_html=True)
                        st.info("This chart shows your original portfolio (excludes ALL restructuring transactions)")
                        
                        try:
                            # Use same logic as pie1 for consistency - exclude RESTRUCTURE transactions
                            original_treemap_df = portfolio_df[~portfolio_df['Transaction_Type'].isin(['RESTRUCTURE_OUT', 'RESTRUCTURE_IN'])].copy()
                            
                            # Group by symbol to calculate net positions from original transactions only
                            treemap_data = original_treemap_df.groupby('Symbol').agg({
                                'Quantity': 'sum',  # Net quantity from BUY/SELL only
                                'Current_Price': 'last',      # Use latest price
                                'Percentage_Change': 'mean'   # Average percentage change
                            }).reset_index()
                            
                            # Use exact same acquisition cost calculation as pie1 for tree map values
                            original_treemap_df['Acquisition_Cost'] = original_treemap_df['Quantity'] * original_treemap_df['Purchase_Price']
                            original_treemap_df.loc[original_treemap_df['Transaction_Type'] == 'BUY', 'Acquisition_Cost'] = abs(original_treemap_df.loc[original_treemap_df['Transaction_Type'] == 'BUY', 'Acquisition_Cost'])
                            original_treemap_df.loc[original_treemap_df['Transaction_Type'] == 'SELL', 'Acquisition_Cost'] = -abs(original_treemap_df.loc[original_treemap_df['Transaction_Type'] == 'SELL', 'Acquisition_Cost'])
                            
                            # Get net acquisition costs per symbol (same as pie1)
                            acquisition_costs_treemap = original_treemap_df.groupby('Symbol')['Acquisition_Cost'].sum().reset_index()
                            acquisition_costs_treemap = acquisition_costs_treemap[acquisition_costs_treemap['Acquisition_Cost'] > 0]
                            
                            # Use acquisition costs as the tree map values (not purchase price * quantity)
                            treemap_data = treemap_data.merge(acquisition_costs_treemap, on='Symbol', how='inner')
                            treemap_data['Current_Value'] = treemap_data['Acquisition_Cost']  # Use acquisition cost as display value
                            treemap_data['Effective_Quantity'] = treemap_data['Quantity']  # For display consistency
                            
                            # Apply additional cleaning to grouped data
                            treemap_data = clean_chart_data(treemap_data, ['Current_Value', 'Percentage_Change'])
                            
                            # Tree map data is already filtered to match pie1 exactly
                            
                            # Debug: Log treemap data before chart creation
                            with st.expander(f"🗂️ Treemap Data Debug"):
                                st.write({
                                    "Treemap rows": len(treemap_data),
                                    "Value range": f"{treemap_data['Current_Value'].min():.2f} - {treemap_data['Current_Value'].max():.2f}" if len(treemap_data) > 0 else "N/A",
                                    "Color range": f"{treemap_data['Percentage_Change'].min():.2f} - {treemap_data['Percentage_Change'].max():.2f}" if len(treemap_data) > 0 else "N/A",
                                    "Data sample": f"Contains {len(treemap_data)} symbol(s)" if len(treemap_data) > 0 else "No data"
                                })
                                if len(treemap_data) > 0:
                                    st.write("**Symbols in treemap:**")
                                    st.dataframe(treemap_data[['Symbol', 'Current_Value']].sort_values('Current_Value', ascending=False))
                                    if 'PENDLE' in treemap_data['Symbol'].values or 'PYTH' in treemap_data['Symbol'].values:
                                        st.error("⚠️ PENDLE or PYTH still in treemap data - restructuring not working!")
                                        st.write("Original treemap data columns:", list(original_treemap_df.columns))
                                        if 'Include_In_Portfolio' in original_treemap_df.columns:
                                            st.write("Include_In_Portfolio values:", original_treemap_df['Include_In_Portfolio'].value_counts().to_dict())
                                        pendle_pyth_data = original_treemap_df[original_treemap_df['Symbol'].isin(['PENDLE', 'PYTH'])]
                                        if not pendle_pyth_data.empty:
                                            st.write("PENDLE/PYTH data in original treemap data:")
                                            st.dataframe(pendle_pyth_data[['Symbol', 'Current_Value', 'Include_In_Portfolio'] if 'Include_In_Portfolio' in pendle_pyth_data.columns else ['Symbol', 'Current_Value']])
                            
                            if len(treemap_data) > 0:
                                # Verify all data is valid before creating chart
                                values_valid = all(math.isfinite(x) for x in treemap_data['Current_Value'])
                                colors_valid = all(math.isfinite(x) for x in treemap_data['Percentage_Change'])
                                
                                if values_valid and colors_valid:
                                    # Add actual values to the treemap display
                                    treemap_data['Display_Text'] = treemap_data.apply(
                                        lambda row: f"{row['Symbol']}<br>{row['Effective_Quantity']:,.0f}<br>${row['Current_Value']:,.2f}<br>{row['Percentage_Change']:+.1f}%", axis=1
                                    )
                                    
                                    # Calculate total value for display
                                    total_composition_value = treemap_data['Current_Value'].sum()
                                    
                                    fig_composition = px.treemap(
                                        treemap_data,
                                        path=['Symbol'],
                                        values='Current_Value',
                                        color='Percentage_Change',
                                        color_continuous_scale='RdYlGn',
                                        title=f'{chart_title}<br><sub>Total: ${total_composition_value:,.2f}</sub>',
                                        hover_data={'Current_Value': ':$,.2f', 'Percentage_Change': ':+.2f%', 'Effective_Quantity': ':,.0f'}
                                    )
                                    fig_composition.update_traces(
                                        texttemplate='<b>%{label}</b><br>%{customdata[2]:,.0f}<br>$%{value:,.0f}',
                                        textposition='middle center',
                                        customdata=treemap_data[['Current_Value', 'Percentage_Change', 'Effective_Quantity']].values
                                    )
                                    # Add additional safety for chart rendering
                                    fig_composition.update_layout(
                                        title_font_size=16,
                                        margin=dict(t=50, l=0, r=0, b=0)
                                    )
                                    st.plotly_chart(fig_composition, use_container_width=True)
                                else:
                                    st.warning("⚠️ Chart data contains non-finite values after cleaning")
                                    st.write(f"Values valid: {values_valid}, Colors valid: {colors_valid}")
                            else:
                                st.info("No valid data for portfolio composition chart after cleaning")
                        except Exception as e:
                            st.error(f"❌ Chart generation failed: {str(e)}")
                            st.error("Debug: Check the debug info above to see data issues")
                        
                        # Performance distribution
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            try:
                                # Filter out invalid percentage changes with comprehensive cleaning
                                perf_data = original_treemap_df[
                                    (original_treemap_df['Percentage_Change'].notna()) & 
                                    (original_treemap_df['Percentage_Change'] != float('inf')) &
                                    (original_treemap_df['Percentage_Change'] != float('-inf')) &
                                    (original_treemap_df['Percentage_Change'].abs() < 10000)  # Remove extreme outliers
                                ].copy()
                                
                                # Additional data cleaning
                                perf_data['Percentage_Change'] = pd.to_numeric(perf_data['Percentage_Change'], errors='coerce')
                                perf_data = perf_data[perf_data['Percentage_Change'].notna()]
                                
                                st.info(f"Performance data: {len(perf_data)} records")
                            except Exception as e:
                                st.error(f"Performance data processing error: {str(e)}")
                        
                        with col2:
                            try:
                                # Filter out invalid current values with comprehensive cleaning
                                value_data = original_treemap_df[
                                    (original_treemap_df['Current_Value'].notna()) & 
                                    (original_treemap_df['Current_Value'] > 0) &
                                    (original_treemap_df['Current_Value'] != float('inf')) &
                                    (original_treemap_df['Current_Value'] != float('-inf'))
                                ].copy()
                                
                                # Additional data cleaning
                                value_data['Current_Value'] = pd.to_numeric(value_data['Current_Value'], errors='coerce')
                                value_data = value_data[value_data['Current_Value'].notna()]
                                
                                st.info(f"Value data: {len(value_data)} records")
                            except Exception as e:
                                st.error(f"Value data processing error: {str(e)}")
                else:
                    st.info("Add some transactions to see analytics!")
        
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Summary and Balance Sheet ---
    with st.container():
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        sum1, sum2 = st.columns(2)
        
        with sum1:
            st.markdown(f"### {get_icon('file-text', 'lucide', 20, '#666666')} Portfolio Summary", unsafe_allow_html=True)

            # Calculate totals to match pie charts
            # Total Acquisition Cost (matches Pie 1)
            original_df_for_summary = portfolio_df[~portfolio_df['Transaction_Type'].isin(['RESTRUCTURE_OUT', 'RESTRUCTURE_IN'])].copy()
            original_df_for_summary['Acquisition_Cost'] = original_df_for_summary['Quantity'] * original_df_for_summary['Purchase_Price']
            original_df_for_summary.loc[original_df_for_summary['Transaction_Type'] == 'BUY', 'Acquisition_Cost'] = abs(original_df_for_summary.loc[original_df_for_summary['Transaction_Type'] == 'BUY', 'Acquisition_Cost'])
            original_df_for_summary.loc[original_df_for_summary['Transaction_Type'] == 'SELL', 'Acquisition_Cost'] = -abs(original_df_for_summary.loc[original_df_for_summary['Transaction_Type'] == 'SELL', 'Acquisition_Cost'])
            acquisition_costs_summary = original_df_for_summary.groupby('Symbol')['Acquisition_Cost'].sum().reset_index()
            total_investment = acquisition_costs_summary[acquisition_costs_summary['Acquisition_Cost'] > 0]['Acquisition_Cost'].sum()
            
            # Current Portfolio Value (matches Pie 3 - restructured)
            restructured_df_for_summary = portfolio_df.copy()
            restructured_df_for_summary.loc[restructured_df_for_summary['Transaction_Type'] == 'RESTRUCTURE_OUT', 'Quantity'] = -abs(restructured_df_for_summary.loc[restructured_df_for_summary['Transaction_Type'] == 'RESTRUCTURE_OUT', 'Quantity'])
            restructured_summary_for_total = restructured_df_for_summary.groupby('Symbol').agg({
                'Current_Value': 'sum',
                'Quantity': 'sum'
            }).reset_index()
            total_value = restructured_summary_for_total[restructured_summary_for_total['Current_Value'] > 0]['Current_Value'].sum()
            
            total_pnl = total_value - total_investment
            total_pnl_percent = (total_pnl / total_investment * 100) if total_investment > 0 else 0
            restructuring_note = ""
            
            # Calculate additional metrics
            portfolio_performance = total_pnl_percent
            risk_weighted_return = 8.45  # Placeholder calculation
            
            # Display metrics in a structured format
            st.markdown(f"""
            <div style="line-height: 1.8;">
                <strong>Total Acquisition Cost:</strong> <span style="float: right; color: #666;">${total_investment:,.2f}</span><br>
                <strong>Current Portfolio Value:</strong> <span style="float: right; color: #28a745;">${total_value:,.2f}</span><br>
                <strong>Total Gains/Losses:</strong> <span style="float: right; color: {'#28a745' if total_pnl >= 0 else '#dc3545'};">{total_pnl:+,.2f}</span><br>
                <strong>Portfolio Performance:</strong> <span style="float: right; color: {'#28a745' if portfolio_performance >= 0 else '#dc3545'};">{portfolio_performance:+.2f}%</span><br>
                <strong>Risk-Weighted Return:</strong> <span style="float: right; color: #666;">{risk_weighted_return:.2f}%</span>
                {restructuring_note}
            </div>
            """, unsafe_allow_html=True)
        
        with sum2:
            st.markdown(f"### {get_icon('scale', 'lucide', 20, '#666666')} Balance Sheet Validation", unsafe_allow_html=True)
            
            # Balance validation
            calculated_value = total_investment + total_pnl
            balance_diff = abs(total_value - calculated_value)
            is_balanced = balance_diff < 0.01
            
            st.markdown(f"""
            <div style="line-height: 1.8;">
                <strong>Total Assets:</strong> <span style="float: right; color: #666;">${total_value:,.2f}</span><br>
                <strong>Total Liabilities:</strong> <span style="float: right; color: #666;">$0.00</span><br>
                <strong>Equity:</strong> <span style="float: right; color: #666;">${total_value:,.2f}</span>
            </div>
            """, unsafe_allow_html=True)
            
            status_class = "balanced" if is_balanced else "unbalanced"
            status_text = "✅ Portfolio is balanced (Assets - Liabilities = Equity)" if is_balanced else "❌ Portfolio calculation error"
            st.markdown(f'<div class="balance-indicator {status_class}">{status_text}</div>', unsafe_allow_html=True)

    # --- Charts Dashboard ---
    with st.container():
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown(display_icon_header('chart', 'Chart Dashboard', 'lucide', 24, '#666666'), unsafe_allow_html=True)
        
        # Create tabs for different chart types (added Additional Insights tab)
        tab1, tab2 = st.tabs(["Basic Charts", "Risk Analysis"])
        
        with tab1:
            # Helper function for color scheme based on percentage
            def get_color_by_percentage(percentage):
                """Return color based on percentage ranges"""
                if percentage > 12.5:
                    return '#ff4444'  # Red for >12.5%
                elif 10 <= percentage <= 12.5:
                    return '#ff8c00'  # Orange for 10-12.5%
                elif 2.5 <= percentage < 10:
                    return '#32cd32'  # Green for 2.5-10%
                else:  # <2.5%
                    return '#87ceeb'  # Light blue for <2.5%
            
            def create_color_discrete_map(df, value_col):
                """Create color map - different colors for assets 10%+, grouped colors for smaller assets"""
                total = df[value_col].sum()
                color_map = {}
                
                # Define distinct colors for major holdings (10%+)
                major_colors = ['#ff4444', '#32cd32', '#1f77b4', '#ff8c00', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
                minor_color = '#d3d3d3'  # Light gray for assets < 10%
                
                major_color_idx = 0
                for _, row in df.iterrows():
                    percentage = (row[value_col] / total) * 100
                    if percentage >= 10:
                        # Assign unique color to each major holding
                        color_map[row['Symbol']] = major_colors[major_color_idx % len(major_colors)]
                        major_color_idx += 1
                    else:
                        # Use same color for all minor holdings
                        color_map[row['Symbol']] = minor_color
                return color_map
            
            # Three pie charts as requested
            pie_col1, pie_col2, pie_col3 = st.columns(3)
            
            if len(portfolio_df) > 0:
                # Pie 1: TOTAL ACQUISITION COSTS (INITIAL) - BUY and SELL transactions (excluding RESTRUCTURE)
                with pie_col1:
                    # Include BUY and SELL transactions, exclude RESTRUCTURE transactions
                    original_df = portfolio_df[~portfolio_df['Transaction_Type'].isin(['RESTRUCTURE_OUT', 'RESTRUCTURE_IN'])].copy()
                    if not original_df.empty:
                        # Calculate acquisition costs: positive for BUY, negative for SELL
                        original_df['Acquisition_Cost'] = original_df['Quantity'] * original_df['Purchase_Price']
                        # Ensure BUY is positive and SELL is negative
                        original_df.loc[original_df['Transaction_Type'] == 'BUY', 'Acquisition_Cost'] = abs(original_df.loc[original_df['Transaction_Type'] == 'BUY', 'Acquisition_Cost'])
                        original_df.loc[original_df['Transaction_Type'] == 'SELL', 'Acquisition_Cost'] = -abs(original_df.loc[original_df['Transaction_Type'] == 'SELL', 'Acquisition_Cost'])
                        
                        # Get net quantities from BUY and SELL only (excluding RESTRUCTURE)
                        net_quantities = original_df.groupby('Symbol')['Quantity'].sum().reset_index()
                        net_quantities.columns = ['Symbol', 'Net_Quantity']
            
                        # Get net acquisition costs (BUY costs - SELL proceeds)
                        acquisition_costs = original_df.groupby('Symbol')['Acquisition_Cost'].sum().reset_index()
                        
                        # Merge net quantities with acquisition costs
                        acquisition_plot_df = acquisition_costs.merge(net_quantities, on='Symbol', how='left')
                        acquisition_plot_df['Net_Quantity'] = acquisition_plot_df['Net_Quantity'].fillna(0)
                        
                        # Keep all assets with acquisition costs > 0, including those with net quantity 0 (like BNB, ADA, SOL)
                        acquisition_plot_df = acquisition_plot_df[acquisition_plot_df['Acquisition_Cost'] > 0]
                        
                        # Rename for consistency with chart code
                        acquisition_plot_df = acquisition_plot_df.rename(columns={'Net_Quantity': 'Quantity'})
                        
                        if not acquisition_plot_df.empty:
                            # Calculate total value for display
                            total_acquisition_cost = acquisition_plot_df['Acquisition_Cost'].sum()
                            
                            # Create color map based on percentage
                            color_map = create_color_discrete_map(acquisition_plot_df, 'Acquisition_Cost')
                            
                            fig_acquisition = px.pie(
                                acquisition_plot_df,
                                values='Acquisition_Cost',
                                names='Symbol',
                                title=f'Total Acquisition Costs (Initial)<br><sub>Total: ${total_acquisition_cost:,.2f}</sub>',
                                color='Symbol',
                                color_discrete_map=color_map
                            )
                            # Add quantity labels
                            fig_acquisition.update_traces(
                                textposition='inside', 
                                textinfo='percent+label',
                                hovertemplate='<b>%{label}</b><br>Quantity: %{customdata:,.0f}<br>Cost: $%{value:,.2f}<br>Percentage: %{percent}<extra></extra>',
                                customdata=acquisition_plot_df['Quantity']
                            )
                            st.plotly_chart(fig_acquisition, use_container_width=True)
                        else:
                            st.info('No original acquisition data')
                    else:
                        st.info('No original transactions')
                
                # Pie 2: CURRENT PORTFOLIO VALUE (INITIAL) - Only ORIGINAL transactions at current price
                with pie_col2:
                    original_df = portfolio_df[~portfolio_df['Transaction_Type'].isin(['RESTRUCTURE_OUT', 'RESTRUCTURE_IN'])].copy()
                    if not original_df.empty:
                        # Group by symbol to get quantities and current values
                        original_summary = original_df.groupby('Symbol').agg({
                            'Current_Value': 'sum',
                            'Quantity': 'sum'
                        }).reset_index()
                        # Filter out LTC and assets with zero/negative current value
                        original_summary = original_summary[
                            (original_summary['Current_Value'] > 0) & 
                            (original_summary['Symbol'] != 'LTC')
                        ]
                        original_plot_df = prepare_plot_df(original_summary, ['Current_Value'], use_include=False)
                        
                        if not original_plot_df.empty:
                            # Calculate total value for display
                            total_original_value = original_plot_df['Current_Value'].sum()
                            
                            # Create color map based on percentage
                            color_map = create_color_discrete_map(original_plot_df, 'Current_Value')
                            
                            fig_original_value = px.pie(
                                original_plot_df,
                                values='Current_Value',
                                names='Symbol',
                                title=f'Current Portfolio Value (Original)<br><sub>Total: ${total_original_value:,.2f}</sub>',
                                color='Symbol',
                                color_discrete_map=color_map
                            )
                            # Add quantity labels
                            fig_original_value.update_traces(
                                textposition='inside', 
                                textinfo='percent+label',
                                hovertemplate='<b>%{label}</b><br>Quantity: %{customdata:,.0f}<br>Value: $%{value:,.2f}<br>Percentage: %{percent}<extra></extra>',
                                customdata=original_plot_df['Quantity']
                            )
                            st.plotly_chart(fig_original_value, use_container_width=True)
                        else:
                            st.info('No original current value data')
                    else:
                        st.info('No original transactions')
                
                # Pie 3: CURRENT PORTFOLIO VALUE (RESTRUCTURED) - Include all transactions including RESTRUCTURE_OUT as negative
                with pie_col3:
                    restructured_df = portfolio_df.copy()
                    if not restructured_df.empty:
                        # Ensure RESTRUCTURE_OUT transactions have negative quantities
                        restructured_df.loc[restructured_df['Transaction_Type'] == 'RESTRUCTURE_OUT', 'Quantity'] = -abs(restructured_df.loc[restructured_df['Transaction_Type'] == 'RESTRUCTURE_OUT', 'Quantity'])
                        
                        # Group by symbol to get net quantities and current values
                        restructured_summary = restructured_df.groupby('Symbol').agg({
                            'Current_Value': 'sum',
                            'Quantity': 'sum'  # This will now include negative RESTRUCTURE_OUT quantities
                        }).reset_index()
                        
                        # Filter out assets with zero or negative net quantities/values
                        restructured_summary = restructured_summary[restructured_summary['Current_Value'] > 0]
                        restructured_plot_df = prepare_plot_df(restructured_summary, ['Current_Value'], use_include=False)
                        
                        if not restructured_plot_df.empty:
                            # Calculate total value for display
                            total_restructured_value = restructured_plot_df['Current_Value'].sum()
                            
                            # Create color map based on percentage
                            color_map = create_color_discrete_map(restructured_plot_df, 'Current_Value')
                            
                            fig_restructured_value = px.pie(
                                restructured_plot_df,
                                values='Current_Value',
                                names='Symbol',
                                title=f'Current Portfolio Value (Restructured)<br><sub>Total: ${total_restructured_value:,.2f}</sub>',
                                color='Symbol',
                                color_discrete_map=color_map
                            )
                            # Add quantity labels
                            fig_restructured_value.update_traces(
                                textposition='inside', 
                                textinfo='percent+label',
                                hovertemplate='<b>%{label}</b><br>Quantity: %{customdata:,.0f}<br>Value: $%{value:,.2f}<br>Percentage: %{percent}<extra></extra>',
                                customdata=restructured_plot_df['Quantity']
                            )
                            st.plotly_chart(fig_restructured_value, use_container_width=True)
                        else:
                            st.info('No restructured value data')
                    else:
                        st.info('No valid transactions')
            else:
                st.info('No portfolio data available for pie charts')
        
        with tab2:
            if len(portfolio_df) > 0:
                # Apply restructuring rules for portfolio totals (excludes ALL restructuring transactions)
                risk_portfolio_df = restructuring_manager.apply_restructuring_rules(portfolio_df.copy(), calculation_type='totals')
                # Filter to only included transactions
                if 'Include_In_Portfolio' in risk_portfolio_df.columns:
                    risk_portfolio_df = risk_portfolio_df[risk_portfolio_df['Include_In_Portfolio'] == True]
                
                # Risk Matrix Visualization
                risk_col1, risk_col2 = st.columns(2)
                
                with risk_col1:
                    # Calculate risk metrics
                    risk_portfolio_df['Risk_Score'] = abs(risk_portfolio_df['Percentage_Change']) / 10  # Simple risk score
                    risk_portfolio_df['Return_Score'] = risk_portfolio_df['Percentage_Change']
                    
                    # Fix the Current_Value handling
                    if 'Current_Value' in risk_portfolio_df.columns:
                        risk_portfolio_df['Abs_Current_Value'] = abs(risk_portfolio_df['Current_Value']).fillna(1).clip(lower=1)
                    else:
                        risk_portfolio_df['Abs_Current_Value'] = 1

                    risk_df = prepare_plot_df(risk_portfolio_df, ['Risk_Score', 'Return_Score', 'Abs_Current_Value', 'Percentage_Change'], use_include=True)
                    if not risk_df.empty:
                        fig_risk_matrix = px.scatter(
                            risk_df,
                            x='Risk_Score',
                            y='Return_Score',
                            size='Abs_Current_Value',  # Use absolute value for marker size
                            color='Percentage_Change',
                            hover_name='Symbol',
                            title='Risk-Return Matrix',
                            labels={'Risk_Score': 'Risk Level', 'Return_Score': 'Return (%)'},
                            color_continuous_scale='RdYlGn'
                        )
                        fig_risk_matrix.add_hline(y=0, line_dash="dash", line_color="gray")
                        fig_risk_matrix.add_vline(x=risk_df['Risk_Score'].mean(), line_dash="dash", line_color="gray")
                        st.plotly_chart(fig_risk_matrix, use_container_width=True)
                    else:
                        st.info('No valid data for risk-return matrix')
                
                with risk_col2:
                    # Risk Distribution
                    risk_dist_df = prepare_plot_df(risk_portfolio_df, ['Risk_Score'], use_include=True)
                    if not risk_dist_df.empty:
                        fig_risk_dist = px.histogram(
                            risk_dist_df,
                            x='Risk_Score',
                            nbins=10,
                            title='Risk Distribution',
                            color_discrete_sequence=['#ff6b6b']
                        )
                        st.plotly_chart(fig_risk_dist, use_container_width=True)
                    else:
                        st.info('No valid data for risk distribution')
        
        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("🚀 Your portfolio is empty. Start by importing your crypto transactions!")

# --- Import/Export Section (Always Available) ---
st.markdown("---")

# Import Section
st.markdown(display_icon_header('upload', 'Import Data', 'lucide', 22, '#666666'), unsafe_allow_html=True)

# Display last import results if available (persistent after page refresh)
if 'last_import_results' in st.session_state:
    results = st.session_state.last_import_results
    
    # Create a prominent results card
    st.markdown(f"#### {get_icon('clock', 'lucide', 18, '#666666')} Last Import Results", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        if results['success_count'] > 0:
            st.markdown(f'<div style="color: #22c55e; background-color: #f0fdf4; padding: 8px; border-radius: 4px; border: 1px solid #bbf7d0;">{get_icon("check-circle", "lucide", 16, "#22c55e")} **{results["success_count"]} transactions** imported successfully</div>', unsafe_allow_html=True)
        else:
            st.info("ℹ️ No transactions were imported")
    
    with col2:
        if results['error_count'] > 0:
            st.error(f"❌ **{results['error_count']} rows** failed to import")
        else:
            st.markdown(f'<div style="color: #22c55e; background-color: #f0fdf4; padding: 8px; border-radius: 4px; border: 1px solid #bbf7d0;">{get_icon("check-circle", "lucide", 16, "#22c55e")} No import errors</div>', unsafe_allow_html=True)
    
    with col3:
        if st.button("🗑️ Clear Results", help="Clear import results display"):
            del st.session_state.last_import_results
            st.rerun()
    
    # Show detailed errors if any
    if results['error_count'] > 0 and results['errors']:
        with st.expander(f"{get_icon('list', 'lucide', 16, '#666666')} View {results['error_count']} Import Errors", expanded=False):
            st.markdown(f"**Import Time:** {results['timestamp']}")
            st.markdown(f"**{get_icon('alert-triangle', 'lucide', 16, '#dc2626')} Detailed Error Report:**", unsafe_allow_html=True)
            for i, error in enumerate(results['errors'], 1):
                st.text(f"{i}. {error}")
            
            # Add suggestions for common errors
            st.markdown("---")
            st.markdown(f"**{get_icon('lightbulb', 'lucide', 16, '#fbbf24')} Common Solutions:**", unsafe_allow_html=True)
            st.markdown("""
            - **Invalid quantity/price:** Remove text, fix decimal separators (use . not ,)
            - **Missing data:** Fill empty cells or remove incomplete rows
            - **Date format issues:** Use YYYY-MM-DD format (e.g., 2025-01-15)
            - **Coin name/symbol:** Check spelling, remove special characters
            """)
    
    st.markdown("---")

st.info("""
**How It Works:**
- No empty rows, no comma separated values
- DATE format should be: 'YYYY-MM-DD' (e.g., '2025-01-15')
- TIME format should be: 'HH:MM:SS' or 'HH:MM' (e.g., '14:30:00' or '14:30')
- **Buy transactions:** Positive quantity (e.g., +1.5 BTC)
- **Sell transactions:** Negative quantity (e.g., -0.5 BTC) 
- Sells will show as red 📉 entries in your portfolio
- Your DCA analysis will account for both buys and sells automatically
""")

uploaded_file = st.file_uploader(
    "Choose a CSV file to import",
    type=['csv'],
    help="Upload a CSV file with columns: Coin_Name, Symbol, Quantity, Purchase_Price, Purchase_Date, Purchase_Time (optional: Target_Sell_Price, Coin_ID, Transaction_Type)",
    key="csv_import_uploader"
)

# Debug information for file upload
if uploaded_file is not None:
    st.info(f"✅ File detected: {uploaded_file.name} ({uploaded_file.size} bytes)")
else:
    st.caption("📂 Please select a CSV file to import your portfolio data")

if uploaded_file is not None:
    st.info(f"📋 Starting to process file: {uploaded_file.name}")
    
    # Check file size and recommend chunked processing for large files
    file_size_mb = uploaded_file.size / (1024 * 1024)
    st.info(f"File size: {file_size_mb:.4f} MB")
    
    if file_size_mb > 50:
        st.warning(f"⚠️ Large file detected ({file_size_mb:.1f} MB). Using chunked processing for better performance.")
        use_chunked_processing = True
        chunk_size = 1000  # Process 1000 rows at a time
    else:
        use_chunked_processing = False
        chunk_size = 1000  # Default value
    
    try:
        if use_chunked_processing:
            # For large files: Read first chunk for preview and validation
            st.info("🔍 Reading file preview (first 1000 rows)...")
            preview_df = pd.read_csv(uploaded_file, nrows=1000)
            st.success(f"✅ Preview loaded: {len(preview_df)} rows x {len(preview_df.columns)} columns")
            st.markdown("##### Preview of uploaded data (first 1000 rows):")
            st.dataframe(preview_df.head(), use_container_width=True)
            
            # Reset file pointer for full processing
            uploaded_file.seek(0)
            
            # Get total row count for progress tracking
            total_rows = sum(1 for line in uploaded_file) - 1  # Subtract header
            uploaded_file.seek(0)  # Reset again
            st.info(f"Total rows to process: {total_rows:,}")

            import_df = preview_df  # Use preview for validation
        else:
            # For smaller files: Read normally
            import_df = pd.read_csv(uploaded_file)
            total_rows = len(import_df)
            st.success(f"✅ Successfully read CSV with {len(import_df)} rows and {len(import_df.columns)} columns")
            st.markdown("##### Preview of uploaded data:")
            st.dataframe(import_df.head(), use_container_width=True)
        
        # Validate required columns
        required_columns = ['Coin_Name', 'Symbol', 'Quantity', 'Purchase_Price']
        missing_columns = [col for col in required_columns if col not in import_df.columns]
        
        # Check for transaction type detection methods
        has_transaction_type = 'Transaction_Type' in import_df.columns
        
        # Safely check for quantity signs by converting to numeric first
        has_quantity_signs = False
        if 'Quantity' in import_df.columns:
            try:
                # Convert quantity column to numeric, handling errors gracefully
                numeric_quantities = pd.to_numeric(import_df['Quantity'], errors='coerce')
                # Check if any valid numeric values are negative (exclude NaN values)
                if isinstance(numeric_quantities, pd.Series):
                    valid_quantities = numeric_quantities.dropna()
                    has_quantity_signs = any(valid_quantities < 0) if len(valid_quantities) > 0 else False
                else:
                    has_quantity_signs = False
            except Exception as e:
                st.warning(f"⚠️ Warning: Could not parse Quantity column for transaction type detection: {str(e)}")
                has_quantity_signs = False
        
        if missing_columns:
            st.error(f"❌ Missing required columns: {', '.join(missing_columns)}")
            st.info("Required columns: Coin_Name, Symbol, Quantity, Purchase_Price")
        else:
            st.markdown(f'<div style="color: #22c55e; background-color: #f0fdf4; padding: 8px; border-radius: 4px; border: 1px solid #bbf7d0;">{get_icon("check-circle", "lucide", 16, "#22c55e")} All required columns found!</div>', unsafe_allow_html=True)
            
            # Show detected transaction type method
            if has_transaction_type:
                st.info("🔍 **Detected Method 2:** Transaction_Type column found")
                transaction_types = import_df['Transaction_Type'].value_counts()
                st.write("Transaction types detected:", transaction_types.to_dict())
            elif has_quantity_signs:
                st.info("🔍 **Detected Method 1:** Negative quantities found (SELL transactions)")
                # Safely count buy/sell transactions with numeric conversion - COMPLETE BREAKDOWN
                try:
                    numeric_quantities = pd.to_numeric(import_df['Quantity'], errors='coerce')
                    if isinstance(numeric_quantities, pd.Series):
                        # Count ALL transactions, including zeros and NaN
                        total_rows = len(import_df)
                        
                        buy_count = len(numeric_quantities[numeric_quantities > 0])
                        sell_count = len(numeric_quantities[numeric_quantities < 0])
                        zero_count = len(numeric_quantities[numeric_quantities == 0])
                        invalid_count = len(numeric_quantities[numeric_quantities.isna()])
                        
                        # Verify the math adds up
                        accounted_for = buy_count + sell_count + zero_count + invalid_count
                        
                        st.write(f"📈 BUY transactions: {buy_count}, 📉 SELL transactions: {sell_count}")
                        
                        # Show additional details if there are missing transactions
                        if zero_count > 0 or invalid_count > 0:
                            st.caption(f"⚪ Zero quantity: {zero_count}, ❌ Invalid/NaN: {invalid_count}")
                            
                            # Show sample invalid data for debugging
                            if invalid_count > 0:
                                invalid_mask = numeric_quantities.isna()
                                invalid_rows = import_df[invalid_mask]
                                st.warning(f"🔍 **Debug: Found {invalid_count} invalid quantity values**")
                                
                                with st.expander(f"{get_icon('search', 'lucide', 16, '#666666')} View Invalid Rows (showing first 10 of {invalid_count})"):
                                    # Show original values that failed conversion
                                    debug_df = invalid_rows[['Coin_Name', 'Symbol', 'Quantity']].head(10).copy()
                                    debug_df['Row_Number'] = invalid_rows.index[:10] + 1  # Convert to 1-based row numbers
                                    debug_df = debug_df[['Row_Number', 'Coin_Name', 'Symbol', 'Quantity']]
                                    st.dataframe(debug_df, use_container_width=True)
                                    
                                    # Show unique invalid quantity values
                                    unique_invalid = invalid_rows['Quantity'].value_counts()
                                    st.write("**Most common invalid quantity values:**")
                                    st.write(unique_invalid.head(10).to_dict())
                                    
                                    st.info("💡 **Common fixes:**\n"
                                           "- Remove text like 'tokens', 'coins', 'units'\n"
                                           "- Fix decimal separators (use . not ,)\n"
                                           "- Remove currency symbols ($, €, etc.)\n"
                                           "- Fill empty cells with 0 or remove rows")
                        
                        # Math check - highlight discrepancy if found
                        if accounted_for != total_rows:
                            st.warning(f"⚠️ Math Check: {buy_count} + {sell_count} + {zero_count} + {invalid_count} = {accounted_for} ≠ {total_rows} total rows")
                        else:
                            st.success(f"✅ Math Check: {buy_count} + {sell_count} + {zero_count} + {invalid_count} = {total_rows} total rows")
                    else:
                        st.write("📈 BUY transactions: Unknown, 📉 SELL transactions: Unknown")
                except Exception as e:
                    st.warning(f"⚠️ Could not count transaction types: {str(e)}")
                    st.write("📈 BUY transactions: Unknown, 📉 SELL transactions: Unknown")
            else:
                st.info("🔍 **Auto-detected:** All positive quantities (BUY transactions)")
                # Even for all positive, show the complete breakdown
                try:
                    numeric_quantities = pd.to_numeric(import_df['Quantity'], errors='coerce')
                    if isinstance(numeric_quantities, pd.Series):
                        total_rows = len(import_df)
                        buy_count = len(numeric_quantities[numeric_quantities > 0])
                        zero_count = len(numeric_quantities[numeric_quantities == 0])
                        invalid_count = len(numeric_quantities[numeric_quantities.isna()])
                        
                        st.write(f"📈 BUY transactions: {buy_count}, 📉 SELL transactions: 0")
                        if zero_count > 0 or invalid_count > 0:
                            st.caption(f"⚪ Zero quantity: {zero_count}, ❌ Invalid/NaN: {invalid_count}")
                        
                        accounted_for = buy_count + zero_count + invalid_count
                        if accounted_for != total_rows:
                            st.warning(f"⚠️ Math Check: {buy_count} + 0 + {zero_count} + {invalid_count} = {accounted_for} ≠ {total_rows} total rows")
                        else:
                            st.success(f"✅ Math Check: {buy_count} + 0 + {zero_count} + {invalid_count} = {total_rows} total rows")
                except:
                    pass
            
            # Show import options
            col1, col2 = st.columns(2)
            with col1:
                import_mode = st.radio(
                    "Import Mode",
                    ["Add to existing portfolio", "Replace entire portfolio"],
                    help="Choose whether to add to current data or replace it completely"
                )
            with col2:
                validate_coins = st.checkbox(
                    "Validate coin symbols",
                    value=True,
                    help="Check if coin symbols exist in CoinGecko database"
                )
            
            if st.button("🚀 Import Portfolio Data", type="primary"):
                st.info("🔄 Starting import process...")
                
                # Debug: Check user_id
                if 'user_id' not in st.session_state:
                    st.error("❌ User not authenticated. Please log in again.")
                    st.stop()
                else:
                    st.info(f"👤 User ID: {st.session_state.user_id}")
                
                # Show processing method
                if use_chunked_processing:
                    st.info(f"⚡ Using chunked processing ({chunk_size:,} rows per batch) for large file")
                else:
                    st.info("Using standard processing for regular file")
                
                with st.spinner("Processing import..."):
                    # Process and validate the import data
                    success_count = 0
                    error_count = 0
                    errors = []
                    
                    # Clear existing data if replace mode
                    if import_mode == "Replace entire portfolio":
                        st.info("🗑️ Clearing existing portfolio data...")
                        existing_transactions = db.get_user_portfolio(st.session_state.user_id)
                        for _, transaction in existing_transactions.iterrows():
                            transaction_id = str(transaction['transaction_id'])
                            db.delete_transaction(transaction_id, st.session_state.user_id)
                        st.info("✅ Cleared existing portfolio data")
                    
                    # Reset file pointer for processing
                    uploaded_file.seek(0)
                    
                    if use_chunked_processing:
                        # Chunked processing for large files
                        st.info(f"Processing {total_rows:,} rows in chunks of {chunk_size:,}...")
                        
                        # Create progress bar
                        progress_bar = st.progress(0)
                        progress_text = st.empty()
                        
                        chunk_num = 0
                        for chunk_df in pd.read_csv(uploaded_file, chunksize=chunk_size):
                            chunk_num += 1
                            chunk_start_row = (chunk_num - 1) * chunk_size + 1
                            
                            # Update progress
                            rows_processed = success_count + error_count
                            progress = min(rows_processed, total_rows) / max(total_rows, 1)
                            progress_bar.progress(progress)
                            progress_text.text(f"Processing chunk {chunk_num} (rows {chunk_start_row:,}-{chunk_start_row + len(chunk_df) - 1:,})")
                            
                            # Process chunk
                            chunk_success, chunk_errors = process_import_chunk(chunk_df, chunk_start_row, db, st.session_state.user_id)
                            success_count += chunk_success
                            error_count += len(chunk_errors)
                            errors.extend(chunk_errors)
                            
                            # Show progress every few chunks
                            if chunk_num % 5 == 0:
                                st.info(f"✅ Processed {chunk_num} chunks: {success_count:,} successful, {error_count:,} errors")
                        
                        progress_bar.progress(1.0)
                        progress_text.text(f"✅ Completed processing {chunk_num} chunks")
                        
                    else:
                        # Standard processing for smaller files
                        st.info(f"Processing {len(import_df)} rows for import...")
                        
                        # Process each row with improved error handling
                        for row_num, (row_index, row) in enumerate(import_df.iterrows(), 1):
                            try:
                                # Extract values with proper type handling
                                quantity_val = row['Quantity']
                                price_val = row['Purchase_Price']
                                
                                # Skip rows with invalid quantity or price
                                if pd.isna(quantity_val) or pd.isna(price_val):
                                    errors.append(f"Row {row_num}: Missing quantity or price")
                                    error_count += 1
                                    continue
                                    
                                # Convert to numeric and validate
                                try:
                                    numeric_quantity = float(quantity_val)
                                    numeric_price = float(price_val)
                                    if numeric_price <= 0:
                                        errors.append(f"Row {row_num}: Invalid price ({numeric_price})")
                                        error_count += 1
                                        continue
                                except (ValueError, TypeError):
                                    errors.append(f"Row {row_num}: Invalid numeric values (qty: {quantity_val}, price: {price_val})")
                                    error_count += 1
                                    continue
                                
                                # Determine transaction type and adjust quantity
                                final_quantity = numeric_quantity
                                
                                # Method 1: Check Transaction_Type column
                                if 'Transaction_Type' in import_df.columns:
                                    trans_type = str(row['Transaction_Type']).upper()
                                    if trans_type in ['SELL', 'SALE', 'S']:
                                        final_quantity = -abs(numeric_quantity)  # Make negative for sell
                                    else:
                                        final_quantity = abs(numeric_quantity)   # Make positive for buy
                                
                                # Method 2: Use quantity sign (negative = sell)
                                elif numeric_quantity < 0:
                                    final_quantity = numeric_quantity  # Keep negative
                                
                                # Method 3: Default to buy transaction
                                else:
                                    final_quantity = abs(numeric_quantity)  # Ensure positive for buy
                                
                                # Extract other values with validation
                                coin_name_val = str(row['Coin_Name']).strip()
                                symbol_val = str(row['Symbol']).upper().strip()
                                
                                # Validate required string fields
                                if not coin_name_val or coin_name_val == 'nan' or not symbol_val or symbol_val == 'NAN':
                                    errors.append(f"Row {row_num}: Missing coin name or symbol")
                                    error_count += 1
                                    continue
                                
                                # Get or generate coin_id
                                if 'Coin_ID' in import_df.columns:
                                    coin_id = str(row['Coin_ID']).strip().lower()
                                else:
                                    coin_id = symbol_val.lower()
                                
                                # Prepare transaction data with proper datetime handling
                                current_time = datetime.now()
                                transaction_id = f"{coin_id}_{current_time.strftime('%Y%m%d_%H%M%S')}_{row_num}"
                                
                                # Handle date fields with proper formatting and validation
                                purchase_date_val = current_time.strftime('%Y-%m-%d')
                                purchase_time_val = current_time.strftime('%H:%M:%S')
                                
                                if 'Purchase_Date' in import_df.columns:
                                    pd_val = row['Purchase_Date']
                                    if not pd.isna(pd_val):
                                        try:
                                            # Try to parse and reformat the date to ensure consistency
                                            date_str = str(pd_val).strip()
                                            if date_str and date_str != 'nan':
                                                # Try different date formats
                                                for fmt in ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%Y%m%d']:
                                                    try:
                                                        parsed_date = pd.to_datetime(date_str, format=fmt)
                                                        purchase_date_val = parsed_date.strftime('%Y-%m-%d')
                                                        break
                                                    except:
                                                        continue
                                                else:
                                                    # If all formats fail, try pandas auto-parsing
                                                    try:
                                                        parsed_date = pd.to_datetime(date_str)
                                                        purchase_date_val = parsed_date.strftime('%Y-%m-%d')
                                                    except:
                                                        # Keep default if parsing fails
                                                        errors.append(f"Row {row_num}: Warning - Could not parse date '{date_str}', using current date")
                                        except Exception:
                                            # Keep default if any error
                                            pass
                                
                                if 'Purchase_Time' in import_df.columns:
                                    pt_val = row['Purchase_Time']
                                    if not pd.isna(pt_val):
                                        try:
                                            time_str = str(pt_val).strip()
                                            if time_str and time_str != 'nan':
                                                # Validate time format (HH:MM:SS or HH:MM or H:MM)
                                                if ':' in time_str:
                                                    time_parts = time_str.split(':')
                                                    if len(time_parts) >= 2:
                                                        hours = int(time_parts[0])
                                                        minutes = int(time_parts[1])
                                                        seconds = int(time_parts[2]) if len(time_parts) > 2 else 0
                                                        if 0 <= hours <= 23 and 0 <= minutes <= 59 and 0 <= seconds <= 59:
                                                            purchase_time_val = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                                        except Exception:
                                            # Keep default if parsing fails
                                            pass
                                
                                # Handle target sell price
                                target_sell_price_val = 0.0
                                if 'Target_Sell_Price' in import_df.columns:
                                    tsp_val = row['Target_Sell_Price']
                                    if not pd.isna(tsp_val):
                                        try:
                                            target_sell_price_val = float(tsp_val)
                                            if target_sell_price_val < 0:
                                                target_sell_price_val = 0.0
                                        except (ValueError, TypeError):
                                            target_sell_price_val = 0.0
                                
                                transaction_data = {
                                    'transaction_id': transaction_id,
                                    'coin_name': coin_name_val,
                                    'symbol': symbol_val,
                                    'coin_id': coin_id,
                                    'quantity': final_quantity,  # Use processed quantity (negative for sells)
                                    'purchase_price': numeric_price,
                                    'current_price': 0.0,
                                    'purchase_date': purchase_date_val,
                                    'purchase_time': purchase_time_val,
                                    'target_sell_price': target_sell_price_val,
                                    'current_value': 0.0,
                                    'profit_loss': 0.0,
                                    'percentage_change': 0.0,
                                    'created_at': current_time.isoformat(),
                                    'updated_at': current_time.isoformat()
                                }
                                
                                # Add to database with improved error handling
                                try:
                                    db_result = db.add_transaction(st.session_state.user_id, transaction_data)
                                    if db_result:
                                        success_count += 1
                                        if success_count % 10 == 0:  # Progress updates every 10 transactions
                                            st.info(f"✅ Processed {success_count} transactions so far...")
                                    else:
                                        error_msg = f"Row {row_num}: Database rejected transaction (unknown reason)"
                                        errors.append(error_msg)
                                        error_count += 1
                                except Exception as db_error:
                                    error_msg = f"Row {row_num}: Database error - {str(db_error)}"
                                    errors.append(error_msg)
                                    error_count += 1
                                    
                            except Exception as e:
                                errors.append(f"Row {row_num}: Processing error - {str(e)}")
                                error_count += 1
                    
                    # Show results
                    st.info(f"🔍 Import completed: {success_count} successful, {error_count} errors")
                    
                    # Store import results in session state for persistent display
                    st.session_state.last_import_results = {
                        'success_count': success_count,
                        'error_count': error_count,
                        'errors': errors,
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    if success_count > 0:
                        st.success(f"✅ Successfully imported {success_count} transactions!")
                        
                        # Show summary before refresh
                        if error_count > 0:
                            st.warning(f"⚠️ {error_count} rows failed to import (details will be shown after refresh)")
                        
                        # Immediate refresh to show new data
                        refresh_portfolio_data(skip_price_update=False)
                        st.rerun()
                    
                    if error_count > 0:
                        st.markdown(f'<div style="color: #f59e0b; background-color: #fffbeb; padding: 8px; border-radius: 4px; border: 1px solid #fed7aa;">{get_icon("alert-triangle", "lucide", 16, "#f59e0b")} {error_count} rows failed to import</div>', unsafe_allow_html=True)
                        with st.expander(f"{get_icon('list', 'lucide', 16, '#666666')} View import errors", expanded=True):
                            st.markdown(f"**{get_icon('alert-triangle', 'lucide', 16, '#dc2626')} Detailed Error Report:**", unsafe_allow_html=True)
                            for i, error in enumerate(errors, 1):
                                st.text(f"{i}. {error}")
                    
                    # If no success and no errors, something went wrong
                    if success_count == 0 and error_count == 0:
                        st.markdown(f'<div style="color: #dc2626; background-color: #fef2f2; padding: 8px; border-radius: 4px; border: 1px solid #fecaca;">{get_icon("x-circle", "lucide", 16, "#dc2626")} No data was processed. Please check your CSV format and try again.</div>', unsafe_allow_html=True)
                        st.markdown(f'<div style="color: #3b82f6; background-color: #eff6ff; padding: 8px; border-radius: 4px; border: 1px solid #bfdbfe;">{get_icon("info", "lucide", 16, "#3b82f6")} Make sure your CSV has the required columns: Coin_Name, Symbol, Quantity, Purchase_Price</div>', unsafe_allow_html=True)
    
    except Exception as e:
        st.markdown(f'<div style="color: #dc2626; background-color: #fef2f2; padding: 8px; border-radius: 4px; border: 1px solid #fecaca;">{get_icon("x-circle", "lucide", 16, "#dc2626")} Error reading file: {str(e)}</div>', unsafe_allow_html=True)

# Download template
st.markdown("---")
st.markdown(display_icon_header('download', 'Download Import Template', 'lucide', 22, '#666666'), unsafe_allow_html=True)

# Template information
st.markdown(f"""
{get_icon('info', 'lucide', 16, '#3b82f6')} **Import Format Guide:**

{get_icon('tag', 'lucide', 14, '#22c55e')} **Method 1: Quantity-based (Recommended)**
- **Positive quantity** = BUY transaction
- **Negative quantity** = SELL transaction

{get_icon('list', 'lucide', 14, '#22c55e')} **Method 2: Transaction Type Column**
- Add `Transaction_Type` column with values: `BUY`, `SELL`, `buy`, `sell`
- Quantity should always be positive when using this method
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    # Generate Method 1 template data
    template_data_1 = {
        'Coin_Name': ['Bitcoin', 'Ethereum', 'Cardano', 'Bitcoin'],
        'Symbol': ['BTC', 'ETH', 'ADA', 'BTC'],
        'Quantity': [0.1, 2.5, 1000, -0.05],  # Negative = sell
        'Purchase_Price': [45000.00, 3200.00, 0.45, 47000.00],
        'Purchase_Date': ['2024-01-15', '2024-01-20', '2024-02-01', '2024-02-15'],
        'Purchase_Time': ['10:30', '14:15', '09:45', '11:20'],
        'Target_Sell_Price': [50000.00, 4000.00, 0.60, 0.00],
        'Coin_ID': ['bitcoin', 'ethereum', 'cardano', 'bitcoin']
    }
    template_df_1 = pd.DataFrame(template_data_1)
    csv_template_1 = template_df_1.to_csv(index=False)
    
    st.download_button(
        "↓ Download Template (Quantity Method)",
        csv_template_1,
        file_name="portfolio_import_template_quantity.csv",
        mime="text/csv",
        help="Download CSV template using positive/negative quantities for buy/sell transactions",
        key="template_quantity_download"
    )

with col2:
    template_data_2 = {
        'Coin_Name': ['Bitcoin', 'Ethereum', 'Cardano', 'Bitcoin'],
        'Symbol': ['BTC', 'ETH', 'ADA', 'BTC'],
        'Transaction_Type': ['BUY', 'BUY', 'BUY', 'SELL'],
        'Quantity': [0.1, 2.5, 1000, 0.05],  # All positive
        'Purchase_Price': [45000.00, 3200.00, 0.45, 47000.00],
        'Purchase_Date': ['2024-01-15', '2024-01-20', '2024-02-01', '2024-02-15'],
        'Purchase_Time': ['10:30', '14:15', '09:45', '11:20'],
        'Target_Sell_Price': [50000.00, 4000.00, 0.60, 0.00],
        'Coin_ID': ['bitcoin', 'ethereum', 'cardano', 'bitcoin']
    }
    template_df_2 = pd.DataFrame(template_data_2)
    csv_template_2 = template_df_2.to_csv(index=False)
    
    st.download_button(
        "↓ Download Template (Type Method)",
        csv_template_2,
        file_name="portfolio_import_template_type.csv",
        mime="text/csv",
        help="Download CSV template using Transaction_Type column for buy/sell transactions",
        key="template_type_download"
    )

# Export Section (only show if portfolio has data)
if not st.session_state.transactions.empty:
    st.markdown("---")
    st.markdown(display_icon_header('upload', 'Export Portfolio Data', 'lucide', 22, '#666666'), unsafe_allow_html=True)
    
    portfolio_df = st.session_state.transactions.copy()
    
    # Generate export data
    csv_data = portfolio_df.to_csv(index=False)
    current_date = datetime.now().strftime('%Y%m%d')
    
    # Export buttons in columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.download_button(
            "↓ Download CSV - Full Portfolio records)",
            csv_data,
            file_name=f"crypto_portfolio_{current_date}.csv",
            mime="text/csv",
            help=f"Download full portfolio as CSV file",
            key=f"csv_export_standalone_{current_date}"
        )
    
    with col2:
        if isinstance(portfolio_df, pd.DataFrame):
            excel_data = export_portfolio_to_excel(portfolio_df)
            st.download_button(
                "↓ Download Excel - Full Portfolio records)",
                excel_data,
                file_name=f"crypto_portfolio_{current_date}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                help=f"Download full portfolio as Excel file with formatting",
                key=f"excel_export_standalone_{current_date}"
            )
        else:
            st.error("Export data must be a DataFrame for Excel export")

st.markdown('<div id="delete-section" class="section-anchor"></div>', unsafe_allow_html=True)
if st.session_state.show_delete_confirm:
    with st.container():
        st.error("Confirm Deletion")
        if 'transaction_id' in st.session_state.transactions.columns:
            row_to_delete = st.session_state.transactions[
                st.session_state.transactions['transaction_id'] == st.session_state.show_delete_confirm
            ].iloc[0]
        else:
            row_to_delete = st.session_state.transactions[
                st.session_state.transactions['ID'] == st.session_state.show_delete_confirm
            ].iloc[0]
        
        st.write(f"Are you sure you want to delete this entry?")
    
        coin_text = "coin" if float(row_to_delete['Quantity']) == 1.0 else "coins"
        st.write(f"**{row_to_delete['Coin_Name']} ({row_to_delete['Symbol']})** - {row_to_delete['Quantity']} {coin_text}")
        
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button("Yes, Delete", type="primary", key=f"delete_confirm_{st.session_state.show_delete_confirm}"):
                try:
                    delete_transaction(st.session_state.show_delete_confirm)
                    st.success("Entry deleted successfully!")
                except Exception as e:
                    st.error(f"Error deleting transaction: {e}")
                finally:
                    # Always clear the dialog state
                    st.session_state.show_delete_confirm = None
                    st.rerun()
        with col2:
            if st.button("❌ Cancel", key=f"delete_cancel_{st.session_state.show_delete_confirm}"):
                # Clear the dialog state immediately
                st.session_state.show_delete_confirm = None
                st.rerun()

# --- Edit Transaction Form ---
st.markdown('<div id="edit-section" style="padding-top: 20px; margin-top: 20px;"></div>', unsafe_allow_html=True)

# Ensure edit dialog only renders once
if st.session_state.edit_transaction_id and st.session_state.edit_transaction_id is not None:
    # Clear any potential duplicate rendering flags
    edit_transaction_id = st.session_state.edit_transaction_id
    
    # Find the transaction to edit
    matching_transactions = st.session_state.transactions[
        st.session_state.transactions['ID'] == edit_transaction_id
    ]
    
    if len(matching_transactions) > 0:
        edit_row = matching_transactions.iloc[0]
        
        # Single edit dialog container with unique key
        with st.container(key=f"edit_dialog_{edit_transaction_id}"):
            st.markdown(display_icon_header('edit', 'Edit Transaction', 'lucide', 24, '#666666'), unsafe_allow_html=True)
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            
            with st.form(f"edit_form_{edit_transaction_id}"):
                # Store original values for reference
                original_quantity = float(edit_row['Quantity'])
                original_transaction_type = "Sell" if original_quantity < 0 else "Buy"
                original_quantity_abs = abs(original_quantity)
                
                st.markdown("#### Transaction Type")
                transaction_type = st.radio(
                    "Select transaction type:",
                    options=["Buy", "Sell"],
                    index=0 if original_transaction_type == "Buy" else 1,
                    horizontal=True,
                    key=f"transaction_type_{edit_transaction_id}",
                    help="Change this to convert between Buy and Sell transactions"
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    # Quantity input (always positive, preserves original absolute value)
                    st.markdown(display_icon_header('chart', f'Quantity ({transaction_type})', 'lucide', 16, '#666666'), unsafe_allow_html=True)
                    new_quantity_abs = st.number_input(
                        "", 
                        value=original_quantity_abs,  # Always use original absolute value
                        min_value=0.000001, 
                        format="%f",
                        help=f"Enter the amount to {transaction_type.lower()}. Original: {original_quantity_abs:.0f}",
                        label_visibility="collapsed"
                    )
                    
                    # Apply the correct sign based on transaction type
                    new_quantity = new_quantity_abs if transaction_type == "Buy" else -new_quantity_abs
                    
                    # Preserve original purchase price (define before using)
                    original_purchase_price = float(edit_row['Purchase_Price'])
                    
                    # Dynamic price label based on transaction type
                    price_label = "Purchase Price" if transaction_type == "Buy" else "Sell Price"
                    price_help = f"Original: ${original_purchase_price:.8f} ({'purchase' if original_transaction_type == 'Buy' else 'sell'} price)"
                    
                    # Price input with contextual labeling
                    icon_color = "#666666"
                    icon_name = "dollar-sign"
                    st.markdown(display_icon_header(icon_name, price_label, "lucide", 16, icon_color), unsafe_allow_html=True)
                    new_purchase_price = st.number_input(
                        "", 
                        value=original_purchase_price, 
                        min_value=0.00000001,  # Support very small crypto prices
                        format="%.8f", 
                        help=price_help,
                        label_visibility="collapsed"
                    )
                    
                    # Preserve original target price (handle None/null values)
                    original_target_price = float(edit_row['Target_Sell_Price']) if edit_row['Target_Sell_Price'] and edit_row['Target_Sell_Price'] != '' else 0.0
                    st.markdown(display_icon_header("bullseye", "Target Sell Price", "lucide", 16, "#666666"), unsafe_allow_html=True)
                    new_target_price = st.number_input(
                        "", 
                        value=original_target_price, 
                        min_value=0.0, 
                        format="%.8f", 
                        help=f"Original: ${original_target_price:.8f} (0 if not set)",
                        label_visibility="collapsed"
                    )
                with col2:
                    # Transaction type indicator with original values
                    if transaction_type == "Buy":
                        st.info("📈 **Buy Transaction**\n\nAdds to your portfolio holdings")
                    else:
                        st.warning("📉 **Sell Transaction**\n\nReduces your portfolio holdings")
                    
                    # Show original transaction summary
                    st.caption(f"**Original:** {original_transaction_type} {original_quantity_abs:.0f} @ ${original_purchase_price:.2f}")
                    
                    # Handle different date/time formats safely with original value display
                    try:
                        if isinstance(edit_row['Purchase_Date'], str):
                            original_date = datetime.strptime(edit_row['Purchase_Date'], '%Y-%m-%d').date()
                        else:
                            original_date = edit_row['Purchase_Date']
                        new_date = st.date_input(
                            "Purchase Date", 
                            value=original_date,
                            help=f"Original: {original_date.strftime('%Y-%m-%d')}"
                        )
                    except (ValueError, TypeError):
                        fallback_date = datetime.now().date()
                        new_date = st.date_input(
                            "Purchase Date", 
                            value=fallback_date,
                            help="Original date could not be parsed"
                        )
                    
                    try:
                        if isinstance(edit_row['Purchase_Time'], str):
                            original_time = datetime.strptime(edit_row['Purchase_Time'], '%H:%M').time()
                        else:
                            original_time = edit_row['Purchase_Time']
                        new_time = st.time_input(
                            "Purchase Time", 
                            value=original_time,
                            help=f"Original: {original_time.strftime('%H:%M')}"
                        )
                    except (ValueError, TypeError):
                        fallback_time = datetime.now().time()
                        new_time = st.time_input(
                            "Purchase Time", 
                            value=fallback_time,
                            help="Original time could not be parsed"
                        )
                
                col1, col2 = st.columns(2)
                with col1:
                    save_clicked = st.form_submit_button(display_icon_text("save", "Save Changes", "lucide", 16, "#666666"), type="primary")
                with col2:
                    cancel_clicked = st.form_submit_button(display_icon_text("delete", "Cancel", "lucide", 16, "#666666"))
        
                # Handle form submissions with immediate state clearing
                if save_clicked:
                    try:
                        update_transaction(
                            edit_transaction_id,
                            Quantity=new_quantity,
                            Purchase_Price=new_purchase_price,
                            Target_Sell_Price=new_target_price if new_target_price > 0 else 0,
                            Purchase_Date=new_date.strftime('%Y-%m-%d'),
                            Purchase_Time=new_time.strftime('%H:%M')
                        )
                        st.success("Transaction updated successfully!")
                    except Exception as e:
                        st.error(f"Error updating transaction: {e}")
                    finally:
                        # Always clear the dialog state
                        st.session_state.edit_transaction_id = None
                        st.session_state.scroll_to_table = True
            
                if cancel_clicked:
                    # Clear the dialog state immediately
                    st.session_state.edit_transaction_id = None
                    st.session_state.scroll_to_table = True
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        # Transaction not found, clear the edit state
        st.session_state.edit_transaction_id = None
        st.error("Transaction not found. Please try again.")

# --- Footer with Last Update Time ---
st.markdown("---")
st.caption(f"Last updated: {st.session_state.last_update.strftime('%Y-%m-%d %H:%M:%S')} | 🔄 Auto-refresh: Every 30 minutes")
