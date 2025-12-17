from GlobalVariables import *
from SSHSession import *
import plistlib
import os 
from datetime import datetime
import shutil
import tkinter as tk
from tkinter import messagebox
import time

class Application:
	def __init__(self, sshClient, mainWin):
		self.apps=[[]]
		self.objSSHClient = sshClient
		self.mainWin=mainWin
		self.globalVariables=GlobalVariables()
		self.currentSelectedAppBundleUUID=''
		self.currentSelectedAppName=''
		self.currentSelectedAppBundleName=''
		self.currentSelectedAppDataUUID=''
		self.currentAppName=''

	def FillAppInList(self):
		rawData = self.objSSHClient.executeCommand(self.globalVariables.appListCmd)
		for line in rawData:
			line=line.strip()
			rfind = line.rfind('/');
			bundleName = line[rfind+1:];
			bundleId = line[2:rfind];
			self.apps.append([bundleName,bundleId])
			self.mainWin.listApplication.addItem(bundleName)
		self.mainWin.tabWidget.setCurrentIndex(1)

	def GetDataDirUUID(self):
		isError=False
		remotePath="{}{}/{}/Info.plist".format(self.globalVariables.bundlePath, self.currentSelectedAppBundleUUID, self.currentSelectedAppName)
		localPath="./Output/{}/Bundle/{}/{}".format(self.currentAppName, self.currentSelectedAppBundleUUID, self.currentSelectedAppName)
		try:
			os.makedirs(localPath)
		except:
			pass

		localPath="{}/Info.plist".format(localPath)		
		self.objSSHClient.get(remotePath,localPath)

		with open(localPath, 'rb') as fp :
			plist_content = plistlib.loads(fp.read())
			if 'CFBundleIdentifier' in plist_content:
				self.currentSelectedAppBundleName = plist_content['CFBundleIdentifier']
		command = "cd {} && find . -name '{}' | grep 'Caches/{}'".format(self.globalVariables.dataPath, self.currentSelectedAppBundleName, self.currentSelectedAppBundleName)
		rawData = self.objSSHClient.executeCommand(command)
		if not rawData:
			self.globalVariables.ShowErrorDailog(self.mainWin, "Open application from device once and try again!")
			self.currentSelectedAppDataUUID = ""
			isError=True
		else:
			dataUUID = rawData[0].strip()
			self.currentSelectedAppDataUUID = dataUUID[2: dataUUID.find("/", 3)]

		localPath="./Output/{}/Bundle/{}".format(self.currentAppName, self.currentSelectedAppBundleUUID)
		shutil.rmtree(localPath)
		return isError

	def isCopyBundleAndDataDirectory(self, appName, force):
		for app in self.apps:
			if len(app) == 2 and app[0] == appName:
				self.currentSelectedAppName = app[0]
				self.currentSelectedAppBundleUUID = app[1]
				self.currentAppName= self.currentSelectedAppName[0: self.currentSelectedAppName.find(".")]
				break

		if not force:
			outputDirName = "./Output/{}".format(self.currentAppName)
			if os.path.exists(outputDirName) and not force:
				root = tk.Tk()
				root.withdraw()  # hide main window
				result = messagebox.askyesno("Folder Exists", f"The folder '{outputDirName}' already exists.\n\nDo you want to copy it again?")
				root.destroy()
				if result:
					return True
				else:
					return False
			else:
				return True
		else:
			return True

	def CopyBundleAndDataDirectory(self, appName, force=False):
		if self.isCopyBundleAndDataDirectory(appName, force):
			if not self.GetDataDirUUID():
				outputBundleDirName = "./Output/{}/Bundle".format(self.currentAppName)
				outputDataDirName = "./Output/{}/Data".format(self.currentAppName)
				if force:
					dateTime = str(datetime.now())
					outDir = "./Output/{}_{}".format(self.currentAppName, str(dateTime).replace(":","_").replace(".","_").replace(" ","__"))
					os.rename("./Output/{}".format(self.currentAppName), outDir)

				metaDataPath = '{}{}'.format(self.globalVariables.bundlePath, self.currentSelectedAppBundleUUID)
				self.objSSHClient.get_all(metaDataPath, outputBundleDirName)
				
				metaDataPath = '{}{}'.format(self.globalVariables.dataPath, self.currentSelectedAppDataUUID)
				self.objSSHClient.get_all(metaDataPath, outputDataDirName)
				
				return True
			return False
		return True

	def CreateIPAFileFromSource(self):
		if self.globalVariables.isWindowsOS:
			command = "cd \"./Output/{}/\" && mkdir Payload && xcopy Bundle Payload /E /I /H && mkdir \"{}\" && move Payload \"{}/\" && powershell -Command \"Compress-Archive -Path '{}\\*' -DestinationPath '{}.zip'\" && ren \"{}.zip\" \"{}.ipa\"".format(self.currentAppName, self.currentAppName, self.currentAppName, self.currentAppName, self.currentAppName, self.currentAppName, self.currentAppName, self.currentAppName)
		else:
			command = "cd ./Output/{}/ && mkdir Payload && cp -r Bundle Payload/ && zip -r Payload.zip Payload/ && mv Payload.zip {}.ipa && rm -rf Payload && mv {}.ipa ../../".format(self.currentAppName, self.currentSelectedAppName, self.currentAppName, self.currentAppName)
		self.globalVariables.ExecuteCommand(command)


