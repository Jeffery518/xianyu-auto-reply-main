import sys
from unittest.mock import MagicMock
sys.modules['aiohttp'] = MagicMock()
sys.modules['PIL'] = MagicMock()
from utils.xianyu_slider_stealth import XianyuSliderStealth
try:
    instance = XianyuSliderStealth("test_user_1", None)
    instance.generate_human_trajectory(distance=200, attempt=2)
    print("Success")
except Exception as e:
    import traceback
    traceback.print_exc()
