# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.0.0-0-g0efcecf)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.dataview

import gettext
_ = gettext.gettext

###########################################################################
## Class UiPartListPanel
###########################################################################

class UiPartListPanel ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 644,-1 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer2 = wx.BoxSizer( wx.VERTICAL )

		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )

		self.result_count = wx.StaticText( self, wx.ID_ANY, _(u"0 Results"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.result_count.Wrap( -1 )

		bSizer4.Add( self.result_count, 0, wx.ALL|wx.LEFT, 5 )

		self.prompt_info = wx.InfoBar( self )
		self.prompt_info.SetShowHideEffects( wx.SHOW_EFFECT_NONE, wx.SHOW_EFFECT_NONE )
		self.prompt_info.SetEffectDuration( 1 )
		bSizer4.Add( self.prompt_info, 0, wx.EXPAND, 0 )


		bSizer2.Add( bSizer4, 0, wx.EXPAND, 5 )

		self.part_list_data_panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer51 = wx.BoxSizer( wx.VERTICAL )

		self.part_list = wx.dataview.DataViewListCtrl( self.part_list_data_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer51.Add( self.part_list, 1, wx.ALL|wx.EXPAND, 5 )


		self.part_list_data_panel.SetSizer( bSizer51 )
		self.part_list_data_panel.Layout()
		bSizer51.Fit( self.part_list_data_panel )
		bSizer2.Add( self.part_list_data_panel, 1, wx.EXPAND |wx.ALL, 0 )

		bSizer1 = wx.BoxSizer( wx.HORIZONTAL )


		bSizer1.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.prev_button = wx.Button( self, wx.ID_ANY, _(u"Previous"), wx.DefaultPosition, wx.Size( 70,26 ), 0 )
		bSizer1.Add( self.prev_button, 0, wx.ALIGN_CENTER|wx.ALL, 10 )

		bSizer5 = wx.BoxSizer( wx.HORIZONTAL )

		self.page_label = wx.StaticText( self, wx.ID_ANY, _(u"0/1000"), wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.page_label.Wrap( -1 )

		self.page_label.SetFont( wx.Font( 14, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "宋体" ) )

		bSizer5.Add( self.page_label, 0, wx.ALL|wx.EXPAND|wx.LEFT, 5 )


		bSizer1.Add( bSizer5, 0, wx.ALIGN_CENTER|wx.ALIGN_LEFT|wx.ALIGN_RIGHT|wx.ALL, 5 )

		self.next_button = wx.Button( self, wx.ID_ANY, _(u"Next"), wx.DefaultPosition, wx.Size( 70,26 ), 0 )
		bSizer1.Add( self.next_button, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		bSizer1.Add( ( 0, 0), 1, wx.EXPAND, 5 )


		bSizer2.Add( bSizer1, 0, wx.EXPAND, 5 )


		self.SetSizer( bSizer2 )
		self.Layout()

	def __del__( self ):
		pass


