import subprocess
import platform
from concurrent.futures import ThreadPoolExecutor, as_completed
from .progress import show_network_progress


def ping_host(host):
    """
    Verifica si un host está activo usando ping.
    """

    param = "-n" if platform.system().lower() == "windows" else "-c"

    command = ["ping", param, "1", host]

    try:
        result = subprocess.run(
            command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

        return result.returncode == 0

    except Exception:
        return False


def discover_hosts(hosts, threads=100):
    """
    Descubre qué hosts están activos en una red.
    """

    active_hosts = []
    total_hosts = len(hosts)
    completed = 0

    with ThreadPoolExecutor(max_workers=threads) as executor:

        futures = {executor.submit(ping_host, host): host for host in hosts}

        for future in as_completed(futures):

            host = futures[future]

            try:
                if future.result():
                    active_hosts.append(host)
            except:
                pass

            completed += 1
            show_network_progress(completed, total_hosts)

    print()  # salto de línea

    return sorted(active_hosts)
