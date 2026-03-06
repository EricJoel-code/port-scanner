import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


def scan_port(ip, port, timeout):
    """
    Escanea un puerto específico en una dirección IP.
    """

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((ip, port))
            return port, result == 0
    except socket.error:
        return port, False


def scan_ports(ip, ports, threads=100, timeout=1, progress_callback=None):
    """
    Escanea una lista o rango de puertos en una IP.

    Parameters
    ----------
    ip : str
        Dirección IP
    ports : iterable
        Lista o rango de puertos
    threads : int
        Número de hilos
    timeout : float
        Timeout de conexión
    progress_callback : function
        Función opcional para mostrar progreso
    """

    start_time = time.time()

    open_ports = []
    closed_ports = []

    ports = list(ports)
    total_ports = len(ports)
    completed = 0

    with ThreadPoolExecutor(max_workers=threads) as executor:

        futures = [executor.submit(scan_port, ip, port, timeout) for port in ports]

        for future in as_completed(futures):

            port, is_open = future.result()

            if is_open:
                open_ports.append(port)
            else:
                closed_ports.append(port)

            completed += 1

            if progress_callback:
                progress_callback(completed, total_ports)

    elapsed_time = round(time.time() - start_time, 4)

    return sorted(open_ports), sorted(closed_ports), elapsed_time
