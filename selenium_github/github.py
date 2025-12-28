from githubUserInfo import username, password
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class Github:
    def __init__(self, username, password):
        self.browser = webdriver.Chrome()
        self.username = username
        self.password = password
        self.followers = []
    def signIn(self):
        self.browser.get("https://github.com/login?return_to=https%3A%2F%2Fgithub.com%2Fsignup%3Fref_cta%3DSign%2Bup%26ref_loc%3Dheader%2Blogged%2Bout%26ref_page%3D%252F%26source%3Dheader-home")
        time.sleep(2)

        self.browser.find_element(By.ID, "login_field").send_keys(self.username)
        self.browser.find_element(By.ID, "password").send_keys(self.password)

        time.sleep(1)

        self.browser.find_element(By.NAME,"commit").click()
        time.sleep(2)
    def loadFollowers(self):
        items = self.browser.find_elements_by_css_selector(".d-table.table-fixed")

        for i in items:
            self.followers.append(i.find_element_by_css_selector("link-gray.pl-1").text)

    def getFollowers(self):
        items = self.browser.find_elements(By.CSS_SELECTOR, ".d-table-cell.col-9.v-align-top.pr-3")
        time.sleep(2)

        while True:
            self.loadFollowers()
            links = self.browser.find_element_by_class_name("BtnGroup").find_elements_by_tag_name("a")
            
            if len(links) == 1:
                if links[0].text == "Next":
                    links[0].click()
                    time.sleep(1)
                    self.loadFollowers()


                else:
                    break
            else:
                for link in links:
                    if link.text == "Next":
                        link.click()
                        time.sleep(1)
                        self.loadFollowers()
                    else:
                        continue
                       

github = Github(username, password)
github.signIn()
github.getFollowers()
print(len(github.followers))
print(github.followers)