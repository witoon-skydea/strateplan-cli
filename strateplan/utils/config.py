"""
Configuration utilities
"""
import os
import json
from pathlib import Path
from typing import Dict, Any, Optional


CONFIG_DIR = Path.home() / ".strateplan"
CONFIG_FILE = CONFIG_DIR / "config.json"


def get_config_dir() -> Path:
    """Get the config directory path
    
    Returns:
        Path to config directory
    """
    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    
    return CONFIG_DIR


def get_config() -> Dict[str, Any]:
    """Get the configuration
    
    Returns:
        Configuration dictionary
    """
    if not CONFIG_FILE.exists():
        return {
            "db_path": str(CONFIG_DIR / "strateplan.db"),
            "default_format": "table",
        }
    
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        # Return default config if file is invalid
        return {
            "db_path": str(CONFIG_DIR / "strateplan.db"),
            "default_format": "table",
        }


def save_config(config: Dict[str, Any]) -> None:
    """Save the configuration
    
    Args:
        config: Configuration dictionary
    """
    get_config_dir()  # Ensure config directory exists
    
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def get_db_path() -> str:
    """Get the database path
    
    Returns:
        Path to the database file
    """
    config = get_config()
    return config.get("db_path", str(CONFIG_DIR / "strateplan.db"))


def set_db_path(path: str) -> None:
    """Set the database path
    
    Args:
        path: Path to the database file
    """
    config = get_config()
    config["db_path"] = path
    save_config(config)


def get_default_format() -> str:
    """Get the default output format
    
    Returns:
        Default format (table, json, etc.)
    """
    config = get_config()
    return config.get("default_format", "table")


def set_default_format(format_name: str) -> None:
    """Set the default output format
    
    Args:
        format_name: Format name (table, json, etc.)
    """
    config = get_config()
    config["default_format"] = format_name
    save_config(config)
