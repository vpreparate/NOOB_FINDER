import socket
import requests
import random
#import secrets
from rich.console import Console
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

console = Console()


def generate_random_user_agent():
    ua = UserAgent()
    return ua.random

def make_requesth(url):
    headers = {
        'User-Agent': generate_random_user_agent()
    }
    
    response = requests.head(f'http://{url}', headers=headers, timeout=1)
    return response

def make_requestg(url):
    headers = {
        'User-Agent': generate_random_user_agent()
    }
    
    response = requests.head(f'http://{url}', headers=headers, timeout=1)
    return response

def gen_ip():
        # Генерируем 4 случайных числа от 0 до 255
        octets = [
            str(random.randint(0, 255)) for _ in range(4)]
            #str(secrets.randbelow(256)),  # от 0 до 255
            #str(secrets.randbelow(256)),
            #str(secrets.randbelow(256)),
            #str(secrets.randbelow(254) + 1)  # от 1 до 254, чтобы избежать 0 и 255]

        # Проверка на наличие в зарезервированных диапазонах
        if not (
            (octets[0] == '10') or
            (octets[0] == '172' and 16 <= int(octets[1]) <= 31) or
            (octets[0] == '192' and octets[1] == '168') or
            (octets[0] == '127') or
            (octets[0] == '0') or
            (octets[0] == '255') or
            (octets[0] == '169' and octets[1] == '254')
        ):
            random_ip = '.'.join(octets)

            # Проверка уникальности
            return random_ip

# Функция для проверки портов
def check_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)  # Устанавливаем таймаут в 1 секунду
    try:
        result = sock.connect_ex((ip, port))
        return result == 0
    finally:
        sock.close()

def log_result(cms_type, message):
    filename = f"{cms_type}.txt"  # Имя файла будет зависеть от типа CMS
    with open(filename, 'a') as log_file:
        log_file.write(message + "\n")

def check_wordpress(url):
    console.print(f"[bold blue][+] Проверка WordPress: {url}")
    wp_check_paths = [
        "/wp-admin/",
        "/wp-login.php",
        "/wp-content/uploads/",
        "/wp-content/plugins/",
        "/readme.html",
        "/license.txt"
    ]

    for path in wp_check_paths:
        try:
            full_url = url + path
            r = make_requesth(full_url)
            if r.status_code == 200:
                console.print(f"[bold green][!] Дира WordPress: {full_url}")
                log_result("Wordpress", f"Найдена WordPress: {full_url}")

        except requests.RequestException as e:
            console.print(f"[bold red][!]" , end="")

def check_joomla(url):
    console.print(f"[bold blue][+] Проверка Joomla: {url}")
    joomla_check_paths = [
        "/administrator/",
        "/index.php?option=com_config"
    ]

    for path in joomla_check_paths:
        try:
            full_url = url + path
            r = make_requesth(full_url)
            if r.status_code == 200:
                console.print(f"[bold green][!] Дира Joomla: {full_url}")
                log_result("Joomla", f"Найдена Joomla: {full_url}")

        except requests.RequestException as e:
            console.print(f"[bold red][!]" , end="")

def check_drupal(url):
    console.print(f"[bold blue][+] Проверка Drupal: {url}")
    drupal_check_paths = [
        "/user/register",
        "/admin",
        "/drupal.xml",
        "/sites/default/files/",
        "/modules"
    ]

    for path in drupal_check_paths:
        try:
            full_url = url + path
            r = make_requesth(full_url)
            if r.status_code == 200:
                console.print(f"[bold green] [!] Дира Drupal: {full_url}")
                log_result("Drupal", f"Найдена Drupal: {full_url}")

        except requests.RequestException as e:
            console.print(f"[bold red][!]" , end="")

def check_magento(url):
    console.print(f"[bold blue][+] Проверка Magento: {url}")
    magento_check_paths = [
        "/admin",
        "/downloader",
        "/setup/install/index.php",
        "/magento_version",
        "/media/"
    ]

    for path in magento_check_paths:
        try:
            full_url = url + path
            r = make_requesth(full_url)
            if r.status_code == 200:
                console.print(f"[bold green][!] Дира Magento: {full_url}")
                log_result("Magento", f"Найдена Magento: {full_url}")

        except requests.RequestException as e:
            console.print(f"[bold red][!]" , end="")


def check_shopify(url):
    console.print(f"[bold blue][+] Проверка Shopify: {url}")
    shopify_check_paths = [
        "/admin",
        "/collections",
        "/products",
        "/cart"
    ]
    for path in shopify_check_paths:
      try:
        full_url = url + path
        response = make_requesth(full_url)
        if response.status_code == 200:
            log_result("Shopify", f"Shopify найден на: {url}")
      except requests.RequestException as e:
            console.print(f"[bold red][!]" , end="")

def check_square_space(url):
    console.print(f"[bold blue][+] Проверка SquareSpace: {url}")
    squarespace_check_paths = [
        "/config",
        "/squarespace/",
        "/index"
    ]
    for path in squarespace_check_paths:
      try:
        full_url = url + path
        response = make_requesth(full_url)
        if response.status_code == 200:
            log_result("Square_space", f"SquareSpace найден на: {url}")
      except requests.RequestException as e:
            console.print(f"[bold red][!]" , end="")

def check_wix(url):
    console.print(f"[bold blue][+] Проверка Wix: {url}")
    wix_check_paths = [
        "/_wix/",
        "/wix",
        "/wix-api"
    ]
    for path in wix_check_paths:
      try:
        full_url = url + path
        response = make_requesth(full_url)
        if response.status_code == 200:
            log_result("Wix", f"Wix найден на: {url}")
      except requests.RequestException as e:
            console.print(f"[bold red][!]" , end="")

def check_static_site(url):
    console.print(f"[bold blue][+] Проверка статического сайта: {url}")
    # В случае статического сайта мы можем просто послать запрос и проверить отсутствие серверных путей
    response = make_requestg(url)
    if response.status_code == 200 and 'text/html' in response.headers.get('Content-Type', ''):
        r = make_requestg(url)
        soup = BeautifulSoup(r.content, "html.parser")
        title = soup.title.string
        log_result("SITES", f"Статический сайт (HTML - {title}) найден на: {url}")
        console.print(f"[bold blue][+] найден сайт {title} на: {url}")

def check_typoscript(url):
    console.print(f"[bold blue][+] Проверка TYPO3: {url}")
    typo3_check_paths = [
        "/typo3/",
        "/typo3/sysext/",
        "/typo3/index.php"
    ]
    for path in typo3_check_paths:
      try:
        full_url = url + path
        response = requests.head(full_url)
        if response.status_code == 200:
            log_result("Typo3", f"TYPO3 найден на: {url}")
      except requests.RequestException as e:
            console.print(f"[bold red][!]" , end="")

def check_cms(ip):
    # Проверка для определения CMS
    try:
        response = requests.get(url)
        page_content = response.text.lower()

        if 'wp-content' in page_content:
            check_wordpress(url)
        elif 'joomla' in page_content:
            check_joomla(url)
        elif 'drupal' in page_content:
            check_drupal(url)
        elif 'magento' in page_content:
            check_magento(url)
        # Добавление других CMS по мере необходимости
        elif 'cdn.shopify.com' in page_content:
            check_shopify(url)
        elif 'squarespace.com' in page_content:
            check_square_space(url)
        elif 'wix.com' in page_content:
            check_wix(url)
        elif 'typo3' in page_content:
            check_typoscript(url)
        else:
            check_static_site(url)

    except requests.RequestException as e:
        console.print(f"[bold red][!!!]" , end="")
