from kicad_search_plugin.order.supported_region import SupportedRegion
from .setting_manager import SETTING_MANAGER

MAPPING = {
    "N/A": "无",
    "Left & Right": "左右",
    "Top & Bottom": "上下",
    "All 4 sides": "四边",
    "Green": "绿色",
    "Red": "红色",
    "Yellow": "黄色",
    "Blue": "蓝色",
    "White": "白色",
    "Matte Black": "哑黑",
    "Black": "黑色",
    "Solder Mask Plug (IV-B)": "过孔塞油墨",
    "Tenting Vias": "过孔盖油",
    "Vias not covered": "过孔开窗",
    "Non-Conductive Fill & Cap (VII)": "过孔塞树脂+电镀填平",
    "HASL": "有铅喷锡",
    "Lead free HASL": "无铅喷锡",
    "ENIG": "沉金",
    "Have": "有",
}


def fitter_and_map_form_value(fn):
    def wrapper(*args, **kwargs):
        form: "dict" = fn(*args, **kwargs)
        new_form = {}
        for i in form:
            if form[i] is None:
                continue
            if (
                SETTING_MANAGER.order_region == SupportedRegion.CHINA_MAINLAND
                and form[i] in MAPPING
            ):
                new_form[i] = MAPPING[form[i]]
            else:
                new_form[i] = form[i]
        return new_form

    return wrapper
