from setuptools import setup, find_packages

setup(
    name="strateplan",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click>=8.0.0",
        "tabulate>=0.8.9",
    ],
    entry_points={
        "console_scripts": [
            "strateplan=strateplan.cli:main",
        ],
    },
    author="MCP Team",
    author_email="example@example.com",
    description="เครื่องมือ CLI สำหรับการจัดการแผนยุทธศาสตร์",
    keywords="strategic plan, strategy, kpi, cli",
    python_requires=">=3.8",
)