import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QListWidgetItem
from gui import *
from banner import *
from GlobalVariables import *
from SSHSession import *
from Application import *
import json
import sqlite3
import webbrowser
import plistlib
import os

class Main:
	def __init__(self, mainWin):
		self.mainWin=mainWin
		self.globalVariables=GlobalVariables()
		self.objSSHClient = None
		self.applications = None

	def SSHConnection(self):
		host=self.mainWin.txtIPAddress.text()
		port=self.mainWin.txtPort.text()
		username=self.mainWin.txtUsername.text()
		password=self.mainWin.txtPassword.text()
		self.objSSHClient = SSHSession(host,port,username,password)
		self.applications = Application(self.objSSHClient, self.mainWin) 
		self.applications.FillAppInList()

	def SelectApplication(self):
		if self.applications.CopyBundleAndDataDirectory(self.mainWin.listApplication.selectedItems()[0].text()):
			self.FillApplicationInformation()

	def FillApplicationInformation(self):
		self.mainWin.lblBundleUUID.setText(self.applications.currentSelectedAppBundleUUID)
		self.mainWin.lblDataUUID.setText(self.applications.currentSelectedAppDataUUID)
		self.mainWin.lblLocalPath.setText("Local directory path : ./Output/{}".format(self.applications.currentSelectedAppName))
		plistFile = "./Output/{}/Bundle/{}/Info.plist".format(self.applications.currentAppName, self.applications.currentSelectedAppName)
		with open(plistFile, 'rb') as fp :
			plist_content = plistlib.loads(fp.read())
			self.mainWin.lblBundleID.setText(plist_content['CFBundleIdentifier'])
			self.mainWin.lblBundleName.setText(plist_content['CFBundleName'])
			self.mainWin.lblBundleVersion.setText(plist_content['CFBundleVersion'])
			self.mainWin.lblPlatformVersion.setText(plist_content['DTPlatformVersion'])
			self.mainWin.lblMinimumOS.setText(plist_content['MinimumOSVersion'])

	def ForceDownloadCodeFromDevice(self):
		self.applications.CopyBundleAndDataDirectory(self.mainWin.listApplication.selectedItems()[0].text(), True)
		self.mainWin.lblDataUUID.setText(self.applications.currentSelectedAppDataUUID)

	def RunMobSFTool(self):
		isSuccess, session_id=self.globalVariables.InitializeMobSFVariables()
		if isSuccess:
			self.applications.CreateIPAFileFromSource()
			ipaPath = "./Output/{}/{}.ipa".format(self.applications.currentAppName, self.applications.currentAppName)
			command = "curl -F \"file=@{}\" {}/api/v1/upload -H \"Authorization:{}\" -H \"Cookie: sessionid= {}\"".format(ipaPath, self.globalVariables.mobSFURL, self.globalVariables.mobSFAPIKey, session_id)
			print (command)
			self.globalVariables.ExecuteCommand(command)
			webbrowser.open_new_tab("{}/recent_scans/".format(self.globalVariables.mobSFURL))

	def DisplayPListFileContent(self, path):
		try:
			with open(path, "rb") as f:  # binary mode
				data = plistlib.load(f)
			self.mainWin.txtFilePreview.setPlainText(str(data))
		except Exception as e:
			self.mainWin.txtFilePreview.setPlainText(f"[Plist Error]\n{e}")

	def DisplayTextFileContent(self, path):
		try:
			with open(path, "r", encoding="utf-8", errors="ignore") as f:
				data = f.read()

			beautified = None
			try:
				parsed = json.loads(data)# Check if valid JSON
				beautified = json.dumps(parsed, indent=4, ensure_ascii=False)
			except Exception:
				pass  # Not JSON → fallback to plain text

			if beautified:
				self.mainWin.txtFilePreview.setPlainText(beautified)
			else:
				self.mainWin.txtFilePreview.setPlainText(data)
		except Exception as e:
			self.mainWin.txtFilePreview.setPlainText(f"[Text Error]\n{e}")

	def DisplayDatabaseFileContent(self, path):
		try:
			conn = sqlite3.connect(path)
			cursor = conn.cursor()

			# Fetch all table names
			cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
			tables = cursor.fetchall()

			if not tables:
				self.mainWin.txtFilePreview.setPlainText("No tables found in database.")
				return

			# Start output
			output = []
			output.append(f"SQLite Database: {path}")

			for (table_name,) in tables:
				output.append("\n\n=== TABLE: {} ===".format(table_name))

				try:
					# Read table content
					cursor.execute(f"SELECT * FROM {table_name}")
					rows = cursor.fetchall()
					colnames = [desc[0] for desc in cursor.description]

					# Header row
					header = " | ".join(colnames)
					separator = "-" * len(header)

					output.append(separator)
					output.append(header)
					output.append(separator)

					# Add each row
					for row in rows:
						safe_row = " | ".join(str(col) for col in row)
						output.append(safe_row)

					output.append(separator)

				except Exception as te:
					output.append(f"[Error reading table {table_name}] {te}")

			# Update UI
			self.mainWin.txtFilePreview.setPlainText("\n".join(output))

		except Exception as e:
			self.mainWin.txtFilePreview.setPlainText(f"[SQLite Error]\n{e}")

	def ShowDirectoryViewOfApplication(self):
		if self.applications == None or self.applications.currentAppName == "":
			self.globalVariables.ShowErrorDailog(self.mainWin, "Application not select in App Info tab")
			self.mainWin.tabWidget.setCurrentIndex(1)
		else:
			dirPath = "{}/Output/{}".format(os.getcwd(), self.applications.currentAppName)
			self.mainWin.treeView.setRootIndex(self.mainWin.dirModel.index(dirPath))

	def DisplayFileContentFromView(self, index):
		path = self.mainWin.dirModel.filePath(index)
		if not QtCore.QFileInfo(path).isFile():
			return
		try:
			root, ext = os.path.splitext(path.lower())
			if ext == ".plist":
				self.DisplayPListFileContent(path)
			elif ext in [".sqlite", ".db"]:
				self.DisplayDatabaseFileContent(path)
			else:
				self.DisplayTextFileContent(path)
		except Exception as e:
			self.mainWin.txtFilePreview.setPlainText(str(e))


	def TabIndexChanged(self):
		tabIndex = self.mainWin.tabWidget.currentIndex()
		if tabIndex == 0:
			"Pass"
		elif tabIndex == 1:
			if self.objSSHClient == None:
				self.globalVariables.ShowErrorDailog(self.mainWin, "SSH Connection not initiated!!")
				self.mainWin.tabWidget.setCurrentIndex(0)
		elif tabIndex == 2:
			self.ShowDirectoryViewOfApplication()
		else:
			print ("Data")

if __name__ == "__main__":
	app = QApplication(sys.argv)
	app.setWindowIcon(QtGui.QIcon('./Usage/icon.png'))
	print (getBanner())

	window = QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(window)
	main = Main(ui)

	ui.tabWidget.currentChanged.connect(lambda: main.TabIndexChanged())
	ui.btnConnect.clicked.connect(lambda: main.SSHConnection())

	ui.treeView.clicked.connect(lambda index: main.DisplayFileContentFromView(index))

	ui.btnReSnapShot.clicked.connect(lambda: main.ForceDownloadCodeFromDevice())
	ui.btnMobSF.clicked.connect(lambda: main.RunMobSFTool())
	ui.listApplication.itemClicked.connect(lambda: main.SelectApplication())

	window.show()
	sys.exit(app.exec())