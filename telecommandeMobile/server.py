from flask import Flask, jsonify, request
from zeroconf import ServiceInfo, Zeroconf
import socket
import subprocess

app = Flask(__name__)

# Zeroconf setup
zeroconf = Zeroconf()
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

# Register the Flask service
service_info = ServiceInfo(
    "_http._tcp.local.",
    f"{hostname}._http._tcp.local.",
    socket.inet_aton(ip_address),
    5000,
    0,
    0,
    {"path": "/"},
)
zeroconf.register_service(service_info)

@app.route('/run', methods=['POST'])
def run_program():
    """Run a specified program."""
    data = request.json
    program_path = data.get("path")
    if not program_path:
        return jsonify({"error": "No program path provided"}), 400
    
    try:
        subprocess.Popen(program_path, shell=True)
        return jsonify({"status": "Program started", "path": program_path}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_ip', methods=['GET'])
def get_ip():
    """Return the server's current IP address."""
    return jsonify({"ip": ip_address, "hostname": hostname}), 200

@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check."""
    return jsonify({"status": "Server is running"}), 200

if __name__ == "__main__":
    try:
        print(f"Starting Flask server on {ip_address}:5000")
        app.run(host="0.0.0.0", port=5000)
    except KeyboardInterrupt:
        zeroconf.unregister_service(service_info)
        zeroconf.close()
        print("Server stopped")
