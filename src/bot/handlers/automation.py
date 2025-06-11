from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import structlog

from src.bot.utils.keyboards import back_keyboard
from src.core.database.connection import get_db
from src.core.database.models import User, Workflow

router = Router()
logger = structlog.get_logger()

class AutomationStates(StatesGroup):
    waiting_workflow_name = State()
    waiting_workflow_description = State()

@router.message(Command("automate"))
@router.callback_query(F.data == "menu_automation")
async def automation_menu(update: types.Message | types.CallbackQuery, state: FSMContext):
    """Show automation menu"""
    
    menu_text = """
🤖 **Menu Automatisation**

Que souhaitez-vous faire ?

• **Créer un workflow** - Automatiser une tâche répétitive
• **Mes workflows** - Voir vos automatisations actives
• **Templates** - Utiliser des modèles prêts à l'emploi
"""
    
    keyboard = [
        [
            types.InlineKeyboardButton(text="➕ Créer Workflow", callback_data="create_workflow"),
            types.InlineKeyboardButton(text="📋 Mes Workflows", callback_data="list_workflows")
        ],
        [
            types.InlineKeyboardButton(text="📄 Templates", callback_data="workflow_templates"),
            types.InlineKeyboardButton(text="◀️ Menu Principal", callback_data="back_main")
        ]
    ]
    markup = types.InlineKeyboardMarkup(inline_keyboard=keyboard)
    
    if isinstance(update, types.CallbackQuery):
        await update.message.edit_text(menu_text, reply_markup=markup, parse_mode="Markdown")
        await update.answer()
    else:
        await update.answer(menu_text, reply_markup=markup, parse_mode="Markdown")

@router.callback_query(F.data == "create_workflow")
async def start_workflow_creation(callback: types.CallbackQuery, state: FSMContext):
    """Start workflow creation process"""
    await callback.message.edit_text(
        "🎯 **Création d'un nouveau workflow**\n\n"
        "Donnez un nom à votre workflow :\n"
        "*(ex: Sauvegarde quotidienne, Rapport hebdomadaire...)*",
        parse_mode="Markdown"
    )
    await state.set_state(AutomationStates.waiting_workflow_name)
    await callback.answer()

@router.message(AutomationStates.waiting_workflow_name)
async def process_workflow_name(message: types.Message, state: FSMContext):
    """Process workflow name input"""
    workflow_name = message.text.strip()
    
    if len(workflow_name) < 3:
        await message.answer("❌ Le nom doit faire au moins 3 caractères. Essayez encore :")
        return
    
    await state.update_data(workflow_name=workflow_name)
    await message.answer(
        f"✅ **Nom:** {workflow_name}\n\n"
        "📝 Maintenant, décrivez ce que ce workflow doit faire :\n"
        "*(ex: Envoyer un rapport Excel tous les lundis à 9h)*",
        parse_mode="Markdown"
    )
    await state.set_state(AutomationStates.waiting_workflow_description)

@router.message(AutomationStates.waiting_workflow_description)
async def process_workflow_description(message: types.Message, state: FSMContext):
    """Process workflow description and create workflow"""
    description = message.text.strip()
    data = await state.get_data()
    
    user_id = message.from_user.id
    
    # Save workflow to database
    with get_db() as db:
        user = db.query(User).filter(User.telegram_id == user_id).first()
        
        workflow = Workflow(
            user_id=user.id,
            name=data['workflow_name'],
            description=description,
            triggers={},  # Will be configured later
        )
        db.add(workflow)
        db.commit()
        
        success_text = f"""
✅ **Workflow créé avec succès !**

📋 **Nom :** {workflow.name}
📝 **Description :** {workflow.description}
🆔 **ID :** {str(workflow.id)[:8]}...

🔧 **Prochaines étapes :**
• Configurez les déclencheurs
• Ajoutez des actions
• Testez votre workflow

Utilisez `/workflows` pour gérer vos automatisations.
"""
        
        await message.answer(success_text, parse_mode="Markdown")
        await state.clear()

@router.callback_query(F.data == "list_workflows")
async def list_user_workflows(callback: types.CallbackQuery):
    """List user's workflows"""
    user_id = callback.from_user.id
    
    with get_db() as db:
        user = db.query(User).filter(User.telegram_id == user_id).first()
        workflows = user.workflows if user else []
        
        if not workflows:
            text = "📋 **Vos Workflows**\n\nAucun workflow créé pour le moment.\nUtilisez ➕ Créer Workflow pour commencer !"
        else:
            text = "📋 **Vos Workflows**\n\n"
            for i, workflow in enumerate(workflows, 1):
                status = "🟢 Actif" if workflow.is_active else "🔴 Inactif"
                text += f"{i}. **{workflow.name}**\n"
                text += f"   {status} • ID: {str(workflow.id)[:8]}\n"
                text += f"   📝 {workflow.description[:50]}...\n\n"
    
    keyboard = [
        [types.InlineKeyboardButton(text="◀️ Retour", callback_data="menu_automation")]
    ]
    markup = types.InlineKeyboardMarkup(inline_keyboard=keyboard)
    
    await callback.message.edit_text(text, reply_markup=markup, parse_mode="Markdown")
    await callback.answer()
