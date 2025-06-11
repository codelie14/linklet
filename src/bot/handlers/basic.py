from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import structlog

from src.bot.utils.keyboards import main_menu_keyboard
from src.core.database.connection import get_db
from src.core.database.models import User

router = Router()
logger = structlog.get_logger()

@router.message(Command("start"))
async def start_handler(message: types.Message, state: FSMContext):
    """Handle /start command"""
    user = message.from_user
    
    # Register user in database
    with get_db() as db:
        db_user = db.query(User).filter(User.telegram_id == user.id).first()
        if not db_user:
            db_user = User(
                telegram_id=user.id,
                username=user.username,
                first_name=user.first_name
            )
            db.add(db_user)
            db.commit()
            logger.info("New user registered", telegram_id=user.id, username=user.username)
    
    welcome_text = f"""
🚀 **Bienvenue sur Linklet, {user.first_name}!**

Je suis votre assistant d'automatisation intelligent. Je peux vous aider à :

✨ **Automatiser vos tâches** avec n8n
🤖 **Créer des workflows** personnalisés  
🔗 **Connecter vos applications** (Google, Notion, GitHub...)
📅 **Gérer vos rappels** et tâches
🧠 **Répondre à vos questions** avec l'IA

Utilisez le menu ci-dessous pour commencer !
"""
    
    await message.answer(
        welcome_text,
        reply_markup=main_menu_keyboard(),
        parse_mode="Markdown"
    )

@router.message(Command("help"))
async def help_handler(message: types.Message):
    """Handle /help command"""
    help_text = """
🆘 **Aide Linklet**

**Commandes principales :**
• `/start` - Démarrer le bot
• `/help` - Afficher cette aide
• `/status` - Statut du compte
• `/automate` - Créer un workflow
• `/tasks` - Gérer les tâches
• `/connect` - Connecter une app
• `/ai` - Assistant IA

**Raccourcis :**
• 🤖 Automatisation
• 📋 Mes Tâches  
• 🔗 Intégrations
• 🧠 Assistant IA
• ⚙️ Paramètres

Besoin d'aide ? Utilisez `/ai` pour poser vos questions !
"""
    
    await message.answer(help_text, parse_mode="Markdown")

@router.message(Command("status"))
async def status_handler(message: types.Message):
    """Handle /status command"""
    user_id = message.from_user.id
    
    with get_db() as db:
        user = db.query(User).filter(User.telegram_id == user_id).first()
        
        if not user:
            await message.answer("❌ Utilisateur non trouvé. Utilisez /start pour vous inscrire.")
            return
        
        # Get user statistics
        workflows_count = len(user.workflows)
        tasks_count = len([t for t in user.tasks if not t.completed_at])
        integrations_count = len([i for i in user.integrations if i.is_active])
        
        status_text = f"""
📊 **Statut de votre compte**

👤 **Utilisateur :** {user.first_name}
🎯 **Plan :** {user.subscription_tier.title()}
📅 **Membre depuis :** {user.created_at.strftime('%d/%m/%Y')}

📈 **Statistiques :**
• 🤖 Workflows actifs : {workflows_count}
• 📋 Tâches en cours : {tasks_count}  
• 🔗 Intégrations : {integrations_count}

**Limites du plan gratuit :**
• Workflows : {workflows_count}/10
• Intégrations : {integrations_count}/3
• Requêtes IA : Usage normal
"""
        
        await message.answer(status_text, parse_mode="Markdown")