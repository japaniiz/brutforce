import itertools
import string
import time
import hashlib
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed

class BruteForcer:
    def __init__(self):
        self.found = False
        self.attempts = 0
        self.start_time = time.time()
        
    def print_banner(self):
        print("""
 ╔══╗╔══╗╔═══╗╔══╗╔╗ ╔╗
 ╚╗╔╝║╔╗║║╔═╗║║╔╗║║╚═╝║
  ║║ ║╚╝║║╚═╝║║╚╝║║╔╗ ║
╔╗║║ ║╔╗║║╔══╝║╔╗║║║╚╗║
║╚╝╚╗║║║║║║   ║║║║║║ ║║
╚═══╝╚╝╚╝╚╝   ╚╝╚╝╚╝ ╚╝

        """)
        print("=== Продвинутый брутфорс-инструмент для тестирования безопасности ===")
        print("=== Используйте только на системах, которыми владеете или имеете разрешение тестировать ===\n")

    def simple_bruteforce(self, length, charset, target_hash=None):
        """Простой перебор всех комбинаций"""
        print(f"\n[+] Запуск простого брутфорса (длина: {length}, символы: {charset})")
        
        for candidate in itertools.product(charset, repeat=length):
            self.attempts += 1
            password = ''.join(candidate)
            
            if target_hash:
                
                if hashlib.md5(password.encode()).hexdigest() == target_hash:
                    self.found = True
                    return password
            else:
                
                print(f"Попытка #{self.attempts}: {password}", end='\r')
                
            if self.attempts % 1000 == 0:
                self.print_stats()
                
        return None

    def dictionary_attack(self, wordlist_path, target_hash=None, mutations=True):
        """Атака по словарю с возможными модификациями"""
        print(f"\n[+] Запуск атаки по словарю: {wordlist_path}")
        
        try:
            with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                for word in f:
                    word = word.strip()
                    self.attempts += 1
                    
                    if mutations:
                        
                        variants = set()
                        variants.add(word)
                        variants.add(word.upper())
                        variants.add(word.lower())
                        variants.add(word.capitalize())
                        for i in range(0, 10):
                            variants.add(word + str(i))
                            variants.add(str(i) + word)
                    else:
                        variants = [word]
                    
                    for variant in variants:
                        if target_hash:
                            if hashlib.md5(variant.encode()).hexdigest() == target_hash:
                                self.found = True
                                return variant
                        else:
                            print(f"Попытка #{self.attempts}: {variant}", end='\r')
                    
                    if self.attempts % 1000 == 0:
                        self.print_stats()
                        
                    if self.found:
                        break
                        
        except FileNotFoundError:
            print(f"[-] Файл словаря не найден: {wordlist_path}")
            
        return None

    def zip_bruteforce(self, zip_path, length=None, charset=None, wordlist=None):
        """Брутфорс ZIP-архива"""
        print(f"\n[+] Попытка взлома ZIP: {zip_path}")
        
        if wordlist:
            return self.dictionary_attack(wordlist_path=wordlist, target_hash=None)
        elif length and charset:
            zf = zipfile.ZipFile(zip_path)
            
            for candidate in itertools.product(charset, repeat=length):
                self.attempts += 1
                password = ''.join(candidate).encode('utf-8')
                
                try:
                    zf.extractall(pwd=password)
                    self.found = True
                    print(f"\n[+] Пароль найден: {password.decode('utf-8')}")
                    return password.decode('utf-8')
                except:
                    print(f"Попытка #{self.attempts}: {password.decode('utf-8')}", end='\r')
                
                if self.attempts % 1000 == 0:
                    self.print_stats()
                    
        return None

    def print_stats(self):
        """Вывод статистики"""
        elapsed = time.time() - self.start_time
        speed = self.attempts / elapsed if elapsed > 0 else 0
        print(f"\n[Статистика] Попыток: {self.attempts} | Время: {elapsed:.2f} сек | Скорость: {speed:.2f} паролей/сек")

    def run(self):
        self.print_banner()
        
        print("1. Простой брутфорс")
        print("2. Атака по словарю")
        print("3. Взлом ZIP-архива")
        choice = input("\nВыберите метод: ")
        
        if choice == "1":
            length = int(input("Длина пароля: "))
            charset = input("Используемые символы (оставьте пустым для a-z0-9): ") or string.ascii_lowercase + string.digits
            target = input("Целевой MD5 хеш (оставьте пустым для демо): ")
            
            result = self.simple_bruteforce(length=length, charset=charset, target_hash=target or None)
            
        elif choice == "2":
            wordlist = input("Путь к файлу словаря: ")
            target = input("Целевой MD5 хеш (оставьте пустым для демо): ")
            
            result = self.dictionary_attack(wordlist_path=wordlist, target_hash=target or None)
            
        elif choice == "3":
            zip_path = input("Путь к ZIP-архиву: ")
            method = input("Метод (1 - словарь, 2 - брутфорс): ")
            
            if method == "1":
                wordlist = input("Путь к файлу словаря: ")
                result = self.zip_bruteforce(zip_path=zip_path, wordlist=wordlist)
            else:
                length = int(input("Длина пароля: "))
                charset = input("Используемые символы (оставьте пустым для a-z0-9): ") or string.ascii_lowercase + string.digits
                result = self.zip_bruteforce(zip_path=zip_path, length=length, charset=charset)
        
        if hasattr(self, 'found') and self.found:
            print(f"\n[+] Успех! Найден пароль: {result}")
        else:
            print("\n[-] Пароль не найден")
        
        self.print_stats()

if __name__ == "__main__":
    bf = BruteForcer()
    bf.run()