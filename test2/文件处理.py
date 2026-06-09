#!/usr/bin/env python3
"""文件处理器 - 支持批量处理和统计功能"""

import os
import json
from pathlib import Path
from typing import List, Dict, Optional


class FileProcessor:
    """批量文件处理工具类"""

    def __init__(self, source_dir: str):
        self.source_dir = Path(source_dir)
        self.stats: Dict[str, int] = {"processed": 0, "skipped": 0, "errors": 0}

    def list_files(self, pattern: str = "*") -> List[Path]:
        """列出匹配的文件"""
        if not self.source_dir.exists():
            return []
        return list(self.source_dir.glob(pattern))

    def process_file(self, file_path: Path) -> bool:
        """处理单个文件"""
        try:
            content = file_path.read_text(encoding="utf-8")
            lines = content.splitlines()
            word_count = len(content.split())

            result = {
                "filename": file_path.name,
                "line_count": len(lines),
                "word_count": word_count,
                "size_bytes": file_path.stat().st_size
            }
            print(f"✓ {file_path.name}: {len(lines)}行, {word_count}词")
            self.stats["processed"] += 1
            return True
        except Exception as e:
            print(f"✗ {file_path.name}: {e}")
            self.stats["errors"] += 1
            return False

    def batch_process(self, pattern: str = "*.txt") -> Dict[str, int]:
        """批量处理文件"""
        files = self.list_files(pattern)
        print(f"\n发现 {len(files)} 个文件:\n")

        for file_path in files:
            if file_path.is_file():
                self.process_file(file_path)

        print(f"\n处理完成: {self.stats}")
        return self.stats


if __name__ == "__main__":
    processor = FileProcessor(".")
    processor.batch_process("*.py")
