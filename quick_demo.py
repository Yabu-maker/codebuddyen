import time
import random
import string
import datetime
import hashlib
from typing import Any

def format_size(size_bytes: float) -> str:
    if size_bytes < 0:
        raise ValueError("字节大小不能为负数")
        
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f}{unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f}ZB"

def generate_id(prefix: str = 'ID', length: int = 4, use_digits_only: bool = True) -> str:
    if length <= 0:
        raise ValueError("随机部分长度必须大于0")
        
    choices = string.digits if use_digits_only else string.ascii_letters + string.digits
    random_part = "".join(random.choices(choices, k=length))
    return f"{prefix}_{random_part}"

def get_time(ms: bool = False) -> int:
    t = time.time()
    return int(t * 1000) if ms else int(t)

def get_timestamp(format_str: str | None = None) -> str:
    if format_str:
        return datetime.datetime.now().strftime(format_str)
    return str(get_time())

def get_file_hash(file_path: str, algo: str = "md5") -> str:
    try:
        h = hashlib.new(algo)
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return ""

def get_nested(data: dict[str, Any], path: str, default: Any = None) -> Any:
    try:
        val: Any = data
        for k in path.split("."):
            val = val[k]
        return val
    except Exception:
        return default


def get_random_why() -> str:
    whys = [
        "为什么天空是蓝色的？",
        "为什么海水是咸的？",
        "为什么人会做梦？",
        "为什么太阳会发光发热？",
        "为什么雨后会出现彩虹？",
        "为什么猫在高处也能平稳落地？",
        "为什么有些植物会向阳生长？",
        "为什么冰会浮在水面上？",
        "为什么月亮有圆缺变化？",
        "为什么打哈欠会传染？",
        "为什么火焰会向上燃烧？",
        "为什么地球会有四季？",
        "为什么有些鸟会迁徙？",
        "为什么人需要睡觉？",
        "为什么有些金属会生锈？",
        "为什么风会吹？",
        "为什么耳朵能听到声音？",
        "为什么眼睛会近视？",
        "为什么星星会闪烁？",
        "为什么时间总感觉过得很快？"
    ]
    return random.choice(whys)


if __name__ == "__main__":
    print("文件大小 (1500000 B):", format_size(1500000))
    print("文件大小 (3.5 TB):", format_size(3.5 * 1024 * 1024 * 1024 * 1024))
    print("生成默认数字ID (USER):", generate_id("USER"))
    print("生成混合字母数字ID (APP):", generate_id("APP", length=8, use_digits_only=False))
    print("当前秒级时间戳:", get_time())
    print("当前毫秒级时间戳:", get_time(ms=True))
    print("当前秒时间戳字符串:", get_timestamp())
    print("格式化当前日期时间:", get_timestamp("%Y-%m-%d %H:%M:%S"))
    print("当前脚本的 MD5 哈希:", get_file_hash(__file__))
    test_dict = {"a": {"b": {"c": 42}}}
    print("多层字典安全取值 (a.b.c):", get_nested(test_dict, "a.b.c"))
    print("多层字典安全取值 (a.x.y) 默认值:", get_nested(test_dict, "a.x.y", "Not Found"))
    print("十万个为什么:", get_random_why())