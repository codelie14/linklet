"""Service for managing workflows with n8n integration."""
from typing import List, Optional, Dict
from sqlalchemy.orm import Session
import structlog

from src.core.database.models import Workflow, User
from src.integrations.n8n.client import N8NClient

logger = structlog.get_logger()

class WorkflowService:
    def __init__(self, db: Session):
        self.db = db
        
    async def list_user_workflows(self, user_id: int) -> List[Workflow]:
        """Get all workflows for a user."""
        return self.db.query(Workflow).filter(Workflow.user_id == user_id).all()
    
    async def create_workflow(
        self,
        user_id: int,
        name: str,
        description: Optional[str] = None,
        nodes: Optional[List[Dict]] = None,
        connections: Optional[Dict] = None
    ) -> Workflow:
        """Create new workflow for user."""
        try:
            # Create workflow in n8n
            async with N8NClient() as n8n:
                n8n_workflow = await n8n.create_workflow(
                    name=name,
                    nodes=nodes or [],
                    connections=connections or {}
                )
            
            # Save to database
            workflow = Workflow(
                user_id=user_id,
                name=name,
                description=description,
                n8n_workflow_id=n8n_workflow["id"],
                is_active=False
            )
            self.db.add(workflow)
            self.db.commit()
            
            logger.info(
                "Workflow created",
                workflow_id=workflow.id,
                user_id=user_id,
                n8n_workflow_id=n8n_workflow["id"]
            )
            
            return workflow
            
        except Exception as e:
            self.db.rollback()
            logger.error(
                "Failed to create workflow",
                error=str(e),
                user_id=user_id,
                name=name
            )
            raise
    
    async def activate_workflow(self, workflow_id: int, user_id: int) -> Workflow:
        """Activate workflow for user."""
        workflow = self.db.query(Workflow).filter(
            Workflow.id == workflow_id,
            Workflow.user_id == user_id
        ).first()
        
        if not workflow:
            raise ValueError("Workflow not found or access denied")
        
        try:
            async with N8NClient() as n8n:
                await n8n.activate_workflow(workflow.n8n_workflow_id)
            
            workflow.is_active = True
            self.db.commit()
            
            logger.info(
                "Workflow activated",
                workflow_id=workflow_id,
                user_id=user_id
            )
            
            return workflow
            
        except Exception as e:
            self.db.rollback()
            logger.error(
                "Failed to activate workflow",
                error=str(e),
                workflow_id=workflow_id,
                user_id=user_id
            )
            raise
    
    async def deactivate_workflow(self, workflow_id: int, user_id: int) -> Workflow:
        """Deactivate workflow for user."""
        workflow = self.db.query(Workflow).filter(
            Workflow.id == workflow_id,
            Workflow.user_id == user_id
        ).first()
        
        if not workflow:
            raise ValueError("Workflow not found or access denied")
        
        try:
            async with N8NClient() as n8n:
                await n8n.deactivate_workflow(workflow.n8n_workflow_id)
            
            workflow.is_active = False
            self.db.commit()
            
            logger.info(
                "Workflow deactivated",
                workflow_id=workflow_id,
                user_id=user_id
            )
            
            return workflow
            
        except Exception as e:
            self.db.rollback()
            logger.error(
                "Failed to deactivate workflow",
                error=str(e),
                workflow_id=workflow_id,
                user_id=user_id
            )
            raise
    
    async def execute_workflow(
        self,
        workflow_id: int,
        user_id: int,
        data: Optional[Dict] = None
    ) -> Dict:
        """Execute workflow with optional data."""
        workflow = self.db.query(Workflow).filter(
            Workflow.id == workflow_id,
            Workflow.user_id == user_id
        ).first()
        
        if not workflow:
            raise ValueError("Workflow not found or access denied")
        
        if not workflow.is_active:
            raise ValueError("Workflow is not active")
        
        try:
            async with N8NClient() as n8n:
                result = await n8n.execute_workflow(
                    workflow.n8n_workflow_id,
                    data
                )
            
            logger.info(
                "Workflow executed",
                workflow_id=workflow_id,
                user_id=user_id
            )
            
            return result
            
        except Exception as e:
            logger.error(
                "Failed to execute workflow",
                error=str(e),
                workflow_id=workflow_id,
                user_id=user_id
            )
            raise
