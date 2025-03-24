import os

ICON_ROOT = os.path.dirname(__file__)


def GetImagePath(bitmap_path):
    return os.path.join(ICON_ROOT, bitmap_path)
