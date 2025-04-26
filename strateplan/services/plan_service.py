"""
Service for managing Strategic Plans
"""
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

from strateplan.models.strategic_plan import StrategicPlan
from strateplan.models.strategic_issue import StrategicIssue
from strateplan.models.kpi import KPI
from strateplan.models.initiative import Initiative
from strateplan.utils.validator import validate_date, validate_date_range, validate_text


class PlanService:
    """Service for managing Strategic Plans"""
    
    @staticmethod
    def create_plan(name: str, description: Optional[str] = None,
                   start_date: Optional[str] = None, 
                   end_date: Optional[str] = None) -> Tuple[Optional[int], Optional[str]]:
        """Create a new strategic plan
        
        Args:
            name: Name of the plan
            description: Optional description
            start_date: Optional start date (YYYY-MM-DD)
            end_date: Optional end date (YYYY-MM-DD)
            
        Returns:
            Tuple of (plan_id, error_message)
        """
        # Validate name
        name_valid, name_error = validate_text(name, min_length=1, allow_none=False)
        if not name_valid:
            return None, f"ชื่อแผนยุทธศาสตร์: {name_error}"
        
        # Validate dates
        date_valid, date_error = validate_date_range(start_date, end_date)
        if not date_valid:
            return None, date_error
        
        # Create plan
        plan = StrategicPlan(
            name=name,
            description=description,
            start_date=start_date,
            end_date=end_date,
        )
        
        # Save to database
        plan_id = plan.save()
        
        return plan_id, None
    
    @staticmethod
    def update_plan(plan_id: int, name: Optional[str] = None,
                   description: Optional[str] = None,
                   start_date: Optional[str] = None, 
                   end_date: Optional[str] = None) -> Tuple[bool, Optional[str]]:
        """Update an existing strategic plan
        
        Args:
            plan_id: ID of the plan to update
            name: New name (if provided)
            description: New description (if provided)
            start_date: New start date (if provided)
            end_date: New end date (if provided)
            
        Returns:
            Tuple of (success, error_message)
        """
        # Get existing plan
        plan = StrategicPlan.get_by_id(plan_id)
        if not plan:
            return False, f"ไม่พบแผนยุทธศาสตร์ ID: {plan_id}"
        
        # Validate name if provided
        if name is not None:
            name_valid, name_error = validate_text(name, min_length=1, allow_none=False)
            if not name_valid:
                return False, f"ชื่อแผนยุทธศาสตร์: {name_error}"
            plan.name = name
        
        # Validate dates
        curr_start = plan.start_date if start_date is None else start_date
        curr_end = plan.end_date if end_date is None else end_date
        
        date_valid, date_error = validate_date_range(curr_start, curr_end)
        if not date_valid:
            return False, date_error
        
        # Update other fields
        if description is not None:
            plan.description = description
        if start_date is not None:
            plan.start_date = start_date
        if end_date is not None:
            plan.end_date = end_date
        
        # Save changes
        plan.save()
        
        return True, None
    
    @staticmethod
    def delete_plan(plan_id: int) -> Tuple[bool, Optional[str]]:
        """Delete a strategic plan
        
        Args:
            plan_id: ID of the plan to delete
            
        Returns:
            Tuple of (success, error_message)
        """
        # Get existing plan
        plan = StrategicPlan.get_by_id(plan_id)
        if not plan:
            return False, f"ไม่พบแผนยุทธศาสตร์ ID: {plan_id}"
        
        # Delete the plan (will cascade delete related issues, KPIs, initiatives)
        success = plan.delete()
        
        if not success:
            return False, f"เกิดข้อผิดพลาดในการลบแผนยุทธศาสตร์ ID: {plan_id}"
        
        return True, None
    
    @staticmethod
    def get_plan_summary(plan_id: int) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Get a summary of a strategic plan
        
        Args:
            plan_id: ID of the plan
            
        Returns:
            Tuple of (summary_dict, error_message)
        """
        # Get plan
        plan = StrategicPlan.get_by_id(plan_id)
        if not plan:
            return None, f"ไม่พบแผนยุทธศาสตร์ ID: {plan_id}"
        
        # Get issues for the plan
        issues = StrategicIssue.get_by_plan_id(plan_id)
        
        # Initialize summary
        summary = {
            "plan": plan.to_dict(),
            "issue_count": len(issues),
            "issues": [],
            "kpi_count": 0,
            "initiative_count": 0,
            "total_budget": 0.0,
        }
        
        # Process each issue
        for issue in issues:
            kpis = KPI.get_by_issue_id(issue.id)
            initiatives = Initiative.get_by_issue_id(issue.id)
            
            # Calculate issue budget
            issue_budget = sum(init.budget or 0 for init in initiatives)
            
            # Create issue summary
            issue_summary = {
                "issue": issue.to_dict(),
                "kpi_count": len(kpis),
                "initiative_count": len(initiatives),
                "budget": issue_budget,
            }
            
            summary["issues"].append(issue_summary)
            summary["kpi_count"] += len(kpis)
            summary["initiative_count"] += len(initiatives)
            summary["total_budget"] += issue_budget
        
        return summary, None
