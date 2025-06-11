"""Workflow-related keyboard layouts."""
from typing import List, Dict
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from src.core.database.models import Workflow

def create_workflow_keyboard() -> InlineKeyboardMarkup:
    """Create workflow menu keyboard."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="➕ Créer", callback_data="create_workflow"),
                InlineKeyboardButton(text="📋 Liste", callback_data="list_workflows")
            ],
            [
                InlineKeyboardButton(text="📄 Templates", callback_data="workflow_templates"),
                InlineKeyboardButton(text="◀️ Menu", callback_data="back_main")
            ]
        ]
    )

def workflow_list_keyboard(workflows: List[Workflow]) -> InlineKeyboardMarkup:
    """Create keyboard with workflow list."""
    buttons = []
    for workflow in workflows:
        buttons.append([
            InlineKeyboardButton(
                text=f"⚙️ {workflow.name}",
                callback_data=f"workflow:{workflow.id}:details"
            )
        ])
    
    buttons.append([
        InlineKeyboardButton(text="◀️ Retour", callback_data="workflow_menu")
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def workflow_actions_keyboard(workflow_id: int) -> InlineKeyboardMarkup:
    """Create keyboard with workflow actions."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="▶️ Exécuter",
                    callback_data=f"workflow:{workflow_id}:execute"
                )
            ],
            [
                InlineKeyboardButton(
                    text="✅ Activer",
                    callback_data=f"workflow:{workflow_id}:activate"
                ),
                InlineKeyboardButton(
                    text="⏸️ Désactiver",
                    callback_data=f"workflow:{workflow_id}:deactivate"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⚙️ Configurer",
                    callback_data=f"workflow:{workflow_id}:configure"
                ),
                InlineKeyboardButton(
                    text="🗑️ Supprimer",
                    callback_data=f"workflow:{workflow_id}:delete"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔙 Retour",
                    callback_data="workflow_list"
                )
            ]
        ]
    )

def workflow_template_keyboard(templates: List[Dict]) -> InlineKeyboardMarkup:
    """Create keyboard with workflow templates."""
    buttons = []
    for template in templates:
        buttons.append([
            InlineKeyboardButton(
                text=f"✨ {template['name']}",
                callback_data=f"template:{template['id']}"
            )
        ])
    
    buttons.append([
        InlineKeyboardButton(text="◀️ Retour", callback_data="workflow_menu")
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def back_keyboard() -> InlineKeyboardMarkup:
    """Create back button keyboard."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="◀️ Retour", callback_data="workflow_menu")
            ]
        ]
    )
