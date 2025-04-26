"""
Initiative model
"""
from typing import Dict, Any, List, Optional
from datetime import datetime

from strateplan.db import get_db


class Initiative:
    """Initiative model class"""

    TABLE_NAME = "initiatives"
    
    # Status constants
    STATUS_NOT_STARTED = "ยังไม่เริ่ม"
    STATUS_IN_PROGRESS = "กำลังดำเนินการ"
    STATUS_COMPLETED = "เสร็จสิ้น"
    STATUS_DELAYED = "ล่าช้า"
    STATUS_CANCELLED = "ยกเลิก"
    
    VALID_STATUSES = [
        STATUS_NOT_STARTED,
        STATUS_IN_PROGRESS,
        STATUS_COMPLETED,
        STATUS_DELAYED,
        STATUS_CANCELLED,
    ]

    def __init__(
        self,
        issue_id: int,
        name: str,
        description: Optional[str] = None,
        status: Optional[str] = None,
        budget: Optional[float] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        id: Optional[int] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
    ):
        """Initialize an initiative
        
        Args:
            issue_id: ID of the parent strategic issue
            name: The name of the initiative
            description: Optional description
            status: Status of the initiative
            budget: Budget allocated for the initiative
            start_date: Start date in ISO format (YYYY-MM-DD)
            end_date: End date in ISO format (YYYY-MM-DD)
            id: Optional ID (for existing initiatives)
            created_at: Creation timestamp
            updated_at: Last update timestamp
        """
        self.id = id
        self.issue_id = issue_id
        self.name = name
        self.description = description
        self.status = status or self.STATUS_NOT_STARTED
        self.budget = budget
        self.start_date = start_date
        self.end_date = end_date
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Initiative':
        """Create an Initiative instance from a dictionary
        
        Args:
            data: Dictionary containing initiative data
            
        Returns:
            Initiative instance
        """
        return cls(
            id=data.get('id'),
            issue_id=data.get('issue_id'),
            name=data.get('name'),
            description=data.get('description'),
            status=data.get('status'),
            budget=data.get('budget'),
            start_date=data.get('start_date'),
            end_date=data.get('end_date'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at'),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary
        
        Returns:
            Dictionary representation of the initiative
        """
        return {
            'id': self.id,
            'issue_id': self.issue_id,
            'name': self.name,
            'description': self.description,
            'status': self.status,
            'budget': self.budget,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

    def save(self) -> int:
        """Save the initiative to the database
        
        Returns:
            ID of the saved initiative
        """
        db = get_db()
        
        data = {
            'issue_id': self.issue_id,
            'name': self.name,
            'description': self.description,
            'status': self.status,
            'budget': self.budget,
            'start_date': self.start_date,
            'end_date': self.end_date,
        }
        
        if self.id is None:
            # Insert new initiative
            self.id = db.insert(self.TABLE_NAME, data)
        else:
            # Update existing initiative
            data['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            db.update(self.TABLE_NAME, self.id, data)
            
        return self.id

    @classmethod
    def get_by_id(cls, initiative_id: int) -> Optional['Initiative']:
        """Get an initiative by ID
        
        Args:
            initiative_id: ID of the initiative
            
        Returns:
            Initiative instance or None if not found
        """
        db = get_db()
        result = db.fetch_one(f"SELECT * FROM {cls.TABLE_NAME} WHERE id = ?", (initiative_id,))
        
        if result:
            return cls.from_dict(result)
        return None

    @classmethod
    def get_by_issue_id(cls, issue_id: int) -> List['Initiative']:
        """Get all initiatives for a strategic issue
        
        Args:
            issue_id: ID of the strategic issue
            
        Returns:
            List of Initiative instances
        """
        db = get_db()
        results = db.fetch_all(
            f"SELECT * FROM {cls.TABLE_NAME} WHERE issue_id = ? ORDER BY id", 
            (issue_id,)
        )
        
        return [cls.from_dict(result) for result in results]

    def delete(self) -> bool:
        """Delete the initiative
        
        Returns:
            True if deleted successfully, False otherwise
        """
        if self.id is None:
            return False
            
        db = get_db()
        return db.delete(self.TABLE_NAME, self.id)
