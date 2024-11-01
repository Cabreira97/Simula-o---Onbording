import os
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager  
import time

def open_github_repo(url, repo_name):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    print(f"\nAcessando {repo_name}: {url}")
    return driver

def run_command(command, description, cwd=None):
    print(f"\n--- {description} ---")
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"\nErro ao executar o comando '{command}': {stderr.decode()}")
    else:
        print(stdout.decode())

def clone_and_setup_frontend():
    run_command("git clone git@github.com:Cabreira97/simula--o-admin.git", "Clonando o repositório do frontend")
    if os.path.exists('simula-admin'):
        os.chdir('simula-admin')  
        if os.path.exists('.env.example'):
            run_command("cp .env.example .env", "Copiando .env.example para .env")
        else:
            print("O arquivo .env.example não foi encontrado. Certifique-se de que ele exista.")
            return
        skip_install = input("Gostaria de pular a instalação das dependências? (s/n): ").strip().lower()
        if skip_install != 's':
            run_command("yarn", "Instalando dependências com Yarn") 
        run_command("yarn start", "Iniciando o frontend") 
    else:
        print("Diretório simula-admin não encontrado. Verifique se o repositório foi clonado corretamente.")

def clone_and_setup_backend():
    run_command("git clone git@github.com:Cabreira97/simula--o-api.git", "Clonando o repositório do backend")
    if os.path.exists('simula-api-main'):
        os.chdir('simula-api-main')  
        if os.path.exists('.env.example'):
            run_command("cp .env.example .env", "Copiando .env.example para .env")
        else:
            print("O arquivo .env.example não foi encontrado. Certifique-se de que ele exista.")
            return
        start_container = input("Gostaria de subir o container do backend? (s/n): ").strip().lower()
        if start_container == 's':
            run_command("docker compose up", "Iniciando o backend com Docker")  
        else:
            print("Container do backend não foi iniciado.")
    else:
        print("Diretório simula-api-main não encontrado. Verifique se o repositório foi clonado corretamente.")

if __name__ == "__main__":
    driver_frontend = open_github_repo("https://github.com/Cabreira97/simula--o-admin", "simula-admin")
    driver_backend = open_github_repo("https://github.com/Cabreira97/simula--o-api", "simula-api-main")
    driver_clickup = open_github_repo("https://clickup.com", "ClickUp")

    clone_and_setup_frontend()
    os.chdir('..')  
    clone_and_setup_backend()
    
    time.sleep(10)
    driver_frontend.quit()
    driver_backend.quit()
    driver_clickup.quit()
