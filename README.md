# StrategicPlan CLI

เครื่องมือ Command Line Interface (CLI) สำหรับการจัดการแผนยุทธศาสตร์ ประเด็นยุทธศาสตร์ ตัวชี้วัด และโครงการ

## คุณสมบัติ

- จัดการแผนยุทธศาสตร์ (Strategic Plans)
- จัดการประเด็นยุทธศาสตร์ (Strategic Issues)
- จัดการตัวชี้วัด (KPIs)
- จัดการโครงการ/กิจกรรม (Initiatives)
- ออกรายงานสรุปแผนยุทธศาสตร์

## การติดตั้ง

```bash
# Clone repository
git clone <repository-url>
cd strateplan-cli

# สร้าง Virtual Environment (แนะนำ)
python -m venv venv
source venv/bin/activate  # บน Windows ใช้ venv\Scripts\activate

# ติดตั้ง package
pip install -e .
```

## การใช้งาน

```bash
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

## Requirement

- Python 3.8+
- SQLite3
- Click
- Tabulate

## License

MIT
