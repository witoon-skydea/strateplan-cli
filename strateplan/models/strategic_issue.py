"""
Strategic Issue model
"""
from typing import Dict, Any, List, Optional
from datetime import datetime

from strateplan.db import get_db


class StrategicIssue:
    """Strategic Issue model class"""

    TABLE_NAME = "strategic_issues"

    def __init__(
        self,
        plan_id: int,
        name: str,
        description: Optional[str] = None,
        priority: Optional[int] = None,
        id: Optional[int] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
    ):
        """Initialize a strategic issue
        
        Args:
            plan_id: ID of the parent strategic plan
            name: The name of the strategic issue
            description: Optional description
            priority: Optional priority (lower number = higher priority)
            id: Optional ID (for existing issues)
            created_at: Creation timestamp
            updated_at: Last update timestamp
        """
        self.id = id
        self.plan_id = plan_id
        self.name = name
        self.description = description
        self.priority = priority
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StrategicIssue':
        """Create a StrategicIssue instance from a dictionary
        
        Args:
            data: Dictionary containing strategic issue data
            
        Returns:
            StrategicIssue instance
        """
        return cls(
            id=data.get('id'),
            plan_id=data.get('plan_id'),
            name=data.get('name'),
            description=data.get('description'),
            priority=data.get('priority'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at'),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary
        
        Returns:
            Dictionary representation of the strategic issue
        """
        return {
            'id': self.id,
            'plan_id': self.plan_id,
            'name': self.name,
            'description': self.description,
            'priority': self.priority,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

    def save(self) -> int:
        """Save the strategic issue to the database
        
        Returns:
            ID of the saved issue
        """
        db = get_db()
        
        data = {
            'plan_id': self.plan_id,
            'name': self.name,
            'description': self.description,
            'priority': self.priority,
        }
        
        if self.id is None:
            # Insert new issue
            self.id = db.insert(self.TABLE_NAME, data)
        else:
            # Update existing issue
            data['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            db.update(self.TABLE_NAME, self.id, data)
            
        return self.id

    @classmethod
    def get_by_id(cls, issue_id: int) -> Optional['StrategicIssue']:
        """Get a strategic issue by ID
        
        Args:
            issue_id: ID of the strategic issue
            
        Returns:
            StrategicIssue instance or None if not found
        """
        db = get_db()
        result = db.fetch_one(f"SELECT * FROM {cls.TABLE_NAME} WHERE id = ?", (issue_id,))
        
        if result:
            return cls.from_dict(result)
        return None

    @classmethod
    def get_by_plan_id(cls, plan_id: int) -> List['StrategicIssue']:
        """Get all strategic issues for a plan
        
        Args:
            plan_id: ID of the strategic plan
            
        Returns:
            List of StrategicIssue instances
        """
        db = get_db()
        results = db.fetch_all(
            f"SELECT * FROM {cls.TABLE_NAME} WHERE plan_id = ? ORDER BY priority, id", 
            (plan_id,)
        )
        
        return [cls.from_dict(result) for result in results]

    def delete(self) -> bool:
        """Delete the strategic issue
        
        Returns:
            True if deleted successfully, False otherwise
        """
        if self.id is None:
            return False
            
        db = get_db()
        return db.delete(self.TABLE_NAME, self.id)
