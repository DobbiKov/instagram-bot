from modules.instagram import Instagram
from config import INSTAGRAM_LOGIN, INSTAGRAM_PASS

def main():
    print("Main!")

if __name__ == "__main__":
    print("Скрипт для скачивая контента из аккаунтов инстаграм.")
    print(" ")
    print("Введите nickName:")
    nickname = input("")
    instagram = Instagram(INSTAGRAM_LOGIN, INSTAGRAM_PASS)
    instagram.login()
    instagram.download_userpage_content(f"https://www.instagram.com/{nickname}/")
    instagram.finish()