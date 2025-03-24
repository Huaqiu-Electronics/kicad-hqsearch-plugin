import wx
import wx.xrc


from .ui_search_panel import UiSearchPanel



class SearchView(UiSearchPanel):
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.TAB_TRAVERSAL, name=wx.EmptyString):
        super().__init__(parent, id=id, pos=pos, size=size, style=style, name=name)


        self.mpn_textctrl.SetHint("e.g. 123456")
        self.manufacturer.SetHint("e.g. Vishay")
