from ImageHandler import *

hwnd = get_aqw_hwnd()
img = get_screenshot_of_window(hwnd, (0, 0, 1920, 300))
img.show()
