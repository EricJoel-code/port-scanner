import argparse
from .scanner import scan_ports
from .services import get_service
from .banner import grab_banner
from .exporter import export_to_csv, export_to_html
from .logger import setup_logger
from .network import get_hosts


def main():
    # Crear el parser
    parser = argparse.ArgumentParser(description="Escaneador de puertos simple")

    parser.add_argument(
        "-i", "--ip", type=str, required=True, help="Direccion IP o red a escanear"
    )

    parser.add_argument("-s", "--start", type=int, required=True, help="Puerto inicial")

    parser.add_argument("-e", "--end", type=int, required=True, help="Puerto final")

    parser.add_argument(
        "-t",
        "--threads",
        type=int,
        default=100,
        help="Numero de hilos para el escaneo (default: 100)",
    )

    parser.add_argument(
        "--timeout",
        type=float,
        default=1,
        help="Tiempo de espera por conexión (default: 1s)",
    )

    parser.add_argument(
        "-o", "--output", type=str, help="Archivo CSV o HTML para guardar resultados"
    )

    args = parser.parse_args()

    logger = setup_logger()

    ip = args.ip
    hosts = get_hosts(ip)

    start_port = args.start
    end_port = args.end
    threads = args.threads
    timeout = args.timeout
    output_file = args.output

    logger.info(f"Escaneo iniciado para {ip}")

    # Escaneo por cada host
    for host in hosts:

        print(f"\n[+] Escaneando {host} ({start_port}-{end_port})...\n")
        logger.info(f"Iniciando escaneo en {host}")

        open_ports, closed_ports, elapsed_time = scan_ports(
            host, start_port, end_port, threads=threads, timeout=timeout
        )

        print("[+] Puertos abiertos:")

        if open_ports:
            for port in open_ports:

                service = get_service(port)
                banner = grab_banner(host, port, timeout)

                logger.info(f"{host}:{port} abierto - Servicio: {service}")

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

        print(f"\n[✔] Escaneo completado en {elapsed_time} segundos.")
        logger.info(f"Escaneo completado en {host}")


if __name__ == "__main__":
    main()
