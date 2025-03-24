import wx
import wx.xrc
import wx.dataview
from .ui_part_list_panel import UiPartListPanel
from .part_list_model import PartListModel
import wx.dataview as dv


class PartListView(UiPartListPanel):
    def __init__(
        self,
        parent,
        id=wx.ID_ANY,
        pos=wx.DefaultPosition,
        size=wx.DefaultSize,
        style=wx.TAB_TRAVERSAL,
        name=wx.EmptyString,
    ):
        super().__init__(parent, id=id, pos=pos, size=size, style=style, name=name)
        # self.part_list.EnableSelectionCopy(True)
        self.index = self.part_list.AppendTextColumn(
            _("index"), width=60, mode=dv.DATAVIEW_CELL_ACTIVATABLE, align=wx.ALIGN_CENTER
        )
        self.mpn = self.part_list.AppendTextColumn(
            _("MPN"), 
            width=150, 
            mode=dv.DATAVIEW_CELL_ACTIVATABLE, 
            align=wx.ALIGN_CENTER,
            flags=dv.DATAVIEW_COL_RESIZABLE,
        )
        self.manfacturer = self.part_list.AppendTextColumn(
            _("Manufacturer"),
            width=250,
            mode=dv.DATAVIEW_CELL_ACTIVATABLE,
            align=wx.ALIGN_CENTER,
        )
        self.footprint = self.part_list.AppendTextColumn(
            _("Package/Footprint"),
            width=250,
            mode=dv.DATAVIEW_CELL_ACTIVATABLE,
            align=wx.ALIGN_CENTER,
        )
        self.p_list = self.part_list.AppendTextColumn(
            _("Category"),
            width=150,
            mode=dv.DATAVIEW_CELL_ACTIVATABLE,
            align=wx.ALIGN_CENTER,
        )
        self.sku = self.part_list.AppendTextColumn(
            _("SKU"), width=150, mode=dv.DATAVIEW_CELL_ACTIVATABLE, align=wx.ALIGN_CENTER
        )
        self.sku = self.part_list.AppendTextColumn(
           _("Price /Pc.")+"(￥)", width=100, mode=dv.DATAVIEW_CELL_ACTIVATABLE, align=wx.ALIGN_CENTER
        )
        self.part_list.AppendTextColumn(
            " ",
            width=1,
            mode=dv.DATAVIEW_CELL_INERT, align=wx.ALIGN_CENTER,
            flags=dv.DATAVIEW_COL_RESIZABLE,
        )
        
    def init_data_view(self, part_list_data):
        
        self.PartListModel = PartListModel( part_list_data )
        
        self.part_list.AssociateModel(self.PartListModel)
    
        wx.CallAfter(self.part_list_data_panel.Layout)
        
    def update_view(self):
        self.Layout()
        