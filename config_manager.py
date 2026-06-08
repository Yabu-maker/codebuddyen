#!/usr/bin/env python3
"""简洁的10行代码 - 配置管理器"""

import json
from pathlib import Path


class ConfigManager:
    """轻量级JSON配置管理"""

    def __init__(self, path: str = "config.json"):
        self.path = Path(path)
        self.data = json.loads(self.path.read_text()) if self.path.exists() else {}

    def get(self, key: str, default=None):
        return self.data.get(key, default)

    def set(self, key: str, value) -> None:
        self.data[key] = value

    def save(self) -> None:
        self.path.write_text(json.dumps(self.data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    cfg = ConfigManager("test_config.json")
    cfg.set("app_name", "MyApp")
    cfg.set("version", "1.0.0")
    cfg.save()
    print(f"Config saved: {cfg.get('app_name')} v{cfg.get('version')}")
