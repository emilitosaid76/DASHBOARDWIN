"""Dashboard de monitoreo para Windows (CPU, GPU, RAM).

- CPU / RAM: psutil
- GPU (NVIDIA): nvidia-smi (viene con el driver)
- Temperatura CPU: LibreHardwareMonitor con "Remote Web Server" activo (puerto 8085)
"""
import json
import os
import subprocess
import threading
import urllib.request
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

import psutil

PORT = int(os.environ.get("DASH_PORT", 8000))
LHM_URL = os.environ.get("LHM_URL", "http://localhost:8085/data.json")
STATIC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)

CPU_USE = 0.0


def _update_cpu():
    # psutil guarda la lectura previa por hilo; muestrear en un hilo fijo
    global CPU_USE
    while True:
        CPU_USE = psutil.cpu_percent(interval=1)


threading.Thread(target=_update_cpu, daemon=True).start()


def gpu_stats():
    try:
        out = subprocess.check_output(
            ["nvidia-smi",
             "--query-gpu=utilization.gpu,temperature.gpu,power.draw,power.limit,memory.used,memory.total",
             "--format=csv,noheader,nounits"],
            text=True, timeout=2, creationflags=NO_WINDOW,
        ).splitlines()[0]
        u, t, p, pl, mu, mt = [float(x) for x in out.split(",")]
        return {"use": u, "temp": t, "power": p, "power_max": pl,
                "mem_used": mu / 1024, "mem_total": mt / 1024}
    except Exception:
        return None


def _walk(node, in_cpu, found):
    img = (node.get("ImageURL") or "").lower()
    text = node.get("Text") or ""
    in_cpu = in_cpu or "cpu" in img
    val = node.get("Value") or ""
    if in_cpu and "°C" in val:
        try:
            found.append((text, float(val.split()[0].replace(",", "."))))
        except ValueError:
            pass
    for c in node.get("Children") or []:
        _walk(c, in_cpu, found)


def cpu_temp():
    """Temperatura CPU vía LibreHardwareMonitor; None si no está disponible."""
    try:
        with urllib.request.urlopen(LHM_URL, timeout=1) as r:
            data = json.load(r)
        found = []
        _walk(data, False, found)
        if not found:
            return None
        for key in ("package", "tctl", "tdie"):
            for name, v in found:
                if key in name.lower():
                    return v
        return max(v for _, v in found)
    except Exception:
        return None


def stats():
    vm = psutil.virtual_memory()
    return {
        "cpu": {"use": CPU_USE, "temp": cpu_temp()},
        "mem": {"use": vm.percent, "used": vm.used / 2**30, "total": vm.total / 2**30},
        "gpu": gpu_stats(),
    }


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=STATIC, **k)

    def do_GET(self):
        if self.path.startswith("/api/stats"):
            body = json.dumps(stats()).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            super().do_GET()

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    print(f"Dashboard en http://localhost:{PORT}")
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
