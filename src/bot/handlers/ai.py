from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import structlog
import openai
from typing import Optional

from src.core.config import settings
from src.bot.utils.keyboards import back_keyboard

router = Router()
logger = structlog.get_logger()

# Configure OpenAI if available
if settings.openai_api_key:
    openai.api_key = settings.openai_api_key

class AIStates(StatesGroup):
    chatting = State()

@router.message(Command("ai"))
@router.callback_query(F.data == "menu_ai")
async def ai_menu(update: types.Message | types.CallbackQuery, state: FSMContext):
    """Show AI assistant menu"""
    
    menu_text = """
🧠 **Assistant IA Linklet**

Je peux vous aider avec :

• 💬 **Chat intelligent** - Posez-moi vos questions
• 🔧 **Aide workflows** - Optimiser vos automatisations  
• 📊 **Analyse de données** - Interpréter vos fichiers
• ✍️ **Génération de contenu** - Rédiger des textes
• 🌐 **Traductions** - Traduire dans toutes les langues

Que puis-je faire pour vous ?
"""
    
    keyboard = [
        [
            types.InlineKeyboardButton(text="💬 Commencer Chat", callback_data="start_ai_chat"),
            types.InlineKeyboardButton(text="🔧 Aide Workflows", callback_data="ai_workflow_help")
        ],
        [
            types.InlineKeyboardButton(text="📊 Analyser Fichier", callback_data="ai_analyze_file"),
            types.InlineKeyboardButton(text="✍️ Générer Contenu", callback_data="ai_generate_content")
        ],
        [
            types.InlineKeyboardButton(text="◀️ Menu Principal", callback_data="back_main")
        ]
    ]
    markup = types.InlineKeyboardMarkup(inline_keyboard=keyboard)
    
    if isinstance(update, types.CallbackQuery):
        await update.message.edit_text(menu_text, reply_markup=markup, parse_mode="Markdown")
        await update.answer()
    else:
        await update.answer(menu_text, reply_markup=markup, parse_mode="Markdown")

@router.callback_query(F.data == "start_ai_chat")
async def start_ai_chat(callback: types.CallbackQuery, state: FSMContext):
    """Start AI chat session"""
    await callback.message.edit_text(
        "🤖 **Mode Chat IA Activé**\n\n"
        "Posez-moi vos questions ! Je peux vous aider avec :\n"
        "• Questions générales\n"
        "• Conseils d'automatisation\n"
        "• Aide technique\n"
        "• Optimisations de workflows\n\n"
        "💡 *Tapez /stop pour arrêter le chat*",
        parse_mode="Markdown"
    )
    await state.set_state(AIStates.chatting)
    await callback.answer()

@router.message(AIStates.chatting)
async def process_ai_chat(message: types.Message, state: FSMContext):
    """Process AI chat messages"""
    if message.text and message.text.lower() in ['/stop', 'stop', 'arrêt']:
        await message.answer(
            "👋 **Chat IA terminé**\n\n"
            "Merci d'avoir utilisé l'assistant IA Linklet !\n"
            "Utilisez `/ai` pour recommencer.",
            parse_mode="Markdown"
        )
        await state.clear()
        return
    
    # Show typing indicator
    await message.bot.send_chat_action(message.chat.id, "typing")
    
    try:
        if settings.openai_api_key:
            # Use OpenAI API
            response = await get_ai_response(message.text)
        else:
            # Fallback response
            response = get_fallback_ai_response(message.text)
        
        await message.answer(f"🤖 {response}", parse_mode="Markdown")
        
    except Exception as e:
        logger.error("AI chat error", error=str(e))
        await message.answer(
            "❌ Désolé, je rencontre un problème technique.\n"
            "Essayez de reformuler votre question."
        )

async def get_ai_response(user_message: str) -> str:
    """Get response from OpenAI API"""
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": "Tu es Linklet, un assistant IA spécialisé dans l'automatisation et les workflows. "
                              "Réponds de manière concise et utile en français. "
                              "Tu peux aider avec l'automatisation, les intégrations d'APIs, et les conseils techniques."
                },
                {"role": "user", "content": user_message}
            ],
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error("OpenAI API error", error=str(e))
        raise

def get_fallback_ai_response(user_message: str) -> str:
    """Fallback response when AI is not available"""
    message_lower = user_message.lower()
    
    if any(word in message_lower for word in ['bonjour', 'salut', 'hello']):
        return "Bonjour ! Comment puis-je vous aider avec vos automatisations aujourd'hui ?"
    
    elif any(word in message_lower for word in ['workflow', 'automatisation', 'automation']):
        return """
**Conseils pour créer un bon workflow :**

1. 🎯 **Définissez clairement l'objectif**
2. 🔄 **Identifiez les déclencheurs** (temps, événement, etc.)
3. ⚡ **Listez les actions** étape par étape
4. 🧪 **Testez** avant la mise en production
5. 📊 **Surveillez** les performances

Besoin d'aide spécifique ? Décrivez votre cas d'usage !
"""
    
    elif any(word in message_lower for word in ['intégration', 'api', 'connecter']):
        return """
**Intégrations populaires disponibles :**

• 📊 **Google Sheets** - Gestion de données
• 📝 **Notion** - Base de connaissances  
• 💾 **Google Drive** - Stockage de fichiers
• 🐙 **GitHub** - Code et projets
• 📧 **Email** - Notifications automatiques

Quelle intégration vous intéresse ?
"""
    
    else:
        return """
Je suis votre assistant Linklet ! 🤖

**Je peux vous aider avec :**
• Création de workflows
• Intégrations d'APIs
• Automatisation de tâches
• Conseils techniques

*Note: IA avancée non configurée. Configurez OpenAI API pour des réponses plus intelligentes.*
"""
