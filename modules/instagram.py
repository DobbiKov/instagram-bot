from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests

import os

from config import FIREFOX_DRIVER_PATH

import time, random

class Instagram:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.browser = webdriver.Firefox(executable_path=FIREFOX_DRIVER_PATH)

    def login(self):
        try:
            self.browser.get(url="https://www.instagram.com")
            time.sleep(random.randrange(3, 5))
            
            username_input = self.browser.find_element_by_name("username")
            username_input.clear()
            username_input.send_keys(self.username)

            time.sleep(random.randrange(3, 5))

            password_input = self.browser.find_element_by_name("password")
            password_input.clear()
            password_input.send_keys(self.password)

            password_input.send_keys(Keys.ENTER)
            time.sleep(random.randrange(3, 5))
        except Exception as ex:
            self.finish()

    def get_all_posts_urls(self, url:str):
        self.browser.get(url)
        time.sleep(4)

        wrong_userpage = "/html/body/div[1]/section/main/div/h2"

        if self.xpath_exists(wrong_userpage):
            print("Такого пользователя не существует, проверьте URL")
            self.finish()
        else:
            self.check_resources_dir()


            print("Пользователь успешно найден, собираем посты!")
            time.sleep(2)

            posts_count = int(self.browser.find_element_by_xpath(
                "/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span").text)
            loops_count = int(posts_count / 12)
            print(loops_count)

            posts_urls = []
            for i in range(0, loops_count):
                hrefs = self.browser.find_elements_by_tag_name('a')
                hrefs = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]

                for href in hrefs:
                    posts_urls.append(href)

                self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.randrange(2, 4))
                print(f"Итерация #{i}")

            file_name = url.split("/")[-2]

            set_posts_urls = set(posts_urls)
            set_posts_urls = list(set_posts_urls)

            with open(f'./resources/post_urls/{file_name}_set.txt', 'a') as file:
                for post_url in set_posts_urls:
                    file.write(post_url + '\n')
            time.sleep(3)
            return set_posts_urls

    def download_userpage_content(self, userpage):

        browser = self.browser
        urls_list = self.get_all_posts_urls(userpage)
        file_name = userpage.split("/")[-2]
        time.sleep(4)
        browser.get(userpage)
        time.sleep(4)

        img_and_video_src_urls = []

        for post_url in urls_list:
            try:
                browser.get(post_url)
                time.sleep(4)

                img_src = "/html/body/div[1]/section/main/div/div[1]/article/div[2]/div/div/div[1]/img"
                video_src = "/html/body/div[1]/section/main/div/div[1]/article/div[2]/div/div/div[1]/div/div/video"
                post_id = post_url.split("/")[-2]

                if os.path.exists(f"resource/img/{file_name}"):
                        pass
                else:
                    os.mdir(f"resource/img/{file_name}")

                if self.xpath_exists(img_src):
                    img_src_url = browser.find_element_by_xpath(img_src).get_attribute("src")
                    img_and_video_src_urls.append(img_src_url)

                    # сохраняем изображение
                    get_img = requests.get(img_src_url)
                    with open(f"./resources/img/{file_name}/{file_name}_{post_id}_img.jpg", "wb") as img_file:
                        img_file.write(get_img.content)

                elif self.xpath_exists(video_src):
                    video_src_url = browser.find_element_by_xpath(video_src).get_attribute("src")
                    img_and_video_src_urls.append(video_src_url)

                    # сохраняем видео
                    get_video = requests.get(video_src_url, stream=True)
                    with open(f"./resources/img/{file_name}/{file_name}_{post_id}_video.mp4", "wb") as video_file:
                        for chunk in get_video.iter_content(chunk_size=1024 * 1024):
                            if chunk:
                                video_file.write(chunk)
                else:
                    # print("Упс! Что-то пошло не так!")
                    img_and_video_src_urls.append(f"{post_url}, нет ссылки!")
                print(f"Контент из поста {post_url} успешно скачан!")

            except Exception as ex:
                print(ex)
                self.finish()


    #проверяет наличие нужных папок для ресуросов, если их нет - создает
    def check_resources_dir(self):
        if os.path.exists(f"resources"):
            print("Папка уже существует!")
        else:
            os.mkdir("resources")

        if os.path.exists(f"resources/post_urls"):
            print("Папка уже существует!")
        else:
            os.mkdir("resources/post_urls")

        if os.path.exists(f"resources/img"):
            print("Папка уже существует!")
        else:
            os.mkdir("resources/img")

    # метод проверяет по xpath существует ли элемент на странице
    def xpath_exists(self, url):

        browser = self.browser
        try:
            browser.find_element_by_xpath(url)
            exist = True
        except Exception as ex:
            exist = False
        return exist

    def finish(self):
        time.sleep(random.randrange(3, 5))
        self.browser.close()
        self.browser.quit()
