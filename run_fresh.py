#!/usr/bin/env python3
"""
Script para ejecutar main.py sin usar caché de Python
"""
import sys
import os
import importlib
import shutil

def clean_cache():
    """Limpia todos los archivos de caché de Python"""
    print("🧹 Limpiando caché de Python...")
    
    # Eliminar archivos .pyc
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pyc'):
                try:
                    os.remove(os.path.join(root, file))
                    print(f"   Eliminado: {os.path.join(root, file)}")
                except:
                    pass
    
    # Eliminar directorios __pycache__
    for root, dirs, files in os.walk('.', topdown=False):
        for dir in dirs:
            if dir == '__pycache__':
                try:
                    shutil.rmtree(os.path.join(root, dir))
                    print(f"   Eliminado directorio: {os.path.join(root, dir)}")
                except:
                    pass
    
    print("✅ Caché limpiado")

def reload_modules():
    """Recarga todos los módulos del proyecto"""
    print("🔄 Recargando módulos...")
    
    # Lista de módulos a recargar
    modules_to_reload = []
    for name in list(sys.modules.keys()):
        if name.startswith('app.') or name == 'main':
            modules_to_reload.append(name)
    
    # Recargar módulos
    for module_name in modules_to_reload:
        if module_name in sys.modules:
            try:
                importlib.reload(sys.modules[module_name])
                print(f"   Recargado: {module_name}")
            except:
                pass
    
    print("✅ Módulos recargados")

if __name__ == "__main__":
    print("🚀 Ejecutando con caché limpio...")
    
    # Limpiar caché
    clean_cache()
    
    # Establecer variable de entorno para evitar bytecode
    os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
    
    # Recargar módulos si ya están en memoria
    reload_modules()
    
    # Importar y ejecutar main
    try:
        import main
        print("\n" + "="*50)
        main.main()
        print("="*50)
    except Exception as e:
        print(f"❌ Error ejecutando main: {e}")
