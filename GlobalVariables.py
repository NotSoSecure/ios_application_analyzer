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
		self.mobSFUsername="mobsf"
		self.mobSFPassword="mobsf"
		self.mobSFAPIKey=""
		self.isWindowsOS=False

		if os.name == 'nt':
			self.isWindowsOS = True

	def InitializeMobSFVariables(self):
		isSuccess=False
		session_id=""
		try:
			session = requests.Session()
			resp = session.post("{}/login/".format(self.mobSFURL), data={"username": self.mobSFUsername, "password": self.mobSFPassword}, allow_redirects=False)
			session_id=resp.cookies.get("sessionid")
			response=requests.get("{}/api_docs".format(self.mobSFURL), timeout=10, cookies={"sessionid": session_id})
			soup = BeautifulSoup(response.text, "lxml")
			self.mobSFAPIKey=soup.find("p", { "class" : "lead" }).find("strong").find("code").text
			isSuccess=True
		except:
			print ("Failed to initiate conection with MobSF!!")
		return isSuccess, session_id

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