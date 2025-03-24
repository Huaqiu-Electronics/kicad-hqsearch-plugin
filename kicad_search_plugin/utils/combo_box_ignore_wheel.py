import wx


class ComboBoxIgnoreWheel(wx.Choice):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.wheel_evt_handle = None
        self.parent_can_hand_wheel = True

    def ProcessEvent(self, evt: wx.Event):
        if evt.EventType == wx.wxEVT_MOUSEWHEEL:
            if self.parent_can_hand_wheel and self.wheel_evt_handle is not None:
                self.wheel_evt_handle.HandleWindowEvent(evt)
            if not self.wheel_evt_handle:
                p = self.Parent
                while p:
                    if p.HandleWindowEvent(evt):
                        self.wheel_evt_handle = p
                        return True
                    p = p.Parent
                self.parent_can_hand_wheel = False
            return True
        return super().ProcessEvent(evt)
