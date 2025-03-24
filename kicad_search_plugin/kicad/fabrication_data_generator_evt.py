import wx
import wx.lib.newevent


import wx


class GenerateStatus:
    FAILED = 0
    RUNNING = 1
    SUCCESS = 2

    MAX_PROGRESS = 1000

    def __init__(self, status: int, msg: str = "", progress: int = -1) -> None:
        self._status = status
        self._msg = msg
        self._progress = progress

    def get_status(self):
        return self._status

    def get_message(self):
        return self._msg

    def get_progress(self):
        return self._progress


fabricationDataGenerateResult = wx.NewEventType()
EVT_BUTTON_FABRICATION_DATA_GEN_RES = wx.PyEventBinder(fabricationDataGenerateResult, 1)


class FabricationDataGenEvent(wx.PyCommandEvent):
    def __init__(self, evtType, id=wx.ID_ANY):
        wx.PyCommandEvent.__init__(self, evtType, id)
        self._status: GenerateStatus = None

    def set_status(self, val: GenerateStatus):
        self._status = val

    def get_status(self):
        return self._status
