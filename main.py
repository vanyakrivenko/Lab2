import re
import requests

# Регулярное выражение для проверки IPv6-адресов
IPv6_REGEX = r"^(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}$|^(?:[a-fA-F0-9]{1,4}:){1,7}:$|^(?:[a-fA-F0-9]{1,4}:){1,6}:[a-fA-F0-9]{1,4}$|^::(?:[a-fA-F0-9]{1,4}:){0,5}[a-fA-F0-9]{1,4}$|^(?:[a-fA-F0-9]{1,4}:){1,5}:(?:[a-fA-F0-9]{1,4}:){1,4}[a-fA-F0-9]{1,4}$|^(?:[a-fA-F0-9]{1,4}:){1,4}:(?:[a-fA-F0-9]{1,4}:){1,3}[a-fA-F0-9]{1,4}$|^(?:[a-fA-F0-9]{1,4}:){1,3}:(?:[a-fA-F0-9]{1,4}:){1,2}[a-fA-F0-9]{1,4}$|^(?:[a-fA-F0-9]{1,4}:){1,2}:(?:[a-fA-F0-9]{1,4}:){1,1}[a-fA-F0-9]{1,4}$|^(?:[a-fA-F0-9]{1,4}:){1,7}:$"
def validate_ipv6(ip):
  return re.match(IPv6_REGEX, ip) is not None

def read_ips_from_file(file_path):
  with open(file_path, "r", encoding = "utf-8") as file:
    ips = file.readlines()
  return [ip.strip() for ip in ips]

def process_ips_from_file(input_file):
  ips = read_ips_from_file(input_file)
  return [ip for ip in ips if validate_ipv6(ip)]

def fetch_ips_from_url(url):
  response = requests.get(url)
  if response.status_code == 200:
    ips = response.text.splitlines()
    return [ip.strip() for ip in ips if validate_ipv6(ip)]
  return []

def validate_ips_from_input():
  print("Введите IP-адреса (по одному на строке). Для завершения введите пустую строку.")
  user_ips = []
  while True:
    ip = input("Введите IP: ").strip()
    if not ip:
      break
    user_ips.append(ip)


  valid_ips = [ip for ip in user_ips if validate_ipv6(ip)]
  print("\nКорректные IP-адреса:")
  print(", ".join(valid_ips))

if __name__ == "__main__":
    print("Выберите действие:")
    print("1. Проверить IP-адреса из файла")
    print("2. Проверить IP-адреса через ввод пользователя")
    choice = input("Введите номер действия: ").strip()

    if choice == "1":
        input_file = input("Введите название файла: ").strip()
        valid_ips = process_ips_from_file(input_file)
        print("\nКорректные IP-адреса из файла:")
        print(", ".join(valid_ips))
    elif choice == "2":
        validate_ips_from_input()
    else:
        print("Некорректный выбор.")
