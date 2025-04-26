"""
Command Line Interface for Strategic Plan CLI
"""
import os
import sys
import click
from datetime import datetime
from tabulate import tabulate

from strateplan.models.strategic_plan import StrategicPlan
from strateplan.models.strategic_issue import StrategicIssue
from strateplan.models.kpi import KPI
from strateplan.models.initiative import Initiative


# Group for strateplan commands
@click.group()
def main():
    """เครื่องมือจัดการแผนยุทธศาสตร์ ประเด็นยุทธศาสตร์ ตัวชี้วัด และโครงการ"""
    pass


# Group for plan commands
@main.group()
def plan():
    """จัดการแผนยุทธศาสตร์ (Strategic Plans)"""
    pass


@plan.command("create")
@click.argument("name")
@click.option("--desc", "--description", help="คำอธิบายแผนยุทธศาสตร์")
@click.option("--start-date", help="วันที่เริ่มต้น (รูปแบบ YYYY-MM-DD)")
@click.option("--end-date", help="วันที่สิ้นสุด (รูปแบบ YYYY-MM-DD)")
def plan_create(name, desc, start_date, end_date):
    """สร้างแผนยุทธศาสตร์ใหม่"""
    # Validate dates if provided
    for date_str, date_name in [(start_date, "วันที่เริ่มต้น"), (end_date, "วันที่สิ้นสุด")]:
        if date_str:
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                click.echo(f"รูปแบบ{date_name}ไม่ถูกต้อง กรุณาใช้รูปแบบ YYYY-MM-DD")
                return

    # Create and save the plan
    plan = StrategicPlan(
        name=name,
        description=desc,
        start_date=start_date,
        end_date=end_date,
    )
    plan_id = plan.save()
    
    click.echo(f"สร้างแผนยุทธศาสตร์ '{name}' เรียบร้อยแล้ว (ID: {plan_id})")


@plan.command("list")
def plan_list():
    """แสดงรายการแผนยุทธศาสตร์ทั้งหมด"""
    plans = StrategicPlan.get_all()
    
    if not plans:
        click.echo("ไม่พบแผนยุทธศาสตร์")
        return
    
    # Prepare data for table
    headers = ["ID", "ชื่อแผน", "คำอธิบาย", "วันที่เริ่มต้น", "วันที่สิ้นสุด"]
    data = [
        [
            plan.id,
            plan.name,
            (plan.description[:30] + "...") if plan.description and len(plan.description) > 30 else plan.description,
            plan.start_date,
            plan.end_date,
        ]
        for plan in plans
    ]
    
    click.echo(tabulate(data, headers=headers, tablefmt="grid"))


@plan.command("show")
@click.argument("plan_id", type=int)
def plan_show(plan_id):
    """แสดงรายละเอียดของแผนยุทธศาสตร์"""
    plan = StrategicPlan.get_by_id(plan_id)
    
    if not plan:
        click.echo(f"ไม่พบแผนยุทธศาสตร์ ID: {plan_id}")
        return
    
    # Display plan details
    click.echo(f"แผนยุทธศาสตร์ ID: {plan.id}")
    click.echo(f"ชื่อแผน: {plan.name}")
    if plan.description:
        click.echo(f"คำอธิบาย: {plan.description}")
    if plan.start_date:
        click.echo(f"วันที่เริ่มต้น: {plan.start_date}")
    if plan.end_date:
        click.echo(f"วันที่สิ้นสุด: {plan.end_date}")
    
    # Get and display strategic issues
    issues = StrategicIssue.get_by_plan_id(plan_id)
    
    if issues:
        click.echo("\nประเด็นยุทธศาสตร์:")
        
        headers = ["ID", "ชื่อประเด็น", "ความสำคัญ"]
        data = [
            [
                issue.id,
                issue.name,
                issue.priority if issue.priority is not None else "-",
            ]
            for issue in issues
        ]
        
        click.echo(tabulate(data, headers=headers, tablefmt="simple"))
    else:
        click.echo("\nยังไม่มีประเด็นยุทธศาสตร์")


@plan.command("update")
@click.argument("plan_id", type=int)
@click.option("--name", help="ชื่อแผนยุทธศาสตร์")
@click.option("--desc", "--description", help="คำอธิบายแผนยุทธศาสตร์")
@click.option("--start-date", help="วันที่เริ่มต้น (รูปแบบ YYYY-MM-DD)")
@click.option("--end-date", help="วันที่สิ้นสุด (รูปแบบ YYYY-MM-DD)")
def plan_update(plan_id, name, desc, start_date, end_date):
    """ปรับปรุงข้อมูลแผนยุทธศาสตร์"""
    plan = StrategicPlan.get_by_id(plan_id)
    
    if not plan:
        click.echo(f"ไม่พบแผนยุทธศาสตร์ ID: {plan_id}")
        return
    
    # Validate dates if provided
    for date_str, date_name in [(start_date, "วันที่เริ่มต้น"), (end_date, "วันที่สิ้นสุด")]:
        if date_str:
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                click.echo(f"รูปแบบ{date_name}ไม่ถูกต้อง กรุณาใช้รูปแบบ YYYY-MM-DD")
                return
    
    # Update fields if provided
    if name:
        plan.name = name
    if desc is not None:  # Allow empty description
        plan.description = desc
    if start_date:
        plan.start_date = start_date
    if end_date:
        plan.end_date = end_date
    
    # Save changes
    plan.save()
    
    click.echo(f"ปรับปรุงข้อมูลแผนยุทธศาสตร์ ID: {plan_id} เรียบร้อยแล้ว")


@plan.command("delete")
@click.argument("plan_id", type=int)
@click.option("--force", is_flag=True, help="ยืนยันการลบโดยไม่ถามคำถาม")
def plan_delete(plan_id, force):
    """ลบแผนยุทธศาสตร์"""
    plan = StrategicPlan.get_by_id(plan_id)
    
    if not plan:
        click.echo(f"ไม่พบแผนยุทธศาสตร์ ID: {plan_id}")
        return
    
    # Confirm deletion
    if not force and not click.confirm(f"คุณต้องการลบแผนยุทธศาสตร์ '{plan.name}' ใช่หรือไม่? (การลบจะลบประเด็นยุทธศาสตร์ ตัวชี้วัด และโครงการที่เกี่ยวข้องทั้งหมด)"):
        click.echo("ยกเลิกการลบ")
        return
    
    # Delete the plan
    success = plan.delete()
    
    if success:
        click.echo(f"ลบแผนยุทธศาสตร์ ID: {plan_id} เรียบร้อยแล้ว")
    else:
        click.echo(f"เกิดข้อผิดพลาดในการลบแผนยุทธศาสตร์ ID: {plan_id}")


# Group for issue commands
@main.group()
def issue():
    """จัดการประเด็นยุทธศาสตร์ (Strategic Issues)"""
    pass


@issue.command("create")
@click.argument("plan_id", type=int)
@click.argument("name")
@click.option("--desc", "--description", help="คำอธิบายประเด็นยุทธศาสตร์")
@click.option("--priority", type=int, help="ลำดับความสำคัญ (ตัวเลขน้อย = สำคัญมาก)")
def issue_create(plan_id, name, desc, priority):
    """สร้างประเด็นยุทธศาสตร์ใหม่"""
    # Check if plan exists
    plan = StrategicPlan.get_by_id(plan_id)
    if not plan:
        click.echo(f"ไม่พบแผนยุทธศาสตร์ ID: {plan_id}")
        return
    
    # Create and save the issue
    issue = StrategicIssue(
        plan_id=plan_id,
        name=name,
        description=desc,
        priority=priority,
    )
    issue_id = issue.save()
    
    click.echo(f"สร้างประเด็นยุทธศาสตร์ '{name}' ภายใต้แผน '{plan.name}' เรียบร้อยแล้ว (ID: {issue_id})")


@issue.command("list")
@click.argument("plan_id", type=int)
def issue_list(plan_id):
    """แสดงรายการประเด็นยุทธศาสตร์ทั้งหมดของแผน"""
    # Check if plan exists
    plan = StrategicPlan.get_by_id(plan_id)
    if not plan:
        click.echo(f"ไม่พบแผนยุทธศาสตร์ ID: {plan_id}")
        return
    
    issues = StrategicIssue.get_by_plan_id(plan_id)
    
    if not issues:
        click.echo(f"ไม่พบประเด็นยุทธศาสตร์ภายใต้แผน '{plan.name}'")
        return
    
    # Prepare data for table
    headers = ["ID", "ชื่อประเด็น", "คำอธิบาย", "ความสำคัญ"]
    data = [
        [
            issue.id,
            issue.name,
            (issue.description[:30] + "...") if issue.description and len(issue.description) > 30 else issue.description,
            issue.priority if issue.priority is not None else "-",
        ]
        for issue in issues
    ]
    
    click.echo(f"ประเด็นยุทธศาสตร์ภายใต้แผน '{plan.name}':")
    click.echo(tabulate(data, headers=headers, tablefmt="grid"))


@issue.command("show")
@click.argument("issue_id", type=int)
def issue_show(issue_id):
    """แสดงรายละเอียดของประเด็นยุทธศาสตร์"""
    issue = StrategicIssue.get_by_id(issue_id)
    
    if not issue:
        click.echo(f"ไม่พบประเด็นยุทธศาสตร์ ID: {issue_id}")
        return
    
    # Get parent plan
    plan = StrategicPlan.get_by_id(issue.plan_id)
    
    # Display issue details
    click.echo(f"ประเด็นยุทธศาสตร์ ID: {issue.id}")
    click.echo(f"ชื่อประเด็น: {issue.name}")
    if issue.description:
        click.echo(f"คำอธิบาย: {issue.description}")
    if issue.priority is not None:
        click.echo(f"ลำดับความสำคัญ: {issue.priority}")
    click.echo(f"ภายใต้แผนยุทธศาสตร์: {plan.name if plan else 'ไม่ทราบ'}")
    
    # Get and display KPIs
    kpis = KPI.get_by_issue_id(issue_id)
    
    if kpis:
        click.echo("\nตัวชี้วัด (KPIs):")
        
        headers = ["ID", "ชื่อตัวชี้วัด", "เป้าหมาย", "ค่าปัจจุบัน", "หน่วย", "ความคืบหน้า"]
        data = [
            [
                kpi.id,
                kpi.name,
                kpi.target_value,
                kpi.current_value,
                kpi.unit,
                f"{kpi.progress:.2f}%" if kpi.progress is not None else "-",
            ]
            for kpi in kpis
        ]
        
        click.echo(tabulate(data, headers=headers, tablefmt="simple"))
    else:
        click.echo("\nยังไม่มีตัวชี้วัด")
    
    # Get and display initiatives
    initiatives = Initiative.get_by_issue_id(issue_id)
    
    if initiatives:
        click.echo("\nโครงการ/กิจกรรม:")
        
        headers = ["ID", "ชื่อโครงการ", "สถานะ", "งบประมาณ", "วันเริ่มต้น", "วันสิ้นสุด"]
        data = [
            [
                init.id,
                init.name,
                init.status,
                f"{init.budget:,.2f}" if init.budget is not None else "-",
                init.start_date,
                init.end_date,
            ]
            for init in initiatives
        ]
        
        click.echo(tabulate(data, headers=headers, tablefmt="simple"))
    else:
        click.echo("\nยังไม่มีโครงการ/กิจกรรม")


@issue.command("update")
@click.argument("issue_id", type=int)
@click.option("--name", help="ชื่อประเด็นยุทธศาสตร์")
@click.option("--desc", "--description", help="คำอธิบายประเด็นยุทธศาสตร์")
@click.option("--priority", type=int, help="ลำดับความสำคัญ")
def issue_update(issue_id, name, desc, priority):
    """ปรับปรุงข้อมูลประเด็นยุทธศาสตร์"""
    issue = StrategicIssue.get_by_id(issue_id)
    
    if not issue:
        click.echo(f"ไม่พบประเด็นยุทธศาสตร์ ID: {issue_id}")
        return
    
    # Update fields if provided
    if name:
        issue.name = name
    if desc is not None:  # Allow empty description
        issue.description = desc
    if priority is not None:
        issue.priority = priority
    
    # Save changes
    issue.save()
    
    click.echo(f"ปรับปรุงข้อมูลประเด็นยุทธศาสตร์ ID: {issue_id} เรียบร้อยแล้ว")


@issue.command("delete")
@click.argument("issue_id", type=int)
@click.option("--force", is_flag=True, help="ยืนยันการลบโดยไม่ถามคำถาม")
def issue_delete(issue_id, force):
    """ลบประเด็นยุทธศาสตร์"""
    issue = StrategicIssue.get_by_id(issue_id)
    
    if not issue:
        click.echo(f"ไม่พบประเด็นยุทธศาสตร์ ID: {issue_id}")
        return
    
    # Confirm deletion
    if not force and not click.confirm(f"คุณต้องการลบประเด็นยุทธศาสตร์ '{issue.name}' ใช่หรือไม่? (การลบจะลบตัวชี้วัดและโครงการที่เกี่ยวข้องทั้งหมด)"):
        click.echo("ยกเลิกการลบ")
        return
    
    # Delete the issue
    success = issue.delete()
    
    if success:
        click.echo(f"ลบประเด็นยุทธศาสตร์ ID: {issue_id} เรียบร้อยแล้ว")
    else:
        click.echo(f"เกิดข้อผิดพลาดในการลบประเด็นยุทธศาสตร์ ID: {issue_id}")


# Group for KPI commands
@main.group()
def kpi():
    """จัดการตัวชี้วัด (KPIs)"""
    pass


@kpi.command("create")
@click.argument("issue_id", type=int)
@click.argument("name")
@click.option("--desc", "--description", help="คำอธิบายตัวชี้วัด")
@click.option("--target", type=float, help="ค่าเป้าหมาย")
@click.option("--current", type=float, help="ค่าปัจจุบัน")
@click.option("--unit", help="หน่วยวัด (เช่น %, คน, บาท)")
def kpi_create(issue_id, name, desc, target, current, unit):
    """สร้างตัวชี้วัดใหม่"""
    # Check if issue exists
    issue = StrategicIssue.get_by_id(issue_id)
    if not issue:
        click.echo(f"ไม่พบประเด็นยุทธศาสตร์ ID: {issue_id}")
        return
    
    # Create and save the KPI
    kpi = KPI(
        issue_id=issue_id,
        name=name,
        description=desc,
        target_value=target,
        current_value=current,
        unit=unit,
    )
    kpi_id = kpi.save()
    
    click.echo(f"สร้างตัวชี้วัด '{name}' ภายใต้ประเด็น '{issue.name}' เรียบร้อยแล้ว (ID: {kpi_id})")


@kpi.command("list")
@click.argument("issue_id", type=int)
def kpi_list(issue_id):
    """แสดงรายการตัวชี้วัดทั้งหมดของประเด็นยุทธศาสตร์"""
    # Check if issue exists
    issue = StrategicIssue.get_by_id(issue_id)
    if not issue:
        click.echo(f"ไม่พบประเด็นยุทธศาสตร์ ID: {issue_id}")
        return
    
    kpis = KPI.get_by_issue_id(issue_id)
    
    if not kpis:
        click.echo(f"ไม่พบตัวชี้วัดภายใต้ประเด็น '{issue.name}'")
        return
    
    # Prepare data for table
    headers = ["ID", "ชื่อตัวชี้วัด", "เป้าหมาย", "ค่าปัจจุบัน", "หน่วย", "ความคืบหน้า"]
    data = [
        [
            kpi.id,
            kpi.name,
            kpi.target_value,
            kpi.current_value,
            kpi.unit,
            f"{kpi.progress:.2f}%" if kpi.progress is not None else "-",
        ]
        for kpi in kpis
    ]
    
    click.echo(f"ตัวชี้วัดภายใต้ประเด็น '{issue.name}':")
    click.echo(tabulate(data, headers=headers, tablefmt="grid"))


@kpi.command("show")
@click.argument("kpi_id", type=int)
def kpi_show(kpi_id):
    """แสดงรายละเอียดของตัวชี้วัด"""
    kpi = KPI.get_by_id(kpi_id)
    
    if not kpi:
        click.echo(f"ไม่พบตัวชี้วัด ID: {kpi_id}")
        return
    
    # Get parent issue
    issue = StrategicIssue.get_by_id(kpi.issue_id)
    
    # Display KPI details
    click.echo(f"ตัวชี้วัด ID: {kpi.id}")
    click.echo(f"ชื่อตัวชี้วัด: {kpi.name}")
    if kpi.description:
        click.echo(f"คำอธิบาย: {kpi.description}")
    if kpi.target_value is not None:
        click.echo(f"ค่าเป้าหมาย: {kpi.target_value}")
    if kpi.current_value is not None:
        click.echo(f"ค่าปัจจุบัน: {kpi.current_value}")
    if kpi.unit:
        click.echo(f"หน่วยวัด: {kpi.unit}")
    if kpi.progress is not None:
        click.echo(f"ความคืบหน้า: {kpi.progress:.2f}%")
    
    click.echo(f"ภายใต้ประเด็นยุทธศาสตร์: {issue.name if issue else 'ไม่ทราบ'}")


@kpi.command("update")
@click.argument("kpi_id", type=int)
@click.option("--name", help="ชื่อตัวชี้วัด")
@click.option("--desc", "--description", help="คำอธิบายตัวชี้วัด")
@click.option("--target", type=float, help="ค่าเป้าหมาย")
@click.option("--current", type=float, help="ค่าปัจจุบัน")
@click.option("--unit", help="หน่วยวัด")
def kpi_update(kpi_id, name, desc, target, current, unit):
    """ปรับปรุงข้อมูลตัวชี้วัด"""
    kpi = KPI.get_by_id(kpi_id)
    
    if not kpi:
        click.echo(f"ไม่พบตัวชี้วัด ID: {kpi_id}")
        return
    
    # Update fields if provided
    if name:
        kpi.name = name
    if desc is not None:  # Allow empty description
        kpi.description = desc
    if target is not None:
        kpi.target_value = target
    if current is not None:
        kpi.current_value = current
    if unit is not None:
        kpi.unit = unit
    
    # Save changes
    kpi.save()
    
    click.echo(f"ปรับปรุงข้อมูลตัวชี้วัด ID: {kpi_id} เรียบร้อยแล้ว")


@kpi.command("delete")
@click.argument("kpi_id", type=int)
@click.option("--force", is_flag=True, help="ยืนยันการลบโดยไม่ถามคำถาม")
def kpi_delete(kpi_id, force):
    """ลบตัวชี้วัด"""
    kpi = KPI.get_by_id(kpi_id)
    
    if not kpi:
        click.echo(f"ไม่พบตัวชี้วัด ID: {kpi_id}")
        return
    
    # Confirm deletion
    if not force and not click.confirm(f"คุณต้องการลบตัวชี้วัด '{kpi.name}' ใช่หรือไม่?"):
        click.echo("ยกเลิกการลบ")
        return
    
    # Delete the KPI
    success = kpi.delete()
    
    if success:
        click.echo(f"ลบตัวชี้วัด ID: {kpi_id} เรียบร้อยแล้ว")
    else:
        click.echo(f"เกิดข้อผิดพลาดในการลบตัวชี้วัด ID: {kpi_id}")


# Group for initiative commands
@main.group()
def initiative():
    """จัดการโครงการ/กิจกรรม (Initiatives)"""
    pass


@initiative.command("create")
@click.argument("issue_id", type=int)
@click.argument("name")
@click.option("--desc", "--description", help="คำอธิบายโครงการ")
@click.option("--status", help=f"สถานะโครงการ ({', '.join(Initiative.VALID_STATUSES)})")
@click.option("--budget", type=float, help="งบประมาณ (บาท)")
@click.option("--start-date", help="วันที่เริ่มต้น (รูปแบบ YYYY-MM-DD)")
@click.option("--end-date", help="วันที่สิ้นสุด (รูปแบบ YYYY-MM-DD)")
def initiative_create(issue_id, name, desc, status, budget, start_date, end_date):
    """สร้างโครงการ/กิจกรรมใหม่"""
    # Check if issue exists
    issue = StrategicIssue.get_by_id(issue_id)
    if not issue:
        click.echo(f"ไม่พบประเด็นยุทธศาสตร์ ID: {issue_id}")
        return
    
    # Validate status if provided
    if status and status not in Initiative.VALID_STATUSES:
        click.echo(f"สถานะไม่ถูกต้อง กรุณาเลือกจาก: {', '.join(Initiative.VALID_STATUSES)}")
        return
    
    # Validate dates if provided
    for date_str, date_name in [(start_date, "วันที่เริ่มต้น"), (end_date, "วันที่สิ้นสุด")]:
        if date_str:
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                click.echo(f"รูปแบบ{date_name}ไม่ถูกต้อง กรุณาใช้รูปแบบ YYYY-MM-DD")
                return
    
    # Create and save the initiative
    initiative = Initiative(
        issue_id=issue_id,
        name=name,
        description=desc,
        status=status,
        budget=budget,
        start_date=start_date,
        end_date=end_date,
    )
    initiative_id = initiative.save()
    
    click.echo(f"สร้างโครงการ '{name}' ภายใต้ประเด็น '{issue.name}' เรียบร้อยแล้ว (ID: {initiative_id})")


@initiative.command("list")
@click.argument("issue_id", type=int)
def initiative_list(issue_id):
    """แสดงรายการโครงการทั้งหมดของประเด็นยุทธศาสตร์"""
    # Check if issue exists
    issue = StrategicIssue.get_by_id(issue_id)
    if not issue:
        click.echo(f"ไม่พบประเด็นยุทธศาสตร์ ID: {issue_id}")
        return
    
    initiatives = Initiative.get_by_issue_id(issue_id)
    
    if not initiatives:
        click.echo(f"ไม่พบโครงการภายใต้ประเด็น '{issue.name}'")
        return
    
    # Prepare data for table
    headers = ["ID", "ชื่อโครงการ", "สถานะ", "งบประมาณ", "วันเริ่มต้น", "วันสิ้นสุด"]
    data = [
        [
            init.id,
            init.name,
            init.status,
            f"{init.budget:,.2f}" if init.budget is not None else "-",
            init.start_date,
            init.end_date,
        ]
        for init in initiatives
    ]
    
    click.echo(f"โครงการภายใต้ประเด็น '{issue.name}':")
    click.echo(tabulate(data, headers=headers, tablefmt="grid"))


@initiative.command("show")
@click.argument("initiative_id", type=int)
def initiative_show(initiative_id):
    """แสดงรายละเอียดของโครงการ"""
    initiative = Initiative.get_by_id(initiative_id)
    
    if not initiative:
        click.echo(f"ไม่พบโครงการ ID: {initiative_id}")
        return
    
    # Get parent issue
    issue = StrategicIssue.get_by_id(initiative.issue_id)
    
    # Display initiative details
    click.echo(f"โครงการ ID: {initiative.id}")
    click.echo(f"ชื่อโครงการ: {initiative.name}")
    if initiative.description:
        click.echo(f"คำอธิบาย: {initiative.description}")
    click.echo(f"สถานะ: {initiative.status}")
    if initiative.budget is not None:
        click.echo(f"งบประมาณ: {initiative.budget:,.2f} บาท")
    if initiative.start_date:
        click.echo(f"วันที่เริ่มต้น: {initiative.start_date}")
    if initiative.end_date:
        click.echo(f"วันที่สิ้นสุด: {initiative.end_date}")
    
    click.echo(f"ภายใต้ประเด็นยุทธศาสตร์: {issue.name if issue else 'ไม่ทราบ'}")


@initiative.command("update")
@click.argument("initiative_id", type=int)
@click.option("--name", help="ชื่อโครงการ")
@click.option("--desc", "--description", help="คำอธิบายโครงการ")
@click.option("--status", help=f"สถานะโครงการ ({', '.join(Initiative.VALID_STATUSES)})")
@click.option("--budget", type=float, help="งบประมาณ")
@click.option("--start-date", help="วันที่เริ่มต้น (รูปแบบ YYYY-MM-DD)")
@click.option("--end-date", help="วันที่สิ้นสุด (รูปแบบ YYYY-MM-DD)")
def initiative_update(initiative_id, name, desc, status, budget, start_date, end_date):
    """ปรับปรุงข้อมูลโครงการ"""
    initiative = Initiative.get_by_id(initiative_id)
    
    if not initiative:
        click.echo(f"ไม่พบโครงการ ID: {initiative_id}")
        return
    
    # Validate status if provided
    if status and status not in Initiative.VALID_STATUSES:
        click.echo(f"สถานะไม่ถูกต้อง กรุณาเลือกจาก: {', '.join(Initiative.VALID_STATUSES)}")
        return
    
    # Validate dates if provided
    for date_str, date_name in [(start_date, "วันที่เริ่มต้น"), (end_date, "วันที่สิ้นสุด")]:
        if date_str:
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                click.echo(f"รูปแบบ{date_name}ไม่ถูกต้อง กรุณาใช้รูปแบบ YYYY-MM-DD")
                return
    
    # Update fields if provided
    if name:
        initiative.name = name
    if desc is not None:  # Allow empty description
        initiative.description = desc
    if status:
        initiative.status = status
    if budget is not None:
        initiative.budget = budget
    if start_date:
        initiative.start_date = start_date
    if end_date:
        initiative.end_date = end_date
    
    # Save changes
    initiative.save()
    
    click.echo(f"ปรับปรุงข้อมูลโครงการ ID: {initiative_id} เรียบร้อยแล้ว")


@initiative.command("delete")
@click.argument("initiative_id", type=int)
@click.option("--force", is_flag=True, help="ยืนยันการลบโดยไม่ถามคำถาม")
def initiative_delete(initiative_id, force):
    """ลบโครงการ"""
    initiative = Initiative.get_by_id(initiative_id)
    
    if not initiative:
        click.echo(f"ไม่พบโครงการ ID: {initiative_id}")
        return
    
    # Confirm deletion
    if not force and not click.confirm(f"คุณต้องการลบโครงการ '{initiative.name}' ใช่หรือไม่?"):
        click.echo("ยกเลิกการลบ")
        return
    
    # Delete the initiative
    success = initiative.delete()
    
    if success:
        click.echo(f"ลบโครงการ ID: {initiative_id} เรียบร้อยแล้ว")
    else:
        click.echo(f"เกิดข้อผิดพลาดในการลบโครงการ ID: {initiative_id}")


# Group for report commands
@main.group()
def report():
    """รายงานและสรุปข้อมูล"""
    pass


@report.command("plan")
@click.argument("plan_id", type=int)
@click.option("--format", type=click.Choice(["text", "table"]), default="table", help="รูปแบบรายงาน")
def report_plan(plan_id, format):
    """รายงานภาพรวมของแผนยุทธศาสตร์"""
    plan = StrategicPlan.get_by_id(plan_id)
    
    if not plan:
        click.echo(f"ไม่พบแผนยุทธศาสตร์ ID: {plan_id}")
        return
    
    issues = StrategicIssue.get_by_plan_id(plan_id)
    
    click.echo("=" * 80)
    click.echo(f"รายงานแผนยุทธศาสตร์: {plan.name}")
    click.echo("=" * 80)
    
    if plan.description:
        click.echo(f"\nคำอธิบาย: {plan.description}")
    
    if plan.start_date and plan.end_date:
        click.echo(f"\nระยะเวลา: {plan.start_date} ถึง {plan.end_date}")
    
    click.echo(f"\nจำนวนประเด็นยุทธศาสตร์: {len(issues)}")
    
    if not issues:
        click.echo("\nไม่มีประเด็นยุทธศาสตร์ในแผนนี้")
        return
    
    # Count KPIs and initiatives
    all_kpis = []
    all_initiatives = []
    total_budget = 0
    
    for issue in issues:
        kpis = KPI.get_by_issue_id(issue.id)
        all_kpis.extend(kpis)
        
        initiatives = Initiative.get_by_issue_id(issue.id)
        all_initiatives.extend(initiatives)
        
        for init in initiatives:
            if init.budget is not None:
                total_budget += init.budget
    
    click.echo(f"จำนวนตัวชี้วัดทั้งหมด: {len(all_kpis)}")
    click.echo(f"จำนวนโครงการทั้งหมด: {len(all_initiatives)}")
    click.echo(f"งบประมาณรวมทั้งสิ้น: {total_budget:,.2f} บาท")
    
    if format == "table":
        # Show issues in table format
        headers = ["ID", "ประเด็นยุทธศาสตร์", "จำนวนตัวชี้วัด", "จำนวนโครงการ", "งบประมาณรวม"]
        data = []
        
        for issue in issues:
            kpis = KPI.get_by_issue_id(issue.id)
            initiatives = Initiative.get_by_issue_id(issue.id)
            
            issue_budget = sum(init.budget or 0 for init in initiatives)
            
            data.append([
                issue.id,
                issue.name,
                len(kpis),
                len(initiatives),
                f"{issue_budget:,.2f}" if issue_budget > 0 else "-"
            ])
        
        click.echo("\nประเด็นยุทธศาสตร์:")
        click.echo(tabulate(data, headers=headers, tablefmt="grid"))
    else:
        # Show issues in text format
        click.echo("\nประเด็นยุทธศาสตร์:")
        
        for i, issue in enumerate(issues, 1):
            kpis = KPI.get_by_issue_id(issue.id)
            initiatives = Initiative.get_by_issue_id(issue.id)
            
            issue_budget = sum(init.budget or 0 for init in initiatives)
            
            click.echo(f"\n{i}. {issue.name} (ID: {issue.id})")
            if issue.description:
                click.echo(f"   คำอธิบาย: {issue.description}")
            click.echo(f"   จำนวนตัวชี้วัด: {len(kpis)}")
            click.echo(f"   จำนวนโครงการ: {len(initiatives)}")
            click.echo(f"   งบประมาณรวม: {issue_budget:,.2f} บาท")


if __name__ == "__main__":
    main()
