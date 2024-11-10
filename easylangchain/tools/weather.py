from langchain_core.tools import tool

weathers = {
    "北京": {"2024-11-10": "晴", "2024-11-11": "多云"},
    "上海": {"2024-11-10": "小雨", "2024-11-11": "多云"},
}

@tool
def get_weather(location: str, date: str = "2024-11-10") -> str:
    """Get the weather of a location on a specific date.
    Args:
        location: The location to get the weather of.
        date: The date to get the weather of. defaults to 2024-11-10.
    """
    return weathers[location][date]

@tool
def get_north_or_south(location: str,) -> str:
    """获取是北方城市还是南方城市
    """
    return {
        "北京": "north",
        "上海": "south"
    }[location]
