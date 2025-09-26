import requests
import os
from bs4 import BeautifulSoup
import subprocess
from PySide6.QtWidgets import QMessageBox

class GlobalVariables:
	def __init__(self):
		self.dataPath=''
		self.toolName = "iOS Application Analyzer"
		self.bundlePath='/var/containers/Bundle/Application/'
		self.dataPath='/var/mobile/Containers/Data/Application/'
		self.appListCmd='cd {} && find . -name "*.app"'.format(self.bundlePath);
		self.mobSFURL="http://localhost:8000"
		self.mobSFAPIKey=""
		self.isWindowsOS=False

		if os.name == 'nt':
			self.isWindowsOS = True

	def InitializeMobSFVariables(self):
		isSuccess=False
		try:
			response=requests.get("{}/api_docs".format(self.mobSFURL), timeout=10)
			soup = BeautifulSoup(response.text, "lxml")
			self.mobSFAPIKey=soup.find("p", { "class" : "lead" }).find("strong").find("code").text
			isSuccess=True
		except:
			print ("Failed to initiate conection with MobSF!!")
		return isSuccess

	def ExecuteCommand(self, command):
		print (command)
		p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
		output = p.communicate()[0].decode("utf-8", errors="ignore")
		p_status = p.wait()
		print (output)
		print ("\n\n")
		return output

	def ShowErrorDailog(self, mainWin, errorMessage):
		QMessageBox.critical(mainWin, self.toolName, errorMessage, QMessageBox.StandardButton.Ok)