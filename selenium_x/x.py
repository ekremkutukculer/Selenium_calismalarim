from xUserInfo import username, password
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By # EKLENDİ
import time

class X:
    def __init__(self, username, password):
        self.browserProfile = webdriver.ChromeOptions()
       
        self.browserProfile.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        
        self.browserProfile.add_experimental_option("detach", True)
        
        
        self.browser = webdriver.Chrome(options=self.browserProfile)
        self.username = username
        self.password = password

    def signIn(self):
        self.browser.get("https://x.com/i/flow/login")
        self.browser.maximize_window()
        time.sleep(4)

        # 1. ADIM: Kullanıcı Adını Gir
        try:
            
            usernameInput = self.browser.find_element(By.NAME, "text")
            usernameInput.send_keys(self.username)
           
            usernameInput.send_keys(Keys.ENTER)
            time.sleep(3)
        except Exception as e:
            print(f"Kullanıcı adı girilirken hata: {e}")


        
        # 2. ADIM: Şifreyi Gir
        try:
            passwordInput = self.browser.find_element(By.NAME, "password")
            passwordInput.send_keys(self.password)
            passwordInput.send_keys(Keys.ENTER)
            time.sleep(5)
            print("Giriş işlemi tamamlandı.")
        except Exception as e:
            print(f"Şifre girilirken hata: {e}")

    def search(self, keyword):
        
        self.browser.get(f"https://x.com/search?q={keyword}&src=typed_query")
        time.sleep(3)
        print(f"'{keyword}' arama sayfasına gidildi.")
    def get_search_results(self, max):
        time.sleep(3)
        
        print(f"Hedeflenen tweet sayısı: {max}. Tarama başlıyor...")
        
        # Benzersiz tweetleri saklamak için küme (Set) kullanıyoruz
        collected_tweets = set()
        
        # Scroll yüksekliğini takip etmek için (Sayfa sonu kontrolü)
        last_height = self.browser.execute_script("return document.body.scrollHeight")
        
        while len(collected_tweets) < max:
            try:
                # 1. Sayfadaki görünür tweetleri bul
                tweets = self.browser.find_elements(By.XPATH, "//article[@data-testid='tweet']")
                
                # 2. Tweetleri topla
                for tweet in tweets:
                    try:
                        # Tweetin tüm içeriğini (Metin, Tarih, İsim) alıyoruz
                        content = tweet.text
                        
                        # Boş değilse kümeye ekle (Set otomatik olarak kopyaları engeller)
                        if content:
                            collected_tweets.add(content)
                            
                        # Eğer hedef sayıya o an ulaşıldıysa döngüyü içeriden kır
                        if len(collected_tweets) >= max:
                            break
                    except:
                        pass
                
                # Sayı kontrolü (Eğer hedefe ulaştıysak ana döngüyü de kır)
                if len(collected_tweets) >= max:
                    print(f"Hedeflenen {max} tweete ulaşıldı.")
                    break
                
                # 3. SCROLL İŞLEMİ (X'te tüm pencere kaydırılır)
                self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
                
                # 4. Sayfa Sonu Kontrolü
                new_height = self.browser.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    print("Sayfa sonuna gelindi, daha fazla tweet yok.")
                    break
                last_height = new_height
                
                print(f"Toplanan tweet sayısı: {len(collected_tweets)}")

            except Exception as e:
                print(f"Bir hata oluştu: {e}")
                break
        
        # 5. Sonuçları Listeye Çevir ve Yazdır
        final_list = list(collected_tweets)[:max]
        
        print(f"\nToplam {len(final_list)} adet tweet listeleniyor:\n")
        
        for index, tweet in enumerate(final_list):
            print(f"{index + 1} --------------------------------")
            print(tweet)
            print("--------------------------------------------\n")
        
        print("Dosyaya kaydediliyor...")
        with open("tweets.txt", "w", encoding="UTF-8") as file:
            for index, tweet in enumerate(final_list):
                
                file.write(f"{index + 1} --------------------------------\n")
                file.write(tweet + "\n")
                file.write("------------------------------------------\n\n")

        print(f"Toplam {len(final_list)} tweet 'tweets.txt' dosyasına başarıyla yazıldı.")


x = X(username, password)
x.signIn()
x.search("python") 

# Örneğin 50 tane tweet bulana kadar aşağı in:
x.get_search_results(50)