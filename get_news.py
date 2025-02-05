import os
import requests
import google.generativeai as genai
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

os.system("taskkill /F /IM chrome.exe")
options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--mute-audio")
options.add_argument("--headless")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(10)
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

# トップニュースのURLとタイトルを取得
driver.get("https://news.yahoo.co.jp")
news = (
    driver.find_element(By.ID, "uamods-topics")
    .find_element(By.TAG_NAME, "ul")
    .find_elements(By.TAG_NAME, "a")
)
urls = [(e.get_attribute("href")) for e in news]
titles = [(e.text) for e in news]

# 記事の掲載日時、タイトル、記事要約文を格納
news_contents = []
for url, title in zip(urls, titles):
    driver.get(url)
    driver.find_element(By.LINK_TEXT, "記事全文を読む").click()
    time = driver.find_element(By.TAG_NAME, "time").text
    article = driver.find_element(By.CLASS_NAME, "article_body").text
    image_url = (
        driver.find_element(By.CLASS_NAME, "article_body")
        .find_element(By.TAG_NAME, "img")
        .get_attribute("src")
    )
    # 画像を保存する
    # with open(os.path.join("images", "image.jpg"), "wb") as f:
    #     f.write(requests.get(image_url).content)
    prompt = model.generate_content(
        "以下はとあるニュース記事の全文です。この文章を100文字以内で要約してください:"
        + article
    ).text
    news_contents.append((time, title, prompt))

pass
