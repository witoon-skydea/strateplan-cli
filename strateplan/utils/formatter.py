"""
Utilities for formatting and displaying data
"""
from typing import List, Dict, Any, Optional
from tabulate import tabulate
import click
import json


def format_table(data: List[Dict[str, Any]], headers: List[str], tablefmt: str = "grid") -> str:
    """Format data as a table
    
    Args:
        data: List of dictionaries containing the data
        headers: List of column headers
        tablefmt: Table format (grid, simple, plain, etc.)
        
    Returns:
        Formatted table as string
    """
    return tabulate(data, headers=headers, tablefmt=tablefmt)


def format_json(data: Any, indent: int = 2) -> str:
    """Format data as JSON
    
    Args:
        data: Data to format
        indent: Number of spaces for indentation
        
    Returns:
        Formatted JSON as string
    """
    return json.dumps(data, indent=indent, ensure_ascii=False)


def echo_success(message: str) -> None:
    """Print a success message
    
    Args:
        message: Message to print
    """
    click.secho(message, fg="green")


def echo_error(message: str) -> None:
    """Print an error message
    
    Args:
        message: Message to print
    """
    click.secho(f"Error: {message}", fg="red")


def echo_warning(message: str) -> None:
    """Print a warning message
    
    Args:
        message: Message to print
    """
    click.secho(f"Warning: {message}", fg="yellow")


def echo_info(message: str) -> None:
    """Print an info message
    
    Args:
        message: Message to print
    """
    click.secho(message, fg="blue")


def format_progress_bar(current: float, target: float, width: int = 30) -> str:
    """Format a progress bar
    
    Args:
        current: Current value
        target: Target value
        width: Width of the progress bar
        
    Returns:
        Formatted progress bar as string
    """
    if current is None or target is None or target == 0:
        return "[" + " " * width + "] N/A"
    
    if current > target:
        current = target
    
    progress = current / target
    filled_width = int(width * progress)
    
    bar = "[" + "#" * filled_width + " " * (width - filled_width) + "]"
    percentage = f" {progress * 100:.1f}%"
    
    return bar + percentage


def format_budget(amount: Optional[float]) -> str:
    """Format budget amount
    
    Args:
        amount: Budget amount
        
    Returns:
        Formatted budget as string
    """
    if amount is None:
        return "N/A"
    
    return f"{amount:,.2f} บาท"


def format_date_range(start_date: Optional[str], end_date: Optional[str]) -> str:
    """Format date range
    
    Args:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        
    Returns:
        Formatted date range as string
    """
    if not start_date and not end_date:
        return "ไม่ระบุ"
    
    if start_date and end_date:
        return f"{start_date} ถึง {end_date}"
    
    if start_date:
        return f"เริ่ม {start_date}"
    
    return f"ถึง {end_date}"
