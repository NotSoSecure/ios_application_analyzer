from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import QWidget, QMessageBox

class Ui_MainWindow(QWidget):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 600)

        boldFont = QtGui.QFont()
        boldFont.setBold(True)

        # Central widget
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)

        mainLayout = QtWidgets.QVBoxLayout(self.centralwidget)

        # Tab Widget (Resizable)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        mainLayout.addWidget(self.tabWidget)

        # ============================================================
        # ---------------------- Device Info Tab ----------------------
        # ============================================================
        self.tabDeviceInfo = QtWidgets.QWidget()
        deviceLayout = QtWidgets.QVBoxLayout(self.tabDeviceInfo)

        formLayout = QtWidgets.QFormLayout()
        titleLabel = QtWidgets.QLabel("SSH Connection")
        font = QtGui.QFont()
        font.setPointSize(28)
        titleLabel.setFont(font)
        titleLabel.setAlignment(QtCore.Qt.AlignCenter)

        deviceLayout.addWidget(titleLabel)

        self.txtIPAddress = QtWidgets.QLineEdit()
        self.txtIPAddress.setInputMask("000.000.000.000;_")
        self.txtIPAddress.setText("127.0.0.1")

        self.txtPort = QtWidgets.QLineEdit("22")
        self.txtUsername = QtWidgets.QLineEdit("mobile")
        self.txtPassword = QtWidgets.QLineEdit("Test@1234")

        formLayout.addRow("IP Address:", self.txtIPAddress)
        formLayout.addRow("Port:", self.txtPort)
        formLayout.addRow("Username:", self.txtUsername)
        formLayout.addRow("Password:", self.txtPassword)

        deviceLayout.addLayout(formLayout)

        self.btnConnect = QtWidgets.QPushButton("Connect")
        deviceLayout.addWidget(self.btnConnect, alignment=QtCore.Qt.AlignCenter)

        self.tabWidget.addTab(self.tabDeviceInfo, "Device Info")

        # ============================================================
        # ---------------------- App Info Tab -------------------------
        # ============================================================
        self.tabAppInfo = QtWidgets.QWidget()
        appLayout = QtWidgets.QHBoxLayout(self.tabAppInfo)

        # Left side list
        leftLayout = QtWidgets.QVBoxLayout()
        lblApplications = QtWidgets.QLabel("Applications")

        font = QtGui.QFont()
        font.setPointSize(28)
        lblApplications.setFont(font)

        leftLayout.addWidget(lblApplications)

        self.listApplication = QtWidgets.QListWidget()
        leftLayout.addWidget(self.listApplication)

        appLayout.addLayout(leftLayout, 1)

        # Right side info panel
        rightLayout = QtWidgets.QVBoxLayout()

        self.gbApplicationInfo = QtWidgets.QGroupBox("Application Information")
        gbLayout = QtWidgets.QFormLayout(self.gbApplicationInfo)

        # Bold label names
        def b(text): 
            l = QtWidgets.QLabel(text)
            l.setFont(boldFont)
            return l

        self.lblBundleID = QtWidgets.QLabel("N/A")
        self.lblBundleName = QtWidgets.QLabel("N/A")
        self.lblBundleUUID = QtWidgets.QLabel("N/A")
        self.lblDataUUID = QtWidgets.QLabel("N/A")
        self.lblBundleVersion = QtWidgets.QLabel("N/A")
        self.lblPlatformVersion = QtWidgets.QLabel("N/A")
        self.lblMinimumOS = QtWidgets.QLabel("N/A")

        gbLayout.addRow(b("Bundle ID:"), self.lblBundleID)
        gbLayout.addRow(b("Bundle Name:"), self.lblBundleName)
        gbLayout.addRow(b("Bundle UUID:"), self.lblBundleUUID)
        gbLayout.addRow(b("Data UUID:"), self.lblDataUUID)
        gbLayout.addRow(b("Bundle Version:"), self.lblBundleVersion)
        gbLayout.addRow(b("Platform Version:"), self.lblPlatformVersion)
        gbLayout.addRow(b("Minimum OS:"), self.lblMinimumOS)

        rightLayout.addWidget(self.gbApplicationInfo)

        self.lblLocalPath = QtWidgets.QLabel("Local Path")
        rightLayout.addWidget(self.lblLocalPath)

        self.btnMobSF = QtWidgets.QPushButton("MobSF")
        self.btnReSnapShot = QtWidgets.QPushButton("Latest Code")

        rightLayout.addWidget(self.btnMobSF)
        rightLayout.addWidget(self.btnReSnapShot)

        rightLayout.addStretch()

        appLayout.addLayout(rightLayout, 2)

        self.tabWidget.addTab(self.tabAppInfo, "App Info")

        # ============================================================
        # --------------------- Directory Browser Tab -----------------
        # ============================================================
        self.tabDirectory = QtWidgets.QWidget()
        dirLayout = QtWidgets.QVBoxLayout(self.tabDirectory)

        splitter = QtWidgets.QSplitter()
        dirLayout.addWidget(splitter)

        # File system model
        self.dirModel = QtWidgets.QFileSystemModel()
        self.dirModel.setRootPath("")

        # Tree view
        self.treeView = QtWidgets.QTreeView()
        self.treeView.setModel(self.dirModel)
        self.treeView.setHeaderHidden(False)
        for i in range(1, 4):
            self.treeView.hideColumn(i)

        # File preview
        self.txtFilePreview = QtWidgets.QTextEdit()

        splitter.addWidget(self.treeView)
        splitter.addWidget(self.txtFilePreview)
        splitter.setSizes([300, 600])

        self.tabWidget.addTab(self.tabDirectory, "File Browser")

        # Status bar
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

    def DisplayMessagebox(self, msg):
        QMessageBox.warning(self, "Invalid IP", msg, QMessageBox.Ok)

    