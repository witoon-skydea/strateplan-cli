"""
Service for managing Initiatives
"""
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

from strateplan.models.strategic_issue import StrategicIssue
from strateplan.models.initiative import Initiative
from strateplan.utils.validator import (
    validate_numeric, validate_text, validate_id_exists,
    validate_date, validate_date_range, validate_in_list
)


class InitiativeService:
    """Service for managing Initiatives"""
    
    @staticmethod
    def create_initiative(issue_id: int, name: str, description: Optional[str] = None,
                         status: Optional[str] = None, budget: Optional[float] = None,
                         start_date: Optional[str] = None, 
                         end_date: Optional[str] = None) -> Tuple[Optional[int], Optional[str]]:
        """Create a new initiative
        
        Args:
            issue_id: ID of the parent strategic issue
            name: Name of the initiative
            description: Optional description
            status: Status of the initiative
            budget: Budget allocated for the initiative
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            
        Returns:
            Tuple of (initiative_id, error_message)
        """
        # Validate issue existence
        issue_valid, issue_error = validate_id_exists(issue_id, StrategicIssue.get_by_id)
        if not issue_valid:
            return None, f"ประเด็นยุทธศาสตร์: {issue_error}"
        
        # Validate name
        name_valid, name_error = validate_text(name, min_length=1, allow_none=False)
        if not name_valid:
            return None, f"ชื่อโครงการ: {name_error}"
        
        # Validate status if provided
        if status is not None:
            status_valid, status_error = validate_in_list(status, Initiative.VALID_STATUSES)
            if not status_valid:
                return None, f"สถานะ: {status_error}"
        else:
            status = Initiative.STATUS_NOT_STARTED
        
        # Validate budget if provided
        if budget is not None:
            budget_valid, budget_error = validate_numeric(budget, min_value=0)
            if not budget_valid:
                return None, f"งบประมาณ: {budget_error}"
        
        # Validate dates
        date_valid, date_error = validate_date_range(start_date, end_date)
        if not date_valid:
            return None, date_error
        
        # Create initiative
        initiative = Initiative(
            issue_id=issue_id,
            name=name,
            description=description,
            status=status,
            budget=budget,
            start_date=start_date,
            end_date=end_date,
        )
        
        # Save to database
        initiative_id = initiative.save()
        
        return initiative_id, None
    
    @staticmethod
    def update_initiative(initiative_id: int, name: Optional[str] = None,
                         description: Optional[str] = None,
                         status: Optional[str] = None, 
                         budget: Optional[float] = None,
                         start_date: Optional[str] = None, 
                         end_date: Optional[str] = None) -> Tuple[bool, Optional[str]]:
        """Update an existing initiative
        
        Args:
            initiative_id: ID of the initiative to update
            name: New name (if provided)
            description: New description (if provided)
            status: New status (if provided)
            budget: New budget (if provided)
            start_date: New start date (if provided)
            end_date: New end date (if provided)
            
        Returns:
            Tuple of (success, error_message)
        """
        # Get existing initiative
        initiative = Initiative.get_by_id(initiative_id)
        if not initiative:
            return False, f"ไม่พบโครงการ ID: {initiative_id}"
        
        # Validate name if provided
        if name is not None:
            name_valid, name_error = validate_text(name, min_length=1, allow_none=False)
            if not name_valid:
                return False, f"ชื่อโครงการ: {name_error}"
            initiative.name = name
        
        # Validate status if provided
        if status is not None:
            status_valid, status_error = validate_in_list(status, Initiative.VALID_STATUSES)
            if not status_valid:
                return False, f"สถานะ: {status_error}"
            initiative.status = status
        
        # Validate budget if provided
        if budget is not None:
            budget_valid, budget_error = validate_numeric(budget, min_value=0)
            if not budget_valid:
                return False, f"งบประมาณ: {budget_error}"
            initiative.budget = budget
        
        # Validate dates
        curr_start = initiative.start_date if start_date is None else start_date
        curr_end = initiative.end_date if end_date is None else end_date
        
        date_valid, date_error = validate_date_range(curr_start, curr_end)
        if not date_valid:
            return False, date_error
        
        # Update date fields if provided
        if start_date is not None:
            initiative.start_date = start_date
        if end_date is not None:
            initiative.end_date = end_date
        
        # Update description if provided
        if description is not None:
            initiative.description = description
        
        # Save changes
        initiative.save()
        
        return True, None
    
    @staticmethod
    def delete_initiative(initiative_id: int) -> Tuple[bool, Optional[str]]:
        """Delete an initiative
        
        Args:
            initiative_id: ID of the initiative to delete
            
        Returns:
            Tuple of (success, error_message)
        """
        # Get existing initiative
        initiative = Initiative.get_by_id(initiative_id)
        if not initiative:
            return False, f"ไม่พบโครงการ ID: {initiative_id}"
        
        # Delete the initiative
        success = initiative.delete()
        
        if not success:
            return False, f"เกิดข้อผิดพลาดในการลบโครงการ ID: {initiative_id}"
        
        return True, None
    
    @staticmethod
    def update_status(initiative_id: int, status: str) -> Tuple[bool, Optional[str]]:
        """Update the status of an initiative
        
        Args:
            initiative_id: ID of the initiative
            status: New status
            
        Returns:
            Tuple of (success, error_message)
        """
        # Get existing initiative
        initiative = Initiative.get_by_id(initiative_id)
        if not initiative:
            return False, f"ไม่พบโครงการ ID: {initiative_id}"
        
        # Validate status
        status_valid, status_error = validate_in_list(status, Initiative.VALID_STATUSES)
        if not status_valid:
            return False, f"สถานะ: {status_error}"
        
        # Update status
        initiative.status = status
        initiative.save()
        
        return True, None
    
    @staticmethod
    def get_initiatives_by_status(status: str) -> List[Initiative]:
        """Get all initiatives with a specific status
        
        Args:
            status: Status to filter by
            
        Returns:
            List of Initiative instances
        """
        from strateplan.db import get_db
        
        db = get_db()
        results = db.fetch_all(
            f"SELECT * FROM {Initiative.TABLE_NAME} WHERE status = ? ORDER BY id", 
            (status,)
        )
        
        return [Initiative.from_dict(result) for result in results]
    
    @staticmethod
    def get_initiative_summary(initiative_id: int) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Get a summary of an initiative
        
        Args:
            initiative_id: ID of the initiative
            
        Returns:
            Tuple of (summary_dict, error_message)
        """
        # Get initiative
        initiative = Initiative.get_by_id(initiative_id)
        if not initiative:
            return None, f"ไม่พบโครงการ ID: {initiative_id}"
        
        # Get parent issue
        issue = StrategicIssue.get_by_id(initiative.issue_id)
        
        # Build summary
        summary = {
            "initiative": initiative.to_dict(),
            "issue": issue.to_dict() if issue else None,
        }
        
        return summary, None
