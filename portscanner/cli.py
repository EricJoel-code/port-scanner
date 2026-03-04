import argparse
from .scanner import scan_ports
from .services import get_service
from .banner import grab_banner
from .exporter import export_to_csv, export_to_html
from .logger import setup_logger


def main():
    # Crear el parser
    parser = argparse.ArgumentParser(description="Escaneador de puertos simple")

    # Argumentos obligatorios
    parser.add_argument(
        "-i", "--ip", type=str, required=True, help="Direccion IP a escanear"
    )

    parser.add_argument(
        "-s",
        "--start",
        type=int,
        required=True,
        help="Puerto inicial del rango a escanear",
    )

    parser.add_argument(
        "-e", "--end", type=int, required=True, help="Puerto final del rango a escanear"
    )

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
        help="Tiempo de espera para cada conexión (default: 1 segundos)",
    )

    parser.add_argument(
        "-o", "--output", type=str, help="Archivo CSV para guardar los resultados"
    )

    # Leer los argumentos de la línea de comandos

    args = parser.parse_args()
    logger = setup_logger()

    ip = args.ip
    start_port = args.start
    end_port = args.end
    threads = args.threads
    timeout = args.timeout
    output_file = args.output

    print(f"[+] Escaneando {ip} ({start_port}-{end_port})...\n")

    logger.info(f"Escaneo iniciado en {ip} ({start_port}-{end_port})")

    # Llamar a la lógica reutilizada, obteniendo los puertos abiertos, cerrados y el tiempo de escaneo.
    open_ports, closed_ports, elapsed_time = scan_ports(
        ip, start_port, end_port, threads=threads, timeout=timeout
    )

    # Mostrar resultados
    print("[+] Puertos abiertos:")
    if open_ports:
        for port in open_ports:
            service = get_service(port)
            banner = grab_banner(ip, port, timeout)

            logger.info(f"Puerto {port} abierto - Servicio: {service}")

            if banner:
                print(f"    [OPEN] {port} → {service} | Banner: {banner}")
            else:
                print(f"    [OPEN] {port} → {service}")
    else:
        print("    Ninguno")

    print("\n[-] Puertos cerrados:")
    for port in closed_ports:
        print(f"    [CLOSED] {port}")

    if output_file:
        if output_file.endswith(".csv"):
            export_to_csv(output_file, open_ports, closed_ports)
            print(f"\n[+] Resultados guardados en {output_file}")
            logger.info(f"Resultados exportados en formato CSV: {output_file}")
        elif output_file.endswith(".html"):
            export_to_html(
                output_file,
                ip,
                start_port,
                end_port,
                open_ports,
                closed_ports,
                elapsed_time,
            )
            print(f"\n[+] Reporte HTML generado en {output_file}")
            logger.info(f"Reporte HTML generado: {output_file}")

        else:
            print(f"\n[!] Formato no soportado. Use .csv o .html")
            logger.warning("Intento de exportación con formato no soportado")

    logger.info(f"Escaneo completado en {elapsed_time} segundos")
    print(f"\n[✔] Escaneo completado en {elapsed_time} segundos.")


if __name__ == "__main__":
    main()
