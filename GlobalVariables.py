import requests
import os
from bs4 import BeautifulSoup
import subprocess
from PyQt5.QtWidgets import QMessageBox

class GlobalVariables:
	def __init__(self):
		self.dataPath=''
		self.toolName = "iOS Application Analyzer"
		self.bundlePath='/var/containers/Bundle/Application/'
		self.dataPath='/var/mobile/Containers/Data/Application/'
		self.appListCmd='cd {} && find . -name "*.app"'.format(self.bundlePath);
		self.mobSFURL="http://localhost:8000"
		self.mobSFAPIKey=""

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
		p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
		output = p.communicate()[0].decode("utf-8", errors="ignore")
		p_status = p.wait()
		return output

	def ShowErrorDailog(self, mainWin, errorMessage):
		error=QMessageBox()
		error.critical(mainWin, self.toolName, errorMessage, QMessageBox.Ok)