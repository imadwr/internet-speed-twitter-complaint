from selenium import webdriver
from time import sleep
from selenium.common.exceptions import TimeoutException
import os

CHROME_DRIVER_PATH = "/Development/chromedriver.exe"

PROMISED_DOWN = 50  # promised minimum download speed by provider
PROMISED_UP = 50  # promised minimum upload speed by provider

TWITTER_EMAIL = os.getenv("email")
TWITTER_PASSWORD = os.getenv("password")


class InternetSpeedTwitterBot:
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
        self.down = None
        self.up = None

    def get_internet_speed(self):
        print("getting internet speed")
        try:
            self.driver.get("https://www.speedtest.net/")
        except TimeoutException:
            self.driver.execute_script("window.stop();")
        print("here")
        start_test = self.driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[1]/a')
        start_test.click()
        sleep(60)
        self.down = float(self.driver.find_element_by_css_selector(".download-speed").text)
        self.up = float(self.driver.find_element_by_css_selector(".upload-speed").text)

    def tweet_at_provider(self):
        print("Tweeting at provider")
        self.driver.get("https://www.twitter.com")
        sleep(2)
        log_in = self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div/main/div/div/div/div[1]/div/div[3]/div[4]/span')
        log_in.click()
        use_email_button = self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div/main/div/div/div/div[1]/div/div[3]/a')
        use_email_button.click()
        sleep(2)
        email_input = self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[1]/label/div/div[2]/div/input')
        email_input.send_keys(TWITTER_EMAIL)
        password_input = self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[2]/label/div/div[2]/div/input')
        password_input.send_keys(TWITTER_PASSWORD)
        log_in_button = self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[3]/div')
        log_in_button.click()
        sleep(2)
        post_input = self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div[2]/div/div/div/div')
        tweet = f"Hey Internet Provider, why is my internet speed {bot.down}down/{bot.up}up, while i pay for {PROMISED_DOWN}down/{PROMISED_UP}up"
        post_input.send_keys(tweet)
        tweet_button = self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]')
        tweet_button.click()


bot = InternetSpeedTwitterBot()

bot.get_internet_speed()
print(f"Up: {bot.up}")
print(f"Down: {bot.down}")
if bot.down < PROMISED_DOWN and bot.up < PROMISED_UP:
    bot.tweet_at_provider()

bot.driver.quit()