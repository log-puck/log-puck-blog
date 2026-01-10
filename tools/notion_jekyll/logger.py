"""
Logging utilities per Notion to Jekyll Builder
"""

import datetime
from typing import Optional


def log(message: str, level: str = "INFO") -> None:
    """
    Logging con timestamp.
    
    Args:
        message: Messaggio da loggare
        level: Livello di log (INFO, DEBUG, ERROR, WARNING)
    """
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")
