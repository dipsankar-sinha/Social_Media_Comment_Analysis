import uvicorn
import socket


def get_ip_addresses():
    """Return a list of local network IP addresses."""
    ip_addresses = []
    hostname = socket.gethostname()
    try:
        # Add the primary IP address from hostname
        ip_addresses.append(socket.gethostbyname(hostname))
    except Exception:
        pass

    # Get additional IP addresses using getaddrinfo
    try:
        for addr in socket.getaddrinfo(hostname, None):
            ip = addr[4][0]
            if ip not in ip_addresses and '.' in ip:  # ignore IPv6
                ip_addresses.append(ip)
    except Exception:
        pass
    return ip_addresses

if __name__ == "__main__":
    # Get and print local addresses
    print("Local addresses:")
    print(" - http://127.0.0.1:8000")
    for ip in get_ip_addresses():
        print(f" - http://{ip}:8000")

    # Start the server bound to 0.0.0.0 (listening on all interfaces)
    uvicorn.run("backend.app:app", host="0.0.0.0", port=8000, reload=True)
