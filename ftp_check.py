from ftplib import FTP, error_perm
from rich.console import Console

console = Console()

def try_connect_ftp(host, username, password):
    try:
        ftp = FTP(host)
        ftp.connect(timeout=1)  # Попытка установить соединение
        ftp.login(username, password)  # Попытка входа
        console.print(f"[green]Successfully connected to FTP server {host} with [/green][yellow] {username}:{password}[/yellow]")
        with open('ftpLoot.txt', 'a') as ftploot:
            ftploot.write(host + ' ' + username + ' ' + password + '\n')
        ftp.quit()  # Закрытие соединения
    except error_perm as e:
        ftp.quit()
        console.print(f"[red]FTP login failed for {username}:{password} on {host}[/red]")
    except Exception as e:
        ftp.quit()
        console.print(f"[red]Error connecting to FTP server {host}[/red]")
        raise



