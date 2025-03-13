import requests

def get_ip():
    try:
        # Получаем внешний IP-адрес
        response = requests.get('https://api.ipify.org?format=json')
        ip_data = response.json()
        return ip_data['ip']
    except Exception as e:
        print(f"Ошибка при получении IP-адреса: {e}")
        return None

def write_ip_to_file(ip):
    try:
        with open('my_ip.txt', 'a') as file:
            file.write(f"{ip}\n")
        print(f"IP-адрес {ip} записан в файл 'my_ip.txt'.")
    except Exception as e:
        print(f"Ошибка при записи в файл: {e}")

if __name__ == "__main__":
    ip = get_ip()
    if ip:
        write_ip_to_file(ip)
