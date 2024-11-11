import sys

MIN_VERSION = (3, 10)

def check_python_version():
    current_version = sys.version_info[:3]

    if current_version < MIN_VERSION:
        raise RuntimeError(f"当前Python版本为{current_version[0]}.{current_version[1]}, 请使用至少Python {MIN_VERSION[0]}.{MIN_VERSION[1]}及以上的版本.")
