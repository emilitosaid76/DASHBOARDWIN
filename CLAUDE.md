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

- **Entorno de prueba:** Validado en Windows 11 (Ryzen 9 7950X, RTX 3090, monitor vertical 800x1280). `run.ps1` detecta correctamente pantalla secundaria en modo kiosco; `nvidia-smi` operativo.
- **Corrección de Bug:** Solucionado error de lectura de CPU (siempre 0) implementando un hilo *daemon* en `server.py` que muestrea cada 1s, evitando el conflicto de hilos entre `psutil` y `ThreadingHTTPServer`.
- **Configuración Chrome:** `run.ps1` incluye flags (`--no-first-run`, `--no-default-browser-check`, `--disable-features=ChromeWhatsNewUI,SigninInterceptBubble`) para omitir diálogos de login en Chrome 154 con perfiles temporales.
- **Interfaz visual:** Medidores con degradado según posición (amarillo suave `hsl(52,85%,72%)` → rojo al 90%). Color aplicado también a valores numéricos (`gradColor/colorFor` en `static/index.html`). Línea de historial mantiene color verde.
- **Monitoreo térmico:** Temperatura de CPU operativa mediante LibreHardwareMonitor v0.9.6 en ruta específica, ejecutado vía tarea programada como administrador al iniciar sesión. Servidor web en puerto 8085.
- **Red:** Servidor configurado para escuchar únicamente en `127.0.0.1`.
- **Pendiente de pruebas:** Ejecución de `instalar.bat`.
- **Próximos pasos:** Decidir si la línea de historial usará degradado; evaluar implementación de paneles para red y VRAM.
