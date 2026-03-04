import argparse
from .scanner import scan_ports
import csv
from .services import get_service
from .banner import grab_banner
from datetime import datetime


# Función para exportar resultados a CSV
def export_to_csv(filename, open_ports, closed_ports):
    with open(filename, mode="w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Puerto", "Estado", "Servicio"])
        for port in open_ports:
            writer.writerow([port, "OPEN", get_service(port)])
        for port in closed_ports:
            writer.writerow([port, "CLOSED", "-"])


# Función para exportar resultados a HTML
def export_to_html(
    filename, ip, start_port, end_port, open_ports, closed_ports, elapsed_time
):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(
            f"""
<!DOCTYPE html>
<html>
<head>
<title>Reporte Port Scanner</title>
<style>
body {{ font-family: Arial; background-color: #f4f4f4; }}
h1 {{ color: #333; }}
table {{ border-collapse: collapse; width: 100%; }}
th, td {{ border: 1px solid #ddd; padding: 8px; text-align: center; }}
th {{ background-color: #333; color: white; }}
.open {{ background-color: #c8f7c5; }}
.closed {{ background-color: #f7c5c5; }}
</style>
</head>
<body>

<h1>Reporte de Escaneo</h1>
<p><strong>IP:</strong> {ip}</p>
<p><strong>Rango:</strong> {start_port} - {end_port}</p>
<p><strong>Fecha:</strong> {datetime.now()}</p>
<p><strong>Tiempo de escaneo:</strong> {elapsed_time} segundos</p>

<table>
<tr>
<th>Puerto</th>
<th>Estado</th>
<th>Servicio</th>
<th>Banner</th>
</tr>
"""
        )

        # Puertos abiertos
        for port in open_ports:
            service = get_service(port)
            banner = grab_banner(ip, port)
            f.write(
                f"""
<tr class="open">
<td>{port}</td>
<td>OPEN</td>
<td>{service}</td>
<td>{banner if banner else "-"}</td>
</tr>
"""
            )

        # Puertos cerrados
        for port in closed_ports:
            f.write(
                f"""
<tr class="closed">
<td>{port}</td>
<td>CLOSED</td>
<td>-</td>
<td>-</td>
</tr>
"""
            )

        f.write(
            """
</table>
</body>
</html>
"""
        )


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
            service = get_service(port)
            banner = grab_banner(ip, port, timeout)
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
        else:
            print(f"\n[!] Formato no soportado. Use .csv o .html")

    print(f"\n[✔] Escaneo completado en {elapsed_time} segundos.")


if __name__ == "__main__":
    main()
