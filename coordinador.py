import os
import subprocess
import sys
import time

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COMPOSE_APP = os.path.join(BASE_DIR, "docker", "docker-compose.yml")
COMPOSE_LLM = os.path.join(BASE_DIR, "docker", "llm", "docker-compose.yml")

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}=== {text} ==={Colors.ENDC}")

def print_success(text):
    print(f"{Colors.GREEN}{text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.BLUE}{text}{Colors.ENDC}")

def run_command(command, cwd=None):
    try:
        print_info(f"Ejecutando: {command}")
        subprocess.run(command, shell=True, check=True, cwd=cwd)
    except subprocess.CalledProcessError as e:
        print(f"{Colors.FAIL}Error ejecutando comando: {e}{Colors.ENDC}")
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Operación cancelada por el usuario.{Colors.ENDC}")

def get_compose_cmd(file_path):
    return f"docker compose -f \"{file_path}\""

def manage_stack(name, compose_file):
    cmd_base = get_compose_cmd(compose_file)

    while True:
        print_header(f"Gestión de {name}")
        print("1. Levantar (Up -d)")
        print("2. Reconstruir y Levantar (Up -d --build)")
        print("3. Detener (Stop)")
        print("4. Bajar (Down)")
        print("5. Ver Logs (Logs -f)")
        print("6. Ver Estado (PS)")
        print("0. Volver al menú principal")

        choice = input(f"\nSeleccione una opción para {name}: ")

        if choice == '1':
            run_command(f"{cmd_base} up -d")
        elif choice == '2':
            run_command(f"{cmd_base} up -d --build")
        elif choice == '3':
            run_command(f"{cmd_base} stop")
        elif choice == '4':
            run_command(f"{cmd_base} down")
        elif choice == '5':
            try:
                run_command(f"{cmd_base} logs -f")
            except KeyboardInterrupt:
                pass
        elif choice == '6':
            run_command(f"{cmd_base} ps")
        elif choice == '0':
            break
        else:
            print("Opción no válida.")

        input("\nPresione Enter para continuar...")

def manage_all():
    cmd_app = get_compose_cmd(COMPOSE_APP)
    cmd_llm = get_compose_cmd(COMPOSE_LLM)

    while True:
        print_header("Gestión Global (Todo)")
        print("1. Levantar Todo (Up -d)")
        print("2. Reconstruir Todo (Up -d --build)")
        print("3. Bajar Todo (Down)")
        print("4. Ver Estado Global")
        print("0. Volver al menú principal")

        choice = input("\nSeleccione una opción global: ")

        if choice == '1':
            print_info("Levantando LLM...")
            run_command(f"{cmd_llm} up -d")
            print_info("Levantando App...")
            run_command(f"{cmd_app} up -d")
        elif choice == '2':
            print_info("Reconstruyendo LLM...")
            run_command(f"{cmd_llm} up -d --build")
            print_info("Reconstruyendo App...")
            run_command(f"{cmd_app} up -d --build")
        elif choice == '3':
            print_info("Bajando App...")
            run_command(f"{cmd_app} down")
            print_info("Bajando LLM...")
            run_command(f"{cmd_llm} down")
        elif choice == '4':
            run_command(f"{cmd_llm} ps")
            run_command(f"{cmd_app} ps")
        elif choice == '0':
            break
        else:
            print("Opción no válida.")

        input("\nPresione Enter para continuar...")

def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print_header("COORDINADOR ANYTHING-LLM")
        print(f"Directorio Base: {BASE_DIR}")
        print("1. Gestionar LLM (Ollama + DeepSeek)")
        print("2. Gestionar App (AnythingLLM)")
        print("3. Gestionar TODO")
        print("4. Utilidades Docker (Prune)")
        print("0. Salir")

        choice = input("\nSeleccione una opción: ")

        if choice == '1':
            manage_stack("LLM Stack", COMPOSE_LLM)
        elif choice == '2':
            manage_stack("App Stack", COMPOSE_APP)
        elif choice == '3':
            manage_all()
        elif choice == '4':
            confirm = input("¿Está seguro de ejecutar docker system prune? (s/n): ")
            if confirm.lower() == 's':
                run_command("docker system prune -f")
        elif choice == '0':
            print_success("¡Hasta luego!")
            sys.exit(0)
        else:
            print("Opción no válida.")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Programa interrumpido.{Colors.ENDC}")
        sys.exit(0)
