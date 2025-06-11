"""N8N client for workflow management."""
import aiohttp
import json
from typing import Dict, List, Optional
from urllib.parse import urljoin

from src.core.config import settings

class N8NClient:
    def __init__(self, base_url: str = None, api_key: str = None):
        """Initialize N8N client.
        
        Args:
            base_url: N8N instance URL (e.g., http://localhost:5678)
            api_key: N8N API key for authentication
        """
        self.base_url = base_url or settings.n8n_base_url
        self.api_key = api_key or settings.n8n_api_key
        self.session = None
    
    async def __aenter__(self):
        """Create aiohttp session on context enter."""
        self.session = aiohttp.ClientSession(
            headers={
                "X-N8N-API-KEY": self.api_key,
                "Content-Type": "application/json"
            }
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Close session on context exit."""
        if self.session:
            await self.session.close()
    
    def _url(self, path: str) -> str:
        """Build full URL for N8N API endpoint."""
        return urljoin(self.base_url, f"/api/v1/{path}")
    
    async def list_workflows(self) -> List[Dict]:
        """Get all workflows."""
        async with self.session.get(self._url("workflows")) as response:
            response.raise_for_status()
            return await response.json()
    
    async def get_workflow(self, workflow_id: str) -> Dict:
        """Get workflow by ID."""
        async with self.session.get(self._url(f"workflows/{workflow_id}")) as response:
            response.raise_for_status()
            return await response.json()
    
    async def create_workflow(self, name: str, nodes: List[Dict], connections: Dict) -> Dict:
        """Create new workflow."""
        data = {
            "name": name,
            "nodes": nodes,
            "connections": connections,
            "active": False  # Inactive by default for safety
        }
        async with self.session.post(self._url("workflows"), json=data) as response:
            response.raise_for_status()
            return await response.json()
    
    async def update_workflow(self, workflow_id: str, data: Dict) -> Dict:
        """Update existing workflow."""
        async with self.session.put(self._url(f"workflows/{workflow_id}"), json=data) as response:
            response.raise_for_status()
            return await response.json()
    
    async def delete_workflow(self, workflow_id: str) -> None:
        """Delete workflow by ID."""
        async with self.session.delete(self._url(f"workflows/{workflow_id}")) as response:
            response.raise_for_status()
    
    async def activate_workflow(self, workflow_id: str) -> Dict:
        """Activate workflow."""
        return await self.update_workflow(workflow_id, {"active": True})
    
    async def deactivate_workflow(self, workflow_id: str) -> Dict:
        """Deactivate workflow."""
        return await self.update_workflow(workflow_id, {"active": False})
    
    async def execute_workflow(self, workflow_id: str, data: Optional[Dict] = None) -> Dict:
        """Execute workflow with optional data."""
        async with self.session.post(
            self._url(f"workflows/{workflow_id}/execute"),
            json=data or {}
        ) as response:
            response.raise_for_status()
            return await response.json()
