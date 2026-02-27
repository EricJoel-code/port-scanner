import argparse

# from portscanner.scanner import scan_ports
from portscanner.scanner import scan_ports
import csv


# Función para exportar resultados a CSV
def export_to_csv(filename, open_ports, closed_ports):
    with open(filename, mode="w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Puerto", "Estado"])
        for port in open_ports:
            writer.writerow([port, "OPEN"])
        for port in closed_ports:
            writer.writerow([port, "CLOSED"])


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

    ip = args.ip
    start_port = args.start
    end_port = args.end
    threads = args.threads
    timeout = args.timeout
    output_file = args.output

    print(f"[+] Escaneando {ip} ({start_port}-{end_port})...\n")

    # Llamar a la lógica reutilizada, obteniendo los puertos abiertos, cerrados y el tiempo de escaneo.
    open_ports, closed_ports, elapsed_time = scan_ports(
        ip, start_port, end_port, threads=threads, timeout=timeout
    )

    # Mostrar resultados
    print("[+] Puertos abiertos:")
    if open_ports:
        for port in open_ports:
            print(f"    [OPEN] {port}")
    else:
        print("    Ninguno")

    print("\n[-] Puertos cerrados:")
    for port in closed_ports:
        print(f"    [CLOSED] {port}")

    if output_file:
        export_to_csv(output_file, open_ports, closed_ports)
        print(f"\n[+] Resultados guardados en {output_file}")

    print(f"\n[✔] Escaneo completado en {elapsed_time} segundos.")


if __name__ == "__main__":
    main()
