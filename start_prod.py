import subprocess
import os

def main():
    # Переход в директорию проекта
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)

    # Сборка Docker-образа для продуктивной среды без использования кэша
    subprocess.run(["docker-compose", "-f", "docker-compose.prod.yml", "build", "--no-cache", "alita_service"], check=True)

    # Остановка и удаление предыдущих контейнеров
    subprocess.run(["docker-compose", "-f", "docker-compose.prod.yml", "rm", "--force", "--stop", "alita_service"], check=True)

    # Запуск новых контейнеров в фоновом режиме
    subprocess.run(["docker-compose", "-f", "docker-compose.prod.yml", "up", "-d", "alita_service"], check=True)

if __name__ == "__main__":
    main()
