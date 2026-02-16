import os
import subprocess
import sys

# Definir rutas relativas a este script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCKER_DIR = os.path.join(BASE_DIR, 'docker')
LLM_DIR = os.path.join(DOCKER_DIR, 'llm')

# Archivos docker-compose
COMPOSE_APP = os.path.join(DOCKER_DIR, 'docker-compose.yml')
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
        print("0. Volver al menú principal")

        choice = input("\nSeleccione una opción global: ")

        if choice == '1':
            print("Levantando LLM...")
            run_command(f"{cmd_llm} up -d")
            print("Levantando App...")
            run_command(f"{cmd_app} up -d")
        elif choice == '2':
            print("Reconstruyendo LLM...")
            run_command(f"{cmd_llm} up -d --build")
            print("Reconstruyendo App...")
            run_command(f"{cmd_app} up -d --build")
        elif choice == '3':
            print("Actualizando LLM...")
            run_command(f"{cmd_llm} pull")
            print("Actualizando App...")
            run_command(f"{cmd_app} pull")
        elif choice == '4':
            print("Reiniciando LLM...")
            run_command(f"{cmd_llm} restart")
            print("Reiniciando App...")
            run_command(f"{cmd_app} restart")
        elif choice == '5':
            print("Bajando App...")
            run_command(f"{cmd_app} down")
            print("Bajando LLM...")
            run_command(f"{cmd_llm} down")
        elif choice == '6':
            print("Estado LLM:")
            run_command(f"{cmd_llm} ps")
            print("\nEstado App:")
            run_command(f"{cmd_app} ps")
        elif choice == '0':
            break
        else:
            print("Opción inválida.")

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
