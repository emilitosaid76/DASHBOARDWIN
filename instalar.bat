@echo off
REM Clona el dashboard, instala dependencias y lo abre en la pantalla secundaria.
REM Repo: DASHBOARDWIN
setlocal
set REPO=https://github.com/emilitosaid76/DASHBOARDWIN.git
set BRANCH=main
set DEST=%USERPROFILE%\DASHBOARDWIN

where git >nul 2>&1 || (echo Falta Git: https://git-scm.com/download/win & pause & exit /b 1)
where python >nul 2>&1 || (echo Falta Python: https://www.python.org/downloads/ ^(marca "Add to PATH"^) & pause & exit /b 1)

if exist "%DEST%\.git" (
  echo Actualizando %DEST% ...
  git -C "%DEST%" pull
) else (
  echo Clonando en %DEST% ...
  git clone --branch %BRANCH% "%REPO%" "%DEST%" || (echo Fallo el clon. Si el repo es privado, inicia sesion en Git/GitHub. & pause & exit /b 1)
)

python -m pip install -r "%DEST%\requirements.txt" || (pause & exit /b 1)

where nvidia-smi >nul 2>&1 || echo AVISO: nvidia-smi no esta en el PATH; los paneles de GPU saldran N/A.
echo.
echo Recuerda: para CPU temp abre LibreHardwareMonitor como administrador y activa Options - Remote Web Server.
echo.
call "%DEST%\run.bat"
