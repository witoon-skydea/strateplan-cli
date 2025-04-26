"""
Service for generating reports
"""
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import json

from strateplan.models.strategic_plan import StrategicPlan
from strateplan.models.strategic_issue import StrategicIssue
from strateplan.models.kpi import KPI
from strateplan.models.initiative import Initiative
from strateplan.utils.formatter import format_table, format_json


class ReportService:
    """Service for generating reports"""
    
    @staticmethod
    def generate_plan_summary(plan_id: int) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Generate a summary report for a strategic plan
        
        Args:
            plan_id: ID of the strategic plan
            
        Returns:
            Tuple of (report_data, error_message)
        """
        # Get the plan
        plan = StrategicPlan.get_by_id(plan_id)
        if not plan:
            return None, f"ไม่พบแผนยุทธศาสตร์ ID: {plan_id}"
        
        # Get issues for the plan
        issues = StrategicIssue.get_by_plan_id(plan_id)
        
        # Initialize summary data
        summary = {
            "plan": plan.to_dict(),
            "issue_count": len(issues),
            "issues": [],
            "kpi_count": 0,
            "initiative_count": 0,
            "total_budget": 0.0,
        }
        
        # Process each issue and its KPIs and initiatives
        for issue in issues:
            kpis = KPI.get_by_issue_id(issue.id)
            initiatives = Initiative.get_by_issue_id(issue.id)
            
            # Calculate issue-level statistics
            issue_budget = sum(init.budget or 0 for init in initiatives)
            kpi_achieved = sum(1 for kpi in kpis if kpi.progress is not None and kpi.progress >= 100)
            kpi_progress = sum(kpi.progress or 0 for kpi in kpis if kpi.progress is not None) / len(kpis) if kpis else None
            
            # Count initiatives by status
            status_counts = {}
            for status in Initiative.VALID_STATUSES:
                status_counts[status] = sum(1 for init in initiatives if init.status == status)
            
            # Create issue summary
            issue_summary = {
                "issue": issue.to_dict(),
                "kpi_count": len(kpis),
                "kpi_achieved": kpi_achieved,
                "kpi_progress": kpi_progress,
                "initiative_count": len(initiatives),
                "initiative_status": status_counts,
                "budget": issue_budget,
            }
            
            summary["issues"].append(issue_summary)
            summary["kpi_count"] += len(kpis)
            summary["initiative_count"] += len(initiatives)
            summary["total_budget"] += issue_budget
        
        return summary, None
    
    @staticmethod
    def generate_kpi_summary(plan_id: int) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Generate a summary report of KPIs for a strategic plan
        
        Args:
            plan_id: ID of the strategic plan
            
        Returns:
            Tuple of (report_data, error_message)
        """
        # Get the plan
        plan = StrategicPlan.get_by_id(plan_id)
        if not plan:
            return None, f"ไม่พบแผนยุทธศาสตร์ ID: {plan_id}"
        
        # Get issues for the plan
        issues = StrategicIssue.get_by_plan_id(plan_id)
        
        # Initialize KPI summary
        kpi_summary = {
            "plan": plan.to_dict(),
            "kpi_count": 0,
            "kpi_achieved": 0,
            "kpi_data": [],
        }
        
        # Collect KPI data
        for issue in issues:
            kpis = KPI.get_by_issue_id(issue.id)
            
            for kpi in kpis:
                is_achieved = kpi.progress is not None and kpi.progress >= 100
                
                kpi_data = {
                    "kpi": kpi.to_dict(),
                    "issue": issue.to_dict(),
                    "progress": kpi.progress,
                    "is_achieved": is_achieved,
                }
                
                kpi_summary["kpi_data"].append(kpi_data)
                kpi_summary["kpi_count"] += 1
                if is_achieved:
                    kpi_summary["kpi_achieved"] += 1
        
        # Calculate overall progress
        if kpi_summary["kpi_count"] > 0:
            kpi_summary["achievement_rate"] = (kpi_summary["kpi_achieved"] / kpi_summary["kpi_count"]) * 100
        else:
            kpi_summary["achievement_rate"] = None
        
        return kpi_summary, None
    
    @staticmethod
    def generate_initiative_summary(plan_id: int) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Generate a summary report of initiatives for a strategic plan
        
        Args:
            plan_id: ID of the strategic plan
            
        Returns:
            Tuple of (report_data, error_message)
        """
        # Get the plan
        plan = StrategicPlan.get_by_id(plan_id)
        if not plan:
            return None, f"ไม่พบแผนยุทธศาสตร์ ID: {plan_id}"
        
        # Get issues for the plan
        issues = StrategicIssue.get_by_plan_id(plan_id)
        
        # Initialize initiative summary
        initiative_summary = {
            "plan": plan.to_dict(),
            "initiative_count": 0,
            "total_budget": 0.0,
            "status_counts": {status: 0 for status in Initiative.VALID_STATUSES},
            "initiative_data": [],
        }
        
        # Collect initiative data
        for issue in issues:
            initiatives = Initiative.get_by_issue_id(issue.id)
            
            for initiative in initiatives:
                initiative_data = {
                    "initiative": initiative.to_dict(),
                    "issue": issue.to_dict(),
                }
                
                initiative_summary["initiative_data"].append(initiative_data)
                initiative_summary["initiative_count"] += 1
                initiative_summary["status_counts"][initiative.status] += 1
                
                if initiative.budget:
                    initiative_summary["total_budget"] += initiative.budget
        
        # Calculate status distribution percentages
        if initiative_summary["initiative_count"] > 0:
            initiative_summary["status_distribution"] = {
                status: (count / initiative_summary["initiative_count"]) * 100
                for status, count in initiative_summary["status_counts"].items()
            }
        else:
            initiative_summary["status_distribution"] = {status: 0 for status in Initiative.VALID_STATUSES}
        
        return initiative_summary, None
    
    @staticmethod
    def export_plan_to_json(plan_id: int) -> Tuple[Optional[str], Optional[str]]:
        """Export a strategic plan to JSON format
        
        Args:
            plan_id: ID of the strategic plan
            
        Returns:
            Tuple of (json_data, error_message)
        """
        # Get summary data
        summary_data, error = ReportService.generate_plan_summary(plan_id)
        if error:
            return None, error
        
        # Get KPI data
        kpi_data, error = ReportService.generate_kpi_summary(plan_id)
        if error:
            return None, error
        
        # Get initiative data
        initiative_data, error = ReportService.generate_initiative_summary(plan_id)
        if error:
            return None, error
        
        # Combine data
        export_data = {
            "plan": summary_data["plan"],
            "issues": [],
            "export_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        
        # Process each issue
        for issue_summary in summary_data["issues"]:
            issue_id = issue_summary["issue"]["id"]
            issue_export = {
                "issue": issue_summary["issue"],
                "kpis": [],
                "initiatives": [],
            }
            
            # Add KPIs for this issue
            for kpi_item in kpi_data["kpi_data"]:
                if kpi_item["issue"]["id"] == issue_id:
                    issue_export["kpis"].append(kpi_item["kpi"])
            
            # Add initiatives for this issue
            for initiative_item in initiative_data["initiative_data"]:
                if initiative_item["issue"]["id"] == issue_id:
                    issue_export["initiatives"].append(initiative_item["initiative"])
            
            export_data["issues"].append(issue_export)
        
        # Convert to JSON
        json_data = json.dumps(export_data, indent=2, ensure_ascii=False)
        
        return json_data, None
