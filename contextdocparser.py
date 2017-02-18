import os
import sys
import yaml
import winreg
import glob
import importlib
import ctypes

class ContextDocParser:
	def __init__(self,document,main):
		self.doc = document
		self.main = main
		self.documentObject = yaml.load(document)
		self.contextName = self.documentObject["name"]
		self.contextTitle = self.documentObject["title"]
		self.SPECIAL_FEXT_LIST ={	"^allfiles" 	: "*", 
									"^desktop" 		: "DesktopBackground", 
									"^directory"	: "Directory", 
									"^directoryba"	: "Directory\\Background", 
									"^folder"		: "Folder", 
									"^folderba"		: "Folder\\Background", 
									"^drive"		: "Drive",
									"^driveba"		: "Drive\\Background" }
		self.actionslist = {}
		self.iconslist = {}
		self.titleslist = {}
		self.out = []
	def run(self):
		# Runs the command tree. Basically, this translates the YAML into
		# a whole bunch of nested lists.
		self.load_extensions()
		self.traverse_tree(self.documentObject["tree"],self.out)
		self.out.reverse()
	def load_extensions(self):
		# Loads the extensions contained in the "actions" and "icon" folders.
		# NEW: titles can be added too, from the "title" folder.
		for item in glob.glob("actions/*.py"):
			mod = importlib.import_module(item[0:-3].replace("\\","."))
			for ex in mod.exports:
				self.actionslist[ex.name] = ex
		for item in glob.glob("icons/*.py"):
			mod = importlib.import_module(item[0:-3].replace("\\","."))
			for ex in mod.exports:
				self.iconslist[ex.name] = ex
		for item in glob.glob("titles/*.py"):
			mod = importlib.import_module(item[0:-3].replace("\\","."))
			for ex in mod.exports:
				self.titleslist[ex.name] = ex
	def make_action(self,action):
		# Takes an action tree and returns an initialized action class.
		return self.actionslist[action['handler']](**action)
	def make_icon(self,icon):
		# Takes an icon tree and returns an initialized icon class.
		return self.iconslist[icon['handler']](**icon)
	def make_title(self,title):
		# Takes an title tree and returns an initialized title class.
		return self.titleslist[title['handler']](**title)
	def make_action_def(self,command):
		# Takes an action name and returns an initialized CommandAction class.
		return self.actionslist['command']('command',command)
	def make_icon_def(self,iconname):
		# Takes an icon file and returns an initialized FileIcon class.
		return self.iconslist['file']('file',iconname)
	def make_title_def(self,title):
		# Takes an title tree and returns an initialized StringTitle class.
		return self.titleslist['string']('string',title)
	def traverse_tree(self,mainList,outx):
		# Recursively looks through tree and adds to main list.
		for itemName, itemValue in mainList.items():
			flags = {}
			if "separator" in itemValue:
				if itemValue["separator"] == True:
					flags["separator"] = True
				else:
					flags["separator"] = False
			else:
				flags["separator"] = False
			if "disabled" in itemValue:
				if itemValue["disabled"] == True:
					flags["disabled"] = True
				else:
					flags["disabled"] = False
			else:
				flags["disabled"] = False
			if "highlight" in itemValue:
				if itemValue["highlight"] == True:
					flags["highlight"] = True
				else:
					flags["highlight"] = False
			else:
				flags["highlight"] = False
			if "icon" in itemValue:
				if type(itemValue["icon"]) == type(""):
					ico = self.make_icon_def(itemValue["icon"])
				elif type(itemValue["icon"]) == type({}):
					ico = self.make_icon(itemValue["icon"])
				else:
					ico = None
			else:
				ico = None
			if type(itemValue["title"]) == type(""):
				title = self.make_title_def(itemValue["title"])
			elif type(itemValue["title"]) == type({}):
				title = self.make_title(itemValue["title"])
			else:
				title = None
			if "action" in itemValue:
				if type(itemValue["action"]) == type(""):
					act = self.make_action_def(itemValue["action"])
				elif type(itemValue["action"]) == type({}):
					act = self.make_action(itemValue["action"])
				else:
					act = None
				outx.append([title,ico,act,flags])
			elif "tree" in itemValue:
				outx.append([title,ico,[],flags])
				self.traverse_tree(itemValue['tree'],outx[-1][2])
				outx[-1][2].reverse()
	def install(self):
		# Installs registry keys, effectively initializing the script.
		self.verify_uac()
		exe = sys.executable
		exe = sys.executable.replace("python.exe","pythonw.exe")
		for fext in self.generate_fexts(self.documentObject["exists"]):
			fk = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT,fext+"\\shell\\" \
				+self.documentObject["name"])
			fsk = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT,fext+"\\shell\\" \
				+self.documentObject["name"]+"\\command")
			winreg.SetValueEx(fk,"",0,winreg.REG_SZ, \
				self.documentObject["title"])
			if self.documentObject["icon"]:
				winreg.SetValueEx(fk,"Icon",0,winreg.REG_SZ, \
				self.documentObject["icon"])
			winreg.SetValueEx(fsk,"",0,winreg.REG_SZ,exe+" \""\
				+os.path.realpath(self.main+"\" \""\
				+os.path.realpath(self.doc.name))+"\" run %1")
	def remove(self):
		# Removes registry keys cleanly.
		self.verify_uac()
		for fext in self.generate_fexts(self.documentObject["exists"]):
			winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT,fext+"\\shell\\"\
				+self.documentObject["name"]+"\\command")
			winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT,fext+"\\shell\\"\
				+self.documentObject["name"])
	def verify_uac(self):
		# Verifies that the use is an admin, so no errors are produced.
		isen = None
		try:
			isen = ctypes.windll.shell32.IsUserAnAdmin()
		except:
			isen = False
		if isen == False:
			print("Administrator privileges are needed to install...")
			sys.exit(0)
	def generate_fexts(self,exists):
		# Helper to generate a list of registry keys.
		fextlist = []
		for exist in exists:
			if exist.startswith("^"):
				if exist == "^everything":
					return self.SPECIAL_FEXT_LIST.values()
				elif exist in self.SPECIAL_FEXT_LIST:
					fextlist.append(self.SPECIAL_FEXT_LIST[exist])
			else:
				fextlist.append(exist)
		return fextlist