"""
KPI (Key Performance Indicator) model
"""
from typing import Dict, Any, List, Optional
from datetime import datetime

from strateplan.db import get_db


class KPI:
    """KPI model class"""

    TABLE_NAME = "kpis"

    def __init__(
        self,
        issue_id: int,
        name: str,
        description: Optional[str] = None,
        target_value: Optional[float] = None,
        current_value: Optional[float] = None,
        unit: Optional[str] = None,
        id: Optional[int] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
    ):
        """Initialize a KPI
        
        Args:
            issue_id: ID of the parent strategic issue
            name: The name of the KPI
            description: Optional description
            target_value: Target value for the KPI
            current_value: Current value of the KPI
            unit: Unit of measurement (e.g., %, days, points)
            id: Optional ID (for existing KPIs)
            created_at: Creation timestamp
            updated_at: Last update timestamp
        """
        self.id = id
        self.issue_id = issue_id
        self.name = name
        self.description = description
        self.target_value = target_value
        self.current_value = current_value
        self.unit = unit
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'KPI':
        """Create a KPI instance from a dictionary
        
        Args:
            data: Dictionary containing KPI data
            
        Returns:
            KPI instance
        """
        return cls(
            id=data.get('id'),
            issue_id=data.get('issue_id'),
            name=data.get('name'),
            description=data.get('description'),
            target_value=data.get('target_value'),
            current_value=data.get('current_value'),
            unit=data.get('unit'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at'),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary
        
        Returns:
            Dictionary representation of the KPI
        """
        return {
            'id': self.id,
            'issue_id': self.issue_id,
            'name': self.name,
            'description': self.description,
            'target_value': self.target_value,
            'current_value': self.current_value,
            'unit': self.unit,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }
        
    @property
    def progress(self) -> Optional[float]:
        """Calculate progress percentage
        
        Returns:
            Progress as a percentage or None if not calculable
        """
        if self.target_value is None or self.current_value is None:
            return None
            
        if self.target_value == 0:
            return None
            
        return (self.current_value / self.target_value) * 100

    def save(self) -> int:
        """Save the KPI to the database
        
        Returns:
            ID of the saved KPI
        """
        db = get_db()
        
        data = {
            'issue_id': self.issue_id,
            'name': self.name,
            'description': self.description,
            'target_value': self.target_value,
            'current_value': self.current_value,
            'unit': self.unit,
        }
        
        if self.id is None:
            # Insert new KPI
            self.id = db.insert(self.TABLE_NAME, data)
        else:
            # Update existing KPI
            data['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            db.update(self.TABLE_NAME, self.id, data)
            
        return self.id

    @classmethod
    def get_by_id(cls, kpi_id: int) -> Optional['KPI']:
        """Get a KPI by ID
        
        Args:
            kpi_id: ID of the KPI
            
        Returns:
            KPI instance or None if not found
        """
        db = get_db()
        result = db.fetch_one(f"SELECT * FROM {cls.TABLE_NAME} WHERE id = ?", (kpi_id,))
        
        if result:
            return cls.from_dict(result)
        return None

    @classmethod
    def get_by_issue_id(cls, issue_id: int) -> List['KPI']:
        """Get all KPIs for a strategic issue
        
        Args:
            issue_id: ID of the strategic issue
            
        Returns:
            List of KPI instances
        """
        db = get_db()
        results = db.fetch_all(
            f"SELECT * FROM {cls.TABLE_NAME} WHERE issue_id = ? ORDER BY id", 
            (issue_id,)
        )
        
        return [cls.from_dict(result) for result in results]

    def delete(self) -> bool:
        """Delete the KPI
        
        Returns:
            True if deleted successfully, False otherwise
        """
        if self.id is None:
            return False
            
        db = get_db()
        return db.delete(self.TABLE_NAME, self.id)
