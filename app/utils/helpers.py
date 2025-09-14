
import subprocess
from dotenv import load_dotenv
import os

def php_get_rates(logger):
    command = ['php', 'artisan', 'get:rates']
    try:
        execution = subprocess.run(
                command,
                cwd=os.getenv("PHP_PROJECT_PATH"),              # Cambia el directorio de trabajo
                capture_output=True,         # Captura salida y errores
                text=True,                   # Devuelve strings en lugar de bytes
                check=True                   # Lanza excepción si el comando falla
            )
        if execution.stderr:
            logger.error(f"❌ Error en servidor PHP Lumen: {execution.stderr}")
            print("Servidor PHP Lumen:")
            print(f"❌ {execution.stderr}")
        else:
            logger.info(f"✅ Respuesta del servidor PHP Lumen: {execution.stdout}")
            print("Servidor PHP Lumen:")
            print(f"✅ {execution.stdout}")
    except subprocess.CalledProcessError as e:
        print("Error executing PHP script:", e.stderr)
        return False