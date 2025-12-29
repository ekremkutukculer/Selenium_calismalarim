import time
import json
import os
from typing import List
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from xUserInfo import username, password
# Şifreleri güvenli çekmek için
# from dotenv import load_dotenv
# load_dotenv()

class XBot:
    """
    X (Twitter) otomasyon ve veri kazıma botu.
    """

    def __init__(self, username: str, password: str, headless: bool = False): #headless bot arkaplanda çalışması için
        self.username = username
        self.password = password
        
        
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_experimental_option("detach", True)
        
        # Headless arayüzsüz çalışma seçeneği
        if headless:
            chrome_options.add_argument("--headless")
            print("Bilgi: Bot arka planda (Headless) çalışıyor...")

        self.browser = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.browser, 15) # Maksimum 15 saniye bekle

    def sign_in(self) -> None:
        try:
            self.browser.get("https://x.com/i/flow/login")
            self.browser.maximize_window()
            
            # Dinamik Bekleme
            print("Giriş sayfası bekleniyor...")
            username_input = self.wait.until(EC.presence_of_element_located((By.NAME, "text")))
            username_input.send_keys(self.username)
            username_input.send_keys(Keys.ENTER)

            # Şifre alanını bekle
            password_input = self.wait.until(EC.presence_of_element_located((By.NAME, "password")))
            password_input.send_keys(self.password)
            password_input.send_keys(Keys.ENTER)
            
            # Girişin başarılı olduğunu ana sayfa elementini görerek doğrula
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='AppTabBar_Home_Link']")))
            print("Başarıyla giriş yapıldı.")
            
        except TimeoutException:
            print("Hata: Sayfa yüklenemedi veya element bulunamadı (Zaman Aşımı).")
        except Exception as e:
            print(f"Beklenmedik bir hata oluştu: {e}")

    def search(self, keyword: str) -> None: # verilen kelime arama yeri
        
        url = f"https://x.com/search?q={keyword}&src=typed_query"
        self.browser.get(url)
        print(f"'{keyword}' için arama yapılıyor...")
        
        
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//article[@data-testid='tweet']")))
        except TimeoutException:
            print("Arama sonucu bulunamadı veya yüklenmesi çok uzun sürdü.")

    def scrape_tweets(self, max: int = 50) -> List[str]:
 
        print(f"Hedef: {max} tweet. Tarama başlıyor...")
        collected_tweets = set()
        
        last_height = self.browser.execute_script("return document.body.scrollHeight")
        
        while len(collected_tweets) < max:
            try:
                # Görünür tweetleri al
                tweets = self.browser.find_elements(By.XPATH, "//article[@data-testid='tweet']")
                
                for tweet in tweets:
                    text = tweet.text
                    if text:
                        collected_tweets.add(text)
                        if len(collected_tweets) >= max:
                            break
                
                print(f"Anlık Toplanan: {len(collected_tweets)}")
                
                if len(collected_tweets) >= max:
                    break

                # Scroll Yap
                self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2) 
                
                # Sayfa sonu kontrolü
                new_height = self.browser.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    print("Sayfa sonuna gelindi.")
                    break
                last_height = new_height
                
            except Exception as e:
                print(f"Scraping sırasında hata: {e}")
                break
        
        return list(collected_tweets)[:max]

    def save_to_json(self, data: List[str], filename: str = "tweets.json") -> None:
        # json formatında kaydetme
        try:
            with open(filename, "w", encoding="utf-8") as f:
                # Veriyi sözlük yapısına çevirip kaydedelim, daha profesyonel durur
                json_data = [{"id": i+1, "content": tweet} for i, tweet in enumerate(data)]
                json.dump(json_data, f, ensure_ascii=False, indent=4)
            print(f"Veriler '{filename}' dosyasına JSON formatında kaydedildi.")
        except IOError as e:
            print(f"Dosya kaydetme hatası: {e}")

    def close(self):
        self.browser.quit()

# --- MAIN ---
if __name__ == "__main__":
    # Kullanıcı bilgilerini buradan veya .env dosyasından al
    # import os
    # USER = os.getenv("X_USERNAME")
    # PASS = os.getenv("X_PASSWORD")
    
    # Şimdilik manuel:
    from xUserInfo import username, password
    
    bot = XBot(username, password)
    bot.sign_in()
    bot.search("Yapay Zeka")
    tweets = bot.scrape_tweets(max=20)
    bot.save_to_json(tweets)
    
    # tarayıcı ve botu kapatmak için işlem bitince
    # bot.close()