from instagramUserInfo import username, password
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--disable-notifications")
prefs = {"intl.accept_languages": "en-US"}
chrome_options.add_experimental_option("prefs", prefs)
class Instagram:
    def __init__(self, username, password):
        self.browser = webdriver.Chrome(options=chrome_options)
        self.username = username
        self.password = password

    def signIn(self):
        self.browser.get("https://www.instagram.com/")
        #self.browser.maximize_window() yorum kaldırılırsa tam ekran yapar
        time.sleep(3)
        
        usernameInput = self.browser.find_element(By.NAME, "username")
        passwordInput = self.browser.find_element(By.NAME, "password")
        
        usernameInput.send_keys(self.username)
        passwordInput.send_keys(self.password)
        passwordInput.send_keys(Keys.ENTER)
        print("Giriş yapılıyor...")
        
        time.sleep(21) 
        
        try:
            self.browser.find_element(By.XPATH, "//div[contains(text(),'Şimdi Değil')]").click()
            time.sleep(2)
        except:
            pass
            
        print("Giriş işlemi tamamlandı.")

    def getFollowers(self, max):
        self.browser.get(f"https://www.instagram.com/{self.username}/")
        time.sleep(5)

        print("Takipçi listesi açılıyor...")
        try:
            self.browser.find_element(By.PARTIAL_LINK_TEXT, "followers").click()
        except:
            self.browser.find_element(By.PARTIAL_LINK_TEXT, "takipçi").click()
        
        time.sleep(5)

        dialog = self.browser.find_element(By.XPATH, "//div[@role='dialog']")
        print(f"Hedeflenen kişi sayısı: {max}. Tarama başlıyor...")

        collected_users = set()

        while len(collected_users) < max:
            try:
             
                users_elements = dialog.find_elements(By.XPATH, ".//a")
                
             
                for element in users_elements:
                    link = element.get_attribute("href")
                   
                    if link and "/p/" not in link and "explore" not in link:
                        collected_users.add(link)
                
                if len(collected_users) >= max:
                    print(f"Hedef sayıya ulaşıldı: {len(collected_users)}")
                    break


                if users_elements:
                    last_user = users_elements[-1]
                    self.browser.execute_script("arguments[0].scrollIntoView(true);", last_user)
                    time.sleep(2)

                    new_len = len(dialog.find_elements(By.XPATH, ".//a"))

                    if len(users_elements) == new_len:
                        print("Listenin sonuna gelindi, daha fazla kişi yok.")
                        break
                else:
                    break

            except Exception as e:
                print(f"Hata oluştu: {e}")
                break
            final_list = list(collected_users)
            
            final_list = final_list[:max]

            print("Dosyaya yazılıyor...")
            with open("followers.txt", "w", encoding="UTF-8") as file:
                for item in final_list:
                    file.write(item + "\n")

            print(f"Toplam {len(final_list)} takipçi bulundu ve kaydedildi:")
            for user in final_list:
                print(user)

    def followUser(self, username): # bir kullanıcı adına göre otomatik takip etme.
        self.browser.get("https://www.instagram.com/"+ username + "/")
        time.sleep(4)
        try:
            followButton = self.browser.find_element(By.XPATH, "//div[contains(text(), 'Takip Et')]")
            followButton.click()
            print(f"BAŞARILI: {username} takip edildi.")
        except:
            try:
                # ingilizce olursa buton
                followButton = self.browser.find_element(By.XPATH, "//div[contains(text(), 'Follow')]")
                followButton.click()
                print(f"BAŞARILI: {username} takip edildi (İngilizce).")
            except:
                print(f"HATA: Buton bulunamadı. Zaten takip ediyor olabilirsin.")

    def unFollowUser(self, username):
        self.browser.get("https://www.instagram.com/" + username + "/")
        time.sleep(4)
        try:
            following_btn = self.browser.find_element(By.XPATH, "//div[text()='Following']")
            following_btn.click()
            
            time.sleep(3)
            confirm_btn = self.browser.find_element(By.XPATH, "//*[text()='Unfollow']")
            confirm_btn.click()
            
            time.sleep(3)
            try:
                final_confirm = self.browser.find_element(By.XPATH, "//div[@role='dialog']//button[text()='Unfollow']")
                final_confirm.click()
                print("İkinci onay penceresi geçildi.")
            except:
                pass # İkinci pencere çıkmadıysa sorun yok, devam et.

            print(f"BAŞARILI: {username} takipten çıkıldı.")

        except Exception as e:
            print(f"HATA: Bu kullanıcıyı zaten takip etmiyorsun veya buton bulunamadı.")
instgrm = Instagram(username, password)
instgrm.signIn()
instgrm.getFollowers(13) #tüm takipcileri gösterir.
#instgrm.followUser("ornek")
# list= ["asdasd","asdasd", "asdasd","asdasd","asdasd"]

# for user in list: # bir listedeki kullancıları takip etmek için
#     instgrm.followUser(user)
#     time.sleep(3)

#instgrm.unFollowUser("ornek")