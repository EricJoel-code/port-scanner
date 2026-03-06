import argparse
from .scanner import scan_ports
from .services import get_service
from .banner import grab_banner
from .exporter import export_to_csv, export_to_html
from .logger import setup_logger
from .network import get_hosts
from .discovery import discover_hosts
from .progress import show_network_progress


def main():

    parser = argparse.ArgumentParser(description="Escáner de puertos TCP profesional")

    # Argumentos obligatorios
    parser.add_argument(
        "-i",
        "--ip",
        type=str,
        required=True,
        help="Dirección IP o red en formato CIDR (ej: 192.168.1.0/24)",
    )

    parser.add_argument("-s", "--start", type=int, required=True, help="Puerto inicial")

    parser.add_argument("-e", "--end", type=int, required=True, help="Puerto final")

    parser.add_argument(
        "-t", "--threads", type=int, default=100, help="Número de hilos (default: 100)"
    )

    parser.add_argument(
        "--timeout", type=float, default=1, help="Timeout por conexión (default: 1)"
    )

    parser.add_argument(
        "-o", "--output", type=str, help="Archivo de salida (.csv o .html)"
    )

    args = parser.parse_args()

    logger = setup_logger()

    ip = args.ip
    start_port = args.start
    end_port = args.end
    threads = args.threads
    timeout = args.timeout
    output_file = args.output

    print(f"\n[+] Red objetivo: {ip}")

    # Obtener hosts de la red
    hosts = get_hosts(ip)

    print(f"[+] Hosts totales en rango: {len(hosts)}")

    logger.info(f"Hosts detectados en rango: {len(hosts)}")

    # Descubrimiento de hosts activos
    print("\n[+] Descubriendo hosts activos...")

    active_hosts = discover_hosts(hosts, threads=threads)

    print(f"[+] Hosts activos encontrados: {len(active_hosts)}")

    logger.info(f"Hosts activos: {active_hosts}")

    if not active_hosts:
        print("\n[!] No se encontraron hosts activos.")
        logger.warning("No se detectaron hosts activos")
        if output_file:
            if output_file.endswith(".html"):
                export_to_html(output_file, ip, start_port, end_port, [], [], 0)
                print(f"[+] Reporte generado: {output_file}")

            elif output_file.endswith(".csv"):
                export_to_csv(output_file, [], [])
                print(f"[+] CSV generado: {output_file}")

        return

    # Escaneo de cada host activo
    total_hosts = len(active_hosts)

    for index, host in enumerate(active_hosts, start=1):

        print(f"\n[+] Escaneando host {host} ({start_port}-{end_port})")

        logger.info(f"Iniciando escaneo en {host}")

        open_ports, closed_ports, elapsed_time = scan_ports(
            host, start_port, end_port, threads=threads, timeout=timeout
        )

        # Mostrar resultados
        print("\n[+] Puertos abiertos:")

        if open_ports:

            for port in open_ports:

                service = get_service(port)
                banner = grab_banner(host, port, timeout)

                logger.info(f"{host}:{port} abierto - servicio: {service}")

                if banner:
                    print(f"    [OPEN] {port} → {service} | Banner: {banner}")
                else:
                    print(f"    [OPEN] {port} → {service}")

        else:
            print("    Ninguno")

        print("\n[-] Puertos cerrados:")

        for port in closed_ports:
            print(f"    [CLOSED] {port}")

        # Exportación
        if output_file:

            if output_file.endswith(".csv"):

                export_to_csv(output_file, open_ports, closed_ports)

                print(f"\n[+] Resultados guardados en {output_file}")

                logger.info(f"Resultados exportados CSV: {output_file}")

            elif output_file.endswith(".html"):

                export_to_html(
                    output_file,
                    host,
                    start_port,
                    end_port,
                    open_ports,
                    closed_ports,
                    elapsed_time,
                )

                print(f"\n[+] Reporte HTML generado en {output_file}")

                logger.info(f"Reporte HTML generado: {output_file}")

            else:

                print("\n[!] Formato no soportado. Use .csv o .html")

                logger.warning("Formato de exportación no soportado")

        logger.info(f"Escaneo finalizado en {host} ({elapsed_time}s)")

        print(f"\n[✔] Escaneo completado en {elapsed_time} segundos.")
        show_network_progress(index, total_hosts)
        print()


if __name__ == "__main__":
    main()
