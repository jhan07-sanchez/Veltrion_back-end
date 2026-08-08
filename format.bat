@echo off
echo "Ejecutando Ruff Linter (auto-fix)..."
venv\Scripts\ruff.exe check --fix .
echo "Ejecutando Ruff Formatter..."
venv\Scripts\ruff.exe format .
echo "Listo! Todos los archivos han sido formateados."
pause
