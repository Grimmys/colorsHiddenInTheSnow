import re


def get_base_name(sprite_name):
    res = re.search('.+?((?=_left)|(?=_right)|(?=_top)|(?=_bottom)|(?=_center)|(?=_middle))', sprite_name)
    if res:
        return res.group(0)
    return None