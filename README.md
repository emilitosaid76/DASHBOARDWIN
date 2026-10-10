# Dashboard de monitoreo (Windows)

Panel estilo Grafana a pantalla completa con: CPU use, CPU temp, MEM use, GPU use, GPU temp, GPU power.
Se adapta a cualquier resolución (usa unidades vw/vh), así que ocupa el segundo monitor completo.

## Requisitos
1. Python 3 y `pip install -r requirements.txt`
2. GPU NVIDIA con driver instalado (`nvidia-smi` en el PATH).
3. Temperatura de CPU: instalar [LibreHardwareMonitor](https://github.com/LibreHardwareMonitor/LibreHardwareMonitor),
   abrirlo como administrador y activar **Options → Remote Web Server** (puerto 8085). Sin esto la temp de CPU muestra N/A.

## Uso
Doble clic en `run.bat`: detecta automáticamente la pantalla secundaria (posición, resolución y orientación) y abre
el dashboard en modo kiosco ahí. En pantalla vertical el diseño cambia solo a 2 columnas x 3 filas. Cierra con Alt+F4.

Solo servidor: `python server.py` y abre http://localhost:8000
