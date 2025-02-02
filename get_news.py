import os
import google.generativeai as genai
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep

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

driver.get("https://news.yahoo.co.jp")
news = (
    driver.find_element(By.ID, "uamods-topics")
    .find_element(By.TAG_NAME, "ul")
    .find_elements(By.TAG_NAME, "a")
)
urls = [(e.get_attribute("href")) for e in news]
titles = [(e.text) for e in news]
news_contents = []
print("実行中", end="")
for i in range(8):
    driver.get(urls[i])
    driver.find_element(By.LINK_TEXT, "記事全文を読む").click()
    time = driver.find_element(By.TAG_NAME, "time").text
    article = driver.find_element(By.CLASS_NAME, "article_body").text
    prompt = model.generate_content(
        "以下はとあるニュース記事の全文です。この文章を100文字以内で要約してください:"
        + article
    )
    news_contents.append((time, titles[i], prompt.text))
    print(".", end="")

print("\n実行完了")
pass
