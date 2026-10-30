@echo off
rem Genera los datos de la GUI y la abre en el navegador (http://localhost:8765)
chcp 65001 > nul
cd /d "%~dp0"

where python > nul 2>&1
if errorlevel 1 (
    echo No se encontro python en el PATH.
    pause
    exit /b 1
)

python main.py -guidata
if errorlevel 1 (
    echo.
    echo Error al generar los datos de la GUI.
    pause
    exit /b 1
)

echo.
echo GUI disponible en http://localhost:8765/Comercios%%20Unidos%%20Insights.html
echo Cierra esta ventana para detener el servidor.
pause > nul
