import json
import time
import webbrowser
import requests
from threading import Thread
import wx

from kicad_search_plugin.kicad.fabrication_data_generator import FabricationDataGenerator
from kicad_search_plugin.order.order_region import URL_KIND, OrderRegion
from kicad_search_plugin.settings.setting_manager import SETTING_MANAGER
from .fabrication_data_generator_evt import (
    FabricationDataGenEvent,
    fabricationDataGenerateResult,
    GenerateStatus,
)


class DataGenThread(Thread):
    def __init__(self, win: wx.Window, gen: FabricationDataGenerator, form, url):
        super().__init__()
        self.win = win
        self.fabrication_data_generator = gen
        self.place_order_form = form
        self._url = url
        self.start()

    def run(self):
        try:
            steps = (
                (
                    _("Create fabrication data folder"),
                    self.fabrication_data_generator.create_folders,
                ),
                (_("Fill zones"), self.fabrication_data_generator.fill_zones),
                (_("Generate gerber"), self.fabrication_data_generator.generate_geber),
                (
                    _("Generate excellon"),
                    self.fabrication_data_generator.generate_excellon,
                ),
                (
                    _("Zip gerber and excellon file"),
                    self.fabrication_data_generator.zip_gerber_excellon,
                ),
            )

            for idx_step in enumerate(steps):
                (
                    idx,
                    step,
                ) = idx_step
                desc, action = step
                evt = FabricationDataGenEvent(fabricationDataGenerateResult)
                evt.set_status(
                    GenerateStatus(
                        GenerateStatus.RUNNING,
                        desc,
                        int((idx + 1) * GenerateStatus.MAX_PROGRESS / (len(steps) + 1)),
                    )
                )
                wx.PostEvent(self.win, event=evt)
                action()

            evt = FabricationDataGenEvent(fabricationDataGenerateResult)
            evt.set_status(
                GenerateStatus(
                    GenerateStatus.RUNNING,
                    _("Sending order request"),
                    GenerateStatus.MAX_PROGRESS - 1,
                )
            )
            wx.PostEvent(self.win, event=evt)
            rsp = requests.post(
                self._url,
                files={
                    "file": open(self.fabrication_data_generator.zip_file_path, "rb")
                },
                data=self.place_order_form,
            )
            urls = json.loads(rsp.content)
            for key in "url", "redirect":
                if key in urls:
                    uat_url = str(urls[key])
                    webbrowser.open(uat_url)
                    evt = FabricationDataGenEvent(fabricationDataGenerateResult)
                    evt.set_status(GenerateStatus(GenerateStatus.SUCCESS))
                    wx.PostEvent(self.win, event=evt)
                    return
            raise Exception("No available order url in the response")
        except Exception as e:
            evt = FabricationDataGenEvent(fabricationDataGenerateResult)
            evt.set_status(GenerateStatus(GenerateStatus.FAILED, str(e)))
            wx.PostEvent(self.win, event=evt)
