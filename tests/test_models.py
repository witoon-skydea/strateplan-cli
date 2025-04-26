"""
Tests for the model classes
"""
import os
import pytest
import tempfile
from datetime import datetime

from strateplan.db import Database
from strateplan.models.strategic_plan import StrategicPlan
from strateplan.models.strategic_issue import StrategicIssue
from strateplan.models.kpi import KPI
from strateplan.models.initiative import Initiative


@pytest.fixture
def temp_db():
    """Fixture to create a temporary database for testing"""
    fd, path = tempfile.mkstemp(suffix=".db")
    # Override the singleton database instance to use our test database
    import strateplan.db
    strateplan.db._db_instance = Database(path)
    strateplan.db._db_instance.connect()
    strateplan.db._db_instance.initialize_db()
    
    yield strateplan.db._db_instance
    
    # Clean up
    strateplan.db._db_instance.close()
    os.close(fd)
    os.unlink(path)
    strateplan.db._db_instance = None


class TestStrategicPlan:
    """Test suite for the StrategicPlan model"""
    
    def test_create(self, temp_db):
        """Test creating a strategic plan"""
        plan = StrategicPlan(
            name="Test Plan",
            description="Test Description",
            start_date="2025-01-01",
            end_date="2025-12-31",
        )
        
        plan_id = plan.save()
        
        assert plan_id is not None
        assert plan_id > 0
        assert plan.id == plan_id
    
    def test_from_dict(self):
        """Test creating a strategic plan from a dictionary"""
        data = {
            "id": 1,
            "name": "Test Plan",
            "description": "Test Description",
            "start_date": "2025-01-01",
            "end_date": "2025-12-31",
            "created_at": "2024-01-01 12:00:00",
            "updated_at": "2024-01-01 12:00:00",
        }
        
        plan = StrategicPlan.from_dict(data)
        
        assert plan.id == 1
        assert plan.name == "Test Plan"
        assert plan.description == "Test Description"
        assert plan.start_date == "2025-01-01"
        assert plan.end_date == "2025-12-31"
        assert plan.created_at == "2024-01-01 12:00:00"
        assert plan.updated_at == "2024-01-01 12:00:00"
    
    def test_to_dict(self):
        """Test converting a strategic plan to a dictionary"""
        plan = StrategicPlan(
            id=1,
            name="Test Plan",
            description="Test Description",
            start_date="2025-01-01",
            end_date="2025-12-31",
            created_at="2024-01-01 12:00:00",
            updated_at="2024-01-01 12:00:00",
        )
        
        data = plan.to_dict()
        
        assert data["id"] == 1
        assert data["name"] == "Test Plan"
        assert data["description"] == "Test Description"
        assert data["start_date"] == "2025-01-01"
        assert data["end_date"] == "2025-12-31"
        assert data["created_at"] == "2024-01-01 12:00:00"
        assert data["updated_at"] == "2024-01-01 12:00:00"
    
    def test_get_by_id(self, temp_db):
        """Test getting a strategic plan by ID"""
        # Create a plan
        plan = StrategicPlan(
            name="Test Plan",
            description="Test Description",
        )
        plan_id = plan.save()
        
        # Get the plan by ID
        retrieved_plan = StrategicPlan.get_by_id(plan_id)
        
        assert retrieved_plan is not None
        assert retrieved_plan.id == plan_id
        assert retrieved_plan.name == "Test Plan"
        assert retrieved_plan.description == "Test Description"
        
        # Test getting a non-existent plan
        retrieved_plan = StrategicPlan.get_by_id(999)
        assert retrieved_plan is None
    
    def test_get_all(self, temp_db):
        """Test getting all strategic plans"""
        # Create some plans
        plan1 = StrategicPlan(name="Plan 1")
        plan1.save()
        
        plan2 = StrategicPlan(name="Plan 2")
        plan2.save()
        
        # Get all plans
        plans = StrategicPlan.get_all()
        
        assert len(plans) == 2
        assert plans[0].name == "Plan 1"
        assert plans[1].name == "Plan 2"
    
    def test_update(self, temp_db):
        """Test updating a strategic plan"""
        # Create a plan
        plan = StrategicPlan(
            name="Original Name",
            description="Original Description",
        )
        plan_id = plan.save()
        
        # Update the plan
        plan.name = "Updated Name"
        plan.description = "Updated Description"
        plan.save()
        
        # Get the updated plan
        updated_plan = StrategicPlan.get_by_id(plan_id)
        
        assert updated_plan is not None
        assert updated_plan.name == "Updated Name"
        assert updated_plan.description == "Updated Description"
    
    def test_delete(self, temp_db):
        """Test deleting a strategic plan"""
        # Create a plan
        plan = StrategicPlan(name="Test Plan")
        plan_id = plan.save()
        
        # Delete the plan
        success = plan.delete()
        
        assert success is True
        
        # Verify deletion
        deleted_plan = StrategicPlan.get_by_id(plan_id)
        assert deleted_plan is None


class TestStrategicIssue:
    """Test suite for the StrategicIssue model"""
    
    @pytest.fixture
    def test_plan(self, temp_db):
        """Fixture to create a test plan"""
        plan = StrategicPlan(name="Test Plan")
        plan_id = plan.save()
        
        yield plan_id
    
    def test_create(self, temp_db, test_plan):
        """Test creating a strategic issue"""
        issue = StrategicIssue(
            plan_id=test_plan,
            name="Test Issue",
            description="Test Description",
            priority=1,
        )
        
        issue_id = issue.save()
        
        assert issue_id is not None
        assert issue_id > 0
        assert issue.id == issue_id
    
    def test_get_by_id(self, temp_db, test_plan):
        """Test getting a strategic issue by ID"""
        # Create an issue
        issue = StrategicIssue(
            plan_id=test_plan,
            name="Test Issue",
            description="Test Description",
            priority=1,
        )
        issue_id = issue.save()
        
        # Get the issue by ID
        retrieved_issue = StrategicIssue.get_by_id(issue_id)
        
        assert retrieved_issue is not None
        assert retrieved_issue.id == issue_id
        assert retrieved_issue.plan_id == test_plan
        assert retrieved_issue.name == "Test Issue"
        assert retrieved_issue.description == "Test Description"
        assert retrieved_issue.priority == 1
        
        # Test getting a non-existent issue
        retrieved_issue = StrategicIssue.get_by_id(999)
        assert retrieved_issue is None
    
    def test_get_by_plan_id(self, temp_db, test_plan):
        """Test getting all strategic issues for a plan"""
        # Create some issues
        issue1 = StrategicIssue(plan_id=test_plan, name="Issue 1", priority=2)
        issue1.save()
        
        issue2 = StrategicIssue(plan_id=test_plan, name="Issue 2", priority=1)
        issue2.save()
        
        # Get issues for the plan
        issues = StrategicIssue.get_by_plan_id(test_plan)
        
        assert len(issues) == 2
        # Should be ordered by priority
        assert issues[0].name == "Issue 2"  # Priority 1
        assert issues[1].name == "Issue 1"  # Priority 2
    
    def test_delete(self, temp_db, test_plan):
        """Test deleting a strategic issue"""
        # Create an issue
        issue = StrategicIssue(plan_id=test_plan, name="Test Issue")
        issue_id = issue.save()
        
        # Delete the issue
        success = issue.delete()
        
        assert success is True
        
        # Verify deletion
        deleted_issue = StrategicIssue.get_by_id(issue_id)
        assert deleted_issue is None


class TestKPI:
    """Test suite for the KPI model"""
    
    @pytest.fixture
    def test_issue(self, temp_db):
        """Fixture to create a test plan and issue"""
        plan = StrategicPlan(name="Test Plan")
        plan_id = plan.save()
        
        issue = StrategicIssue(plan_id=plan_id, name="Test Issue")
        issue_id = issue.save()
        
        yield issue_id
    
    def test_create(self, temp_db, test_issue):
        """Test creating a KPI"""
        kpi = KPI(
            issue_id=test_issue,
            name="Test KPI",
            description="Test Description",
            target_value=100.0,
            current_value=75.0,
            unit="%",
        )
        
        kpi_id = kpi.save()
        
        assert kpi_id is not None
        assert kpi_id > 0
        assert kpi.id == kpi_id
    
    def test_progress(self, temp_db, test_issue):
        """Test calculating progress"""
        # Test with values
        kpi = KPI(
            issue_id=test_issue,
            name="Test KPI",
            target_value=100.0,
            current_value=75.0,
        )
        
        assert kpi.progress == 75.0
        
        # Test with target 0
        kpi = KPI(
            issue_id=test_issue,
            name="Test KPI",
            target_value=0.0,
            current_value=75.0,
        )
        
        assert kpi.progress is None
        
        # Test with missing values
        kpi = KPI(
            issue_id=test_issue,
            name="Test KPI",
        )
        
        assert kpi.progress is None
    
    def test_get_by_issue_id(self, temp_db, test_issue):
        """Test getting all KPIs for an issue"""
        # Create some KPIs
        kpi1 = KPI(issue_id=test_issue, name="KPI 1", target_value=100.0)
        kpi1.save()
        
        kpi2 = KPI(issue_id=test_issue, name="KPI 2", target_value=200.0)
        kpi2.save()
        
        # Get KPIs for the issue
        kpis = KPI.get_by_issue_id(test_issue)
        
        assert len(kpis) == 2
        assert kpis[0].name == "KPI 1"
        assert kpis[1].name == "KPI 2"


class TestInitiative:
    """Test suite for the Initiative model"""
    
    @pytest.fixture
    def test_issue(self, temp_db):
        """Fixture to create a test plan and issue"""
        plan = StrategicPlan(name="Test Plan")
        plan_id = plan.save()
        
        issue = StrategicIssue(plan_id=plan_id, name="Test Issue")
        issue_id = issue.save()
        
        yield issue_id
    
    def test_create(self, temp_db, test_issue):
        """Test creating an initiative"""
        initiative = Initiative(
            issue_id=test_issue,
            name="Test Initiative",
            description="Test Description",
            status=Initiative.STATUS_IN_PROGRESS,
            budget=1000000.0,
            start_date="2025-01-01",
            end_date="2025-12-31",
        )
        
        initiative_id = initiative.save()
        
        assert initiative_id is not None
        assert initiative_id > 0
        assert initiative.id == initiative_id
    
    def test_default_status(self, test_issue):
        """Test default status for new initiatives"""
        initiative = Initiative(
            issue_id=test_issue,
            name="Test Initiative",
        )
        
        assert initiative.status == Initiative.STATUS_NOT_STARTED
    
    def test_get_by_issue_id(self, temp_db, test_issue):
        """Test getting all initiatives for an issue"""
        # Create some initiatives
        initiative1 = Initiative(issue_id=test_issue, name="Initiative 1")
        initiative1.save()
        
        initiative2 = Initiative(issue_id=test_issue, name="Initiative 2")
        initiative2.save()
        
        # Get initiatives for the issue
        initiatives = Initiative.get_by_issue_id(test_issue)
        
        assert len(initiatives) == 2
        assert initiatives[0].name == "Initiative 1"
        assert initiatives[1].name == "Initiative 2"
