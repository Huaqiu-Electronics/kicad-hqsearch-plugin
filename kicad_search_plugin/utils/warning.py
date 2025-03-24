import wx

class SilentLogTarget(wx.LogStderr):
    def DoLogRecord(self, level, msg, time):
        # 只记录非警告级别的日志消息
        if level != wx.LOG_Warning:
            super(SilentLogTarget, self).DoLogRecord(level, msg, time)
