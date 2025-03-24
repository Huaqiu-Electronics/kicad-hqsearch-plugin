from kicad_search_plugin.language.lang_const import LANG_DOMAIN
from kicad_search_plugin.settings.supported_layer_count import AVAILABLE_LAYER_COUNTS
import builtins
import sys
import os
from kicad_search_plugin import PLUGIN_ROOT
from kicad_search_plugin.kicad.board_manager import load_board_manager
from kicad_search_plugin.utils.combo_box_ignore_wheel import ComboBoxIgnoreWheel
from kicad_search_plugin.icon import GetImagePath
import wx
from kicad_search_plugin.settings.setting_manager import SETTING_MANAGER

# add translation macro to builtin similar to what gettext does
builtins.__dict__["_"] = wx.GetTranslation
wx.Choice = ComboBoxIgnoreWheel


def _displayHook(obj):
    if obj is not None:
        print(repr(obj))


class BaseApp(wx.EvtHandler):
    def __init__(self):
        super().__init__()
        sys.displayhook = _displayHook
        wx.Locale.AddCatalogLookupPathPrefix(
            os.path.join(PLUGIN_ROOT, "language", "locale")
        )
        existing_locale = wx.GetLocale()
        if existing_locale is not None:
            existing_locale.AddCatalog(LANG_DOMAIN)
        self.progress_dialog = wx.ProgressDialog(_("Open Software"), _("In progress") )
        self.progress_dialog.Update( 30 )

    def load_success(self):
        from kicad_search_plugin.settings.setting_manager import SETTING_MANAGER
        SETTING_MANAGER.register_app(self)
        self.board_manager = load_board_manager()
        if self.board_manager.board.GetCopperLayerCount() not in AVAILABLE_LAYER_COUNTS:
            wx.MessageBox(_("Unsupported layer count!"))
            return False
        return True

    def startup_dialog(self):
        # from kicad_search_plugin.gui.main_frame import MainFrame
        # from kicad_search_plugin.settings.setting_manager import SETTING_MANAGER
        # from kicad_search_plugin.kicad_nextpcb_new.mainwindow import NextPCBTools
        
        from kicad_search_plugin.part_selector_view.part_selector import PartSelectorframe


        self.dialog = PartSelectorframe()
        self.dialog.SetIcon(wx.Icon(GetImagePath("HQS.ico")))
        self.dialog.Show()
        
        # self.progress_dialog.Update( 60 )
        # self.main_wind = MainFrame(
        #     self.board_manager, SETTING_MANAGER.get_window_size()
        # )
        # self.main_wind.SetIcon(wx.Icon(GetImagePath("Huaqiu.ico")))
        # self.main_wind.Show()

        self.progress_dialog.Update( 100 )
        self.progress_dialog.Destroy()

    def __del__(self):
        self.progress_dialog.Destroy()
        