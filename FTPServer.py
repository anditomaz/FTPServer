from PyQt5 import QtCore, QtGui, QtWidgets
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import threading
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(478, 333)
        MainWindow.setFixedSize(478, 333)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.EdtFTPHost = QtWidgets.QLineEdit(self.centralwidget)
        self.EdtFTPHost.setGeometry(QtCore.QRect(123, 97, 171, 20))
        self.EdtFTPHost.setObjectName("EdtFTPHost")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(123, 81, 47, 13))
        self.label.setObjectName("label")
        self.EdtPorta = QtWidgets.QLineEdit(self.centralwidget)
        self.EdtPorta.setGeometry(QtCore.QRect(303, 97, 50, 20))
        self.EdtPorta.setObjectName("EdtPorta")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(303, 82, 47, 13))
        self.label_2.setObjectName("label_2")
        self.EdtUsuario = QtWidgets.QLineEdit(self.centralwidget)
        self.EdtUsuario.setGeometry(QtCore.QRect(123, 139, 230, 20))
        self.EdtUsuario.setObjectName("EdtUsuario")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(123, 123, 47, 13))
        self.label_3.setObjectName("label_3")
        self.EdtSenha = QtWidgets.QLineEdit(self.centralwidget)
        self.EdtSenha.setGeometry(QtCore.QRect(123, 181, 230, 20))
        self.EdtSenha.setObjectName("EdtSenha")
        self.EdtSenha.setEchoMode(QtWidgets.QLineEdit.Password)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(124, 165, 47, 13))
        self.label_4.setObjectName("label_4")
        self.EdtCaminhoPath = QtWidgets.QLineEdit(self.centralwidget)
        self.EdtCaminhoPath.setGeometry(QtCore.QRect(123, 222, 230, 20))
        self.EdtCaminhoPath.setObjectName("EdtCaminhoPath")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(124, 206, 47, 13))
        self.label_5.setObjectName("label_5")
        self.toolButton = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton.setGeometry(QtCore.QRect(358, 221, 25, 21))
        self.toolButton.setObjectName("toolButton")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(0, 50, 491, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.BtnIniciar = QtWidgets.QPushButton(self.centralwidget)
        self.BtnIniciar.setGeometry(QtCore.QRect(202, 260, 75, 23))
        self.BtnIniciar.setObjectName("BtnIniciar")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(119, 12, 241, 31))
        self.label_6.setObjectName("label_6")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "FTP Server"))
        self.label.setText(_translate("MainWindow", "Server"))
        self.label_2.setText(_translate("MainWindow", "Porta"))
        self.label_3.setText(_translate("MainWindow", "Usuário"))
        self.label_4.setText(_translate("MainWindow", "Senha"))
        self.label_5.setText(_translate("MainWindow", "Diretório"))
        self.toolButton.setText(_translate("MainWindow", "..."))
        self.BtnIniciar.setText(_translate("MainWindow", "Start"))
        self.label_6.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600; color:#00aaff;\">FTP Server Configuration</span></p></body></html>"))


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.BtnIniciar.clicked.connect(self.iniciar_ftp_server)
        self.toolButton.clicked.connect(self.select_directory)

    def iniciar_ftp_server(self):
        host = self.EdtFTPHost.text()
        porta = int(self.EdtPorta.text())
        usuario = self.EdtUsuario.text()
        senha = self.EdtSenha.text()
        diretorio = self.EdtCaminhoPath.text()

        ftp_thread = threading.Thread(target=self.start_ftp_server, args=(host, porta, usuario, senha, diretorio))
        ftp_thread.start()

        QMessageBox.information(self, "Info", "FTP Server iniciado com sucesso!")

    def start_ftp_server(self, host, porta, usuario, senha, diretorio):
        authorizer = DummyAuthorizer()
        authorizer.add_user(usuario, senha, diretorio, perm='elradfmw')
        handler = FTPHandler
        handler.authorizer = authorizer
        server = FTPServer((host, porta), handler)
        server.serve_forever()



    def select_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Selecione um diretório")
        if directory:
            self.EdtCaminhoPath.setText(directory)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
