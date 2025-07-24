import os
import json
from typing import List, Dict, Any, Optional


class LogReader:
    def __init__(self, files: List[str], date: Optional[str] = None):
        self.files = files
        self.date = date

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
