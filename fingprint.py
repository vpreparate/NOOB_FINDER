import socket
import os
import re
import requests
from bs4 import BeautifulSoup
from rich.console import Console
from fake_useragent import UserAgent

console = Console()

# Регулярные выражения для определения версий серверов
apache_version_regex = r'Apache\/([\d\.]+)'  # Пример: Apache/2.4.41
MicrosoftIIS_regex = r'Microsoft-IIS\/([\d\.]+)'  # Пример: Microsoft-IIS/10.0
nginx_version_regex = r'nginx\/([\d\.]+)'  # Пример: nginx/1.18.0


def generate_random_user_agent():
    ua = UserAgent()
    return ua.random

def make_request(url):
    headers = {
        'User-Agent': generate_random_user_agent()
    }
    
    response = requests.get(f'http://{url}', headers=headers, timeout=1)
    return response


def ftpfing(ip, port=21):
    """ Получает название сервиса и его версию по указанному IP и порту. """
    try:
        # Создание сокета
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((ip, port))

        # Получаем данные от сервера
        response = sock.recv(1024).decode('utf-8')
        
        # Инициализация переменных для сервиса и версии
        service = "Unknown Service"
        version = "Unknown Version"
        
        # Регулярные выражения для поиска версий
        version_pattern = r'(\d+\.\d+(\.\d+)?)'  # Паттерн для поиска номеров версий

        if response.startswith("220"):
            # Если ответ начинается с "220", это типичное приветствие FTP-сервера
            if "Pure-FTP" in response:
                service = "Pure-FTP"
            elif "vsftpd" in response:
                service = "vsftpd"
            elif "ProFTPD" in response:
                service = "ProFTPD"
            elif "FileZilla" in response:
                service = "FileZilla"
            elif "Microsoft FTP Service" in response:
                service = "Microsoft FTP Service"
            elif "Wu-FTPD" in response:
                service = "Wu-FTPD"
            elif "Net::FTP" in response:
                service = "Net::FTP"
            elif "BSD" in response and "ftp" in response:
                service = "BSD FTPD"
            else:  # Если сервис не найден, пытаемся распарсить
                service_regex = r'(?<=220 ).*?(?=\r\n|\n)'  # Извлечь строку, следующую за 220
                service_match = re.search(service_regex, response)
                service = service_match.group(0) if service_match else "Unknown Service"

            # Поиск версии в ответе
            version_matches = re.findall(version_pattern, response)
            if version_matches:
                version = version_matches[0][0]  # Используя первую найденную версию
            else:
                #version = response.strip()  # Если версия не найдена, записываем полный ответ сервера
                version = "Unknown Version"

        return service, version
    except Exception as e:
        return "Unknown Service", str(e)
    finally:
        sock.close()
        with open('ftpfing.txt', 'a') as file:
            file.write(f"IP: {ip}, Service: {service}, Version: {version}\n")

def httpfing(url):
    with open('Apache.txt', "a") as apache_file, open('other.txt', "a") as others, open('Microsoft_IIS.txt', "a") as MICROIIS, open('nginx.txt', "a") as nginx_file:
        try:
            response = make_request(url)
            
            server_header = response.headers.get("Server", "").lower()  # Приводим к нижнему регистру для удобства
            
            # Проверяем, что сервер использует Apache
            if "apache" in server_header:
                apache_version_match = re.search(apache_version_regex, server_header)
                version = apache_version_match.group(1) if apache_version_match else "Unknown"
                
                # Проверяем, используется ли SAML
                soup = BeautifulSoup(response.content, "html.parser")
                saml_forms = soup.find_all("form", attrs={"action": lambda x: x and "saml" in x.lower()})
                saml_status = "Yes" if saml_forms else "No"
                
                apache_file.write(f"IP: {url} | Apache version: {version} | SAML: {saml_status}\n")
            
            elif "microsoft-iis" in server_header:
                microsoft_version_match = re.search(MicrosoftIIS_regex, server_header)
                versionMicrosoft = microsoft_version_match.group(1) if microsoft_version_match else "Unknown"
                
                MICROIIS.write(f"IP: {url} | Microsoft IIS version: {versionMicrosoft}\n")
            
            elif "nginx" in server_header:
                nginx_version_match = re.search(nginx_version_regex, server_header)
                version_nginx = nginx_version_match.group(1) if nginx_version_match else "Unknown"

                nginx_file.write(f"IP: {url} | Nginx version: {version_nginx}\n")
            
            else:
                if server_header:
                    others.write(f"IP: {url} | Server: {server_header}\n")
                else:
                    others.write(f"IP: {url} | Unknown server\n")
                    

        except requests.exceptions.RequestException:
            console.print(".", end="")
        except Exception as e:
            console.print(".", end="")

def sshfing(ip, port=22):
    sock = None  # Инициализация сокета
    try:
        # Создание сокета и подключение к SSH серверу
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect((ip, port))

        # Чтение баннера SSH сервера
        banner = sock.recv(1024)  # Увеличено до 2048 для возможного более полного баннера
        try:
            banner = banner.decode('utf-8').strip()
        except UnicodeDecodeError:
            try:
                banner = banner.decode('latin-1').strip()
            except UnicodeDecodeError:
                banner = banner.decode('ISO-8859-1', errors='ignore').strip()
        
        # Запись баннера в файл
        with open('sshfing.txt', 'a') as output_file:
            output_file.write(f'{ip} {banner}\n')
    except Exception as e:
        console.print("[bold red]-_-", end="")
    finally:
        if sock:
            sock.close()  # Закрываем сокет только если он был инициализирован



