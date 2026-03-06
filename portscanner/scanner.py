# socket es una biblioteca que se utiliza para crear conexiones de red
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
import time


def scan_port(ip, port, timeout):
    """
    Escanea un puerto específico en una dirección IP.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)

    try:
        result = sock.connect_ex((ip, port))
        return result == 0
    except socket.error:
        return False
    finally:
        sock.close()


def print_progress(completed, total):
    """
    Muestra una barra de progreso visual en consola.
    """
    bar_length = 30
    percent = completed / total
    filled_length = int(bar_length * percent)

    bar = "█" * filled_length + "-" * (bar_length - filled_length)

    print(
        f"\rProgress: [{bar}] {percent*100:.1f}% ({completed}/{total})",
        end="",
        flush=True,
    )


def scan_ports(ip, start_port, end_port, threads=100, timeout=1):
    """
    Escanea un rango de puertos en una dirección IP específica.
    """

    start_time = time.time()

    open_ports = []
    closed_ports = []

    ports = list(range(start_port, end_port + 1))
    total_ports = len(ports)
    completed = 0

    with ThreadPoolExecutor(max_workers=threads) as executor:

        future_to_port = {
            executor.submit(scan_port, ip, port, timeout): port for port in ports
        }

        for future in as_completed(future_to_port):
            port = future_to_port[future]

            try:
                if future.result():
                    open_ports.append(port)
                else:
                    closed_ports.append(port)
            except Exception:
                closed_ports.append(port)

            # actualizar progreso
            completed += 1
            print_progress(completed, total_ports)

    elapsed_time = round(time.time() - start_time, 4)

    print()  # salto de línea después de la barra

    return sorted(open_ports), sorted(closed_ports), elapsed_time
