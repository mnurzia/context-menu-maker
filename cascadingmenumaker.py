# Much of this code was taken from Simon Brunning's SysTrayIcon.py.
# I used most of the code pertaining to creating a popup menu.
import os
import sys
import win32api
import win32con
import win32gui_struct
import win32gui

class CascadingMenuMaker:
	def __init__(self,options,docObj):
		self.menu_options = options
		self.action_map = {}
		# Initializes win32gui components
		self.window_class = win32gui.WNDCLASS()
		self.documentObject = docObj
		self.hinst = self.window_class.hInstance = \
					 win32gui.GetModuleHandle(None)
		self.message_map = {win32con.WM_COMMAND: self.callback,
							win32con.WM_DESTROY: self.destroy,
							win32con.WM_UNINITMENUPOPUP: self.destroy}
		self.window_class.lpfnWndProc = self.message_map
		self.window_menu_name = self.documentObject["title"]
		self.window_class_name = "Python.ContextMenu."+ \
								 self.documentObject["name"].upper()
		self.number_ids(self.menu_options,0)
		self.create_window()
	def number_ids(self,menu_opts,onum):
		# Recursively gives numerical UIDs to objects in the command tree.
		for opt in menu_opts:
			if type(opt[2]) == type([]):
				opt.append(onum)
				onum += 1
				onum = self.number_ids(opt[2],onum)
			else:
				opt.append(onum)
				self.action_map[onum] = opt[2]
				onum += 1
		return onum
	def create_window(self):
		# Creates the dummy invisible window that the popup will come from.
		self.window_class.lpszMenuName = self.window_menu_name
		self.window_class.lpszClassName = self.window_class_name
		self.classAtom = win32gui.RegisterClass(self.window_class)
		self.style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
		self.hwnd = win32gui.CreateWindow(self.classAtom,
										  self.window_class_name,
										  self.style,
										  0,
										  0,
										  win32con.CW_USEDEFAULT,
										  win32con.CW_USEDEFAULT,
										  0,
										  0,
										  self.hinst,
										  None)
		win32gui.UpdateWindow(self.hwnd)
		self.notify_id = None
		self.add_popup()
		win32gui.PumpMessages()
	def add_popup(self):
		# Creates the popup from the dummy window.
		menu = win32gui.CreatePopupMenu()
		self.create_menu(menu,self.menu_options)
		pos = win32gui.GetCursorPos()
		win32gui.SetForegroundWindow(self.hwnd)
		win32gui.TrackPopupMenu(menu,
								win32con.TPM_LEFTALIGN,
								pos[0],
								pos[1],
								0,
								self.hwnd,
								None)
		win32gui.PostMessage(self.hwnd, win32con.WM_NULL, 0, 0)
	def create_menu(self, menu, menopts):
		# Inserts all items into the popup (again, recursive)
		for opt in menopts:
			if opt[1] != None:
				opt_icon = opt[1].get()
			else:
				opt_icon = None
			mi_fstate = 0
			mi_ftype = 0
			if opt[3]["disabled"]:
				mi_fstate = mi_fstate | win32con.MFS_DISABLED
			if opt[3]["highlight"]:
				mi_fstate = mi_fstate | win32con.MFS_HILITE
			if opt[3]["separator"]:
				mi_ftype = mi_ftype | win32con.MFT_SEPARATOR
			if type(opt[2]) == type([]):
				submenu = win32gui.CreatePopupMenu()
				self.create_menu(submenu, opt[2])
				item, extras = win32gui_struct.PackMENUITEMINFO(
														text=opt[0].get(),
														hbmpItem=opt_icon,
														hSubMenu=submenu,
														fState=mi_fstate,
														fType=mi_ftype,
														wID=opt[-1])
			else:
				item, extras = win32gui_struct.PackMENUITEMINFO(
														text=opt[0].get(),
														hbmpItem=opt_icon,
														fState=mi_fstate,
														fType=mi_ftype,
														wID=opt[-1])
			win32gui.InsertMenuItem(menu, 0, 1, item)
	def destroy(self, hwnd, msg, wparam, lparam):
		# Called from win32gui when we want to quit.
		self.destroy_nothing()
	def destroy_nothing(self):
		# Called by other things when we want to quit.
		win32gui.PostQuitMessage(0)
	def callback(self, hwnd, msg, wparam, lparam):
		# Called when the user clicks an item.
		self.destroy_nothing()
		self.action_map[win32gui.LOWORD(wparam)].run()
		sys.exit(0)