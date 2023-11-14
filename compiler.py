import subprocess

# Reemplaza 'tu_script.py' con el nombre real de tu script
script_name = 'game.py'

# Comando de PyInstaller para compilar el script en un solo archivo ejecutable
command = f'C:\\Users\\yamir\\AppData\\Local\\Programs\\Python\\Python310\\Scripts\\pyinstaller --onefile {script_name}'

# Ejecuta el comando en la terminal o símbolo del sistema
subprocess.run(command, shell=True)
