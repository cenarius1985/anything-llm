import os
import subprocess
import sys

# Definir rutas relativas a este script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCKER_DIR = os.path.join(BASE_DIR, 'docker')
LLM_DIR = os.path.join(DOCKER_DIR, 'llm')

# Archivos docker-compose
COMPOSE_APP = os.path.join(DOCKER_DIR, 'docker-compose.yml')

# La ruta a LLM es opcional ya que el usuario puede no usarla
COMPOSE_LLM = os.path.join(LLM_DIR, 'docker-compose.yml')

def print_header(text):
    print(f"\n{'='*50}")
    print(f" {text}")
    print(f"{'='*50}")

def run_command(command, cwd=None):
    try:
        print(f"Ejecutando: {command}")
        subprocess.run(command, shell=True, check=True, cwd=cwd)
    except subprocess.CalledProcessError as e:
        print(f"Error ejecutando comando: {e}")
    except KeyboardInterrupt:
        print("\nOperación cancelada por el usuario.")

def get_compose_cmd(file_path):
    return f"docker compose -f \"{file_path}\""

def manage_stack(name, compose_file):
    cmd = get_compose_cmd(compose_file)
    while True:
        print_header(f"Gestión {name}")
        print("1. Levantar (Up -d)")
        print("2. Reconstruir (Up -d --build)")
        print("3. Actualizar Imágenes (Pull)")
        print("4. Reiniciar Contenedores (Restart)")
        print("5. Eliminar/Bajar (Down)")
        print("6. Ver Logs (Logs -f)")
        print("7. Ver Estado (PS)")
        print("0. Volver al menú principal")

        choice = input(f"\nSeleccione una opción para {name}: ")

        if choice == '1':
            run_command(f"{cmd} up -d")
        elif choice == '2':
            run_command(f"{cmd} up -d --build")
        elif choice == '3':
            run_command(f"{cmd} pull")
        elif choice == '4':
            run_command(f"{cmd} restart")
        elif choice == '5':
            run_command(f"{cmd} down")
        elif choice == '6':
            try:
                run_command(f"{cmd} logs -f")
            except KeyboardInterrupt:
                pass
        elif choice == '7':
            run_command(f"{cmd} ps")
        elif choice == '0':
            break
        else:
            print("Opción inválida.")

def manage_all():
    cmd_app = get_compose_cmd(COMPOSE_APP)
    cmd_llm = get_compose_cmd(COMPOSE_LLM)

    while True:
        print_header("Gestión Global (Todo)")
        print("1. Levantar Todo (LLM + App)")
        print("2. Reconstruir Todo (LLM + App)")
        print("3. Actualizar Todo (Pull)")
        print("4. Reiniciar Todo")
        print("5. Bajar Todo (Down)")
        print("6. Ver Estado Global")
        print("7. Actualización Automática Completa (Git + Docker)")
        print("0. Volver al menú principal")

        choice = input("\nSeleccione una opción global: ")

        if choice == '1':
            print("Levantando LLM...")
            if os.path.exists(COMPOSE_LLM):
                run_command(f"{cmd_llm} up -d")
            else:
                print("No se encontró docker-compose de LLM, saltando...")
            print("Levantando App...")
            run_command(f"{cmd_app} up -d")
        elif choice == '2':
            print("Reconstruyendo LLM...")
            if os.path.exists(COMPOSE_LLM):
                run_command(f"{cmd_llm} up -d --build")
            else:
                print("No se encontró docker-compose de LLM, saltando...")
            print("Reconstruyendo App...")
            run_command(f"{cmd_app} up -d --build")
        elif choice == '3':
            print("Actualizando LLM...")
            if os.path.exists(COMPOSE_LLM):
                run_command(f"{cmd_llm} pull")
            else:
                print("No se encontró docker-compose de LLM, saltando...")
            print("Actualizando App...")
            run_command(f"{cmd_app} pull")
        elif choice == '4':
            print("Reiniciando LLM...")
            if os.path.exists(COMPOSE_LLM):
                run_command(f"{cmd_llm} restart")
            else:
                print("No se encontró docker-compose de LLM, saltando...")
            print("Reiniciando App...")
            run_command(f"{cmd_app} restart")
        elif choice == '5':
            print("Bajando App...")
            run_command(f"{cmd_app} down")
            print("Bajando LLM...")
            if os.path.exists(COMPOSE_LLM):
                run_command(f"{cmd_llm} down")
            else:
                print("No se encontró docker-compose de LLM, saltando...")
        elif choice == '6':
            print("Estado LLM:")
            if os.path.exists(COMPOSE_LLM):
                run_command(f"{cmd_llm} ps")
            else:
                print("No se encontró docker-compose de LLM.")
            print("\nEstado App:")
            run_command(f"{cmd_app} ps")
        elif choice == '7':
            auto_update_full()
        elif choice == '0':
            break
        else:
            print("Opción inválida.")

def auto_update_full():
    print_header("Actualización Automática Completa")
    print("Esta acción realizará los siguientes pasos:")
    print("1. Git: Checkout master")
    print("2. Git: Pull upstream master (Actualizar código fuente oficial)")
    print("3. Git: Checkout anything-lm-studio (Tu rama)")
    print("4. Git: Merge master (Fusionar cambios)")
    print("5. Docker: Down (Bajar contenedores)")
    print("6. Docker: Up -d --build (Reconstruir y levantar)")
    
    confirm = input("\n¿Desea continuar? (s/n): ")
    if confirm.lower() != 's':
        print("Operación cancelada.")
        return

    try:
        # Git Operations
        print("\n[GIT] Cambiando a master...")
        run_command("git checkout master")
        
        print("\n[GIT] Actualizando master desde upstream...")
        # Intentar upstream primero, si falla probar origin
        try:
            run_command("git pull upstream master")
        except:
            print("Falló upstream, intentando origin...")
            run_command("git pull origin master")
            
        print("\n[GIT] Cambiando a rama anything-lm-studio...")
        run_command("git checkout anything-lm-studio")
        
        print("\n[GIT] Fusionando cambios de master...")
        run_command("git merge master")
        
        # Docker Operations
        cmd_app = get_compose_cmd(COMPOSE_APP)
        
        print("\n[DOCKER] Bajando contenedores...")
        run_command(f"{cmd_app} down")
        
        print("\n[DOCKER] Reconstruyendo y levantando contenedores...")
        run_command(f"{cmd_app} up -d --build")
        
        print("\n¡Actualización completada exitosamente!")
        
    except Exception as e:
        print(f"\n[ERROR] Ocurrió un error durante la actualización: {e}")
        print("Se recomienda revisar el estado manualmente.")

def menu():
    while True:
        print_header("Coordinador AnythingLLM")
        print("1. Gestionar Stack LLM (Ollama/DeepSeek)")
        print("2. Gestionar Stack App (AnythingLLM)")
        print("3. Gestión Global (Todo)")
        print("0. Salir")

        choice = input("\nSeleccione una opción: ")

        if choice == '1':
            manage_stack("LLM", COMPOSE_LLM)
        elif choice == '2':
            manage_stack("App", COMPOSE_APP)
        elif choice == '3':
            manage_all()
        elif choice == '0':
            sys.exit()
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\nSaliendo...")
        sys.exit()
