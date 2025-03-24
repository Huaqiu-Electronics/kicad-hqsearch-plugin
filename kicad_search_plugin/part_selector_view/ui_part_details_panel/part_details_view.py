import wx
import wx.xrc
import wx.dataview
import requests
import webbrowser
import io
import logging
from .ui_part_details_panel import UiPartDetailsPanel
import wx.dataview as dv
import threading

from requests.exceptions import Timeout, ConnectionError, HTTPError
from .part_details_model import PartDetailsModel
import pcbnew
import json
import os
from kicad_search_plugin.utils.warning import SilentLogTarget


parameters = {
    "mpn": _("MPN"),
    "manufacturer": _("Manufacturer"),
    "pkg": _("Package / Footprint"),
    "category": _("Category"),
    "part_desc": _("Description"),
    "datasheet":_("Datasheet"),
    "sku": _("SKU"),
}

class PartDetailsView(UiPartDetailsPanel):
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
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.part_details_data=[]

        # ---------------------------------------------------------------------
        # ----------------------- Properties List -----------------------------
        # ---------------------------------------------------------------------
        self.property = self.data_list.AppendTextColumn(
            _("Property"),
            width=180,
            mode=dv.DATAVIEW_CELL_ACTIVATABLE,
            align=wx.ALIGN_LEFT,
        )
        self.value = self.data_list.AppendTextColumn(
            _("Value"), width=-1, mode=dv.DATAVIEW_CELL_ACTIVATABLE, align=wx.ALIGN_LEFT
        )
        self.data_list.Bind(wx.dataview.EVT_DATAVIEW_SELECTION_CHANGED, self.on_open_pdf)
        self.data_list.Bind(wx.dataview.EVT_DATAVIEW_SELECTION_CHANGED, self.on_show_more_info)
        self.data_list.Bind(wx.dataview.EVT_DATAVIEW_SELECTION_CHANGED, self.on_tooltip)

        log_target = SilentLogTarget()
        wx.Log.SetActiveTarget(log_target)
        
        self.init_UI()
        self.get_language_setting()

    def init_UI(self):
        for k, v in parameters.items():
            self.part_details_data.append([v, " "])
        self.PartDetailsModel = PartDetailsModel( self.part_details_data )
        self.data_list.AssociateModel(self.PartDetailsModel)
        wx.CallAfter(self.m_panel3.Layout)


    def initialize_data(self):
        self.PartDetailsModel.DeleteAll()
        for k, v in parameters.items():
            self.PartDetailsModel.AddRow([v, " "])
        self.part_image.SetBitmap(wx.NullBitmap)
        self.Layout()

    def on_open_pdf(self, event):
        """Open the linked datasheet PDF on button click."""
        item = self.data_list.GetSelection()
        row = self.data_list.ItemToRow(item)
        if item is None or row == -1:
            return 
        datasheet = self.data_list.GetTextValue(row, 0)
        if datasheet == _("Datasheet"): 
            if self.pdfurl != "-" :
                self.logger.info("opening %s", str(self.pdfurl))
                filename_pos = self.pdfurl.find('filename=')
                if filename_pos != -1:
                    query_pos = self.pdfurl.rfind('?')
                    if query_pos != -1:
                        self.pdfurl = self.pdfurl[:query_pos]

                if not self.pdfurl.startswith('http'):
                    self.pdfurl = 'http:' + self.pdfurl
                webbrowser.open(self.pdfurl)
        else:
            self.logger.debug(f"pdf trigger link error")
        event.Skip()

    def show_image(self, picture):
        if picture:
            self.logger.debug(f"image: {self.get_scaled_bitmap(picture)}")
            if self.get_scaled_bitmap(picture) is None:
                self.part_image.SetBitmap(wx.NullBitmap)
            else:
                self.part_image.SetBitmap(self.get_scaled_bitmap(picture))
        else:
            self.part_image.SetBitmap(wx.NullBitmap)
        self.Layout()

    def get_scaled_bitmap(self, url):
        """Download a picture from a URL and convert it into a wx Bitmap"""
        # 确保 URL 是一个完整的网址，添加 https:// 如果缺失
        if not url.startswith("http:") and not url.startswith("https:"):
            url = "https:" + url
        self.logger.debug(f"image_count: {url}")
        header = {
             "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"    
        }

        try:
            response = requests.get(url, headers=header)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            content = response.content
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error downloading image: {e}")
            return None
        if not content:
            return None
        bitmap = self.display_bitmap(content)
        return bitmap



    def display_bitmap(self, content):
        io_bytes = io.BytesIO(content)
        sb_size = self.part_image.GetSize()
        min_dimension = min(sb_size.GetWidth(), sb_size.GetHeight())
        if min_dimension <= 0:
            self.report_part_data_fetch_error( 
                _("The width and height of new size must be greater than 0")
            )
            return
        wx.InitAllImageHandlers()
        try:
            from PIL import Image
            image = Image.open(io_bytes)

            # Scale the image
            factor = min_dimension / max(image.width, image.height) 
            new_width = int(image.width * factor)
            new_height = int(image.height * factor)
            resized_image = image.resize((new_width, new_height), Image.LANCZOS)
            wx_image = wx.Image(new_width, new_height)
            wx_image.SetData(resized_image.convert('RGB').tobytes())
            
        except (IOError, SyntaxError,ImportError) as e:
            try:
                wx_image = wx.Image(io_bytes, wx.BITMAP_TYPE_ANY, -1)
                if not wx_image.IsOk():
                    return None
                
                # Scale the image
                factor = min_dimension / max(wx_image.GetWidth(), wx_image.GetHeight())
                new_width = int(wx_image.GetWidth() * factor)
                new_height = int(wx_image.GetHeight() * factor)
                wx_image = wx_image.Rescale(new_width, new_height )
                bitmap = wx_image.ConvertToBitmap()

                self.part_image.SetBitmap(bitmap)
            except Exception as e:
                # Handle the error if the image file is not valid
                print(f"Error opening image: {e}")
                return None

        if not wx_image.IsOk():
            self.logger.error("The wx.Image is not valid.")
            return None
        result = wx.Bitmap(wx_image)
        return result



    def get_part_data(self, _clicked_part):
        """fetch part data from NextPCB API and parse it into the table, set picture and PDF link"""
        if _clicked_part == "":
            self.report_part_data_fetch_error(
                _("returned data does not have expected clicked part")
            )
        self.clicked_part = _clicked_part
        self.PartDetailsModel.DeleteAll()

        manu_id = self.clicked_part.get("manufacturer_id", "-")
        mpn = self.clicked_part.get("mpn", "-")
        self.show_more_body = {
            "leaderPartId": "",
            "manufacturer_id": manu_id,
            "mpn": mpn
            }


        self.part_details_data.clear()
        for k, v in parameters.items():
            val = self.clicked_part.get(k, "-")
            if val != "null" and val:
                self.PartDetailsModel.AddRow([v, str(val)])
            else:
                self.PartDetailsModel.AddRow( [v, "-"] )
    
        prices_stair = self.clicked_part.get("price", [])
        if prices_stair == "-":
            self.PartDetailsModel.AddRow([_("Price"), "-"])
        else:
            # Populate price_echelon based on prices_stair data
            price_echelon = {}
            for index, price_range in enumerate(prices_stair):
                break_min = price_range.get("breakMin")
                break_max = price_range.get("breakMax")
                if break_max is 0:
                    key = f">{break_min} " + _("Piece")+"(￥)"
                else:
                    key = f"{break_min}-{break_max} " + _("Piece")+"(￥)"

                val = str( price_range["rmb"] )
                price_echelon[key] = "-" if val == "0.0" else val
            # Populate self.data_list with the key-value pairs
            for key, value in price_echelon.items():
                self.PartDetailsModel.AddRow([key, value ])

        self.PartDetailsModel.AddRow( [_("Show more"), ""] )
        self.data_list.Refresh()


        self.pdfurl = self.clicked_part.get("datasheet", {})
        self.pdfurl = "-" if self.pdfurl == "" else self.pdfurl

        picture = self.clicked_part.get("image", [])
        threading.Thread(target= self.show_image,args=(picture, ) ).start()


    def on_show_more_info(self, event):
        item = self.data_list.GetSelection()
        row = self.data_list.ItemToRow(item)
        if item is None or row == -1:
            return 
        show_more = self.data_list.GetTextValue(row, 0)
        if show_more == _("Show more"): 
            url = "https://www.eda.cn/api/chiplet/products/productDetail"

            response = self.api_request_interface( url, self.show_more_body )
            res_datas = response.json().get("result", {})
            if not response.json():
                wx.MessageBox( _("No corresponding sku data was matched") )
            
            self.PartDetailsModel.DeleteRows( [row] )
            extraction_datas =  res_datas.get("groupAttrInfoVOList", {})
            for res_data in extraction_datas:
                for data in res_data.get("attrInfoVO", "-"):
                    if not data:
                        return
                    if self.lang.count("中文"):
                        property = data.get("attrName", "-")
                        value = data.get("attrValue", "-")
                        self.PartDetailsModel.AddRow( [property, value] )
                    else:
                        property = data.get("attrShortName", "-")
                        value = data.get("attrValue", "-")
                        self.PartDetailsModel.AddRow( [property, value] )
                        
            self.data_list.Refresh()
        event.Skip()

    def get_language_setting(self):
        kicad_setting_path = str(pcbnew.SETTINGS_MANAGER.GetUserSettingsPath())
        if len(kicad_setting_path):
            kicad_common_json = os.path.join(
                kicad_setting_path, "kicad_common.json"
            )
            with open(kicad_common_json) as f:
                data = json.loads(f.read())
                self.lang: str = data["system"]["language"]

    def report_part_data_fetch_error(self, reason):
        mpn = self.clicked_part.get('mpn', "-")
        wx.MessageBox(
            _("Failed to download part detail: {reason}\r\nWe looked for a part named:\r\n{mpn} \r\n").format(reason=reason ,mpn = mpn),
            _("Error"),
            style=wx.ICON_ERROR,
        )


    def on_tooltip(self, event):
        selected_item = self.data_list.GetSelectedRow()
        if selected_item >= 0:
            data = self.data_list.GetValue(selected_item, 1)
            tip = wx.ToolTip("{}".format(data))
            self.data_list.SetToolTip(tip)
            tip.Enable(True)
        else:
            self.data_list.SetToolTip(None)
        event.Skip()



    def api_request_interface(self, url, data ):
        headers = {"Content-Type": "application/json"}
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            return response
        except Timeout:
            self.report_part_search_error(_("HTTP request timed out"))
        except (ConnectionError, HTTPError) as e:
            self.report_part_search_error(_("HTTP error occurred: {error}").format(error=e))
        except Exception as e:
            self.report_part_search_error(_("An unexpected HTTP error occurred: {error}").format(error=e))


    def report_part_search_error(self, reason):
        wx.MessageBox(
            _("Failed to download part detail from the BOM API:\r\n{reasons}\r\n").format(reasons=reason),
            _("Error"),
            style=wx.ICON_ERROR,
        )
