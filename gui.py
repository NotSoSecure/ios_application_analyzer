from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import QWidget, QMessageBox

class Ui_MainWindow(QWidget):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(782, 516)

        # Bold font for some labels
        boldFont = QtGui.QFont()
        boldFont.setBold(True)

        # Central widget
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Tab Widget
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 781, 551))
        self.tabWidget.setObjectName("tabWidget")

        # ---------------------- Device Info Tab ----------------------
        self.tabDeviceInfo = QtWidgets.QWidget()
        self.tabDeviceInfo.setObjectName("tabDeviceInfo")

        self.btnConnect = QtWidgets.QPushButton(self.tabDeviceInfo)
        self.btnConnect.setGeometry(QtCore.QRect(280, 340, 220, 32))
        self.btnConnect.setObjectName("btnConnect")

        self.txtIPAddress = QtWidgets.QLineEdit(self.tabDeviceInfo)
        self.txtIPAddress.setGeometry(QtCore.QRect(370, 180, 121, 21))
        self.txtIPAddress.setText("")
        self.txtIPAddress.setObjectName("txtIPAddress")

        self.txtPort = QtWidgets.QLineEdit(self.tabDeviceInfo)
        self.txtPort.setGeometry(QtCore.QRect(370, 220, 121, 21))
        self.txtPort.setObjectName("txtPort")

        self.lblIPAddress = QtWidgets.QLabel(self.tabDeviceInfo)
        self.lblIPAddress.setGeometry(QtCore.QRect(290, 180, 81, 16))
        self.lblIPAddress.setObjectName("lblIPAddress")

        self.lblPort = QtWidgets.QLabel(self.tabDeviceInfo)
        self.lblPort.setGeometry(QtCore.QRect(290, 220, 81, 16))
        self.lblPort.setObjectName("lblPort")

        self.lblTitle = QtWidgets.QLabel(self.tabDeviceInfo)
        self.lblTitle.setGeometry(QtCore.QRect(290, 120, 201, 51))
        font = QtGui.QFont()
        font.setPointSize(28)
        self.lblTitle.setFont(font)
        self.lblTitle.setObjectName("lblTitle")

        self.lblUsername = QtWidgets.QLabel(self.tabDeviceInfo)
        self.lblUsername.setGeometry(QtCore.QRect(290, 260, 81, 16))
        self.lblUsername.setObjectName("lblUsername")

        self.lblChangePassword = QtWidgets.QLabel(self.tabDeviceInfo)
        self.lblChangePassword.setGeometry(QtCore.QRect(290, 300, 81, 16))
        self.lblChangePassword.setObjectName("lblChangePassword")

        self.txtUsername = QtWidgets.QLineEdit(self.tabDeviceInfo)
        self.txtUsername.setGeometry(QtCore.QRect(370, 260, 121, 21))
        self.txtUsername.setObjectName("txtUsername")

        self.txtPassword = QtWidgets.QLineEdit(self.tabDeviceInfo)
        self.txtPassword.setGeometry(QtCore.QRect(370, 300, 121, 21))
        self.txtPassword.setObjectName("txtPassword")

        self.tabWidget.addTab(self.tabDeviceInfo, "")

        # ---------------------- App Info Tab ----------------------
        self.tabAppInfo = QtWidgets.QWidget()
        self.tabAppInfo.setObjectName("tabAppInfo")

        self.listApplication = QtWidgets.QListWidget(self.tabAppInfo)
        self.listApplication.setGeometry(QtCore.QRect(10, 50, 251, 400))
        self.listApplication.setObjectName("listApplication")

        self.lblApplications = QtWidgets.QLabel(self.tabAppInfo)
        self.lblApplications.setGeometry(QtCore.QRect(10, 0, 201, 51))
        font = QtGui.QFont()
        font.setPointSize(28)
        self.lblApplications.setFont(font)
        self.lblApplications.setObjectName("lblApplications")

        self.gbApplicationInfo = QtWidgets.QGroupBox(self.tabAppInfo)
        self.gbApplicationInfo.setGeometry(QtCore.QRect(270, 40, 501, 240))
        self.gbApplicationInfo.setObjectName("gbApplicationInfo")

        # Static labels with bold font
        self.stlblBundleID = QtWidgets.QLabel(self.gbApplicationInfo)
        self.stlblBundleID.setGeometry(QtCore.QRect(10, 30, 111, 16))
        self.stlblBundleID.setObjectName("stlblBundleID")
        self.stlblBundleID.setFont(boldFont)

        self.stlblBundelName = QtWidgets.QLabel(self.gbApplicationInfo)
        self.stlblBundelName.setGeometry(QtCore.QRect(10, 60, 111, 16))
        self.stlblBundelName.setObjectName("stlblBundelName")
        self.stlblBundelName.setFont(boldFont)

        self.stlblBundleUUID = QtWidgets.QLabel(self.gbApplicationInfo)
        self.stlblBundleUUID.setGeometry(QtCore.QRect(10, 90, 111, 16))
        self.stlblBundleUUID.setObjectName("stlblBundleUUID")
        self.stlblBundleUUID.setFont(boldFont)

        self.stlblDataUUID = QtWidgets.QLabel(self.gbApplicationInfo)
        self.stlblDataUUID.setGeometry(QtCore.QRect(10, 120, 111, 16))
        self.stlblDataUUID.setObjectName("stlblDataUUID")
        self.stlblDataUUID.setFont(boldFont)

        self.stlblBundleVersion = QtWidgets.QLabel(self.gbApplicationInfo)
        self.stlblBundleVersion.setGeometry(QtCore.QRect(10, 150, 111, 16))
        self.stlblBundleVersion.setObjectName("stlblBundleVersion")
        self.stlblBundleVersion.setFont(boldFont)

        self.stlblPlatformVersion = QtWidgets.QLabel(self.gbApplicationInfo)
        self.stlblPlatformVersion.setGeometry(QtCore.QRect(10, 180, 121, 16))
        self.stlblPlatformVersion.setObjectName("stlblPlatformVersion")
        self.stlblPlatformVersion.setFont(boldFont)

        self.stlblMinimumOS = QtWidgets.QLabel(self.gbApplicationInfo)
        self.stlblMinimumOS.setGeometry(QtCore.QRect(10, 210, 121, 16))
        self.stlblMinimumOS.setObjectName("stlblMinimumOS")
        self.stlblMinimumOS.setFont(boldFont)

        # Dynamic labels
        self.lblBundleVersion = QtWidgets.QLabel(self.gbApplicationInfo)
        self.lblBundleVersion.setGeometry(QtCore.QRect(140, 150, 351, 16))
        self.lblBundleVersion.setObjectName("lblBundleVersion")

        self.lblDataUUID = QtWidgets.QLabel(self.gbApplicationInfo)
        self.lblDataUUID.setGeometry(QtCore.QRect(140, 120, 351, 16))
        self.lblDataUUID.setObjectName("lblDataUUID")

        self.lblMinimumOS = QtWidgets.QLabel(self.gbApplicationInfo)
        self.lblMinimumOS.setGeometry(QtCore.QRect(140, 210, 351, 16))
        self.lblMinimumOS.setObjectName("lblMinimumOS")

        self.lblPlatformVersion = QtWidgets.QLabel(self.gbApplicationInfo)
        self.lblPlatformVersion.setGeometry(QtCore.QRect(140, 180, 351, 16))
        self.lblPlatformVersion.setObjectName("lblPlatformVersion")

        self.lblBundleUUID = QtWidgets.QLabel(self.gbApplicationInfo)
        self.lblBundleUUID.setGeometry(QtCore.QRect(140, 90, 351, 16))
        self.lblBundleUUID.setObjectName("lblBundleUUID")

        self.lblBundleName = QtWidgets.QLabel(self.gbApplicationInfo)
        self.lblBundleName.setGeometry(QtCore.QRect(140, 60, 351, 16))
        self.lblBundleName.setObjectName("lblBundleName")

        self.lblBundleID = QtWidgets.QLabel(self.gbApplicationInfo)
        self.lblBundleID.setGeometry(QtCore.QRect(140, 30, 351, 16))
        self.lblBundleID.setObjectName("lblBundleID")

        self.lblLocalPath = QtWidgets.QLabel(self.tabAppInfo)
        self.lblLocalPath.setGeometry(QtCore.QRect(280, 290, 481, 16))
        self.lblLocalPath.setObjectName("lblLocalPath")

        self.btnMobSF = QtWidgets.QPushButton(self.tabAppInfo)
        self.btnMobSF.setGeometry(QtCore.QRect(270, 310, 501, 32))
        self.btnMobSF.setObjectName("btnMobSF")

        self.btnReSnapShot = QtWidgets.QPushButton(self.tabAppInfo)
        self.btnReSnapShot.setGeometry(QtCore.QRect(270, 340, 501, 32))
        self.btnReSnapShot.setObjectName("btnReSnapShot")

        self.tabWidget.addTab(self.tabAppInfo, "")

        # ---------------------- PList Files Tab ----------------------
        self.tabPListFiles = QtWidgets.QWidget()
        self.tabPListFiles.setObjectName("tabPListFiles")

        self.lstPListFiles = QtWidgets.QListWidget(self.tabPListFiles)
        self.lstPListFiles.setGeometry(QtCore.QRect(5, 5, 765, 140))
        self.lstPListFiles.setObjectName("lstPListFiles")

        self.txtPListFileData = QtWidgets.QTextEdit(self.tabPListFiles)
        self.txtPListFileData.setGeometry(QtCore.QRect(5, 155, 765, 300))
        self.txtPListFileData.setObjectName("txtPListFileData")

        self.tabWidget.addTab(self.tabPListFiles, "")

        # ---------------------- SQL Databases Tab ----------------------
        self.tabSQLDatabases = QtWidgets.QWidget()
        self.tabSQLDatabases.setObjectName("tabSQLDatabases")

        self.txtDatabaseFileContent = QtWidgets.QTextEdit(self.tabSQLDatabases)
        self.txtDatabaseFileContent.setGeometry(QtCore.QRect(5, 155, 765, 300))
        self.txtDatabaseFileContent.setObjectName("txtDatabaseFileContent")

        self.lstDatabaseFiles = QtWidgets.QListWidget(self.tabSQLDatabases)
        self.lstDatabaseFiles.setGeometry(QtCore.QRect(5, 5, 765, 140))
        self.lstDatabaseFiles.setObjectName("lstDatabaseFiles")

        self.tabWidget.addTab(self.tabSQLDatabases, "")

        # ---------------------- Keychain Tab ----------------------
        self.tabKeychain = QtWidgets.QWidget()
        self.tabKeychain.setObjectName("tabKeychain")

        self.txtKeyChainData = QtWidgets.QTextEdit(self.tabKeychain)
        self.txtKeyChainData.setGeometry(QtCore.QRect(5, 5, 765, 450))
        self.txtKeyChainData.setObjectName("txtKeyChainData")

        self.tabWidget.addTab(self.tabKeychain, "")

        MainWindow.setCentralWidget(self.centralwidget)

        # Status Bar
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # Final initialization
        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "iOS Application Analyzer"))

        self.txtIPAddress.setInputMask("000.000.000.000;_")
        self.txtIPAddress.setText("127.0.0.1")

        self.btnConnect.setText(_translate("MainWindow", "Connect"))
        self.txtPort.setText(_translate("MainWindow", "22"))

        self.lblIPAddress.setText(_translate("MainWindow", "IP Address"))
        self.lblPort.setText(_translate("MainWindow", "Port"))
        self.lblTitle.setText(_translate("MainWindow", "SSH Connection"))
        self.lblUsername.setText(_translate("MainWindow", "Username"))
        self.lblChangePassword.setText(_translate("MainWindow", "Password"))
        self.txtUsername.setText(_translate("MainWindow", "mobile"))
        self.txtPassword.setText(_translate("MainWindow", "Test@1234"))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabDeviceInfo), _translate("MainWindow", "Device Info"))

        self.lblApplications.setText(_translate("MainWindow", "Applications"))
        self.gbApplicationInfo.setTitle(_translate("MainWindow", "Application Information"))

        self.stlblBundleID.setText(_translate("MainWindow", "Bundle ID"))
        self.stlblBundelName.setText(_translate("MainWindow", "Bundle Name"))
        self.stlblBundleUUID.setText(_translate("MainWindow", "Bundle UUID"))
        self.stlblDataUUID.setText(_translate("MainWindow", "Data UUID"))
        self.stlblBundleVersion.setText(_translate("MainWindow", "Bundle Version"))
        self.stlblPlatformVersion.setText(_translate("MainWindow", "Platform Version"))
        self.stlblMinimumOS.setText(_translate("MainWindow", "Minimum OS"))

        self.lblBundleVersion.setText("N/A")
        self.lblDataUUID.setText("N/A")
        self.lblMinimumOS.setText("N/A")
        self.lblPlatformVersion.setText("N/A")
        self.lblBundleUUID.setText("N/A")
        self.lblBundleName.setText("N/A")
        self.lblBundleID.setText("N/A")

        self.lblLocalPath.setText("Local Path")
        self.btnMobSF.setText("MobSF")
        self.btnReSnapShot.setText("Latest Code")

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabAppInfo), _translate("MainWindow", "App Info"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabPListFiles), _translate("MainWindow", "PListFiles"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSQLDatabases), _translate("MainWindow", "SQLDatabases"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabKeychain), _translate("MainWindow", "Keychain"))

    def DisplayMessagebox(self, msg):
        QMessageBox.warning(self, "Invalid IP", msg, QMessageBox.Ok)