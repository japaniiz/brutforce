import itertools
import hashlib
import time
from concurrent.futures import ThreadPoolExecutor

class MrRobotBruteforcer:
    def __init__(self):
        self.found = False
        self.attempts = 0
        self.start_time = time.time()

    # ASCII-арт как в Mr. Robot
    def show_banner(self):
        print("""
         _____  _____   _____    _____  _    _  _____ 
        |  __ \|  __ \ / ____|  / ____|| |  | ||_   _|
        | |__) | |__) | |      | |     | |__| |  | |  
        |  _  /|  ___/| |      | |     |  __  |  | |  
        | | \ \| |    | |____  | |____ | |  | | _| |_ 
        |_|  \_\_|     \_____|  \_____||_|  |_||_____|
        >> Advanced Password Bruteforcer (Mr. Robot Style)
        """)

    # Проверка пароля (можно заменить на запрос к API/сервису)
    def check_password(self, password, target_hash=None):
        self.attempts += 1
        if target_hash:
            # Если передан хеш, проверяем совпадение
            if hashlib.sha256(password.encode()).hexdigest() == target_hash:
                return True
        else:
            # Имитация проверки (для демо)
            return password == "admin123!"  # Замените на реальный пароль
        return False

    # 1. Обычный брутфорс (перебор всех комбинаций)
    def brute_force(self, length, charset):
        for candidate in itertools.product(charset, repeat=length):
            password = ''.join(candidate)
            if self.check_password(password):
                return password
        return None

    # 2. Словарная атака + мутации (как у Эллиота)
    def dictionary_attack(self, wordlist_path, mutations=True):
        try:
            with open(wordlist_path, 'r', errors='ignore') as f:
                for word in f:
                    word = word.strip()
                    if mutations:
                        # Генерация вариантов (qwerty → Qwerty, qwerty123, qwerty! и т.д.)
                        variants = {
                            word,
                            word.lower(),
                            word.upper(),
                            word.capitalize(),
                            word + "123",
                            word + "!",
                            word + "2024",
                            "!" + word,
                        }
                        for variant in variants:
                            if self.check_password(variant):
                                return variant
                    else:
                        if self.check_password(word):
                            return word
        except FileNotFoundError:
            print("[!] Wordlist not found!")
        return None

    # 3. Атака по маске (например, "Слово + Год")
    def mask_attack(self, pattern, years_range=(1990, 2024)):
        # Пример: pattern = "Password{YEAR}" → Password2023, Password1995...
        for year in range(years_range[0], years_range[1] + 1):
            password = pattern.replace("{YEAR}", str(year))
            if self.check_password(password):
                return password
        return None

    # 4. Многопоточный брутфорс (ускорение атаки)
    def threaded_bruteforce(self, charset, length, threads=4):
        def worker(start_char):
            for candidate in itertools.product(charset, repeat=length-1):
                password = start_char + ''.join(candidate)
                if self.check_password(password):
                    return password
            return None

        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(worker, c) for c in charset]
            for future in (futures):
                result = future.result()
                if result:
                    return result
        return None

    # Запуск
    def run(self):
        self.show_banner()
        print("[1] Bruteforce Attack")
        print("[2] Dictionary Attack")
        print("[3] Mask Attack (e.g., 'Password{YEAR}')")
        print("[4] Threaded Bruteforce (Fast)")

        choice = input("\nSelect attack method: ")

        if choice == "1":
            length = int(input("Password length: "))
            charset = input("Charset (default: a-z0-9): ") or "abcdefghijklmnopqrstuvwxyz0123456789"
            print("\n[+] Starting bruteforce...")
            result = self.brute_force(length, charset)

        elif choice == "2":
            wordlist = input("Wordlist path (e.g., rockyou.txt): ")
            mutations = input("Use mutations? (y/n): ").lower() == "y"
            print("\n[+] Starting dictionary attack...")
            result = self.dictionary_attack(wordlist, mutations)

        elif choice == "3":
            pattern = input("Mask (e.g., 'admin{YEAR}'): ")
            print("\n[+] Starting mask attack...")
            result = self.mask_attack(pattern)

        elif choice == "4":
            length = int(input("Password length: "))
            charset = input("Charset (default: a-z0-9): ") or "abcdefghijklmnopqrstuvwxyz0123456789"
            threads = int(input("Threads (recommended 4-8): "))
            print("\n[+] Starting threaded bruteforce...")
            result = self.threaded_bruteforce(charset, length, threads)

        else:
            print("[!] Invalid choice!")
            return

        if result:
            print(f"\n[+] PASSWORD FOUND: {result}")
        else:
            print("\n[-] Password not found.")

        print(f"\nAttempts: {self.attempts}")
        print(f"Time: {time.time() - self.start_time:.2f}s")

if __name__ == "__main__":
    tool = MrRobotBruteforcer()
    tool.run()