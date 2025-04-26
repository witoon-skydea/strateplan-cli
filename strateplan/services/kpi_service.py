"""
Service for managing KPIs (Key Performance Indicators)
"""
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

from strateplan.models.strategic_issue import StrategicIssue
from strateplan.models.kpi import KPI
from strateplan.utils.validator import validate_numeric, validate_text, validate_id_exists


class KPIService:
    """Service for managing KPIs"""
    
    @staticmethod
    def create_kpi(issue_id: int, name: str, description: Optional[str] = None,
                  target_value: Optional[float] = None, current_value: Optional[float] = None,
                  unit: Optional[str] = None) -> Tuple[Optional[int], Optional[str]]:
        """Create a new KPI
        
        Args:
            issue_id: ID of the parent strategic issue
            name: Name of the KPI
            description: Optional description
            target_value: Target value for the KPI
            current_value: Current value of the KPI
            unit: Unit of measurement
            
        Returns:
            Tuple of (kpi_id, error_message)
        """
        # Validate issue existence
        issue_valid, issue_error = validate_id_exists(issue_id, StrategicIssue.get_by_id)
        if not issue_valid:
            return None, f"ประเด็นยุทธศาสตร์: {issue_error}"
        
        # Validate name
        name_valid, name_error = validate_text(name, min_length=1, allow_none=False)
        if not name_valid:
            return None, f"ชื่อตัวชี้วัด: {name_error}"
        
        # Validate target value if provided
        if target_value is not None:
            target_valid, target_error = validate_numeric(target_value)
            if not target_valid:
                return None, f"ค่าเป้าหมาย: {target_error}"
        
        # Validate current value if provided
        if current_value is not None:
            current_valid, current_error = validate_numeric(current_value)
            if not current_valid:
                return None, f"ค่าปัจจุบัน: {current_error}"
        
        # Create KPI
        kpi = KPI(
            issue_id=issue_id,
            name=name,
            description=description,
            target_value=target_value,
            current_value=current_value,
            unit=unit,
        )
        
        # Save to database
        kpi_id = kpi.save()
        
        return kpi_id, None
    
    @staticmethod
    def update_kpi(kpi_id: int, name: Optional[str] = None,
                  description: Optional[str] = None,
                  target_value: Optional[float] = None,
                  current_value: Optional[float] = None,
                  unit: Optional[str] = None) -> Tuple[bool, Optional[str]]:
        """Update an existing KPI
        
        Args:
            kpi_id: ID of the KPI to update
            name: New name (if provided)
            description: New description (if provided)
            target_value: New target value (if provided)
            current_value: New current value (if provided)
            unit: New unit (if provided)
            
        Returns:
            Tuple of (success, error_message)
        """
        # Get existing KPI
        kpi = KPI.get_by_id(kpi_id)
        if not kpi:
            return False, f"ไม่พบตัวชี้วัด ID: {kpi_id}"
        
        # Validate name if provided
        if name is not None:
            name_valid, name_error = validate_text(name, min_length=1, allow_none=False)
            if not name_valid:
                return False, f"ชื่อตัวชี้วัด: {name_error}"
            kpi.name = name
        
        # Validate target value if provided
        if target_value is not None:
            target_valid, target_error = validate_numeric(target_value)
            if not target_valid:
                return False, f"ค่าเป้าหมาย: {target_error}"
            kpi.target_value = target_value
        
        # Validate current value if provided
        if current_value is not None:
            current_valid, current_error = validate_numeric(current_value)
            if not current_valid:
                return False, f"ค่าปัจจุบัน: {current_error}"
            kpi.current_value = current_value
        
        # Update other fields if provided
        if description is not None:
            kpi.description = description
        if unit is not None:
            kpi.unit = unit
        
        # Save changes
        kpi.save()
        
        return True, None
    
    @staticmethod
    def delete_kpi(kpi_id: int) -> Tuple[bool, Optional[str]]:
        """Delete a KPI
        
        Args:
            kpi_id: ID of the KPI to delete
            
        Returns:
            Tuple of (success, error_message)
        """
        # Get existing KPI
        kpi = KPI.get_by_id(kpi_id)
        if not kpi:
            return False, f"ไม่พบตัวชี้วัด ID: {kpi_id}"
        
        # Delete the KPI
        success = kpi.delete()
        
        if not success:
            return False, f"เกิดข้อผิดพลาดในการลบตัวชี้วัด ID: {kpi_id}"
        
        return True, None
    
    @staticmethod
    def update_progress(kpi_id: int, current_value: float) -> Tuple[bool, Optional[str]]:
        """Update the current value of a KPI
        
        Args:
            kpi_id: ID of the KPI
            current_value: New current value
            
        Returns:
            Tuple of (success, error_message)
        """
        # Get existing KPI
        kpi = KPI.get_by_id(kpi_id)
        if not kpi:
            return False, f"ไม่พบตัวชี้วัด ID: {kpi_id}"
        
        # Validate current value
        current_valid, current_error = validate_numeric(current_value)
        if not current_valid:
            return False, f"ค่าปัจจุบัน: {current_error}"
        
        # Update current value
        kpi.current_value = current_value
        kpi.save()
        
        return True, None
    
    @staticmethod
    def get_kpi_progress(kpi_id: int) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Get the progress of a KPI
        
        Args:
            kpi_id: ID of the KPI
            
        Returns:
            Tuple of (progress_dict, error_message)
        """
        # Get KPI
        kpi = KPI.get_by_id(kpi_id)
        if not kpi:
            return None, f"ไม่พบตัวชี้วัด ID: {kpi_id}"
        
        # Calculate progress
        progress = kpi.progress
        
        # Get parent issue
        issue = StrategicIssue.get_by_id(kpi.issue_id)
        
        # Build result
        result = {
            "kpi": kpi.to_dict(),
            "issue": issue.to_dict() if issue else None,
            "progress": progress,
            "is_achieved": progress >= 100 if progress is not None else False,
        }
        
        return result, None
