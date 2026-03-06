def show_port_progress(current, total):

    bar_length = 30
    progress = current / total

    filled = int(bar_length * progress)

    bar = "█" * filled + "-" * (bar_length - filled)

    print(f"\r[PORT SCAN] [{bar}] {current}/{total} ports", end="")


def show_network_progress(current, total):

    bar_length = 30
    progress = current / total

    filled = int(bar_length * progress)

    bar = "█" * filled + "-" * (bar_length - filled)

    print(f"\r[NETWORK SCAN] [{bar}] {current}/{total} hosts", end="")
