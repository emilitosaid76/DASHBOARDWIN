@echo off
REM Detecta la pantalla auxiliar (tambien si esta en vertical) y abre el dashboard a pantalla completa ahi.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0run.ps1"
