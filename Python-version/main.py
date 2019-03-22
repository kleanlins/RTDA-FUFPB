from PyQt5 import QtWidgets, QtCore, QtGui
from plot_window import *
import sys
import serial.tools.list_ports


class WelcomeWindow(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.title = "Formula UFPB - Análise de dados em tempo real"
        self.left = 400
        self.top = 400
        self.width = 360
        self.lenght = 240
        self.init_UI()


    def init_UI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.lenght)
        self.setMaximumSize(self.width, self.lenght)

        self.create_grid()

        window_layout = QtWidgets.QVBoxLayout()
        window_layout.addWidget(self.horizontal_arrangement)
        self.setLayout(window_layout)

        self.show()


    def create_grid(self):
        accept_button = QtWidgets.QPushButton("Aceitar")
        accept_button.clicked.connect(self.open_plottage)

        refuse_button = QtWidgets.QPushButton("Recusar")
        refuse_button.setToolTip("Quer dar uma de doido é?")
        refuse_button.clicked.connect(self.close_application)

        welcome_label = QtWidgets.QLabel("Sistema de análise de dados em tempo real do Formula UFPB.\n"\
                                        + "Este programa encontra-se em fase beta, caso encontre algo de errado, \nfavor reportar.")
        welcome_label.setAlignment(QtCore.Qt.AlignCenter)

        self.horizontal_arrangement = QtWidgets.QGroupBox("Seja bem-vindo(a)")

        layout = QtWidgets.QGridLayout()
        layout.addWidget(welcome_label, 0, 0, 0, 2)
        layout.addWidget(accept_button, 1, 0)
        layout.addWidget(refuse_button, 1, 1)

        self.horizontal_arrangement.setLayout(layout)


    def open_plottage(self):
        self.plot_window = PlotWindow()
        self.plot_window.show()
        self.hide()


    def close_application(self):
        sys.exit()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = WelcomeWindow()
    sys.exit(app.exec_())
