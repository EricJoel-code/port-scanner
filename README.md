# 🔍 PortScanner — Escáner de Puertos TCP en Python

EHerramienta profesional de escaneo de puertos TCP desarrollada en Python.
Permite identificar puertos abiertos y cerrados en un host específico utilizando sockets y ejecución concurrente mediante multithreading.

El proyecto está estructurado como paquete instalable y puede ejecutarse como:

* 🖥️ Interfaz gráfica (GUI) desarrollada con tkinter
* ⌨️ Herramienta CLI profesional (portscan)

---

## 🚀 Características

* Escaneo de puertos TCP
* Definición de rango personalizado
* Identificación de puertos abiertos y cerrados
* Escaneo concurrente con multithreading configurable
* Detección básica de servicios por puerto estándar
* Banner Grabbing (identificación real del servicio)
* Exportación de resultados a CSV
* Generación de reportes HTML estructurados
* Sistema de logging profesional configurable (INFO, WARNING, ERROR)
* Manejo robusto de excepciones y errores de red
* Configuración de número de hilos (--threads)
* Configuración de timeout por puerto (--timeout)
* Medición del tiempo total de escaneo
* CLI profesional con argumentos avanzados
* Interfaz gráfica no bloqueante (GUI desacoplada del core)
* Separación clara de responsabilidades (arquitectura modular)
* Código reutilizable orientado a paquetes
* Instalación como paquete local (pip install -e .)
* Arquitectura preparada para expansión profesional
* Proyecto orientado a ciberseguridad y análisis de red

---

## 🧱 Estructura del Proyecto

```text
port_scanner/
│
├── portscanner/
│   ├── __init__.py
│   └── scanner.py        # Motor de escaneo concurrente
│   └── cli.py            # Escáner por línea de comandos
│   └── services.py       # Mapeo de puertos comunes
│   └── banner.py         # Banner grabbing
│   └── export.py         # Funcionalidad para exportar los resultados a csv y html
│   └── logger.py         # Configuración profesional de logging
│
├── gui/
│   └── app.py            # Interfaz gráfica (tkinter)
│
├── venv/                 # Entorno virtual
│
├── setup.py
├── reporte-ejemplo.html  # Visualización de los resultados escaneados
├── portscanner.log       # Visualización de los logs
├── requirements.txt
├── main.py               # Archivo principal
└── README.md
```

---

## 🛠 Instalación (Recomendado)

1️⃣ Crear entorno virtual
```
python -m venv venv
```
Activar:

Windows:
```
venv\Scripts\activate
```
Linux / macOS:
```
source venv/bin/activate
```

2️⃣ Instalar el proyecto en modo editable
```
pip install -e .
```
Esto habilita el comando:
```
portscan
```

---

## ⌨️ Uso — CLI Profesional (Actualizado)

Ejecuta el escáner desde la raíz del proyecto:

```bash
portscan -i 127.0.0.1 -s 1 -e 100
```

### Parámetros disponibles

| Parámetro      | Descripción                                          |
| -------------- | ---------------------------------------------------- |
| -i/--i         | Dirección IP objetivo                                |
| -s/--start     | Puerto inicial                                       |
| -e/--end       | Puerto final                                         |
| -t/--threads   | Número de hilos (default: 100)                       |
| --timeout      | Tiempo de espera por puerto en segundos (default: 1) |
| -h             | Mostrar ayuda                                        |
| -o/--output    | Archivo CSV para exportar resultados                 |

### Ejemplo Avanzado

```bash
portscan -i 127.0.0.1 -s 1 -e 100 --threads 200 --timeout 0.5
```

### Redireccion de Salida

```bash
portscan -i 127.0.0.1 -s 1 -e 100 > resultados.txt
```

### Redireccion de Salida con exportación CSV

```bash
portscan -i 192.168.1.1 -s 1 -e 200 -t 200 --timeout 0.5 -o resultados.csv
```

### Redireccion de Salida con exportación HTML

```bash
portscan -i 8.8.8.8 -s 1 -e 200 -t 200 --timeout 0.5 -o reporte.html
```

### Ejemplo de Salida

```bash
[OPEN] 22 → SSH | Banner: SSH-2.0-OpenSSH_8.4
[OPEN] 80 → HTTP | Banner: HTTP/1.1 200 OK
```

---

## 🖥️ Uso — Interfaz Gráfica (GUI)

Desde la carpeta raíz del proyecto:

```bash
python -m gui.app
```

### Pasos

1. Ingresa la dirección IP objetivo
2. Define el puerto inicial y final
3. Haz clic en **Iniciar Escaneo**
4. Visualiza los puertos abiertos y cerrados
5. Usa **Nuevo Escaneo** para reiniciar

---

## 📋 Requisitos

* Python 3.9 o superior
* Librerías estándar de Python:

  * socket
  * threading
  * tkinter
  * argparse

No se requieren dependencias externas.

---

## 🧪 Ejemplos de IP para pruebas

* 127.0.0.1 — localhost
* 192.168.1.1 — router doméstico
* 8.8.8.8 — DNS público de Google

---

## ⚠️ Aviso Legal

Este proyecto es solo para fines educativos.
No escanees sistemas sin autorización explícita.

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Puedes:

* Reportar errores
* Proponer mejoras
* Enviar pull requests

---

## 🛣️ Roadmap

* [x] Escaneo secuencial de puertos
* [x] Interfaz gráfica (GUI)
* [x] Interfaz CLI
* [x] Escaneo multithreading
* [x] Configuración de threads y timeout
* [x] Medición de tiempo de escaneo
* [x] Exportación a CSV 
* [x] Detección de servicios comunes
* [x] Banner grabbing
* [x] Exportación HTML
* [x] Sistema de logs
* [ ] Tests automatizados
* [ ] Banner grabbing concurrente optimizado

---

## ⚙️ Configuración avanzada

El escáner permite ajustar el rendimiento mediante:

- --threads: Controla el número de hilos concurrentes.
- --timeout: Define el tiempo máximo de espera por puerto.

Esto permite adaptar la herramienta a redes rápidas o lentas.

---

## 🎯 Objetivo del Proyecto

Proyecto enfocado en aprendizaje práctico de:

* Sockets en Python
* Concurrencia con threading
* Arquitectura modular
* Empaquetado profesional
* Buenas prácticas de desarrollo

---

⭐ Si te resulta útil, ¡no olvides darle una estrella al repositorio!
