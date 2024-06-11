import functools
# import get_current_weather from tools.weather_tools
from .weathertools import get_current_weather, get_today_pollen_level

TOOL_NAMES_TO_FUNCTIONS = {
    "get_current_weather": functools.partial(get_current_weather),
    "get_today_pollen_level": functools.partial(get_today_pollen_level),
}

