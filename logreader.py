import os
import json
from typing import List, Dict, Any, Optional
from datetime import datetime


class LogReader:
    def __init__(self, files: List[str], date: Optional[str] = None):
        self.files = files
        self.date = self.validate_date(date) if date else None

    @classmethod
    def validate_date(cls, date_str: str):
        try:
            # Предполагается формат ГГГГ-ММ-ДД
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            raise ValueError(f"Invalid date format: {date_str}. Expected YYYY-MM-DD.")

    def read_logs(self) -> List[Dict[str, Any]]:
        logs = []
        for file in self.files:
            if not os.path.exists(file):
                raise FileNotFoundError(file)
            with open(file, encoding="utf-8") as f:
                for line in f:
                    entry = json.loads(line)
                    if self.date:
                        if entry["@timestamp"][:10] != self.date:
                            continue
                    logs.append(entry)

        return logs
