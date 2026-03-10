import socket
from concurrent.futures import ThreadPoolExecutor, as_completed


# Función para intentar grabar el banner de un servicio en un puerto específico
def grab_banner(ip, port, timeout=1):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((ip, port))

            # Intentar recibir un banner genérico
            banner = s.recv(1024).decode(errors="ignore").strip()

            if banner:
                return banner

            # Si no se recibe un banner, intentar enviar una solicitud específica para ciertos servicios
            if port in [80, 8080, 8000]:
                s.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
                response = s.recv(1024).decode(errors="ignore")

                return response.split("\r\n")[
                    0
                ]  # Retorna la primera línea del banner HTTP

    except Exception:
        return None

    return None


def grab_banners_concurrent(ip, ports, timeout=1, threads=20):
    """
    Obtiene banners de múltiples puertos abiertos de forma concurrente.
    """

    results = {}

    if not ports:
        return results

    with ThreadPoolExecutor(max_workers=threads) as executor:

        future_to_port = {
            executor.submit(grab_banner, ip, port, timeout): port for port in ports
        }

        for future in as_completed(future_to_port):

            port = future_to_port[future]

            try:
                banner = future.result()
                results[port] = banner
            except Exception:
                results[port] = None

    return results
