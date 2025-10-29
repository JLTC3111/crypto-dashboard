"""
Internationalization (i18n) Module
Supports multiple languages: English, German, French, Russian, Spanish, Vietnamese, Japanese, Korean, Thai
"""

import streamlit as st
from typing import Dict, Any


class Translations:
    """Translation strings for all supported languages"""
    
    LANGUAGES = {
        'en': 'English',
        'de': 'Deutsch',
        'fr': 'Français',
        'ru': 'Русский',
        'es': 'Español',
        'vi': 'Tiếng Việt',
        'jp': '日本語',
        'kr': '한국어',
        'th': 'ไทย'
    }
    
    TRANSLATIONS = {
        # Navigation & Pages
        'home': {
            'en': 'Home',
            'de': 'Startseite',
            'fr': 'Accueil',
            'ru': 'Главная',
            'es': 'Inicio',
            'vi': 'Trang chủ',
            'jp': 'ホーム',
            'kr': '홈',
            'th': 'หน้าแรก'
        },
        'dashboard': {
            'en': 'Dashboard',
            'de': 'Dashboard',
            'fr': 'Tableau de bord',
            'ru': 'Панель управления',
            'es': 'Panel',
            'vi': 'Bảng điều khiển',
            'jp': 'ダッシュボード',
            'kr': '대시보드',
            'th': 'แดชบอร์ด'
        },
        'comparison': {
            'en': 'Comparison',
            'de': 'Vergleich',
            'fr': 'Comparaison',
            'ru': 'Сравнение',
            'es': 'Comparación',
            'vi': 'So sánh',
            'jp': '比較',
            'kr': '비교',
            'th': 'เปรียบเทียบ'
        },
        'portfolio': {
            'en': 'My Portfolio',
            'de': 'Mein Portfolio',
            'fr': 'Mon Portefeuille',
            'ru': 'Мой портфель',
            'es': 'Mi Cartera',
            'vi': 'Danh mục của tôi',
            'jp': 'マイポートフォリオ',
            'kr': '내 포트폴리오',
            'th': 'พอร์ตของฉัน'
        },
        
        # Common UI Elements
        'select_asset': {
            'en': 'Select Asset',
            'de': 'Asset auswählen',
            'fr': 'Sélectionner un actif',
            'ru': 'Выбрать актив',
            'es': 'Seleccionar activo',
            'vi': 'Chọn tài sản',
            'jp': '資産を選択',
            'kr': '자산 선택',
            'th': 'เลือกสินทรัพย์'
        },
        'refresh': {
            'en': 'Refresh',
            'de': 'Aktualisieren',
            'fr': 'Actualiser',
            'ru': 'Обновить',
            'es': 'Actualizar',
            'vi': 'Làm mới',
            'jp': '更新',
            'kr': '새로고침',
            'th': 'รีเฟรช'
        },
        'loading': {
            'en': 'Loading...',
            'de': 'Laden...',
            'fr': 'Chargement...',
            'ru': 'Загрузка...',
            'es': 'Cargando...',
            'vi': 'Đang tải...',
            'jp': '読み込み中...',
            'kr': '로딩 중...',
            'th': 'กำลังโหลด...'
        },
        
        # Risk Metrics
        'max_drawdown': {
            'en': 'Max Drawdown',
            'de': 'Maximaler Drawdown',
            'fr': 'Drawdown Maximum',
            'ru': 'Макс. просадка',
            'es': 'Drawdown Máximo',
            'vi': 'Sụt giảm tối đa',
            'jp': '最大ドローダウン',
            'kr': '최대 낙폭',
            'th': 'การลดลงสูงสุด'
        },
        'sharpe_ratio': {
            'en': 'Sharpe Ratio',
            'de': 'Sharpe-Ratio',
            'fr': 'Ratio de Sharpe',
            'ru': 'Коэффициент Шарпа',
            'es': 'Ratio de Sharpe',
            'vi': 'Tỷ lệ Sharpe',
            'jp': 'シャープレシオ',
            'kr': '샤프 비율',
            'th': 'อัตราส่วนชาร์ป'
        },
        'value_at_risk': {
            'en': 'Value at Risk',
            'de': 'Value at Risk',
            'fr': 'Valeur en Risque',
            'ru': 'Стоимость под риском',
            'es': 'Valor en Riesgo',
            'vi': 'Giá trị rủi ro',
            'jp': 'バリュー・アット・リスク',
            'kr': '위험 가치',
            'th': 'มูลค่าความเสี่ยง'
        },
        'volatility': {
            'en': 'Volatility',
            'de': 'Volatilität',
            'fr': 'Volatilité',
            'ru': 'Волатильность',
            'es': 'Volatilidad',
            'vi': 'Biến động',
            'jp': 'ボラティリティ',
            'kr': '변동성',
            'th': 'ความผันผวน'
        },
        
        # Financial Terms
        'current_price': {
            'en': 'Current Price',
            'de': 'Aktueller Preis',
            'fr': 'Prix Actuel',
            'ru': 'Текущая цена',
            'es': 'Precio Actual',
            'vi': 'Giá hiện tại',
            'jp': '現在価格',
            'kr': '현재 가격',
            'th': 'ราคาปัจจุบัน'
        },
        'market_cap': {
            'en': 'Market Cap',
            'de': 'Marktkapitalisierung',
            'fr': 'Capitalisation',
            'ru': 'Капитализация',
            'es': 'Capitalización',
            'vi': 'Vốn hóa',
            'jp': '時価総額',
            'kr': '시가총액',
            'th': 'มูลค่าตลาด'
        },
        'total_value': {
            'en': 'Total Value',
            'de': 'Gesamtwert',
            'fr': 'Valeur Totale',
            'ru': 'Общая стоимость',
            'es': 'Valor Total',
            'vi': 'Tổng giá trị',
            'jp': '総額',
            'kr': '총 가치',
            'th': 'มูลค่ารวม'
        },
        'profit_loss': {
            'en': 'Profit/Loss',
            'de': 'Gewinn/Verlust',
            'fr': 'Profit/Perte',
            'ru': 'Прибыль/Убыток',
            'es': 'Ganancia/Pérdida',
            'vi': 'Lãi/Lỗ',
            'jp': '損益',
            'kr': '손익',
            'th': 'กำไร/ขาดทุน'
        },
        
        # Actions
        'buy': {
            'en': 'Buy',
            'de': 'Kaufen',
            'fr': 'Acheter',
            'ru': 'Купить',
            'es': 'Comprar',
            'vi': 'Mua',
            'jp': '購入',
            'kr': '구매',
            'th': 'ซื้อ'
        },
        'sell': {
            'en': 'Sell',
            'de': 'Verkaufen',
            'fr': 'Vendre',
            'ru': 'Продать',
            'es': 'Vender',
            'vi': 'Bán',
            'jp': '売却',
            'kr': '판매',
            'th': 'ขาย'
        },
        'export': {
            'en': 'Export',
            'de': 'Exportieren',
            'fr': 'Exporter',
            'ru': 'Экспорт',
            'es': 'Exportar',
            'vi': 'Xuất',
            'jp': 'エクスポート',
            'kr': '내보내기',
            'th': 'ส่งออก'
        },
        
        # Time Periods
        'daily': {
            'en': 'Daily',
            'de': 'Täglich',
            'fr': 'Quotidien',
            'ru': 'Ежедневно',
            'es': 'Diario',
            'vi': 'Hàng ngày',
            'jp': '日次',
            'kr': '일일',
            'th': 'รายวัน'
        },
        'weekly': {
            'en': 'Weekly',
            'de': 'Wöchentlich',
            'fr': 'Hebdomadaire',
            'ru': 'Еженедельно',
            'es': 'Semanal',
            'vi': 'Hàng tuần',
            'jp': '週次',
            'kr': '주간',
            'th': 'รายสัปดาห์'
        },
        'monthly': {
            'en': 'Monthly',
            'de': 'Monatlich',
            'fr': 'Mensuel',
            'ru': 'Ежемесячно',
            'es': 'Mensual',
            'vi': 'Hàng tháng',
            'jp': '月次',
            'kr': '월간',
            'th': 'รายเดือน'
        },
        
        # Status Messages
        'success': {
            'en': 'Success',
            'de': 'Erfolgreich',
            'fr': 'Succès',
            'ru': 'Успешно',
            'es': 'Éxito',
            'vi': 'Thành công',
            'jp': '成功',
            'kr': '성공',
            'th': 'สำเร็จ'
        },
        'error': {
            'en': 'Error',
            'de': 'Fehler',
            'fr': 'Erreur',
            'ru': 'Ошибка',
            'es': 'Error',
            'vi': 'Lỗi',
            'jp': 'エラー',
            'kr': '오류',
            'th': 'ข้อผิดพลาด'
        },
        'warning': {
            'en': 'Warning',
            'de': 'Warnung',
            'fr': 'Avertissement',
            'ru': 'Предупреждение',
            'es': 'Advertencia',
            'vi': 'Cảnh báo',
            'jp': '警告',
            'kr': '경고',
            'th': 'คำเตือน'
        },
        
        # Risk Levels
        'low_risk': {
            'en': 'Low Risk',
            'de': 'Niedriges Risiko',
            'fr': 'Risque Faible',
            'ru': 'Низкий риск',
            'es': 'Riesgo Bajo',
            'vi': 'Rủi ro thấp',
            'jp': '低リスク',
            'kr': '낮은 위험',
            'th': 'ความเสี่ยงต่ำ'
        },
        'medium_risk': {
            'en': 'Medium Risk',
            'de': 'Mittleres Risiko',
            'fr': 'Risque Moyen',
            'ru': 'Средний риск',
            'es': 'Riesgo Medio',
            'vi': 'Rủi ro trung bình',
            'jp': '中リスク',
            'kr': '중간 위험',
            'th': 'ความเสี่ยงปานกลาง'
        },
        'high_risk': {
            'en': 'High Risk',
            'de': 'Hohes Risiko',
            'fr': 'Risque Élevé',
            'ru': 'Высокий риск',
            'es': 'Riesgo Alto',
            'vi': 'Rủi ro cao',
            'jp': '高リスク',
            'kr': '높은 위험',
            'th': 'ความเสี่ยงสูง'
        },
        
        # Settings
        'settings': {
            'en': 'Settings',
            'de': 'Einstellungen',
            'fr': 'Paramètres',
            'ru': 'Настройки',
            'es': 'Configuración',
            'vi': 'Cài đặt',
            'jp': '設定',
            'kr': '설정',
            'th': 'การตั้งค่า'
        },
        'language': {
            'en': 'Language',
            'de': 'Sprache',
            'fr': 'Langue',
            'ru': 'Язык',
            'es': 'Idioma',
            'vi': 'Ngôn ngữ',
            'jp': '言語',
            'kr': '언어',
            'th': 'ภาษา'
        },
        'theme': {
            'en': 'Theme',
            'de': 'Design',
            'fr': 'Thème',
            'ru': 'Тема',
            'es': 'Tema',
            'vi': 'Giao diện',
            'jp': 'テーマ',
            'kr': '테마',
            'th': 'ธีม'
        },
        
        # Descriptions
        'welcome_message': {
            'en': 'Welcome to the Crypto Risk Management Dashboard',
            'de': 'Willkommen beim Krypto-Risikomanagement-Dashboard',
            'fr': 'Bienvenue sur le tableau de bord de gestion des risques crypto',
            'ru': 'Добро пожаловать в панель управления криптовалютными рисками',
            'es': 'Bienvenido al panel de gestión de riesgos cripto',
            'vi': 'Chào mừng đến với bảng điều khiển quản lý rủi ro tiền điện tử',
            'jp': '暗号資産リスク管理ダッシュボードへようこそ',
            'kr': '암호화폐 위험 관리 대시보드에 오신 것을 환영합니다',
            'th': 'ยินดีต้อนรับสู่แดชบอร์ดการจัดการความเสี่ยงคริปโต'
        },
        'no_data': {
            'en': 'No data available',
            'de': 'Keine Daten verfügbar',
            'fr': 'Aucune donnée disponible',
            'ru': 'Нет доступных данных',
            'es': 'No hay datos disponibles',
            'vi': 'Không có dữ liệu',
            'jp': 'データがありません',
            'kr': '데이터 없음',
            'th': 'ไม่มีข้อมูล'
        },
        'last_updated': {
            'en': 'Last updated',
            'de': 'Zuletzt aktualisiert',
            'fr': 'Dernière mise à jour',
            'ru': 'Последнее обновление',
            'es': 'Última actualización',
            'vi': 'Cập nhật lần cuối',
            'jp': '最終更新',
            'kr': '마지막 업데이트',
            'th': 'อัปเดตล่าสุด'
        }
    }


class I18n:
    """Internationalization handler"""
    
    @staticmethod
    def get_current_language() -> str:
        """Get the current language from session state"""
        if 'language' not in st.session_state:
            st.session_state.language = 'en'
        return st.session_state.language
    
    @staticmethod
    def set_language(lang_code: str):
        """Set the current language"""
        if lang_code in Translations.LANGUAGES:
            st.session_state.language = lang_code
    
    @staticmethod
    def t(key: str, **kwargs) -> str:
        """
        Translate a key to the current language
        
        Args:
            key: Translation key
            **kwargs: Format arguments for the translation
        
        Returns:
            Translated string
        """
        lang = I18n.get_current_language()
        
        if key not in Translations.TRANSLATIONS:
            return key
        
        translation = Translations.TRANSLATIONS[key].get(lang, Translations.TRANSLATIONS[key].get('en', key))
        
        # Format with kwargs if provided
        if kwargs:
            try:
                translation = translation.format(**kwargs)
            except:
                pass
        
        return translation
    
    @staticmethod
    def get_available_languages() -> Dict[str, str]:
        """Get all available languages"""
        return Translations.LANGUAGES


def create_language_selector():
    """Create a language selector widget"""
    languages = I18n.get_available_languages()
    current_lang = I18n.get_current_language()
    
    # Find current language index
    lang_codes = list(languages.keys())
    current_index = lang_codes.index(current_lang) if current_lang in lang_codes else 0
    
    selected_lang = st.selectbox(
        I18n.t('language'),
        options=lang_codes,
        format_func=lambda x: f"{languages[x]} ({x.upper()})",
        index=current_index,
        key='language_selector'
    )
    
    if selected_lang != current_lang:
        I18n.set_language(selected_lang)
        st.rerun()


# Convenience function
def t(key: str, **kwargs) -> str:
    """Shorthand for I18n.t()"""
    return I18n.t(key, **kwargs)


# Export main components
__all__ = [
    'I18n',
    't',
    'create_language_selector',
    'Translations'
]
