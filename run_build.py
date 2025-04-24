import uvicorn
import socket
import subprocess
import os


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
    # Run npm build inside frontend directory
    frontend_dir = os.path.join(os.getcwd(), "frontend")
    if os.path.exists(frontend_dir):
        try:
            print("Running npm build in frontend directory...")
            subprocess.run(["npm.cmd", "run", "build"], cwd=frontend_dir, check=True)
            print("npm build completed successfully.")
        except subprocess.CalledProcessError:
            print("npm build failed. Check for errors.")

    else:
        print("Frontend directory not found. Skipping build step.")
    # Get and print local addresses
    print("Local addresses:")
    print(" - http://127.0.0.1:8000")
    for ip in get_ip_addresses():
        print(f" - http://{ip}:8000")
    # Start the server bound to 0.0.0.0 (listening on all interfaces)
    uvicorn.run("backend.app:app", host="0.0.0.0", port=8000, reload=True)
