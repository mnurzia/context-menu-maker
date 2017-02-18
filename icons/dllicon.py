import win32api
import win32gui
import win32con

class DllFileIconHandler:
	name = "dll"
	def __init__(self,handler,dll,id):
		self.dll = dll
		self.id = id
		self.hbm = self.prep()
	def prep(self):
		ico_x = win32api.GetSystemMetrics(win32con.SM_CXSMICON)
		ico_y = win32api.GetSystemMetrics(win32con.SM_CYSMICON)
		lr, sm = win32gui.ExtractIconEx(self.dll,self.id)
		win32gui.DestroyIcon(lr[0])
		hicon = sm[0]
		hdcBitmap = win32gui.CreateCompatibleDC(0)
		hdcScreen = win32gui.GetDC(0)
		hbm = win32gui.CreateCompatibleBitmap(hdcScreen, ico_x, ico_y)
		hbmOld = win32gui.SelectObject(hdcBitmap, hbm)
		brush = win32gui.GetSysColorBrush(win32con.COLOR_MENU)
		win32gui.FillRect(hdcBitmap, (0, 0, 16, 16), brush)
		win32gui.DrawIconEx(hdcBitmap, 0, 0, hicon, ico_x, ico_y, 0, 0, win32con.DI_NORMAL)
		win32gui.SelectObject(hdcBitmap, hbmOld)
		win32gui.DeleteDC(hdcBitmap)
		return hbm
	def get(self):
		return self.hbm
		
exports = [DllFileIconHandler]