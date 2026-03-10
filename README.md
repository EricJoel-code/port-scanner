# 🔍 PortScanner — Escáner de Puertos TCP en Python

EHerramienta profesional de escaneo de puertos TCP desarrollada en Python.
Permite identificar puertos abiertos y cerrados en un host específico utilizando sockets y ejecución concurrente mediante multithreading.

El proyecto está estructurado como paquete instalable y puede ejecutarse como:

* 🖥️ Interfaz gráfica (GUI) desarrollada con tkinter
* ⌨️ Herramienta CLI profesional (portscan)

---

## 🚀 Características

* Escaneo de puertos TCP
* Definición de rango personalizado de puertos
* Escaneo rápido usando Top Ports (puertos más comunes) con --top-ports
* Escaneo de red completa usando CIDR (ej: 192.168.1.0/24)
* Descubrimiento automático de hosts activos en la red
* Identificación de puertos abiertos y cerrados
* Escaneo concurrente con multithreading configurable
* Motor de escaneo optimizado que acepta listas de puertos o rangos
* Detección básica de servicios por puerto estándar
* Banner Grabbing para identificación real del servicio
* Banner Grabbing Concurrente para mejorar la velocidad del escaneo  
* Barra de progreso en tiempo real durante el escaneo
* Medición del tiempo total de escaneo
---
📊 Exportación y Reportes
* Exportación de resultados a CSV
* Generación de reportes HTML estructurados
* Resultados listos para análisis o documentación
---
⚙️ Configuración avanzada
* Configuración de número de hilos --threads
* Configuración de timeout por puerto --timeout
* Modo de escaneo optimizado con --top-ports
---
🛠 Arquitectura del proyecto
* CLI profesional con argumentos avanzados
* Interfaz gráfica desacoplada del core
* Arquitectura modular
* Separación clara de responsabilidades
* Código reutilizable orientado a paquetes
* Sistema de logging profesional (INFO, WARNING, ERROR)
* Manejo robusto de excepciones y errores de red
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
│   └── discovery.py      # Configuración para verifica si un host está activo 
│   └── network.py        # Configuración para convertir una IP o red CIDR en una lista de hosts
│   └── progress.py       # Configuración para ver la barra de progreso al escanear un puerto y el host
│   └── top_ports.py      # Lista de puertos comunes
│
├── gui/
│   └── app.py            # Interfaz gráfica (tkinter)
│
├── venv/                 # Entorno virtual
│
├── setup.py
├── reporte-puertos.html  # Visualización de los puertos escaneados 
├── reporte-hosts.html    # Visualización de los resultados de los hosts activos (si no hay hosts activos los campos quedan vacios)
├── portscanner.log       # Visualización de los logs
├── requirements.txt
├── main.py               # Archivo principal
└── README.md
```

---

### 🧠 Explicación del flujo de ejecución

1. El usuario ejecuta la herramienta desde CLI o GUI.
2. El módulo de red genera los hosts a partir de la IP o red CIDR.
3. Se realiza descubrimiento de hosts activos.
4. El motor de escaneo analiza los puertos de cada host.
5. Se identifican servicios y se obtiene el banner de los puertos abiertos.
6. Los resultados se muestran al usuario y pueden exportarse a CSV o HTML.
7. Todo el proceso queda registrado en el sistema de logs.

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

### Escaneo rápido con puertos comunes

```bash
portscan -i 127.0.0.1 --top-ports
```

### Parámetros disponibles

| Parámetro      | Descripción                                          |
| -------------- | ---------------------------------------------------- |
| -i/--i         | Dirección IP objetivo o red CIDR                     |
| -s/--start     | Puerto inicial                                       |
| -e/--end       | Puerto final                                         |
| -t/--threads   | Número de hilos (default: 100)                       |
| --timeout      | Tiempo de espera por puerto en segundos (default: 1) |
| -h             | Mostrar ayuda                                        |
| -o/--output    | Exportar resultados a archivo CSV o HTML             |
| --top-ports    | Escanea solo los más comunes                         |

### Ejemplo Avanzado

```bash
portscan -i 127.0.0.1 -s 1 -e 100 --threads 200 --timeout 0.5
```

### Ejemplo de Salida

```bash
[OPEN] 22 → SSH | Banner: SSH-2.0-OpenSSH_8.4
[OPEN] 80 → HTTP | Banner: HTTP/1.1 200 OK
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

### Escaneo de red completa
Esto escaneará todos los hosts de la red dentro del rango de puertos indicado

```bash
portscan -i 192.168.1.0/24 -s 20 -e 50
```

### Escaneo de red rápido

```bash
portscan -i 192.168.1.0/24 --top-ports --threads 200
```

### Escaneo rápido de red con exportación

Este comando:
```bash
portscan -i 192.168.1.0/24 -s 20 -e 50 --threads 200 --timeout 0.5 -o reporte.html
```
- Escanea toda la red local
- Revisa puertos del 20 al 50
- Usa 200 hilos concurrentes
- Timeout de 0.5 segundos por puerto
- Genera reporte HTML

¿Cuándo termina el escaneo?
El escaneo finaliza cuando:
```
Todos los puertos del rango definido
han sido evaluados en todos los hosts objetivo
```
Por ejemplo:
```
192.168.1.0/24
Puertos 20 → 50
```
Se ejecutarán aproximadamente:
```
254 hosts × 31 puertos ≈ 7874 conexiones
```
El uso de threads permite acelerar significativamente este proceso.

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

### Fase 1 — Base del escáner
* [x] Escaneo secuencial de puertos
* [x] Interfaz CLI
* [x] Interfaz gráfica (GUI)
* [x] Detección de puertos abiertos y cerrados
* [x] Configuración de rango de puertos

### Fase 2 — Rendimiento y optimización
* [x] Escaneo concurrente con multithreading
* [x] Configuración de threads y timeout
* [x] Medición de tiempo de escaneo
* [x] Motor de escaneo optimizado que acepta listas de puertos
* [x] Escaneo rápido con **Top Ports**

### Fase 3 — Análisis de servicios
* [x] Detección de servicios comunes por puerto
* [x] Banner grabbing
* [x] Banner grabbing concurrente optimizado

### Fase 4 — Escaneo de red
* [x] Descubrimiento de hosts activos
* [x] Escaneo de red usando CIDR
* [x] Barra de progreso durante el escaneo

### Fase 5 — Reportes y exportación
* [x] Exportación a CSV
* [x] Generación de reportes HTML
* [x] Sistema de logging profesional

### Fase 6 — Próximas mejoras
* [ ] Detección avanzada de servicios por banner
* [ ] Resultados en tiempo real durante el escaneo
* [ ] Reportes separados por host
* [ ] Sistema de configuración por archivo
* [ ] Tests automatizados


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
