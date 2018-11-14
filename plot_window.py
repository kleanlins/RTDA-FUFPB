# IMPORTS FOR pyqtgraph TEMPORAL GRAPH
from PyQt5 import QtWidgets, QtCore, QtGui
import pyqtgraph as pg

# IMPORTS FOR MATPLOTLIB BAR GRAPHS
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

# MISC IMPORTS
import socket
import serial
import csv
import os

class PlotWindow(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.title = "RT Data Analysis - Formula UFPB"
        self.top = 150
        self.left = 250
        self.width = 1280
        self.lenght = 720

        #connection parameters
        self.port = 0
        self.baud_rate = 0
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.init_UI()


    def init_UI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.lenght)
        self.setAutoFillBackground(True)
        self.p_whiteBackground = self.palette()
        self.p_whiteBackground.setColor(self.backgroundRole(), QtCore.Qt.white)
        self.setPalette(self.p_whiteBackground)

        self.create_gui_elements()

        self.main_layout = QtWidgets.QGridLayout()
        self.main_layout.setRowMinimumHeight(3, 60)
        self.main_layout.setRowMinimumHeight(4, 200)

        self.main_layout.addWidget(self.connection_box, 0, 0)
        self.main_layout.addWidget(self.right_panel_group, 0, 3)
        self.main_layout.addWidget(self.temp_group, 1, 0)
        self.main_layout.addWidget(self.dist_group, 2, 0)
        self.main_layout.addWidget(self.press_group, 3, 0)
        self.main_layout.addWidget(self.misc_group, 4, 0)
        self.main_layout.addWidget(self.box_graph_1, 1, 1, 4, 3)

        self.main_layout.setColumnMinimumWidth(1, 700)
        self.connection_box.setFixedWidth(250)
        self.right_panel_group.setFixedWidth(200)

        self.setLayout(self.main_layout)


    def create_gui_elements(self):

        # CONNECTION GROUP AND LAYOUT, LINE EDITS AND LABELS
        self.connection_box = QtWidgets.QGroupBox("CONEXÃO")
        connection_layout = QtWidgets.QGridLayout()
        self.connection_box.setLayout(connection_layout)

        host_label = QtWidgets.QLabel("Servidor:")
        port_label = QtWidgets.QLabel("Porta:")
        self.c_status = "Desconectado"
        self.connections_status_label = QtWidgets.QLabel(self.c_status)

        # HOST AND PORT TEXT ENTRY
        self.host_entry = QtWidgets.QLineEdit()
        self.host_entry.setText("192.168.0.104")

        self.port_entry = QtWidgets.QLineEdit()
        self.port_entry.setText("5555")

        self.connect_btn_label = "Conectar"
        self.connect_button = QtWidgets.QPushButton(self.connect_btn_label)
        self.connect_button.clicked.connect(self.cd_wireless)

        connection_layout.addWidget(host_label, 0, 0)
        connection_layout.addWidget(port_label, 1, 0)

        connection_layout.addWidget(self.host_entry, 0, 1)
        connection_layout.addWidget(self.connections_status_label, 0, 2)
        connection_layout.addWidget(self.port_entry, 1, 1)
        connection_layout.addWidget(self.connect_button, 1, 2)

        # connection_layout.setcolumn


        # PLOT SETTINGS AND EXPORT TO CSV BUTTON
        graph_time_label = QtWidgets.QLabel("Tempo do gráfico: ")

        self.plot_time_spin = QtWidgets.QComboBox()
        scales = ["5 segundos", "15 segundos", "30 segundos", "60 segundos"]
        self.plot_time_spin.addItems(scales)

        self.export_button = QtWidgets.QPushButton("Salvar log")
        self.export_button.clicked.connect(self.save_data)

        self.right_panel_group = QtWidgets.QGroupBox("DADOS")
        layout_right_panel = QtWidgets.QGridLayout()
        self.right_panel_group.setLayout(layout_right_panel)

        layout_right_panel.addWidget(graph_time_label, 0, 0)
        layout_right_panel.addWidget(self.plot_time_spin, 0, 1)
        layout_right_panel.addWidget(self.export_button, 1, 0, 1, 2)



        # ************ GROUP 1 ************

        # BOXES AND LAYOUTS
        self.temp_group = QtWidgets.QGroupBox("TEMPERATURA")
        group1_layout = QtWidgets.QGridLayout()
        self.temp_group.setLayout(group1_layout)

        self.dist_group = QtWidgets.QGroupBox("MOVIMENTO")
        group2_layout = QtWidgets.QGridLayout()
        self.dist_group.setLayout(group2_layout)

        self.press_group = QtWidgets.QGroupBox("PRESSÃO")
        group3_layout = QtWidgets.QGridLayout()
        self.press_group.setLayout(group3_layout)

        self.misc_group = QtWidgets.QGroupBox("MISCELANEOUS")
        group4_layout = QtWidgets.QGridLayout()
        self.misc_group.setLayout(group4_layout)

        # TEMPERATURE LABELS
        tmp_oleo_lb = QtWidgets.QCheckBox("Óleo")
        tmp_radE_lb = QtWidgets.QCheckBox("Rad. Entrada")
        tmp_radS_lb = QtWidgets.QCheckBox("Rad. Saída")
        tmp_esc1_lb = QtWidgets.QCheckBox("Escape - 1")
        tmp_esc2_lb = QtWidgets.QCheckBox("Escape - 2")
        tmp_esc3_lb = QtWidgets.QCheckBox("Escape - 3")
        tmp_esc4_lb = QtWidgets.QCheckBox("Escape - 4")
        tmp_arRet_lb = QtWidgets.QCheckBox("Ar Retificador")
        tmp_arBat_lb = QtWidgets.QCheckBox("Ar Bateria")

        self.tmp_oleo_vl = QtWidgets.QLabel(" °")
        self.tmp_radE_vl = QtWidgets.QLabel(" °")
        self.tmp_radS_vl = QtWidgets.QLabel(" °")
        self.tmp_esc1_vl = QtWidgets.QLabel(" °")
        self.tmp_esc2_vl = QtWidgets.QLabel(" °")
        self.tmp_esc3_vl = QtWidgets.QLabel(" °")
        self.tmp_esc4_vl = QtWidgets.QLabel(" °")
        self.tmp_arRet_vl = QtWidgets.QLabel(" °")
        self.tmp_arBat_vl = QtWidgets.QLabel(" °")

        group1_layout.addWidget(tmp_oleo_lb, 0, 0)
        group1_layout.addWidget(tmp_radE_lb, 1, 0)
        group1_layout.addWidget(tmp_radS_lb, 2, 0)
        group1_layout.addWidget(tmp_esc1_lb, 3, 0)
        group1_layout.addWidget(tmp_esc2_lb, 4, 0)
        group1_layout.addWidget(tmp_esc3_lb, 5, 0)
        group1_layout.addWidget(tmp_esc4_lb, 6, 0)
        group1_layout.addWidget(tmp_arRet_lb, 7, 0)
        group1_layout.addWidget(tmp_arBat_lb, 8, 0)

        group1_layout.addWidget(self.tmp_oleo_vl, 0, 1, QtCore.Qt.AlignRight)
        group1_layout.addWidget(self.tmp_radE_vl, 1, 1, QtCore.Qt.AlignRight)
        group1_layout.addWidget(self.tmp_radS_vl, 2, 1, QtCore.Qt.AlignRight)
        group1_layout.addWidget(self.tmp_esc1_vl, 3, 1, QtCore.Qt.AlignRight)
        group1_layout.addWidget(self.tmp_esc2_vl, 4, 1, QtCore.Qt.AlignRight)
        group1_layout.addWidget(self.tmp_esc3_vl, 5, 1, QtCore.Qt.AlignRight)
        group1_layout.addWidget(self.tmp_esc4_vl, 6, 1, QtCore.Qt.AlignRight)
        group1_layout.addWidget(self.tmp_arRet_vl, 7, 1, QtCore.Qt.AlignRight)
        group1_layout.addWidget(self.tmp_arBat_vl, 8, 1, QtCore.Qt.AlignRight)


        # DISTANCE LABELS
        esterc_lb = QtWidgets.QCheckBox("Esterçamento")
        mRatio_lb = QtWidgets.QCheckBox("Motion Ratio")
        deslMola_lb = QtWidgets.QCheckBox("Desl. Mola")

        self.esterc_vl = QtWidgets.QLabel(" X")
        self.mRatio_vl = QtWidgets.QLabel(" X")
        self.deslMola_vl = QtWidgets.QLabel(" X")

        group2_layout.addWidget(esterc_lb, 0, 0)
        group2_layout.addWidget(mRatio_lb, 1, 0)
        group2_layout.addWidget(deslMola_lb, 2, 0)

        group2_layout.addWidget(self.esterc_vl, 0, 1, QtCore.Qt.AlignRight)
        group2_layout.addWidget(self.mRatio_vl, 1, 1, QtCore.Qt.AlignRight)
        group2_layout.addWidget(self.deslMola_vl, 2, 1, QtCore.Qt.AlignRight)

        # PRESSURE LABELS
        press_cilF_lb = QtWidgets.QCheckBox("Cilindro Diant.")
        press_cilT_lb = QtWidgets.QCheckBox("Cilindro Trase.")
        press_oleo_lb = QtWidgets.QCheckBox("Óleo")
        press_comb_lb = QtWidgets.QCheckBox("Combustível")

        self.press_cilF_vl = QtWidgets.QLabel(" bar")
        self.press_cilT_vl = QtWidgets.QLabel(" bar")
        self.press_oleo_vl = QtWidgets.QLabel(" bar")
        self.press_comb_vl = QtWidgets.QLabel(" bar")

        group3_layout.addWidget(press_cilF_lb, 0, 0)
        group3_layout.addWidget(press_cilT_lb, 1, 0)
        group3_layout.addWidget(press_oleo_lb, 2, 0)
        group3_layout.addWidget(press_comb_lb, 3, 0)

        group3_layout.addWidget(self.press_cilF_vl, 0, 1, QtCore.Qt.AlignRight)
        group3_layout.addWidget(self.press_cilT_vl, 1, 1, QtCore.Qt.AlignRight)
        group3_layout.addWidget(self.press_oleo_vl, 2, 1, QtCore.Qt.AlignRight)
        group3_layout.addWidget(self.press_comb_vl, 3, 1, QtCore.Qt.AlignRight)


        # MISCELANEOUS LABELS
        acc_lb = QtWidgets.QCheckBox("Acelerômetro")
        gyro_lb = QtWidgets.QCheckBox("Giroscópio")
        speed_lb = QtWidgets.QCheckBox("Velocidade")
        rpm_lb = QtWidgets.QCheckBox("RPM")

        self.acc_vl = QtWidgets.QLabel(" a")
        self.gyro_vl = QtWidgets.QLabel(" g")
        self.speed_vl = QtWidgets.QLabel(" m/s")
        self.rpm_vl = QtWidgets.QLabel(" RPM")

        group4_layout.addWidget(acc_lb, 0, 0)
        group4_layout.addWidget(gyro_lb, 1, 0)
        group4_layout.addWidget(speed_lb, 2, 0)
        group4_layout.addWidget(rpm_lb, 3, 0)

        group4_layout.addWidget(self.acc_vl, 0, 1, QtCore.Qt.AlignRight)
        group4_layout.addWidget(self.gyro_vl, 1, 1, QtCore.Qt.AlignRight)
        group4_layout.addWidget(self.speed_vl, 2, 1, QtCore.Qt.AlignRight)
        group4_layout.addWidget(self.rpm_vl, 3, 1, QtCore.Qt.AlignRight)


        group1_layout.setColumnMinimumWidth(0, 30)


        # TIMED GRAPH PLOT 1
        self.box_graph_1 = QtWidgets.QGroupBox("GRÁFICOS - FUFPB")
        layout_graphs = QtWidgets.QGridLayout()
        self.box_graph_1.setLayout(layout_graphs)

        self.plot_widget1 = pg.PlotWidget(name='GROUP1', background='w')
        self.plot_widget1.hideAxis('left')
        self.plot_widget1.hideAxis('bottom')
        self.plot_widget1.hideAxis('right')
        self.plot_widget1.setRange(yRange=[0, 100, 250, 500, 750, 1030])


        # TIMED GRAPH PLOT 2
        self.plot_widget2 = pg.PlotWidget(name='GROUP2', background='w')
        self.plot_widget2.hideAxis('left')
        self.plot_widget2.hideAxis('bottom')
        self.plot_widget2.hideAxis('right')
        self.plot_widget2.setRange(yRange=[0, 100, 250, 500, 750, 1030])


        # HORIZONTAL GRAPH BAR
        self.hbar_figure = plt.figure(frameon=False)
        self.horizontal_canvas = FigureCanvas(self.hbar_figure)

        self.h_ax = self.hbar_figure.add_axes([0, 0, 1, 1])
        self.h_ax.barh(0, 15, 0.3, align='center')
        self.h_ax.set_xticks([0, 250, 500, 750, 1000])
        self.h_ax.set_xticklabels(["Horizontal value"])

        self.h_ax.axes.yaxis.set_visible(False)
        self.h_ax.spines['top'].set_visible(False)
        # self.h_ax.spines['bottom'].set_visible(False)
        self.h_ax.spines['left'].set_visible(False)
        # self.h_ax.spines['right'].set_visible(False)
        # self.h_ax.axis('off')

        # VERTICAL GRAPH BAR
        self.vbars_figure = plt.figure(figsize=(1, 10), dpi=80)
        self.vertical_canvas = FigureCanvas(self.vbars_figure)

        self.v_ax = self.vbars_figure.add_subplot(111)
        self.v_ax.bar(0.25, 15, 0.2, color='red', align='center')
        self.v_ax.bar(0, 10, 0.2, color='green')
        self.v_ax.set_yticks([0, 250, 500, 750, 1000])
        self.v_ax.set_xticks([0, 0.25])
        self.v_ax.set_xticklabels(("Throttle", "Break"))
        self.v_ax.axes.yaxis.set_visible(False)
        self.v_ax.spines['top'].set_visible(False)
        self.v_ax.spines['right'].set_visible(False)
        self.v_ax.spines['bottom'].set_visible(False)
        self.v_ax.spines['left'].set_visible(False)

        layout_graphs.addWidget(self.plot_widget1, 0, 0, 1, 4)
        layout_graphs.addWidget(self.horizontal_canvas, 1, 0, 1, 4)
        layout_graphs.addWidget(self.vertical_canvas, 2, 3)
        layout_graphs.addWidget(self.plot_widget2, 2, 0, 1, 3)

        layout_graphs.setRowMinimumHeight(0, 200)
        layout_graphs.setRowMinimumHeight(1, 50)
        layout_graphs.setRowMinimumHeight(2, 200)

    def wupdate_plot(self):
        # graph time = plot_time/delay_data
        plot_time, ig = self.plot_time_spin.currentText().split()
        graph_time = (int(plot_time)*1000)/50
        X = list(range(int(graph_time)))
        self.Y = list([200] * int(graph_time))
        self.Y2 = list([200] * int(graph_time))
        pen_color = 'b'
        x_value = 0
        all_values = list()
        self.plt_size = int(graph_time) * (-1)

        # PLOT 1 CURVES
        self.curve = self.plot_widget1.plot(clear=True)
        self.curve2 = self.plot_widget1.plot()

        #PLOT 2 CURVES
        self.curve3 = self.plot_widget2.plot(clear=True)

        while True:
            pen_color = (0, 0, 0) if x_value < (1023*0.8) else 'r'

            # self.plot_widget1.plot(X, Y, clear=True, pen=pg.mkPen(pen_color, width=2))

            self.curve.setData(self.Y[self.plt_size:], pen=pg.mkPen(pen_color, width=2))
            self.curve2.setData(self.Y2[self.plt_size:], pen=pg.mkPen('b', width=2))

            self.curve3.setData(self.Y[self.plt_size:], pen=pg.mkPen('g', width=2))
            # self.plot_widget2.plot(X, Y, clear=True, pen='b')
            try:
                self.socket_con.send("ok".encode())
                all_values = list(int(self.socket_con.recv(1024).decode('utf-8')))
                x_value = all_values[0]
            except Exception as e:
                print(f"Unreadable value: {e}")
            else:
                self.Y.append(x_value)
                self.Y2.append(x_value * 2)


                print(x_value)
                print("size of array: ", len(self.Y),  len(self.Y2))

            self.tmp_oleo_vl.setText(str(x_value) + " °")
            self.tmp_radE_vl.setText(str(x_value) + " °")
            self.tmp_radS_vl.setText(str(x_value) + " °")
            self.tmp_esc1_vl.setText(str(x_value) + " °")
            self.tmp_esc2_vl.setText(str(x_value) + " °")
            self.tmp_esc3_vl.setText(str(x_value) + " °")
            self.tmp_esc4_vl.setText(str(x_value) + " °")
            self.tmp_arRet_vl.setText(str(x_value) + " °")
            self.tmp_arBat_vl.setText(str(x_value) + " °")
            self.esterc_vl.setText(str(x_value) + " X")
            self.mRatio_vl.setText(str(x_value) + " X")
            self.deslMola_vl.setText(str(x_value) + " X")
            self.press_cilF_vl.setText(str(x_value) + " bar")
            self.press_cilT_vl.setText(str(x_value) + " bar")
            self.press_oleo_vl.setText(str(x_value) + " bar")
            self.press_comb_vl.setText(str(x_value) + " bar")
            self.acc_vl.setText(str(x_value) + " a")
            self.gyro_vl.setText(str(x_value) + " g")
            self.speed_vl.setText(str(x_value) + " m/s")
            self.rpm_vl.setText(str(x_value) + " RPM")

            self.v_ax.patches[1].set_height(x_value)
            self.v_ax.patches[0].set_height(x_value*2)
            self.h_ax.patches[0].set_width(x_value)

            self.horizontal_canvas.draw()
            self.vertical_canvas.draw()
            QtGui.QApplication.processEvents()

            if self.c_status == "Desconectado":
                break


    def cd_wireless(self):
        host = self.host_entry.text()
        port = int(self.port_entry.text())
        self.socket_con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.c_status == "Desconectado":
            try:
                self.socket_con.connect((host, port))
            except Exception as e:
                print("Could not stablish connection: ", e)
            else:
                print("Connected.")
                self.connect_btn_label = "Desconectar"
                self.c_status = "Conectado"
                self.connections_status_label.setText(self.c_status)
                self.connect_button.setText(self.connect_btn_label)
                self.wupdate_plot()
        else:
            print("Disconnected from {}.".format(host))
            self.socket_con.close()
            self.connect_btn_label = "Conectar"
            self.c_status = "Desconectado"
            self.connections_status_label.setText(self.c_status)
            self.connect_button.setText(self.connect_btn_label)
            # self.curve.cle

        pass


    def save_data(self):
        i = 0
        while os.path.exists("data%s.csv" % i):
            i += 1

        csvfile = "data" + str(i) + ".csv"
        with open(csvfile, "w") as output:
            writer = csv.writer(output, lineterminator='\n')
            for value in self.Y[100:]:
                writer.writerow(['value','value2'])
                writer.writerow([value, value*2])


        pass
