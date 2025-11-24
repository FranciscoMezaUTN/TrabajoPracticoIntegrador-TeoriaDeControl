# Simulador de Control de Ancho de Banda (PID) - Router TP-Link Archer C7

![Python](https://img.shields.io/badge/Python-3.x-blue.svg) ![Status](https://img.shields.io/badge/Status-Finalizado-green.svg) ![UTN](https://img.shields.io/badge/UTN-FRBA-red.svg)

Este repositorio contiene el código fuente de la simulación desarrollada para el **Trabajo Práctico Integrador (TPI)** de la asignatura **Teoría de Control**.

El proyecto modela y simula un sistema de control de lazo cerrado (PID) aplicado a la gestión de QoS (*Quality of Service*) en un router SOHO, demostrando la capacidad de regulación de *throughput* y rechazo a perturbaciones de tráfico.

## 📋 Descripción del Sistema

La simulación implementa un modelo matemático discretizado que representa:
* **Planta:** Dinámica de un router TP-Link Archer C7 (Primer orden + Retardo).
* **Controlador:** Algoritmo PID digital sintonizado mediante el método de Ziegler-Nichols.
* **Perturbaciones:** Inyección de carga de tráfico variable (usuarios concurrentes).

El objetivo es visualizar cómo el sistema mantiene la velocidad de transmisión real igual a la deseada, compensando automáticamente la congestión de la red.

---

## ⚙️ Requisitos Previos (Pre-seteo)

Para ejecutar la simulación correctamente, es necesario contar con **Python 3** instalado y las bibliotecas gráficas y de cálculo numérico.

### 1. Instalar Python
Si no tiene Python instalado, descárguelo desde [python.org](https://www.python.org/downloads/). Asegúrese de marcar la opción **"Add Python to PATH"** durante la instalación.

### 2. Instalar Dependencias
Abra una terminal (o consola de comandos) y ejecute el siguiente comando para instalar las librerías necesarias (`PyQt5`, `pyqtgraph`, `numpy`):

```bash
pip install PyQt5 pyqtgraph numpy
