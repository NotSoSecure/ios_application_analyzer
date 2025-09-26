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


	def FillPListFiles(self):
		self.mainWin.lstPListFiles.clear()
		self.mainWin.txtPListFileData.setText("")
		if self.applications == None or self.applications.currentAppName == "":
			self.globalVariables.ShowErrorDailog(self.mainWin, "Application not select in App Info tab")
			self.mainWin.tabWidget.setCurrentIndex(1)
		else:
			command = ""
			if self.globalVariables.isWindowsOS:
				command = "cd ./Output/{} && dir /s /b *.plist".format(self.applications.currentAppName)
			else:
				command = "cd ./Output/{} && find . -name '*.plist'".format(self.applications.currentAppName)
			output = self.globalVariables.ExecuteCommand(command)
			for line in output.split("\n"):
				line = line.strip()
				if not self.globalVariables.isWindowsOS:
					line = line[1:]
				self.mainWin.lstPListFiles.addItem(QListWidgetItem(line))

	def DisplayPListFileContent(self):
		if len(self.mainWin.lstPListFiles.selectedItems()) == 1:
			try:
				filePath=""
				if self.globalVariables.isWindowsOS:
					filePath=self.mainWin.lstPListFiles.selectedItems()[0].text()
				else:
					filePath="./Output/{}{}".format(self.applications.currentAppName, self.mainWin.lstPListFiles.selectedItems()[0].text())
				with open(filePath, 'rb') as fp :
					plist_content = plistlib.loads(fp.read())
					self.mainWin.txtPListFileData.setText(json.dumps(plist_content, sort_keys=True, indent=4))
			except:
				raise

	def FillDatabaseFiles(self):
		self.mainWin.lstDatabaseFiles.clear()
		self.mainWin.txtDatabaseFileContent.setText("")
		if self.applications == None or self.applications.currentAppName == "":
			self.globalVariables.ShowErrorDailog(self.mainWin, "Application not select in App Info tab")
			self.mainWin.tabWidget.setCurrentIndex(1)
		else:
			if self.globalVariables.isWindowsOS:
				command = "cd ./Output/{} && dir /s /b *.db".format(self.applications.currentAppName)
			else:
				command = "cd ./Output/{} && find . -name '*.db'".format(self.applications.currentAppName)
			output = self.globalVariables.ExecuteCommand(command)
			for line in output.split("\n"):
				line = line.strip()
				if not self.globalVariables.isWindowsOS:
					line = line[1:]
				self.mainWin.lstDatabaseFiles.addItem(QListWidgetItem(line))
	
	def GetTableData(self, dbPath, tableName):
		rows=[]
		con = sqlite3.connect(dbPath)
		cursor = con.cursor()
		cursor.execute("SELECT * FROM " + tableName)

		colnames = cursor.description
		row=''
		for colname in colnames:
			row+=colname[0] + " | "
		rows.append(row)

		for row in cursor.fetchall():
			rows.append(row)
		return rows

	def DisplayDatabaseFileContent(self):
		if len(self.mainWin.lstDatabaseFiles.selectedItems()) == 1:
			filePath=""
			if self.globalVariables.isWindowsOS:
				filePath=self.mainWin.lstDatabaseFiles.selectedItems()[0].text()
			else:	
				filePath="./Output/{}{}".format(self.applications.currentAppName, self.mainWin.lstDatabaseFiles.selectedItems()[0].text())
			self.mainWin.txtDatabaseFileContent.setText("SQLiteDB : "+filePath)
			tables=[]
			con = sqlite3.connect(filePath)
			cursor = con.cursor()
			cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
			for table_name in cursor.fetchall():
				table = table_name[0]
				self.mainWin.txtDatabaseFileContent.append("\n\n\nTable => " + table.format(type(str), repr(str)))
				rows=self.GetTableData(filePath, table)
				isFirstRow=True
				for columns in rows:
					rowData=""
					for column in columns:
						try:
							rowData+=column.format(type(str), repr(str))
							if not isFirstRow:
								rowData+=" | "
						except:
							rowData+=str(column)
							if not isFirstRow:
								rowData+=" | "
					isFirstRow=False
					dataLen = len(rowData)
					if dataLen > 174:
						dataLen = 174
					self.mainWin.txtDatabaseFileContent.append("-"*dataLen)
					self.mainWin.txtDatabaseFileContent.append(rowData)
					self.mainWin.txtDatabaseFileContent.append("-"*dataLen)

	def FillKeyChainData(self, data):
		self.mainWin.txtKeyChainData.setText("KeyChain Data:\n=============")
		for line in data:
			line.strip()
			self.mainWin.txtKeyChainData.append(line)

	def DumpKeyChainData(self):
		if self.objSSHClient == None:
			self.globalVariables.ShowErrorDailog(self.mainWin, "SSH Connection not initiated!!")
			self.mainWin.tabWidget.setCurrentIndex(0)
		else:
			self.objSSHClient.put_all("./tools/keychain_dumper", "/var/tmp/")
			output = self.objSSHClient.executeCommand("./keychain_dumper -a")
			self.FillKeyChainData(output)

	def TabIndexChanged(self):
		tabIndex = self.mainWin.tabWidget.currentIndex()
		if tabIndex == 0:
			"Pass"
		elif tabIndex == 1:
			if self.objSSHClient == None:
				self.globalVariables.ShowErrorDailog(self.mainWin, "SSH Connection not initiated!!")
				self.mainWin.tabWidget.setCurrentIndex(0)
		elif tabIndex == 2:
			self.FillPListFiles()
		elif tabIndex == 3:
			self.FillDatabaseFiles()
		elif tabIndex == 4:
			self.DumpKeyChainData()
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
	ui.lstPListFiles.itemClicked.connect(lambda: main.DisplayPListFileContent())
	ui.lstDatabaseFiles.itemClicked.connect(lambda: main.DisplayDatabaseFileContent())
	ui.btnConnect.clicked.connect(lambda: main.SSHConnection())
	ui.btnReSnapShot.clicked.connect(lambda: main.ForceDownloadCodeFromDevice())
	ui.btnMobSF.clicked.connect(lambda: main.RunMobSFTool())
	ui.listApplication.itemClicked.connect(lambda: main.SelectApplication())

	window.show()
	sys.exit(app.exec())