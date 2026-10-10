# DASHBOARDWIN — notas del proyecto

Dashboard de monitoreo para Windows, estilo Grafana, a pantalla completa en una **pantalla secundaria/auxiliar en vertical**.

## Contexto del usuario
- PC destino: Windows 11, GPU **NVIDIA** (se lee con `nvidia-smi`). El PC es "el .7" de la red local (IP terminada en .7; sin confirmar el detalle).
- Métricas: CPU use, CPU temp, MEM use, GPU use, GPU temp, GPU power.
- Imagen de referencia: paneles con medidor de colores (verde/naranja/rojo) arriba y gráfica de historial abajo. Posible extra pendiente: panel de red (RX/TX), VRAM, ventilador.
- El usuario habla español; responder en español.

## Arquitectura
- `server.py`: servidor HTTP (stdlib) en 127.0.0.1:8000, endpoint `/api/stats`. CPU/RAM con psutil, GPU con nvidia-smi, temp CPU vía LibreHardwareMonitor (Remote Web Server, puerto 8085; requiere admin).
- `static/index.html`: front sin dependencias (SVG + canvas). Layout 3x2 en horizontal, 2x3 en vertical (`@media (orientation: portrait)`).
- `run.ps1` / `run.bat`: detectan la pantalla no principal y abren Chrome/Edge en kiosco ahí.
- `instalar.bat`: clona/actualiza el repo en `%USERPROFILE%\DASHBOARDWIN`, instala deps y lanza.

## Estado
- Probado solo en Linux (servidor + render vertical simulado 1080x1920). **Sin probar en Windows**: detección de pantalla, nvidia-smi, temp CPU, instalar.bat.
- Siguiente paso: correr en el PC real (sesión local) y corregir lo que salga N/A o abra en la pantalla equivocada.
- El servidor escucha solo en localhost; si se quiere ver desde otro equipo, cambiar a 0.0.0.0 y abrir el firewall.
