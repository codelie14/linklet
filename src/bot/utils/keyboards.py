from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu_keyboard() -> InlineKeyboardMarkup:
    """Main menu keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(text="🤖 Automatisation", callback_data="menu_automation"),
            InlineKeyboardButton(text="📋 Mes Tâches", callback_data="menu_tasks")
        ],
        [
            InlineKeyboardButton(text="🔗 Intégrations", callback_data="menu_integrations"),
            InlineKeyboardButton(text="🧠 Assistant IA", callback_data="menu_ai")
        ],
        [
            InlineKeyboardButton(text="⚙️ Paramètres", callback_data="menu_settings"),
            InlineKeyboardButton(text="📊 Statut", callback_data="menu_status")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def back_keyboard() -> InlineKeyboardMarkup:
    """Back button keyboard"""
    keyboard = [
        [InlineKeyboardButton(text="◀️ Retour", callback_data="back_main")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)