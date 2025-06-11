"""Workflow management command handlers."""
from aiogram import Router, F, types
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import structlog

from src.core.config import settings
from src.core.database.connection import get_db
from src.core.services.workflow_service import WorkflowService
from src.integrations.n8n.client import N8NClient
from src.bot.utils.keyboards import (
    create_workflow_keyboard,
    workflow_list_keyboard,
    workflow_actions_keyboard,
    back_keyboard,
    workflow_template_keyboard
)

router = Router()
logger = structlog.get_logger()

class WorkflowStates(StatesGroup):
    waiting_name = State()
    waiting_description = State()
    waiting_template = State()
    waiting_trigger = State()
    waiting_schedule = State()
    waiting_webhook = State()
    waiting_action = State()

@router.message(Command("workflow"))
async def workflow_menu(message: Message):
    """Show workflow management menu."""
    text = """
🔄 **Menu des Workflows**

Commandes disponibles :
• `/workflow create` - Créer un nouveau workflow
• `/workflow list` - Voir vos workflows
• `/workflow templates` - Voir les templates disponibles

Utilisez les boutons ci-dessous pour naviguer.
"""
    await message.answer(
        text,
        reply_markup=create_workflow_keyboard()
    )

@router.message(Command("workflow", "create"))
async def workflow_create_start(message: Message, state: FSMContext):
    """Start workflow creation process."""
    await state.set_state(WorkflowStates.waiting_name)
    await message.answer(
        "Comment voulez-vous nommer ce workflow ? "
        "(exemple : 'Sauvegarde quotidienne des emails')",
        reply_markup=back_keyboard()
    )

@router.message(WorkflowStates.waiting_name)
async def workflow_name_received(message: Message, state: FSMContext):
    """Handle workflow name input."""
    await state.update_data(name=message.text)
    await state.set_state(WorkflowStates.waiting_description)
    await message.answer(
        "Donnez une brève description de ce que fait ce workflow : "
        "(exemple : 'Sauvegarde les emails importants dans Google Drive')",
        reply_markup=back_keyboard()
    )

@router.message(WorkflowStates.waiting_description)
async def workflow_description_received(message: Message, state: FSMContext):
    """Handle workflow description and create workflow."""
    user_data = await state.get_data()
    await state.clear()

    try:
        with get_db() as db:
            service = WorkflowService(db)
            workflow = await service.create_workflow(
                user_id=message.from_user.id,
                name=user_data["name"],
                description=message.text
            )
        
        await message.answer(
            f"✅ Workflow '{workflow.name}' créé avec succès!\n\n"
            "Vous pouvez maintenant l'activer ou le configurer.",
            reply_markup=workflow_actions_keyboard(workflow.id)
        )
    except Exception as e:
        logger.error(
            "Failed to create workflow",
            error=str(e),
            user_id=message.from_user.id
        )
        await message.answer(
            "❌ Désolé, une erreur est survenue lors de la création du workflow.\n"
            "Veuillez réessayer plus tard.",
            reply_markup=back_keyboard()
        )

@router.message(Command("workflow", "list"))
async def list_workflows(message: Message):
    """List user's workflows."""
    try:
        with get_db() as db:
            service = WorkflowService(db)
            workflows = await service.list_user_workflows(message.from_user.id)
        
        if not workflows:
            await message.answer(
                "Vous n'avez pas encore de workflow.\n"
                "Utilisez /workflow create pour en créer un !",
                reply_markup=create_workflow_keyboard()
            )
            return

        text = "**Vos Workflows**\n\n"
        for wf in workflows:
            status = "✅ Actif" if wf.is_active else "⏸️ Inactif"
            text += f"• {wf.name} - {status}\n"
            if wf.description:
                text += f"  _{wf.description}_\n"
        
        await message.answer(
            text,
            reply_markup=workflow_list_keyboard(workflows)
        )
    except Exception as e:
        logger.error(
            "Failed to list workflows",
            error=str(e),
            user_id=message.from_user.id
        )
        await message.answer("❌ Erreur lors de la récupération des workflows.")

@router.callback_query(F.data.startswith("workflow:"))
async def workflow_action(callback: CallbackQuery):
    """Handle workflow action buttons."""
    action = callback.data.split(":")
    if len(action) != 3:
        await callback.answer("❌ Action invalide")
        return

    _, workflow_id, action_type = action
    try:
        with get_db() as db:
            service = WorkflowService(db)
            
            if action_type == "activate":
                workflow = await service.activate_workflow(int(workflow_id), callback.from_user.id)
                await callback.answer("✅ Workflow activé")
            
            elif action_type == "deactivate":
                workflow = await service.deactivate_workflow(int(workflow_id), callback.from_user.id)
                await callback.answer("⏸️ Workflow désactivé")
            
            elif action_type == "delete":
                # TODO: Ajouter confirmation avant suppression
                await service.delete_workflow(int(workflow_id), callback.from_user.id)
                await callback.answer("🗑️ Workflow supprimé")
            
            elif action_type == "execute":
                result = await service.execute_workflow(int(workflow_id), callback.from_user.id)
                await callback.answer("▶️ Workflow exécuté")
            
            # Mettre à jour le message avec le nouvel état
            await list_workflows(callback.message)
            
    except ValueError as e:
        await callback.answer(f"❌ Erreur : {str(e)}")
    except Exception as e:
        logger.error(
            "Workflow action failed",
            error=str(e),
            workflow_id=workflow_id,
            action=action_type
        )
        await callback.answer("❌ Une erreur est survenue")

async def finish_trigger_config(callback: types.CallbackQuery, state: FSMContext):
    """Finish trigger configuration."""
    data = await state.get_data()
    workflow_id = data.get("workflow_id")
    
    async with N8NClient() as n8n:
        workflow = await n8n.update_workflow(
            workflow_id,
            {
                "trigger": {
                    "type": "manual"
                }
            }
        )
    
    await callback.message.edit_text(
        "✅ Configuration terminée!\n\n"
        "Le workflow peut maintenant être exécuté manuellement.",
        reply_markup=workflow_actions_keyboard(workflow_id)
    )
    await state.clear()

@router.message(Command("workflow", "templates"))
async def list_templates(message: types.Message):
    """List available workflow templates."""
    templates = [
        {
            "id": "daily-backup",
            "name": "Sauvegarde Quotidienne",
            "description": "Sauvegarde automatique de fichiers vers le cloud"
        },
        {
            "id": "weekly-report",
            "name": "Rapport Hebdomadaire",
            "description": "Génération et envoi de rapports chaque semaine"
        },
        {
            "id": "monitor-website",
            "name": "Surveillance Site Web", 
            "description": "Alerte en cas d'indisponibilité d'un site"
        }
    ]
    
    text = "📋 **Templates de Workflow**\n\n"
    for template in templates:
        text += f"• **{template['name']}**\n"
        text += f"  _{template['description']}_\n\n"
    
    await message.answer(
        text,
        reply_markup=workflow_template_keyboard(templates),
        parse_mode="Markdown"
    )

@router.callback_query(F.data.startswith("template:"))
async def use_template(callback: types.CallbackQuery, state: FSMContext):
    """Start workflow creation from template."""
    template_id = callback.data.split(":")[1]
    
    # Store template ID in state
    await state.update_data(template_id=template_id)
    await state.set_state(WorkflowStates.waiting_name)
    
    await callback.message.edit_text(
        "✨ **Création depuis un template**\n\n"
        "Comment voulez-vous nommer ce workflow ?\n"
        "*(ex: 'Sauvegarde Photos Quotidienne')*",
        reply_markup=back_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()

@router.callback_query(F.data == "configure_trigger")
async def configure_trigger(callback: types.CallbackQuery, state: FSMContext):
    """Configure workflow trigger."""
    text = """
⚡ **Configuration du déclencheur**

Choisissez quand le workflow doit s'exécuter:

• **Schedule** - À une heure précise
• **Webhook** - Via une URL HTTP
• **Manual** - Manuellement uniquement
"""
    keyboard = [
        [
            types.InlineKeyboardButton(text="⏰ Schedule", callback_data="trigger:schedule"),
            types.InlineKeyboardButton(text="🔗 Webhook", callback_data="trigger:webhook")
        ],
        [
            types.InlineKeyboardButton(text="🤚 Manuel", callback_data="trigger:manual")
        ],
        [
            types.InlineKeyboardButton(text="◀️ Retour", callback_data="workflow_menu")
        ]
    ]
    markup = types.InlineKeyboardMarkup(inline_keyboard=keyboard)
    
    await callback.message.edit_text(text, reply_markup=markup, parse_mode="Markdown")
    await callback.answer()

@router.callback_query(F.data.startswith("trigger:"))
async def set_trigger_type(callback: types.CallbackQuery, state: FSMContext):
    """Handle trigger type selection."""
    trigger_type = callback.data.split(":")[1]
    data = await state.get_data()
    workflow_id = data.get("workflow_id")
    
    await state.update_data(trigger_type=trigger_type)
    
    if trigger_type == "schedule":
        await state.set_state(WorkflowStates.waiting_schedule)
        await callback.message.edit_text(
            "⏰ **Configuration du planning**\n\n"
            "Quand souhaitez-vous que le workflow s'exécute ?\n"
            "*(ex: '9:00 tous les jours' ou 'Lundi 10h')*",
            reply_markup=back_keyboard(),
            parse_mode="Markdown"
        )
    elif trigger_type == "webhook":
        await state.set_state(WorkflowStates.waiting_webhook)
        # Generate webhook URL
        if workflow_id:
            webhook_url = f"{settings.n8n_webhook_base_url}/workflow/{workflow_id}"
            await callback.message.edit_text(
                f"🔗 **Webhook URL**\n\n"
                f"`{webhook_url}`\n\n"
                "Utilisez cette URL pour déclencher le workflow via HTTP POST.",
                reply_markup=back_keyboard(),
                parse_mode="Markdown"
            )
        else:
            await callback.message.edit_text(
                "❌ Erreur: Workflow non trouvé",
                reply_markup=back_keyboard()
            )
    else:
        # Manual trigger - no additional config needed
        await finish_trigger_config(callback, state)
    
    await callback.answer()

@router.message(WorkflowStates.waiting_schedule)
async def process_schedule(message: types.Message, state: FSMContext):
    """Process schedule input and configure cron trigger."""
    schedule = message.text.strip().lower()
    data = await state.get_data()
    workflow_id = data.get("workflow_id")
    
    if not workflow_id:
        await message.answer(
            "❌ Erreur: Workflow non trouvé",
            reply_markup=back_keyboard()
        )
        return
    
    try:
        # Convert natural language to cron
        cron = parse_schedule_to_cron(schedule)
        
        async with N8NClient() as n8n:
            workflow = await n8n.update_workflow(
                workflow_id,
                {
                    "trigger": {
                        "type": "schedule",
                        "cron": cron
                    }
                }
            )
        
        await message.answer(
            "✅ Planning configuré avec succès!\n\n"
            f"Le workflow s'exécutera : {schedule}",
            reply_markup=workflow_actions_keyboard(workflow_id)
        )
        await state.clear()
        
    except Exception as e:
        logger.error("Failed to configure schedule", error=str(e))
        await message.answer(
            "❌ Erreur lors de la configuration du planning.\n"
            "Format invalide ou erreur serveur.",
            reply_markup=back_keyboard()
        )

async def parse_schedule_to_cron(schedule: str) -> str:
    """Convert natural language schedule to cron expression."""
    # TODO: Implement proper natural language parsing
    # For now, just handle basic daily schedule
    if "tous les jours" in schedule:
        time = schedule.split()[0]
        hour, minute = time.split(":")
        return f"{minute} {hour} * * *"
    raise ValueError("Format de planning non supporté")
