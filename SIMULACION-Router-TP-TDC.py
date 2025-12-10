import sys
import numpy as np
from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg

# ==========================================
# PARÁMETROS AJUSTADOS PARA DEMO VISUAL
# ==========================================
DT = 0.01

# PID
KP = 24
KI = 2400
KD = 0.06  # (No se usa en tu demo, pero lo mostramos igual en pantalla)

# Planta
TAU = 0.5
L_DELAY = 0.0

# Límites
MAX_MBPS = 100.0
MIN_MBPS = 0.0
HISTORY_LEN = 500

class SimuladorRouter(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulación TPI - Control de Ancho de Banda")
        self.resize(1100, 1100)

        # Estado inicial
        self.referencia_setpoint = 0.0
        self.perturbacion_val = 0.0
        self.integral_sum = 0.0
        self.salida_real_actual = 0.0
        self.prev_error = 0.0  # Necesario para calcular la acción Derivativa (D)

        # Arrays de datos
        self.data_ref = np.zeros(HISTORY_LEN)
        self.data_salida_real = np.zeros(HISTORY_LEN)
        self.data_error = np.zeros(HISTORY_LEN)
        self.data_pid_out = np.zeros(HISTORY_LEN)
        self.data_actuator = np.zeros(HISTORY_LEN)
        self.data_perturb = np.zeros(HISTORY_LEN)

        self.setup_ui()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start(30)

    def setup_ui(self):
        pg.setConfigOption('background', 'k')
        pg.setConfigOption('foreground', 'w')

        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)

        # -----------------------------
        # CONTROLES SUPERIORES
        # -----------------------------
        ctrl_layout = QtWidgets.QHBoxLayout()

        # Grupo Referencia
        gb_ref = QtWidgets.QGroupBox("Entrada: Velocidad Deseada (θi)")
        vb_ref = QtWidgets.QVBoxLayout()
        self.sld_ref = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.sld_ref.setRange(0, 100)
        self.lbl_ref = QtWidgets.QLabel("0 Mbps")
        vb_ref.addWidget(self.sld_ref)
        vb_ref.addWidget(self.lbl_ref)
        gb_ref.setLayout(vb_ref)

        # Grupo Perturbación
        gb_dist = QtWidgets.QGroupBox("Perturbación: Carga Extra (D)")
        vb_dist = QtWidgets.QVBoxLayout()
        self.sld_dist = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.sld_dist.setRange(0, 50)
        self.lbl_dist = QtWidgets.QLabel("0 Mbps")
        vb_dist.addWidget(self.sld_dist)
        vb_dist.addWidget(self.lbl_dist)
        gb_dist.setLayout(vb_dist)

        # Grupo PID Values
        gb_pid = QtWidgets.QGroupBox("Sintonización PID (En vivo)")
        form = QtWidgets.QFormLayout()

        # SpinBox para Kp
        self.spin_kp = QtWidgets.QDoubleSpinBox()
        self.spin_kp.setRange(0.0, 500.0)
        self.spin_kp.setValue(KP)
        
        # SpinBox para Ki (Rango alto para permitir 2400)
        self.spin_ki = QtWidgets.QDoubleSpinBox()
        self.spin_ki.setRange(0.0, 5000.0)
        self.spin_ki.setValue(KI)

        # SpinBox para Kd (Decimales para precisión en 0.06)
        self.spin_kd = QtWidgets.QDoubleSpinBox()
        self.spin_kd.setRange(0.0, 10.0)
        self.spin_kd.setSingleStep(0.01)
        self.spin_kd.setDecimals(3)
        self.spin_kd.setValue(KD)

        form.addRow("Kp:", self.spin_kp)
        form.addRow("Ki:", self.spin_ki)
        form.addRow("Kd:", self.spin_kd)
        gb_pid.setLayout(form)

        ctrl_layout.addWidget(gb_ref)
        ctrl_layout.addWidget(gb_dist)
        ctrl_layout.addWidget(gb_pid)
        layout.addLayout(ctrl_layout)

        # Conectar eventos
        self.sld_ref.valueChanged.connect(self.update_labels)
        self.sld_dist.valueChanged.connect(self.update_labels)

        # -----------------------------
        # GRÁFICOS
        # -----------------------------
        self.graph_win = pg.GraphicsLayoutWidget()
        layout.addWidget(self.graph_win)

        # --- PLOT 1: Entrada vs Salida ---
        p1 = self.graph_win.addPlot(title="Referencia (verde) vs Salida Real (amarillo)")
        p1.setYRange(-5, 105)
        p1.showGrid(x=True, y=True)
        self.curve_ref = p1.plot(pen=pg.mkPen('g', width=3, style=QtCore.Qt.DashLine))
        self.curve_out = p1.plot(pen=pg.mkPen('y', width=3))

        self.graph_win.nextRow()

        # --- PLOT 2: Acciones de Control ---
        p2 = self.graph_win.addPlot(title="Salida del Controlador PID (cyan) y Salida del Actuador Saturada (blanco)")
        p2.setYRange(-10, 150)
        p2.showGrid(x=True, y=True)
        self.curve_pid = p2.plot(pen=pg.mkPen('c', width=2))
        self.curve_act = p2.plot(pen=pg.mkPen('w', width=2))
        p2.addLine(y=100, pen=pg.mkPen('r', width=1, style=QtCore.Qt.DotLine))

        self.graph_win.nextRow()

        # --- PLOT 3: Perturbación ---
        p3 = self.graph_win.addPlot(title="Perturbación (D)")
        p3.setYRange(-5, 55)
        p3.showGrid(x=True, y=True)
        self.curve_dist = p3.plot(pen=pg.mkPen('r', width=2))

        self.graph_win.nextRow()

        # --- PLOT 4: ERROR ---
        p4 = self.graph_win.addPlot(title="Error (e = θi − θo)")
        p4.setYRange(-100, 100)
        p4.showGrid(x=True, y=True)
        self.curve_err = p4.plot(pen=pg.mkPen('m', width=2))

    def update_labels(self):
        self.referencia_setpoint = self.sld_ref.value()
        self.perturbacion_val = self.sld_dist.value()
        self.lbl_ref.setText(f"{self.referencia_setpoint} Mbps")
        self.lbl_dist.setText(f"{self.perturbacion_val} Mbps")

    def update_simulation(self):
        # --- 1. PID ---
        # Leer ganancias actuales de la interfaz gráfica
        curr_kp = self.spin_kp.value()
        curr_ki = self.spin_ki.value()
        curr_kd = self.spin_kd.value()

        feedback = self.salida_real_actual
        error = self.referencia_setpoint - feedback

        # Acción Proporcional
        P = curr_kp * error

        # Acción Integral
        self.integral_sum += error * DT
        # Anti-windup simple (puedes ajustarlo si Ki es muy alto)
        self.integral_sum = np.clip(self.integral_sum, -100, 100)
        I = curr_ki * self.integral_sum

        # Acción Derivativa (Ahora sí funcional)
        derivative = (error - self.prev_error) / DT
        D = curr_kd * derivative
        
        # Guardar error para la siguiente iteración
        self.prev_error = error

        pid_out = P + I + D

        # --- 2. Saturación (Actuador) ---
        actuator_out = np.clip(pid_out, MIN_MBPS, MAX_MBPS)

        # --- 3. Planta ---
        entrada = actuator_out - self.perturbacion_val

        self.salida_real_actual += (entrada - self.salida_real_actual) * (DT / TAU)
        self.salida_real_actual = max(0, self.salida_real_actual)

        # --- 4. Actualización de buffers ---
        def roll(buf, value):
            buf[:-1] = buf[1:]
            buf[-1] = value

        roll(self.data_ref, self.referencia_setpoint)
        roll(self.data_salida_real, self.salida_real_actual)
        roll(self.data_error, error)
        roll(self.data_pid_out, pid_out)
        roll(self.data_actuator, actuator_out)
        roll(self.data_perturb, self.perturbacion_val)

        # --- 5. Dibujar ---
        self.curve_ref.setData(self.data_ref)
        self.curve_out.setData(self.data_salida_real)
        self.curve_pid.setData(self.data_pid_out)
        self.curve_act.setData(self.data_actuator)
        self.curve_dist.setData(self.data_perturb)
        self.curve_err.setData(self.data_error)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = SimuladorRouter()
    win.show()
    sys.exit(app.exec_())
