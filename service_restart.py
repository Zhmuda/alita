import subprocess

def restart_service(service_name):
    subprocess.run(["sudo", "systemctl", "restart", service_name], check=True)

if __name__ == "__main__":
    # Перезапуск тестовой службы
    restart_service("alita_test.service")

    # Перезапуск продуктивной службы
    restart_service("alita_prod.service")
