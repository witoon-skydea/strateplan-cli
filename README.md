# StrategicPlan CLI

เครื่องมือ Command Line Interface (CLI) สำหรับการจัดการแผนยุทธศาสตร์ ประเด็นยุทธศาสตร์ ตัวชี้วัด และโครงการ

## คุณสมบัติ

- จัดการแผนยุทธศาสตร์ (Strategic Plans)
- จัดการประเด็นยุทธศาสตร์ (Strategic Issues)
- จัดการตัวชี้วัด (KPIs)
- จัดการโครงการ/กิจกรรม (Initiatives)
- ออกรายงานสรุปแผนยุทธศาสตร์

## ความต้องการของระบบ

- Python 3.8+
- SQLite3
- pip (Package Installer for Python)

## การติดตั้ง

### วิธีที่ 1: ติดตั้งโดยใช้ Virtual Environment (แนะนำ)

การใช้ virtual environment เป็นวิธีที่แนะนำสำหรับการติดตั้งและใช้งาน Python packages เพื่อหลีกเลี่ยงความขัดแย้งของ dependencies

```bash
# Clone repository
git clone https://github.com/witoon-skydea/strateplan-cli.git
cd strateplan-cli

# ใช้สคริปต์ setup อัตโนมัติ
./setup.sh  # สำหรับ macOS/Linux
# หรือ
# setup.sh  # สำหรับ Windows
```

หากต้องการตั้งค่าด้วยตนเอง:

```bash
# Clone repository
git clone https://github.com/witoon-skydea/strateplan-cli.git
cd strateplan-cli

# สร้าง Virtual Environment
python -m venv venv

# เปิดใช้งาน Virtual Environment
source venv/bin/activate  # สำหรับ macOS/Linux
# หรือ
# venv\Scripts\activate  # สำหรับ Windows

# ติดตั้ง dependencies
pip install -r requirements.txt

# ติดตั้งแบบ Development Mode
pip install -e .
```

### วิธีที่ 2: ติดตั้งโดยตรง

```bash
# Clone repository
git clone https://github.com/witoon-skydea/strateplan-cli.git
cd strateplan-cli

# ติดตั้ง package
pip install -e .
```

## การใช้งาน

เมื่อติดตั้งแล้ว คุณสามารถใช้คำสั่ง `strateplan` ได้โดยตรง:

```bash
# ตรวจสอบคำสั่งที่มีให้ใช้
strateplan --help

# สร้างแผนยุทธศาสตร์
strateplan plan create "แผนพัฒนาองค์กร 2025" --desc "แผนยุทธศาสตร์ระยะ 5 ปี" --start-date "2025-01-01" --end-date "2029-12-31"

# ดูรายการแผนยุทธศาสตร์ทั้งหมด
strateplan plan list

# สร้างประเด็นยุทธศาสตร์
strateplan issue create 1 "พัฒนาศักยภาพบุคลากร" --desc "การเพิ่มขีดความสามารถของบุคลากรในองค์กร" --priority 1

# สร้างตัวชี้วัด (KPI)
strateplan kpi create 1 "ร้อยละความพึงพอใจของบุคลากร" --target 90 --current 75 --unit "%"

# สร้างโครงการ (Initiative)
strateplan initiative create 1 "โครงการฝึกอบรมทักษะดิจิทัล" --desc "การฝึกอบรมทักษะด้าน digital literacy" --budget 500000 --start-date "2025-03-01" --end-date "2025-06-30"
```

### การทดลองใช้งานผ่าน Demo Script

คุณสามารถทดลองใช้งานฟีเจอร์หลักทั้งหมดโดยการรันสคริปต์ demo:

```bash
# ต้องอยู่ใน virtual environment ถ้าติดตั้งแบบวิธีที่ 1
python demo.py
```

## คำสั่งทั้งหมด

### แผนยุทธศาสตร์ (Plans)

```bash
strateplan plan create <name> [--desc DESCRIPTION] [--start-date DATE] [--end-date DATE]
strateplan plan list
strateplan plan show <plan_id>
strateplan plan update <plan_id> [--name NAME] [--desc DESCRIPTION] [--start-date DATE] [--end-date DATE]
strateplan plan delete <plan_id> [--force]
```

### ประเด็นยุทธศาสตร์ (Issues)

```bash
strateplan issue create <plan_id> <name> [--desc DESCRIPTION] [--priority PRIORITY]
strateplan issue list <plan_id>
strateplan issue show <issue_id>
strateplan issue update <issue_id> [--name NAME] [--desc DESCRIPTION] [--priority PRIORITY]
strateplan issue delete <issue_id> [--force]
```

### ตัวชี้วัด (KPIs)

```bash
strateplan kpi create <issue_id> <name> [--desc DESCRIPTION] [--target VALUE] [--current VALUE] [--unit UNIT]
strateplan kpi list <issue_id>
strateplan kpi show <kpi_id>
strateplan kpi update <kpi_id> [--name NAME] [--desc DESCRIPTION] [--target VALUE] [--current VALUE] [--unit UNIT]
strateplan kpi delete <kpi_id> [--force]
```

### โครงการ/กิจกรรม (Initiatives)

```bash
strateplan initiative create <issue_id> <name> [--desc DESCRIPTION] [--status STATUS] [--budget VALUE] [--start-date DATE] [--end-date DATE]
strateplan initiative list <issue_id>
strateplan initiative show <initiative_id>
strateplan initiative update <initiative_id> [--name NAME] [--desc DESCRIPTION] [--status STATUS] [--budget VALUE] [--start-date DATE] [--end-date DATE]
strateplan initiative delete <initiative_id> [--force]
```

### รายงาน (Reports)

```bash
strateplan report plan <plan_id> [--format {text,table}]
```

## การบำรุงรักษา/การพัฒนาต่อ

การทดสอบระบบ:

```bash
# ต้องอยู่ใน virtual environment (ถ้าติดตั้งแบบวิธีที่ 1)
pip install pytest
pytest
```

## License

MIT
