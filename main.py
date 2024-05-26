# pip install ipaddress

import ipaddress
import time

def subnet_calculator(ip_with_mask, num_subnets):
    try:
        # Преобразуем строку в объект IPv4 сети
        network = ipaddress.IPv4Network(ip_with_mask, strict=False)
    except ValueError as e:
        return f"Ошибка: {e}"

    # Вычисляем количество дополнительных бит для маски подсети
    additional_bits = (num_subnets - 1).bit_length()

    # Новая маска подсети
    new_prefix = network.prefixlen + additional_bits

    if new_prefix > 32:
        return "Ошибка: Недостаточно адресов для указанного количества подсетей."

    # Разделяем сеть на подсети
    subnets = list(network.subnets(new_prefix=new_prefix))

    results = []
    for subnet in subnets[:num_subnets]:  # Ограничиваем вывод до запрашиваемого количества подсетей
        results.append({
            "network_address": str(subnet.network_address),
            "broadcast_address": str(subnet.broadcast_address),
            "netmask": str(subnet.netmask),
            "num_hosts": subnet.num_addresses - 2,  # минус сетевой и широковещательный адреса
            "host_range": f"{list(subnet.hosts())[0]} - {list(subnet.hosts())[-1]}" if subnet.num_addresses > 2 else "N/A"
        })

    return results

# Пример использования
ip_with_mask = input("Введите IP-адрес с маской подсети (например, 192.168.1.0/24): ")
num_subnets = int(input("Введите количество подсетей: "))

start_time = time.time()  # Записываем начальное время
subnets = subnet_calculator(ip_with_mask, num_subnets)
end_time = time.time()  # Записываем конечное время

execution_time = end_time - start_time  # Вычисляем время выполнения

if isinstance(subnets, str):
    print(subnets)
else:
    for i, subnet in enumerate(subnets):
        print(f"Подсеть {i + 1}:")
        print(f"  Сетевой адрес: {subnet['network_address']}")
        print(f"  Широковещательный адрес: {subnet['broadcast_address']}")
        print(f"  Маска подсети: {subnet['netmask']}")
        print(f"  Количество хостов: {subnet['num_hosts']}")
        print(f"  Диапазон доступных IP-адресов: {subnet['host_range']}\n")

print(f"Время выполнения: {execution_time:.6f} секунд")
