import ipaddress


def get_hosts(target):
    """
    Convierte una IP o red CIDR en una lista de hosts.
    """

    try:
        # Intentar interpretarlo como red
        network = ipaddress.ip_network(target, strict=False)

        hosts = [str(ip) for ip in network.hosts()]

        return hosts

    except ValueError:
        # Si no es red se asume que es una red simple
        return [target]
