import socket
from concurrent.futures import ThreadPoolExecutor

def scan_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)  # Устанавливаем таймаут в 1 секунду
    result = sock.connect_ex((ip, port))
    sock.close()
    return port, result == 0  # Возвращаем порт и статус (открыт или закрыт)

def get_service_name(port):
    try:
        return socket.getservbyport(port)  # Получаем название сервиса по номеру порта
    except OSError:
        return None  # Если название не найдено, возвращаем None

def scan_ports(ip):
    open_ports = []
    with ThreadPoolExecutor(max_workers=100) as executor:
        results = executor.map(lambda p: scan_port(ip, p), range(1, 65536))
        for port, is_open in results:
            if is_open:
                service_name = get_service_name(port)  # Получаем название сервиса
                if service_name:
                    print(f"Порт {port} открыт: {service_name}.")
                else:
                    print(f"Порт {port} открыт: (название не найдено).")
                open_ports.append(port)
    return open_ports

if __name__ == "__main__":
    target_ip = input("Введите IP-адрес для сканирования: ")
    
    print(f"Сканирование всех портов на {target_ip}...")
    open_ports = scan_ports(target_ip)
    
    print("\nРезультаты сканирования:")
    if open_ports:
        print(f"Открытые порты: {open_ports}")
    else:
        print("Нет открытых портов.")
