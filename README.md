# Simulador de Control de Ancho de Banda (PID) - Router TP-Link Archer C7

![Python](https://img.shields.io/badge/Python-3.x-blue.svg) ![Status](https://img.shields.io/badge/Status-Finalizado-green.svg) ![UTN](https://img.shields.io/badge/UTN-FRBA-red.svg)

Este repositorio contiene el código fuente de la simulación desarrollada para el **Trabajo Práctico Integrador Final (TFI)** de la asignatura **Teoría de Control**.

El proyecto modela y simula un sistema de control de lazo cerrado (PID) aplicado a la gestión de QoS (*Quality of Service*) en un router SOHO, demostrando la capacidad de regulación de la velocidad y rechazo a perturbaciones de tráfico.

## 📋 Descripción del Sistema

La simulación implementa un modelo matemático que representa:
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
```

Nota: Si el comando anterior falla en Windows, intente con:

```bash
python -m pip install PyQt5 pyqtgraph numpy
```

## 🚀 Instrucciones de Ejecución

Siga estos pasos para poner en marcha la simulación:

### 1. Clonar o Descargar el Repositorio: 
Descargue los archivos de este proyecto en su computadora.

### 2. Abrir en el IDE: 
Abra la carpeta del proyecto en su entorno de desarrollo favorito (se recomienda Microsoft Visual Studio Code).

### 3. Ejecutar el Script: 
Abra una terminal integrada en el IDE (asegúrese de estar en la carpeta correcta donde está el archivo) y ejecute el siguiente comando:

```bash
python SIMULACION-Router-TP-TDC.py
```

## 🎮 Guía de Uso de la Simulación

Una vez iniciada la ventana gráfica, siga esta secuencia para observar el comportamiento del control:

### 1. Establecer Referencia (Paso 1): 
Mueva el slider superior izquierdo para fijar una velocidad deseada (ej. 50 Mbps). Observe cómo la salida (curva azul) alcanza el objetivo (curva verde punteada).

### 2. Inyectar Perturbación (Paso 2): 
Mueva el slider superior derecho para simular una carga repentina de tráfico (ej. 35 Mbps).

### 3. Observar la Corrección: 
Verá cómo la velocidad real cae momentáneamente debido a la perturbación, pero el controlador PID acciona (curva roja) y logra recuperar la velocidad al valor deseado automáticamente y el Error volverá a cero. 
Nota: se recomienda hacer zoom en los graficos de la entrada y el error usando la ruedita del mouse para ver la variación con mayor claridad.

## 👥 Autores e Información Académica

### Universidad Tecnológica Nacional - Facultad Regional Buenos Aires (UTN.BA)

· Materia: Teoría de Control (K4572)

· Docente: Prof. Mgtr. Omar Civale

· Ciclo Lectivo: 2025

### Integrantes del Grupo:

· Meza Longa, Juan Francisco

· Rabaglia Garberi, Sabrina Victoria
