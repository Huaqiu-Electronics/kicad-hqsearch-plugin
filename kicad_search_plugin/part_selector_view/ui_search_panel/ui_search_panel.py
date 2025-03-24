# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.0.0-0-g0efcecf)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc


###########################################################################
## Class UiSearchPanel
###########################################################################

class UiSearchPanel ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 711,78 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer7 = wx.BoxSizer( wx.VERTICAL )

		bSizer9 = wx.BoxSizer( wx.VERTICAL )

		self.description = wx.SearchCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		self.description.ShowSearchButton( True )
		self.description.ShowCancelButton( False )
		bSizer9.Add( self.description, 0, wx.ALIGN_TOP|wx.EXPAND, 5 )


		bSizer7.Add( bSizer9, 0, wx.EXPAND, 5 )

		bSizer8 = wx.BoxSizer( wx.HORIZONTAL )

		self.mpn_textctrl_label = wx.StaticText( self, wx.ID_ANY, _("MPN: "), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.mpn_textctrl_label.Wrap( -1 )

		bSizer8.Add( self.mpn_textctrl_label, 0, wx.ALIGN_CENTER|wx.ALL|wx.BOTTOM, 5 )

		self.mpn_textctrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,-1 ), wx.TE_PROCESS_ENTER )
		bSizer8.Add( self.mpn_textctrl, 1, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.manufacturer_label = wx.StaticText( self, wx.ID_ANY, _("Manufacturer: "), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.manufacturer_label.Wrap( -1 )

		bSizer8.Add( self.manufacturer_label, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.manufacturer = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,-1 ), wx.TE_PROCESS_ENTER )
		bSizer8.Add( self.manufacturer, 1, wx.ALIGN_CENTER|wx.ALL, 5 )


		bSizer8.Add( ( 50, 0), 0, wx.EXPAND, 5 )

		self.search_button = wx.Button( self, wx.ID_ANY, _("Search"), wx.DefaultPosition, wx.Size( 100,28 ), 0 )
		bSizer8.Add( self.search_button, 0, wx.ALIGN_CENTER|wx.RIGHT, 5 )


		bSizer7.Add( bSizer8, 0, wx.EXPAND, 5 )


		self.SetSizer( bSizer7 )
		self.Layout()

	def __del__( self ):
		pass

