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
