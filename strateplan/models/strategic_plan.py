"""
Strategic Plan model
"""
from typing import Dict, Any, List, Optional
from datetime import datetime

from strateplan.db import get_db


class StrategicPlan:
    """Strategic Plan model class"""

    TABLE_NAME = "strategic_plans"

    def __init__(
        self,
        name: str,
        description: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        id: Optional[int] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
    ):
        """Initialize a strategic plan
        
        Args:
            name: The name of the strategic plan
            description: Optional description
            start_date: Start date in ISO format (YYYY-MM-DD)
            end_date: End date in ISO format (YYYY-MM-DD)
            id: Optional ID (for existing plans)
            created_at: Creation timestamp
            updated_at: Last update timestamp
        """
        self.id = id
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StrategicPlan':
        """Create a StrategicPlan instance from a dictionary
        
        Args:
            data: Dictionary containing strategic plan data
            
        Returns:
            StrategicPlan instance
        """
        return cls(
            id=data.get('id'),
            name=data.get('name'),
            description=data.get('description'),
            start_date=data.get('start_date'),
            end_date=data.get('end_date'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at'),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary
        
        Returns:
            Dictionary representation of the strategic plan
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

    def save(self) -> int:
        """Save the strategic plan to the database
        
        Returns:
            ID of the saved plan
        """
        db = get_db()
        
        data = {
            'name': self.name,
            'description': self.description,
            'start_date': self.start_date,
            'end_date': self.end_date,
        }
        
        if self.id is None:
            # Insert new plan
            self.id = db.insert(self.TABLE_NAME, data)
        else:
            # Update existing plan
            data['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            db.update(self.TABLE_NAME, self.id, data)
            
        return self.id

    @classmethod
    def get_by_id(cls, plan_id: int) -> Optional['StrategicPlan']:
        """Get a strategic plan by ID
        
        Args:
            plan_id: ID of the strategic plan
            
        Returns:
            StrategicPlan instance or None if not found
        """
        db = get_db()
        result = db.fetch_one(f"SELECT * FROM {cls.TABLE_NAME} WHERE id = ?", (plan_id,))
        
        if result:
            return cls.from_dict(result)
        return None

    @classmethod
    def get_all(cls) -> List['StrategicPlan']:
        """Get all strategic plans
        
        Returns:
            List of StrategicPlan instances
        """
        db = get_db()
        results = db.fetch_all(f"SELECT * FROM {cls.TABLE_NAME} ORDER BY id")
        
        return [cls.from_dict(result) for result in results]

    def delete(self) -> bool:
        """Delete the strategic plan
        
        Returns:
            True if deleted successfully, False otherwise
        """
        if self.id is None:
            return False
            
        db = get_db()
        return db.delete(self.TABLE_NAME, self.id)
