import logging

import wx
import requests
import wx.dataview
from requests.exceptions import Timeout
from .ui_part_details_panel.part_details_view import PartDetailsView
from .ui_search_panel.search_view import SearchView
from .ui_part_list_panel.part_list_view import PartListView
import time
import threading
import logging
from requests.exceptions import Timeout, ConnectionError, HTTPError

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

ID_SELECT_PART = wx.NewIdRef()

COLUM_SKU = 5

MAX_PART_COUNT = 500

def ceil(x, y):
    return -(-x // y)

class PartSelectorframe( wx.Frame ):
    def __init__(self, parent=None):
        wx.SizerFlags.DisableConsistencyChecks()
        wx.Frame.__init__(
            self,
            parent,
            id=wx.ID_ANY,
            title=_(" HQ Search "),
            pos=wx.DefaultPosition,
            size=  wx.Size(1200, 800),
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.MAXIMIZE_BOX,
        )

        self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )

        self.logger = logging.getLogger(__name__)
        self.parent = parent
        parts ={'C4': '22pF,C_Disc_D3.0mm_W2.0mm_P2.50mm,,'}
        self.parts = parts

        self.current_page = 0
        self.total_pages = 0
        self.one_page_size =24
        self.is_searching = False
        
        self.last_call_time = 0  # 记录上一次事件触发的时间
        self.throttle_interval = 0.4  # 设置时间间隔，单位为秒
        self.page_last_call_time = 0  # 记录上一次事件触发的时间
        self.page_throttle_interval = 4  # 设置时间间隔，单位为秒
        self.thread = None


        part_selection = self.get_existing_selection(parts)
        self.part_info = part_selection.split(",")

        self.part_details_view = PartDetailsView(self)
        self.search_view = SearchView(self)
        self.part_list_view = PartListView(self)
        # ---------------------------------------------------------------------
        # ---------------------------- Hotkeys --------------------------------
        # ---------------------------------------------------------------------
        quitid = wx.NewId()
        self.Bind(wx.EVT_MENU, self.quit_dialog, id=quitid)

        entries = [wx.AcceleratorEntry(), wx.AcceleratorEntry(), wx.AcceleratorEntry()]
        entries[0].Set(wx.ACCEL_CTRL, ord("W"), quitid)
        entries[1].Set(wx.ACCEL_CTRL, ord("Q"), quitid)
        entries[2].Set(wx.ACCEL_SHIFT, wx.WXK_ESCAPE, quitid)
        accel = wx.AcceleratorTable(entries)
        self.SetAcceleratorTable(accel)

        # ---------------------------------------------------------------------
        # ---------------------------- bind events ----------------------------
        # ---------------------------------------------------------------------
        self.search_view.description.SetValue(
            self.part_info[0]+ "  " + self.part_info[1] + "  " +  self.part_info[2] + "  " + self.part_info[3] 
        )
        self.search_view.description.Bind(wx.EVT_SEARCH, self.search_delay)
        self.search_view.mpn_textctrl.Bind(wx.EVT_TEXT_ENTER, self.search_delay)
        self.search_view.manufacturer.Bind(wx.EVT_TEXT_ENTER, self.search_delay)
        self.search_view.search_button.Bind(wx.EVT_BUTTON, self.search_delay)

        self.part_list_view.part_list.Bind(
            wx.dataview.EVT_DATAVIEW_COLUMN_HEADER_CLICK, self.search_delay
        )
        self.part_list_view.part_list.Bind(
            wx.dataview.EVT_DATAVIEW_SELECTION_CHANGED, self.on_part_selected_timer_event
        )

        self.part_list_view.part_list.Bind(
            wx.dataview.EVT_DATAVIEW_ITEM_CONTEXT_MENU, self.on_right_down
        )
        


        self.part_list_view.prev_button.Bind(wx.EVT_BUTTON, self.on_prev_page)
        self.part_list_view.next_button.Bind(wx.EVT_BUTTON, self.on_next_page)
        self.update_page_label()

        # self.part_list_view.select_part_button.Bind(wx.EVT_BUTTON, self.select_part)
        # self.part_list_view.select_part_button.SetBitmap(
        #     loadBitmapScaled(
        #         "nextpcb-select-part.png",
        #     )
        # )

        self.enable_toolbar_buttons(False)
        # ---------------------------------------------------------------------
        # ------------------------------ layout  ------------------------------
        # ---------------------------------------------------------------------
        bSizer2 = wx.BoxSizer(wx.VERTICAL)
        bSizer2.Add(self.search_view, 0, wx.EXPAND, 5)
        bSizer2.Add(self.part_list_view, 1, wx.LEFT | wx.EXPAND, 5)

        bSizer1 = wx.BoxSizer(wx.HORIZONTAL)
        bSizer1.Add(bSizer2, 15, wx.EXPAND | wx.ALL, 5)
        bSizer1.Add(self.part_details_view, 7, wx.EXPAND | wx.ALL, 0)

        layout = wx.BoxSizer(wx.VERTICAL)

        layout.Add(bSizer1, 1, wx.EXPAND, 5)

        self.SetSizer(layout)
        self.Layout()
        self.Centre(wx.BOTH)


    @staticmethod
    def get_existing_selection(parts):
        """Check if exactly one LCSC part number is amongst the selected parts."""
        s = set(val for val in parts.values())
        return list(s)[0]

    def quit_dialog(self, e):
        self.Destroy()
        self.EndModal(0)

    def OnSortPartList(self, e):
        """Set order_by to the clicked column and trigger list refresh."""
        self.search(e)


    def enable_toolbar_buttons(self, state):
        """Control the state of all the buttons in toolbar on the right side"""
        pass
        # for b in [
        #     self.part_list_view.select_part_button,
        # ]:
        #     b.Enable(bool(state))

    def search_delay(self, e):
        """Search the library for parts that meet the search criteria."""
        current_time = time.time()
        if current_time - self.page_last_call_time < self.page_throttle_interval :
            return  # 如果时间间隔小于设定的阈值，则不处理事件
        self.page_last_call_time = current_time
        self.search( e )

    def search(self, e):
        """Search the library for parts that meet the search criteria."""
        if self.current_page == 0:
            self.current_page = 1

        if self.search_view.mpn_textctrl.GetValue():
            # body_value = self.search_view.mpn_textctrl.GetValue()
        
            body_value1 = self.search_view.mpn_textctrl.GetValue()
            body_value2 = self.search_view.manufacturer.GetValue()
            body = {
                "mpn": body_value1,
                "mfg": body_value2
            }
            url = "http://www.fdatasheets.com/api/chiplet/kicad/queryByMpn"

        else: 
            body_value = self.search_view.description.GetValue()

        # word_count = len(body_value.split())
        # if word_count >= 4:
        #     body = {
        #         "data":[
        #             {
        #                 "filterName":"mpns",
        #                 "filterDetails":[
        #                     {
        #                         "textParam":self.part_info[2]
        #                     },
        #                     {
        #                         "textParam":""
        #                     }
        #                 ]
        #             },
        #             {
        #                 "filterName":"manufacturers",
        #                 "filterDetails":[
        #                     {
        #                         "textParam":self.part_info[3]
        #                     }
        #                 ]
        #             }
        #         ],
        #         "desc": self.part_info[0] + " " + self.part_info[1],
        #         "pageNum": self.current_page,
        #         "pageSize": self.one_page_size
        #     }
        # else:
            body = {
                "desc": body_value,
                "pageNum": self.current_page,
                "pageSize": self.one_page_size
            }
            url = "https://www.eda.cn/api/chiplet/products/queryPage"
        wx.BeginBusyCursor()
        self.search_view.search_button.Disable()
        try:
            
            self.search_api_request(url, body)
        finally:
            wx.EndBusyCursor()
            self.search_view.search_button.Enable()
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
    def search_api_request(self, url, data):
        response = self.api_request_interface(url, data )
        self.search_part_list = []
        datas = response.json()
        res_datas = datas.get("result", {})
        if not res_datas:
            wx.MessageBox( _("No corresponding data was matched") )
            return
        self.total_num = response.json().get("total", -1)
        if self.total_num == -1:
            self.total_num = 10
        if self.total_num == 0:
            self.current_page = 0
        if self.total_num > MAX_PART_COUNT:
            self.total_num = MAX_PART_COUNT
            
        for item in res_datas:
            if item.get("queryPartVO", {}).get("part", {}):
                search_part = item.get("queryPartVO", {}).get("part", {})
            else:
                search_part = item.get("part", {})             
            self.search_part_list.append(search_part)
        wx.CallAfter(self.populate_part_list)



    def populate_part_list(self):
        """Populate the list with the result of the search."""
        if self.search_part_list is None:
            return
        self.total_pages = ceil(self.total_num, self.one_page_size)
        self.update_page_label()
        self.part_list_view.result_count.SetLabel(_("{total} Results").format(total=self.total_num))
        if self.total_num >= MAX_PART_COUNT:
            self.part_list_view.result_count.SetLabel(_("{max_part_count} Results" ).format(max_part_count=MAX_PART_COUNT))
        else:
            self.part_list_view.result_count.SetLabel(_("{total} Results").format(total=self.total_num))

        parameters = ["mpn", "manufacturer", "pkg", "category", "sku", "price"]
        body = []
        if not self.search_part_list: 
            print("Search results are empty with no data to process.")
            return
        
        for part_info in self.search_part_list:
            manu_id = part_info.get("manufacturer_id", {})
            mpn = part_info.get("mpn", {})
            body_value = ( f"{manu_id}-{mpn}" )
            body.append(body_value)
        part_list_data = []
        
        for idx, part_info in enumerate(self.search_part_list, start=1):
            sku = "-" 
            price = "-"
            mpn = part_info["mpn"]
            part_info["sku"] = sku
            part_info["price"] = price

            # 确保idx-1不会超出列表的范围
            if idx-1 < len(self.search_part_list):
                self.search_part_list[idx-1]["sku"] = sku
            part = []
            for k in parameters:
                if k == "price":
                    val = "-"
                    prices_stair = part_info.get(k, "-")
                    if prices_stair != "-":
                        for index, price_range in enumerate(prices_stair):
                            val = str(price_range["rmb"])
                            val = "-" if val == "0.0" else val
                            break
                else:
                    val = part_info.get(k, "")
                    val = "-" if val == "" else val
                part.append(val)
            part.insert(0, f"{idx}")
            part_list_data.append(part)
        self.part_list_view.init_data_view(part_list_data)
        
        # thread = threading.Thread(target=self.search_supply_chain, args=(body, parameters))
        # # 启动线程
        # thread.start()
        wx.BeginBusyCursor()
        if self.thread is not None:
            self.thread.join()  # 等待线程结束

        # 创建并启动新线程
        self.thread = threading.Thread(target=self.search_supply_chain, args=(body, parameters))
        self.thread.start()
        wx.EndBusyCursor()




    def search_supply_chain(self, body, parameters ):
        part_list_data = []
        url = "https://www.eda.cn/api/chiplet/kicad/searchSupplyChain"
        response = self.api_request_interface( url, body )
        res_datas = response.json().get("result", {})
        if not response.json():
            wx.MessageBox( _("No corresponding sku data was matched") )

        for idx, part_info in enumerate(self.search_part_list, start=1):
            sku = "-" 
            price = "-"
            mpn = part_info["mpn"]
            for data in res_datas:
                if data.get("mpn") == mpn and data.get("vendor") == "hqself":
                    sku = data.get("sku", "-") 
                    price = data.get("price", "-") 
                    break 
            part_info["sku"] = sku
            part_info["price"] = price

            # 确保idx-1不会超出列表的范围
            if idx-1 < len(self.search_part_list):
                self.search_part_list[idx-1]["sku"] = sku
            part = []
            for k in parameters:
                if k == "price":
                    val = "-"
                    prices_stair = part_info.get(k, "-")
                    if prices_stair != "-":
                        for index, price_range in enumerate(prices_stair):
                            val = str(price_range["rmb"])
                            val = "-" if val == "0.0" else val
                            break
                else:
                    val = part_info.get(k, "")
                    val = "-" if val == "" else val
                part.append(val)
            part.insert(0, f"{idx}")
            part_list_data.append(part)
        self.part_list_view.init_data_view(part_list_data)


    def api_request_interface(self, url, data ):
        headers = {"Content-Type": "application/json"}
        try:
            response = requests.post(url, headers=headers, json=data, timeout = 30)
            response.raise_for_status()
            return response
        except Timeout:
            self.report_part_search_error(_("HTTP request timed out"))
        except (ConnectionError, HTTPError) as e:
            self.report_part_search_error(_("HTTP error occurred: {error}").format(error=e))
        except Exception as e:
            self.report_part_search_error(_("An unexpected HTTP error occurred: {error}").format(error=e))


    # def select_part(self, e):
    #     """Save the selected part number and close the modal."""
    #     item = self.part_list_view.part_list.GetSelection()
    #     row = self.part_list_view.part_list.ItemToRow(item)
    #     if row == -1:
    #         return
    #     selection = self.part_list_view.part_list.GetValue(row, 1)
    #     manu = self.part_list_view.part_list.GetValue(row, 2)
    #     cate = self.part_list_view.part_list.GetValue(row, 4)
    #     sku = self.part_list_view.part_list.GetValue(row, 5)
    #     price = self.part_list_view.part_list.GetValue(row, 6)
    #     self.selected_part = self.search_part_list[row]
    #     evt = AssignPartsEvent(
    #         mpn=selection,
    #         manufacturer=manu,
    #         category=cate,
    #         sku=sku,
    #         price=price,
    #         references=list(self.parts.keys()),
    #         selected_part_detail=self.selected_part,
    #     )
    #     wx.PostEvent(self.parent, evt)
    #     self.EndModal(wx.ID_OK)

    def cancel_selcetion(self ):
        item = self.part_list_view.part_list.GetSelection()
        if item.IsOk():
            self.part_list_view.part_list.Unselect(item)
            self.part_details_view.initialize_data()


    def on_part_selected_timer_event(self, event):
        current_time = time.time()
        if current_time - self.last_call_time < self.throttle_interval or current_time - self.page_last_call_time  < self.throttle_interval :
            return  # 如果时间间隔小于设定的阈值，则不处理事件
        self.last_call_time = current_time
        self.on_part_selected()

    def on_part_selected(self):
        """Enable the toolbar buttons when a selection was made."""
        if self.part_list_view.part_list.GetSelectedItemsCount() > 0:
            self.enable_toolbar_buttons(True)
        else:
            self.enable_toolbar_buttons(False)

        item = self.part_list_view.part_list.GetSelection()
        row = self.part_list_view.part_list.ItemToRow(item)
        if item is None or row == -1:
            return 
        self.clicked_part = self.search_part_list[row]
        if self.clicked_part != "":
            try:
                wx.BeginBusyCursor()
                wx.CallAfter(self.part_details_view.get_part_data ,self.clicked_part )

            finally:
                wx.EndBusyCursor()
        else:
            wx.MessageBox(
                _("Failed to get clicked part from NextPCB"),
                _("Error"),
                style=wx.ICON_ERROR,
            )

    def on_prev_page(self, event):
        current_time = time.time()
        if current_time - self.page_last_call_time < self.page_throttle_interval :
            return  # 如果时间间隔小于设定的阈值，则不处理事件
        self.page_last_call_time = current_time
        if self.current_page > 1:
            self.current_page -= 1
            self.update_page_label()
            self.search(None)
            self.cancel_selcetion()
            

    def on_next_page(self, event):
        current_time = time.time()
        if current_time - self.page_last_call_time < self.page_throttle_interval :
            return  # 如果时间间隔小于设定的阈值，则不处理事件
        self.page_last_call_time = current_time
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.update_page_label()
            self.search(None)
            self.cancel_selcetion()


    def update_page_label(self):
        self.part_list_view.page_label.SetLabel(
            f" {self.current_page}/{self.total_pages} "
        )
        self.part_list_view.update_view()

    def help(self, e):
        """Show message box with help instructions"""
        title = _("Help")
        text ="""
        Use % as wildcard selector. \n
        For example DS24% will match DS2411\n
        %QFP% wil match LQFP-64 as well as TQFP-32\n
        The keyword search box is automatically post- and prefixed with wildcard operators.
        The others are not by default.\n
        The keyword search field is applied to "LCSC Part", "Description", "MFR.Part",
        "Package" and "Manufacturer".\n
        Enter triggers the search the same way the search button does.\n
        The results are  500.
        """
        wx.MessageBox(text, title, style=wx.ICON_INFORMATION)

    def report_part_search_error(self, reason):
        wx.MessageBox(
            _("Failed to download part detail from the BOM API:\r\n{reasons}\r\n").format(reasons=reason),
            _("Error"),
            style=wx.ICON_ERROR,
        )

    def on_right_down(self, e):
        conMenu = wx.Menu()
        selcet_part = wx.MenuItem(conMenu, ID_SELECT_PART, _("Select Part") )
        conMenu.Append(selcet_part)
        conMenu.Bind(wx.EVT_MENU, self.select_part, selcet_part)
        item = self.part_list_view.part_list.GetSelection()
        row = self.part_list_view.part_list.ItemToRow(item)
        if row == -1:
            return
        conMenu.Enable(ID_SELECT_PART, True)
        self.part_list_view.part_list.PopupMenu(conMenu)
        conMenu.Destroy()

