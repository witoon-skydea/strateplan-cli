#!/bin/bash
# Script สำหรับตั้งค่า virtual environment และติดตั้ง package สำหรับ strateplan-cli

# สีสำหรับ terminal output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}====== การตั้งค่า StrategicPlan CLI ======${NC}"

# ตรวจสอบว่ามี Python ติดตั้งหรือไม่
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}ไม่พบ Python 3 กรุณาติดตั้ง Python 3.8 หรือสูงกว่า${NC}"
    exit 1
fi

# สร้าง virtual environment
echo -e "${BLUE}กำลังสร้าง virtual environment...${NC}"
python3 -m venv venv

# เปิดใช้งาน virtual environment
if [[ "$OSTYPE" == "darwin"* ]] || [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo -e "${BLUE}กำลังเปิดใช้งาน virtual environment (macOS/Linux)...${NC}"
    source venv/bin/activate
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    echo -e "${BLUE}กำลังเปิดใช้งาน virtual environment (Windows)...${NC}"
    source venv/Scripts/activate
else
    echo -e "${YELLOW}ไม่สามารถเปิดใช้งาน virtual environment โดยอัตโนมัติ${NC}"
    echo -e "${YELLOW}กรุณาเปิดใช้งานด้วยตนเอง:${NC}"
    echo -e "${YELLOW}- Windows: venv\\Scripts\\activate${NC}"
    echo -e "${YELLOW}- macOS/Linux: source venv/bin/activate${NC}"
    exit 1
fi

# อัปเดต pip
echo -e "${BLUE}กำลังอัปเดต pip...${NC}"
python -m pip install --upgrade pip

# ติดตั้ง package ที่จำเป็น
echo -e "${BLUE}กำลังติดตั้ง dependencies...${NC}"
pip install -r requirements.txt

# ติดตั้ง package ในโหมด development
echo -e "${BLUE}กำลังติดตั้ง strateplan-cli ในโหมด development...${NC}"
pip install -e .

echo -e "${GREEN}====== การตั้งค่าเสร็จสมบูรณ์ ======${NC}"
echo -e "${GREEN}ตอนนี้คุณสามารถใช้งาน strateplan-cli ได้แล้ว${NC}"
echo -e "${GREEN}ทดลองใช้งานด้วยคำสั่ง: strateplan --help${NC}"
echo ""
echo -e "${YELLOW}เมื่อต้องการใช้งาน strateplan-cli ในภายหลัง กรุณาเปิดใช้งาน virtual environment ก่อนด้วยคำสั่ง:${NC}"
echo -e "${YELLOW}- Windows: venv\\Scripts\\activate${NC}"
echo -e "${YELLOW}- macOS/Linux: source venv/bin/activate${NC}"
