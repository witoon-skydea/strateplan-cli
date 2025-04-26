"""
Service for managing Strategic Issues
"""
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

from strateplan.models.strategic_plan import StrategicPlan
from strateplan.models.strategic_issue import StrategicIssue
from strateplan.models.kpi import KPI
from strateplan.models.initiative import Initiative
from strateplan.utils.validator import validate_numeric, validate_text, validate_id_exists


class IssueService:
    """Service for managing Strategic Issues"""
    
    @staticmethod
    def create_issue(plan_id: int, name: str, description: Optional[str] = None,
                    priority: Optional[int] = None) -> Tuple[Optional[int], Optional[str]]:
        """Create a new strategic issue
        
        Args:
            plan_id: ID of the parent strategic plan
            name: Name of the issue
            description: Optional description
            priority: Optional priority (lower number = higher priority)
            
        Returns:
            Tuple of (issue_id, error_message)
        """
        # Validate plan existence
        plan_valid, plan_error = validate_id_exists(plan_id, StrategicPlan.get_by_id)
        if not plan_valid:
            return None, f"แผนยุทธศาสตร์: {plan_error}"
        
        # Validate name
        name_valid, name_error = validate_text(name, min_length=1, allow_none=False)
        if not name_valid:
            return None, f"ชื่อประเด็นยุทธศาสตร์: {name_error}"
        
        # Validate priority if provided
        if priority is not None:
            priority_valid, priority_error = validate_numeric(priority, min_value=1)
            if not priority_valid:
                return None, f"ลำดับความสำคัญ: {priority_error}"
        
        # Create issue
        issue = StrategicIssue(
            plan_id=plan_id,
            name=name,
            description=description,
            priority=priority,
        )
        
        # Save to database
        issue_id = issue.save()
        
        return issue_id, None
    
    @staticmethod
    def update_issue(issue_id: int, name: Optional[str] = None,
                    description: Optional[str] = None,
                    priority: Optional[int] = None) -> Tuple[bool, Optional[str]]:
        """Update an existing strategic issue
        
        Args:
            issue_id: ID of the issue to update
            name: New name (if provided)
            description: New description (if provided)
            priority: New priority (if provided)
            
        Returns:
            Tuple of (success, error_message)
        """
        # Get existing issue
        issue = StrategicIssue.get_by_id(issue_id)
        if not issue:
            return False, f"ไม่พบประเด็นยุทธศาสตร์ ID: {issue_id}"
        
        # Validate name if provided
        if name is not None:
            name_valid, name_error = validate_text(name, min_length=1, allow_none=False)
            if not name_valid:
                return False, f"ชื่อประเด็นยุทธศาสตร์: {name_error}"
            issue.name = name
        
        # Validate priority if provided
        if priority is not None:
            priority_valid, priority_error = validate_numeric(priority, min_value=1)
            if not priority_valid:
                return False, f"ลำดับความสำคัญ: {priority_error}"
            issue.priority = priority
        
        # Update description if provided
        if description is not None:
            issue.description = description
        
        # Save changes
        issue.save()
        
        return True, None
    
    @staticmethod
    def delete_issue(issue_id: int) -> Tuple[bool, Optional[str]]:
        """Delete a strategic issue
        
        Args:
            issue_id: ID of the issue to delete
            
        Returns:
            Tuple of (success, error_message)
        """
        # Get existing issue
        issue = StrategicIssue.get_by_id(issue_id)
        if not issue:
            return False, f"ไม่พบประเด็นยุทธศาสตร์ ID: {issue_id}"
        
        # Delete the issue (will cascade delete related KPIs and initiatives)
        success = issue.delete()
        
        if not success:
            return False, f"เกิดข้อผิดพลาดในการลบประเด็นยุทธศาสตร์ ID: {issue_id}"
        
        return True, None
    
    @staticmethod
    def get_issue_summary(issue_id: int) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Get a summary of a strategic issue
        
        Args:
            issue_id: ID of the issue
            
        Returns:
            Tuple of (summary_dict, error_message)
        """
        # Get issue
        issue = StrategicIssue.get_by_id(issue_id)
        if not issue:
            return None, f"ไม่พบประเด็นยุทธศาสตร์ ID: {issue_id}"
        
        # Get parent plan
        plan = StrategicPlan.get_by_id(issue.plan_id)
        
        # Get KPIs and initiatives
        kpis = KPI.get_by_issue_id(issue_id)
        initiatives = Initiative.get_by_issue_id(issue_id)
        
        # Calculate total budget
        total_budget = sum(init.budget or 0 for init in initiatives)
        
        # Calculate KPI progress
        kpi_summaries = []
        for kpi in kpis:
            kpi_summaries.append({
                "kpi": kpi.to_dict(),
                "progress": kpi.progress
            })
        
        # Create initiative summaries
        initiative_summaries = []
        for init in initiatives:
            initiative_summaries.append(init.to_dict())
        
        # Build summary
        summary = {
            "issue": issue.to_dict(),
            "plan": plan.to_dict() if plan else None,
            "kpis": kpi_summaries,
            "initiatives": initiative_summaries,
            "kpi_count": len(kpis),
            "initiative_count": len(initiatives),
            "total_budget": total_budget,
        }
        
        return summary, None
    
    @staticmethod
    def reorder_priorities(plan_id: int, issue_ids: List[int]) -> Tuple[bool, Optional[str]]:
        """Reorder issue priorities for a plan
        
        Args:
            plan_id: ID of the strategic plan
            issue_ids: List of issue IDs in desired priority order
            
        Returns:
            Tuple of (success, error_message)
        """
        # Validate plan existence
        plan = StrategicPlan.get_by_id(plan_id)
        if not plan:
            return False, f"ไม่พบแผนยุทธศาสตร์ ID: {plan_id}"
        
        # Get all issues for the plan
        all_issues = StrategicIssue.get_by_plan_id(plan_id)
        all_issue_ids = {issue.id for issue in all_issues}
        
        # Validate all issue IDs belong to the plan
        for issue_id in issue_ids:
            if issue_id not in all_issue_ids:
                return False, f"ประเด็นยุทธศาสตร์ ID: {issue_id} ไม่ได้อยู่ในแผนนี้"
        
        # Update priorities
        for i, issue_id in enumerate(issue_ids, 1):
            issue = StrategicIssue.get_by_id(issue_id)
            issue.priority = i
            issue.save()
        
        return True, None
