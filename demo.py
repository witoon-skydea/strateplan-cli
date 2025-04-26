#!/usr/bin/env python
"""
Demo script for StrategicPlan CLI
"""
import os
import sys
import tempfile
import subprocess
import time
from pathlib import Path


def run_command(command):
    """Run a CLI command and print the output
    
    Args:
        command: Command to run
    """
    print(f"\n$ {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(f"Error: {result.stderr}", file=sys.stderr)
    return result


def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def pause():
    """Pause for user input"""
    input("\nกดปุ่ม Enter เพื่อดำเนินการต่อ...")


def setup_demo_db():
    """Set up a temporary database for the demo"""
    db_dir = tempfile.mkdtemp()
    db_path = os.path.join(db_dir, "strateplan-demo.db")
    
    print(f"สร้างฐานข้อมูลชั่วคราวที่: {db_path}")
    
    # Create config directory if it doesn't exist
    config_dir = Path.home() / ".strateplan"
    config_dir.mkdir(exist_ok=True)
    
    # Create or update config file
    config_file = config_dir / "config.json"
    with open(config_file, "w") as f:
        f.write(f'{{"db_path": "{db_path}", "default_format": "table"}}')
    
    return db_path


def main():
    """Run the demo"""
    # Set up demo database
    db_path = setup_demo_db()
    
    clear_screen()
    print("=" * 80)
    print("                      StrategicPlan CLI Demo")
    print("=" * 80)
    print("\nการสาธิตนี้จะแสดงวิธีการใช้งาน StrategicPlan CLI ในการจัดการแผนยุทธศาสตร์")
    print("โดยใช้ฐานข้อมูลชั่วคราวสำหรับการสาธิตเท่านั้น")
    pause()
    
    # Step 1: Create a strategic plan
    clear_screen()
    print("ขั้นตอนที่ 1: สร้างแผนยุทธศาสตร์")
    run_command('python -m strateplan.cli plan create "แผนพัฒนาองค์กร 2025-2029" --desc "แผนยุทธศาสตร์ระยะ 5 ปี" --start-date "2025-01-01" --end-date "2029-12-31"')
    pause()
    
    # Step 2: List strategic plans
    clear_screen()
    print("ขั้นตอนที่ 2: แสดงรายการแผนยุทธศาสตร์")
    run_command('python -m strateplan.cli plan list')
    pause()
    
    # Step 3: Create strategic issues
    clear_screen()
    print("ขั้นตอนที่ 3: สร้างประเด็นยุทธศาสตร์")
    run_command('python -m strateplan.cli issue create 1 "พัฒนาศักยภาพบุคลากร" --desc "การเพิ่มขีดความสามารถของบุคลากรในองค์กร" --priority 1')
    run_command('python -m strateplan.cli issue create 1 "เพิ่มประสิทธิภาพกระบวนการทำงาน" --desc "การปรับปรุงกระบวนการทำงานให้มีประสิทธิภาพมากขึ้น" --priority 2')
    run_command('python -m strateplan.cli issue create 1 "พัฒนานวัตกรรมและเทคโนโลยี" --desc "การนำนวัตกรรมและเทคโนโลยีมาใช้ในการพัฒนาองค์กร" --priority 3')
    pause()
    
    # Step 4: List strategic issues
    clear_screen()
    print("ขั้นตอนที่ 4: แสดงรายการประเด็นยุทธศาสตร์")
    run_command('python -m strateplan.cli issue list 1')
    pause()
    
    # Step 5: Create KPIs
    clear_screen()
    print("ขั้นตอนที่ 5: สร้างตัวชี้วัด (KPIs)")
    run_command('python -m strateplan.cli kpi create 1 "ร้อยละความพึงพอใจของบุคลากร" --target 90 --current 75 --unit "%"')
    run_command('python -m strateplan.cli kpi create 1 "จำนวนชั่วโมงฝึกอบรมเฉลี่ยต่อคนต่อปี" --target 40 --current 25 --unit "ชั่วโมง"')
    run_command('python -m strateplan.cli kpi create 2 "ร้อยละของกระบวนการที่ได้รับการปรับปรุง" --target 70 --current 30 --unit "%"')
    run_command('python -m strateplan.cli kpi create 3 "จำนวนนวัตกรรมที่นำมาใช้ในองค์กร" --target 10 --current 3 --unit "ชิ้น"')
    pause()
    
    # Step 6: List KPIs for an issue
    clear_screen()
    print("ขั้นตอนที่ 6: แสดงรายการตัวชี้วัดของประเด็นยุทธศาสตร์")
    run_command('python -m strateplan.cli kpi list 1')
    pause()
    
    # Step 7: Create initiatives
    clear_screen()
    print("ขั้นตอนที่ 7: สร้างโครงการ/กิจกรรม")
    run_command('python -m strateplan.cli initiative create 1 "โครงการฝึกอบรมทักษะดิจิทัล" --desc "การฝึกอบรมทักษะด้าน digital literacy" --budget 500000 --start-date "2025-03-01" --end-date "2025-06-30" --status "กำลังดำเนินการ"')
    run_command('python -m strateplan.cli initiative create 1 "โครงการพัฒนาภาวะผู้นำ" --desc "การพัฒนาทักษะภาวะผู้นำให้กับผู้บริหารระดับกลาง" --budget 800000 --start-date "2025-07-01" --end-date "2025-12-31" --status "ยังไม่เริ่ม"')
    run_command('python -m strateplan.cli initiative create 2 "โครงการ Lean Management" --desc "การประยุกต์ใช้แนวคิด Lean ในการปรับปรุงกระบวนการ" --budget 300000 --start-date "2025-02-01" --end-date "2025-10-31" --status "กำลังดำเนินการ"')
    run_command('python -m strateplan.cli initiative create 3 "โครงการพัฒนาระบบ AI ช่วยวิเคราะห์ข้อมูล" --desc "การพัฒนาระบบ AI เพื่อช่วยในการวิเคราะห์ข้อมูล" --budget 1500000 --start-date "2025-04-01" --end-date "2026-03-31" --status "ยังไม่เริ่ม"')
    pause()
    
    # Step 8: List initiatives for an issue
    clear_screen()
    print("ขั้นตอนที่ 8: แสดงรายการโครงการของประเด็นยุทธศาสตร์")
    run_command('python -m strateplan.cli initiative list 1')
    pause()
    
    # Step 9: Show a strategic issue details
    clear_screen()
    print("ขั้นตอนที่ 9: แสดงรายละเอียดของประเด็นยุทธศาสตร์")
    run_command('python -m strateplan.cli issue show 1')
    pause()
    
    # Step 10: Update a KPI
    clear_screen()
    print("ขั้นตอนที่ 10: ปรับปรุงข้อมูลตัวชี้วัด")
    run_command('python -m strateplan.cli kpi update 1 --current 85')
    run_command('python -m strateplan.cli kpi show 1')
    pause()
    
    # Step 11: Update initiative status
    clear_screen()
    print("ขั้นตอนที่ 11: ปรับปรุงสถานะโครงการ")
    run_command('python -m strateplan.cli initiative update 2 --status "เสร็จสิ้น"')
    run_command('python -m strateplan.cli initiative show 2')
    pause()
    
    # Step 12: Generate plan report
    clear_screen()
    print("ขั้นตอนที่ 12: สร้างรายงานแผนยุทธศาสตร์")
    run_command('python -m strateplan.cli report plan 1')
    pause()
    
    # Cleanup
    clear_screen()
    print("=" * 80)
    print("                  การสาธิต StrategicPlan CLI เสร็จสิ้น")
    print("=" * 80)
    print(f"\nฐานข้อมูลชั่วคราวถูกสร้างที่: {db_path}")
    print("คุณสามารถใช้คำสั่งต่อไปนี้เพื่อทดลองใช้งานเพิ่มเติม:")
    print("\n  python -m strateplan.cli --help")
    print("\nหรือดูคำสั่งย่อยเพิ่มเติม:")
    print("\n  python -m strateplan.cli plan --help")
    print("  python -m strateplan.cli issue --help")
    print("  python -m strateplan.cli kpi --help")
    print("  python -m strateplan.cli initiative --help")
    print("  python -m strateplan.cli report --help")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
