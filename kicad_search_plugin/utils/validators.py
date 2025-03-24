import wx


class NumericTextCtrlValidator(wx.Validator):
    def __init__(self):
        wx.Validator.__init__(self)

    def Clone(self):
        return NumericTextCtrlValidator()

    def Validate(self, parent):
        text_ctrl = self.GetWindow()
        value = text_ctrl.GetValue()
        if value.isdigit():
            text_ctrl.SetBackgroundColour(
                wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW)
            )
            text_ctrl.Refresh()
            return True
        else:
            text_ctrl.SetBackgroundColour(wx.Colour(255, 128, 128))
            text_ctrl.Refresh()
            return False

    def TransferToWindow(self):
        return True

    def TransferFromWindow(self):
        return True


class FloatTextCtrlValidator(wx.Validator):
    def __init__(self):
        wx.Validator.__init__(self)

    def Clone(self):
        return FloatTextCtrlValidator()

    def Validate(self, parent):
        text_ctrl = self.GetWindow()
        value = text_ctrl.GetValue()
        if value.isdigit():
            text_ctrl.SetBackgroundColour(
                wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW)
            )
            text_ctrl.Refresh()
            return True
        elif value.replace(".", "", 1).isdigit() and value.count(".") < 2:
            text_ctrl.SetBackgroundColour(
                wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW)
            )
            text_ctrl.Refresh()
            return True
        else:
            text_ctrl.SetBackgroundColour(wx.Colour(255, 128, 128))
            text_ctrl.Refresh()
            return False

    def TransferToWindow(self):
        return True

    def TransferFromWindow(self):
        return True
