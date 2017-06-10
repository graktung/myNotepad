import wx
import wx.lib.dialogs
import wx.stc as stc
import os
from webbrowser import open_new_tab

class MainWindow(wx.Frame):
	def __init__(self, parent, title):
		self.filename = ''
		self.dirname = ''
		self.lineNumbersEnabled = True
		self.leftMarginWidth = 30

		wx.Frame.__init__(self, parent, title=title, size=(800, 600))
		self.control = stc.StyledTextCtrl(self, style=wx.TE_MULTILINE | wx.TE_WORDWRAP)

		self.control.CmdKeyAssign(ord('='), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMIN)
		self.control.CmdKeyAssign(ord('-'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMOUT)

		self.control.SetViewWhiteSpace(False)
		self.control.SetMargins(5, 5)
		self.control.SetMarginType(1, stc.STC_MARGIN_NUMBER)
		self.control.SetMarginWidth(1, self.leftMarginWidth)

		self.CreateStatusBar()
		self.StatusBar.SetBackgroundColour((220, 220, 220))

		fileMenu = wx.Menu()
		menuNew = fileMenu.Append(wx.ID_NEW, "New                    Ctrl + N", "Create new document")
		menuOpen = fileMenu.Append(wx.ID_OPEN, "Open                  Ctrl + O", "Open existing document")
		menuSave = fileMenu.Append(wx.ID_SAVE, "Save                    Ctrl + S", "Save the current document")
		menuSaveAs = fileMenu.Append(wx.ID_SAVEAS, "Save As               Ctrl + Shift  + S", "Save a new document")
		fileMenu.AppendSeparator()
		menuClose = fileMenu.Append(wx.ID_EXIT, "Close                  Ctrl + W", "Close the application")

		editMenu = wx.Menu()
		menuUndo = editMenu.Append(wx.ID_UNDO, "Undo                   Ctrl + Z", "Undo last action")
		menuRedo = editMenu.Append(wx.ID_REDO, "Redo                    Ctrl + Y", "Redo last action")
		editMenu.AppendSeparator()
		menuSelectAll = editMenu.Append(wx.ID_SELECTALL, "Select All             Ctrl + A", "Select the entire document")
		menuCopy = editMenu.Append(wx.ID_COPY, "Copy                    Ctrl + C", "Copy selected text")
		menuCut = editMenu.Append(wx.ID_CUT, "Cut                       Ctrl + X", "Cut selected text")
		menuPaste = editMenu.Append(wx.ID_PASTE, "Paste                    Ctrl + V", "Paste text from the clipboard")

		prefMenu = wx.Menu()
		menuLineNumbers = prefMenu.Append(wx.ID_ANY, "Show/Hide Line Numbers", "Show/Hide line numbers column")

		helpMenu = wx.Menu()
		menuGithub = helpMenu.Append(wx.ID_ANY, "Github                 F1", "Link github")
		helpMenu.AppendSeparator()
		menuAbout = helpMenu.Append(wx.ID_ABOUT, "About                  F2", "About the author")

		menuBar = wx.MenuBar()
		menuBar.Append(fileMenu, "File")
		menuBar.Append(editMenu, "Edit")
		menuBar.Append(prefMenu, "Preferences")
		menuBar.Append(helpMenu, "Info")
		self.SetMenuBar(menuBar)

		self.Bind(wx.EVT_MENU, self.onNew, menuNew)
		self.Bind(wx.EVT_MENU, self.onOpen, menuOpen)
		self.Bind(wx.EVT_MENU, self.onSave, menuSave)
		self.Bind(wx.EVT_MENU, self.onSaveAs, menuSaveAs)
		self.Bind(wx.EVT_MENU, self.onClose, menuClose)

		self.Bind(wx.EVT_MENU, self.onUndo, menuUndo)
		self.Bind(wx.EVT_MENU, self.onRedo, menuRedo)
		self.Bind(wx.EVT_MENU, self.onSelectAll, menuSelectAll)
		self.Bind(wx.EVT_MENU, self.onCopy, menuCopy)
		self.Bind(wx.EVT_MENU, self.onCut, menuCut)
		self.Bind(wx.EVT_MENU, self.onPaste, menuPaste)

		self.Bind(wx.EVT_MENU, self.onToggleLineNumbers, menuLineNumbers)

		self.Bind(wx.EVT_MENU, self.onGithub, menuGithub)
		self.Bind(wx.EVT_MENU, self.onAbout, menuAbout)

		self.control.Bind(wx.EVT_KEY_UP, self.updateLineCol)
		self.control.Bind(wx.EVT_CHAR, self.onCharEvent)

		self.Show()
		self.updateLineCol(self)

	def onNew(self, e):
		self.filename = ''
		self.control.SetValue("")

	def onOpen(self, e):
		try:
			dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.FD_OPEN)
			if dlg.ShowModal() == wx.ID_OK:
				self.filename = dlg.GetFilename()
				self.dirname = dlg.GetDirectory()
				with open(os.path.join(self.dirname, self.filename)) as f:
					self.control.SetValue(f.read())
					f.close()
			dlg.Destroy()
		except:
			dlg = wx.MessageDialog(self, "Couldn't open the file", "Error", wx.ICON_ERROR)
			dlg.ShowModal()
			dlg.Destroy()

	def onSave(self, e):
		try:
			with open(os.path.join(self.dirname, self.filename), 'w') as f:
				f.write(self.control.GetValue())
				f.close()
		except:
			try:
				dlg = wx.FileDialog(self, "Save file as", self.dirname, "Untitled", "*.*", wx.FD_SAVE |\
					wx.FD_OVERWRITE_PROMPT)
				if dlg.ShowModal() == wx.ID_OK:
					self.filename = dlg.GetFilename()
					self.dirname = dlg.GetDirectory()
					with open(os.path.join(self.dirname, self.filename), 'w') as f:
						f.write(self.control.GetValue())
						f.close()
				dlg.Destroy()
			except:
				pass

	def onSaveAs(self, e):
		try:
			dlg = wx.FileDialog(self, "Save file as", self.dirname, "Untitled", "*.*", wx.FD_SAVE |\
				wx.FD_OVERWRITE_PROMPT)
			if dlg.ShowModal() == wx.ID_OK:
				self.filename = dlg.GetFilename()
				self.dirname = dlg.GetDirectory()
				with open(os.path.join(self.dirname, self.filename), 'w') as f:
					f.write(self.control.GetValue())
					f.close()
			dlg.Destroy()
		except:
			pass		

	def onClose(self, e):
		self.Close(True)

	def onUndo(self, e):
		self.control.Undo()

	def onRedo(self, e):
		self.control.Redo()

	def onSelectAll(self, e):
		self.control.SelectAll()

	def onCopy(self, e):
		self.control.Copy()

	def onCut(self, e):
		self.control.Cut()

	def onPaste(self, e):
		self.control.Paste()

	def onToggleLineNumbers(self, e):
		if self.lineNumbersEnabled:
			self.control.SetMarginWidth(1, 0)
			self.lineNumbersEnabled = False
		else:
			self.control.SetMarginWidth(1, self.leftMarginWidth)
			self.lineNumbersEnabled = True

	def onGithub(self, e):
		open_new_tab('https://github.com/graktung/myNotepad')

	def onAbout(self, e):
		open_new_tab('https://www.facebook.com/356a4368')

	def updateLineCol(self, e):
		line = self.control.GetCurrentLine() + 1
		col = self.control.GetColumn(self.control.GetCurrentPos())
		stat = "Line %s, Column %s" %(line, col)
		self.StatusBar.SetStatusText(stat, 0)

	def onCharEvent(self, e):
		keyCode = e.GetKeyCode()
		altDown = e.AltDown()
		if keyCode == 14: # Ctrl + N
			self.onNew(self)
		elif keyCode == 15: # Ctrl + O
			self.onOpen(self)
		elif keyCode == 19: # Ctrl + S
			self.onSave(self)
		elif altDown and keyCode == 19: # Alt + S
			self.onSaveAs(self)
		elif keyCode == 23: # Ctrl + W
			self.onClose(self)
		elif keyCode == 340: # F1
			self.onGithub(self)
		elif keyCode == 341: # F2
			self.onAbout(self)
		else:
			e.Skip()

app = wx.App()
frame = MainWindow(None, "Gr^k-T's Notepad+++")
app.MainLoop()