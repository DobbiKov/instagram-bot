from modules.instagram import Instagram
from config import INSTAGRAM_LOGIN, INSTAGRAM_PASS

def main():
    print("Main!")

if __name__ == "__main__":
    instagram = Instagram(INSTAGRAM_LOGIN, INSTAGRAM_PASS)
    instagram.login()
    instagram.finish()