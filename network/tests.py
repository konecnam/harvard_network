from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from .models import User, Post
class MySeleniumTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        # cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_all_posts_page(self):
        self.selenium.get(f"{self.live_server_url}")
        h2 = self.selenium.find_element(By.TAG_NAME, "h2")
        new_posts_title = self.selenium.find_element(By.ID, "new_posts_title")
        all_posts_title = self.selenium.find_element(By.ID, "all_posts_title")
        self.assertEqual(h2.text, "All Posts")
        self.assertEqual(new_posts_title.text, "New posts")
        self.assertEqual(all_posts_title.text, "Posts:")

    def test_register_page(self):
        self.selenium.get(f"{self.live_server_url}/register")
        h2 = self.selenium.find_element(By.TAG_NAME, "h2")
        self.assertEqual(h2.text, "Register")
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys("auto")
        email_input = self.selenium.find_element(By.NAME, "email")
        email_input.send_keys("car@car.cz")
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys("redcar")
        password_confirmation_input = self.selenium.find_element(By.NAME, "confirmation")
        password_confirmation_input.send_keys("redcar")
        self.selenium.find_element(By.XPATH, '//input[@value="Register"]').click()
        strong_layout  = self.selenium.find_element(By.TAG_NAME, "strong")
        self.assertEqual(strong_layout.text, "auto")

    def test_same_pastword(self):
        self.selenium.get(f"{self.live_server_url}/register")
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys("susenka")
        email_input = self.selenium.find_element(By.NAME, "email")
        email_input.send_keys("susenka@sus.cz")
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys("susenka")
        password_confirmation_input = self.selenium.find_element(By.NAME, "confirmation")
        password_confirmation_input.send_keys("susblabla")
        self.selenium.find_element(By.XPATH, '//input[@value="Register"]').click()
        message = self.selenium.find_element(By.ID, "message")
        self.assertEqual(message.text, "Passwords must match.")


class MyUserIn(StaticLiveServerTestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()

    def setUp (self):
        user = User.objects.create_superuser(username='auto', password='redcar', email='test@test.com', is_active=True)
        user.save()

    def login(self):
        self.selenium.get(f"{self.live_server_url}/login")
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys("auto")
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys("redcar")
        self.selenium.find_element(By.XPATH, '//input[@value="Login"]').click()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_all_posts_pages(self):
        self.selenium.get(f"{self.live_server_url}")
        h2 = self.selenium.find_element(By.TAG_NAME, "h2")
        new_posts_title = self.selenium.find_element(By.ID, "new_posts_title")
        all_posts_title = self.selenium.find_element(By.ID, "all_posts_title")
        self.assertEqual(h2.text, "All Posts")
        self.assertEqual(new_posts_title.text, "New posts")
        self.assertEqual(all_posts_title.text, "Posts:")

    def test_new_post(self):
        self.login()
        self.selenium.get(f"{self.live_server_url}")
        post_input = self.selenium.find_element(By.NAME, "new_post")
        post_input.send_keys("novy produkt je super")
        self.selenium.find_element(By.XPATH, '//input[@value="Post"]').click()
        username_post = self.selenium.find_element(By.CLASS_NAME, "post_author")
        post_information = self.selenium.find_element(By.CLASS_NAME, "post_information")
        heart = self.selenium.find_element(By.CLASS_NAME, "heart")
        likes = self.selenium.find_element(By.CLASS_NAME, "likes")
        self.assertEqual(username_post.text, "auto")
        self.assertEqual(post_information.text, "novy produkt je super")
        self.assertEqual(likes.text, "0")
        self.assertEqual(heart.text, "🖤")
        heart.click()
        self.assertEqual(likes.text, "1")
        self.assertEqual(heart.text, "❤️")
        heart.click()
        self.assertEqual(likes.text, "0")
        self.assertEqual(heart.text, "🖤")

    def test_pagination(self):
        self.login()
        self.selenium.get(f"{self.live_server_url}")
        for i in range(11):
            post_input = self.selenium.find_element(By.NAME, "new_post")
            post_input.send_keys(i)
            self.selenium.find_element(By.XPATH, '//input[@value="Post"]').click()
        page_two = self.selenium.find_element(By.ID, "page-link-2")
        page_two.click()
        username_post = self.selenium.find_element(By.CLASS_NAME, "post_author")
        post_information = self.selenium.find_element(By.CLASS_NAME, "post_information")
        self.assertEqual(username_post.text, "auto")
        self.assertEqual(post_information.text, '0')

    def test_paginations(self):
        self.login()
        self.selenium.get(f"{self.live_server_url}")
        for i in range(11):
            post_input = self.selenium.find_element(By.NAME, "new_post")
            post_input.send_keys(i)
            self.selenium.find_element(By.XPATH, '//input[@value="Post"]').click()
        next = self.selenium.find_element(By.ID, "next")
        next.click()
        username_post = self.selenium.find_element(By.CLASS_NAME, "post_author")
        post_information = self.selenium.find_element(By.CLASS_NAME, "post_information")
        self.assertEqual(username_post.text, "auto")
        self.assertEqual(post_information.text, '0')
        previous = self.selenium.find_element(By.ID, "previous")
        previous.click()
        username_post = self.selenium.find_element(By.CLASS_NAME, "post_author")
        post_information = self.selenium.find_element(By.CLASS_NAME, "post_information")
        self.assertEqual(username_post.text, "auto")
        self.assertEqual(post_information.text, '10')

    def test_search(self):
        self.login()
        self.selenium.get(f"{self.live_server_url}")
        nahodne_posty=["auto", "maso", "prasnice", "Auta", "auticko", "voda", "potok"]
        for nahodny_post in nahodne_posty:
            post_input = self.selenium.find_element(By.NAME, "new_post")
            post_input.send_keys(nahodny_post)
            self.selenium.find_element(By.XPATH, '//input[@value="Post"]').click()
        values = ["auto", "AUTA", "auticka", "pase", "praseci", "prasnice", "voda", "vodka"]
        self.login()
        self.selenium.get(f"{self.live_server_url}/search_page")
        for value in values:
            post_input = self.selenium.find_element(By.NAME, "new_search")
            post_input.send_keys(value)
            self.selenium.find_element(By.XPATH, '//input[@value="Search"]').click()
        # post_information = self.selenium.find_element(By.CLASS_NAME, "post_information")
        # self.assertEqual(post_information.text, '0')
        search_results = self.selenium.find_elements(By.CLASS_NAME, "post_information")
        result_texts = [result.text for result in search_results]
        expected_results = [post for post in nahodne_posty if value.lower() in post.lower()]
        self.assertListEqual(result_texts, expected_results, f"Search for '{value}' failed")

    def test_search_2(self):
        self.login()
        self.selenium.get(f"{self.live_server_url}")
        nahodne_posty=["krava", "kravi hlava", "prasnice", "Auta", "auticko", "voda", "potok", "kravmaga"]
        for nahodny_post in nahodne_posty:
            post_input = self.selenium.find_element(By.NAME, "new_post")
            post_input.send_keys(nahodny_post)
            self.selenium.find_element(By.XPATH, '//input[@value="Post"]').click()
        self.selenium.find_element(By.ID, "search_id").click()
        post_input = self.selenium.find_element(By.NAME, "new_search")
        
        post_input.send_keys("krav")
        self.selenium.find_element(By.XPATH, '//input[@value="Search"]').click()
        search_results = self.selenium.find_elements(By.CLASS_NAME, "post_information")
        result_texts = []
        for result in search_results:
            result_texts.append(result.text)
        self.assertTrue("krava" in result_texts)
        self.assertTrue("kravi hlava" in result_texts)
        self.assertTrue("kravmaga" in result_texts)

    def test_search_no_found(self):
        self.login()
        self.selenium.get(f"{self.live_server_url}")
        nahodne_posty=["auticko", "maso", "prasnice", "Krava", "potok"]
        for nahodny_post in nahodne_posty:
            post_input = self.selenium.find_element(By.NAME, "new_post")
            post_input.send_keys(nahodny_post)
            self.selenium.find_element(By.XPATH, '//input[@value="Post"]').click()
        values = ["auto", "masenko", "pase", "cow", "praseci", "voda"]
        self.selenium.get(f"{self.live_server_url}/search_page")
        for value in values:
            post_input = self.selenium.find_element(By.NAME, "new_search")
            post_input.send_keys(value)
            self.selenium.find_element(By.XPATH, '//input[@value="Search"]').click()
            message_no = self.selenium.find_element(By.ID, "no_post")
            self.assertEqual(message_no.text, "No post found!")


    def test_pege_navigation(self):
        self.login()
        self.selenium.get(f"{self.live_server_url}")
        all_posts_h2 = self.selenium.find_element(By.ID, "all_posts")
        self.assertEqual(all_posts_h2.text, "All Posts")

        self.selenium.find_element(By.ID, "following_id").click()
        following_h2 = self.selenium.find_element(By.ID, "following")
        self.assertEqual(following_h2.text, "Following")

        self.selenium.find_element(By.ID, "search_id").click()
        search_h4 = self.selenium.find_element(By.ID, "search")
        self.assertEqual(search_h4.text, "Search")

        self.selenium.find_element(By.ID, "log_out_id").click()
        all_posts_h2 = self.selenium.find_element(By.ID, "all_posts")
        self.assertEqual(all_posts_h2.text, "All Posts")

    def test_edit(self):
        self.login()
        self.selenium.get(f"{self.live_server_url}")
        post_input = self.selenium.find_element(By.XPATH, "/html/body/div/form/div/textarea")
        post_input.send_keys("novy katalog se povedl")
        self.selenium.find_element(By.XPATH, '//input[@value="Post"]').click()
        self.selenium.find_element(By.XPATH, '/html/body/div/div[1]/div[1]/button').click()
        post_input_edit = self.selenium.find_element(By.XPATH, '/html/body/div/div[1]/div[2]/textarea')
        post_input_edit.clear()
        post_input_edit.send_keys("novy katalog se povedl, velmi hezky vypada")
        self.selenium.find_element(By.XPATH, '/html/body/div/div[1]/div[2]/button[1]').click()
        edit_post = self.selenium.find_element(By.XPATH, '/html/body/div/div[1]/div[1]/h6[1]')
        self.assertEqual(edit_post.text, "novy katalog se povedl, velmi hezky vypada")
        

    def test_cancel(self):
        self.login()
        self.selenium.get(f"{self.live_server_url}")
        post_input = self.selenium.find_element(By.XPATH, "/html/body/div/form/div/textarea")
        post_input.send_keys("novy katalog se povedl")
        self.selenium.find_element(By.XPATH, '//input[@value="Post"]').click()
        self.selenium.find_element(By.XPATH, '/html/body/div/div[1]/div[1]/button').click()
        self.selenium.find_element(By.XPATH, '/html/body/div/div[1]/div[2]/button[2]').click()
        no_edit_post = self.selenium.find_element(By.XPATH, '/html/body/div/div[1]/div[1]/h6[1]')
        self.assertEqual(no_edit_post.text, "novy katalog se povedl")
        button_edit = self.selenium.find_element(By.XPATH, '/html/body/div/div[1]/div[1]/button')
        self.assertEqual(button_edit.text, "Edit")


    def test_two_no_edit(self):
        self.login()
        self.selenium.get(f"{self.live_server_url}")
        post_input = self.selenium.find_element(By.XPATH, "/html/body/div/form/div/textarea")
        post_input.send_keys("novy katalog se povedl")
        self.selenium.find_element(By.XPATH, '//input[@value="Post"]').click()
        self.selenium.find_element(By.XPATH, '//*[@id="log_out_id"]').click()

        user = User.objects.create_superuser(username='salina', password='bluetram', email='bluetram@tram.com', is_active=True)
        user.save()
        self.selenium.get(f"{self.live_server_url}/login")
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys("salina")
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys("bluetram")
        self.selenium.find_element(By.XPATH, '//input[@value="Login"]').click()

        no_edit_button = len(self.selenium.find_elements(By.XPATH, '/html/body/div/div[1]/div[1]/button')) > 0
        self.assertFalse (no_edit_button)

    def test_two_no_edit2(self):
        user = User.objects.create_superuser(username='salina', password='bluetram', email='bluetram@tram.com', is_active=True)
        user.save()
        post = Post (information='Novy post', author=user)
        post.save()

        self.login()   
        all_edit_buttons = self.selenium.find_elements(By.XPATH, '/html/body/div/div[1]/div[1]/button')
        self.assertTrue(len(all_edit_buttons) == 0)
        
    def test_following(self):
        self.login()
        self.selenium.get(f"{self.live_server_url}")
        self.selenium.find_element(By.XPATH, '//*[@id="following_id"]').click()
        following_h2 = self.selenium.find_element(By.XPATH, '//*[@id="following"]')
        self.assertEqual(following_h2.text, "Following")
    

    def test_following_two(self):
        user_two = User.objects.create_superuser(username='kachna', password='blueduck', email='duck@test.com', is_active=True)
        user_two.save()
        #do databaze ulozim post - nemusim to delat pres stranku.
        post_user_two = Post (information='kachna je modra', author=user_two)
        post_user_two.save()
    
        self.login()
        self.selenium.get(f"{self.live_server_url}")
        self.selenium.find_element(By.XPATH,'/html/body/div/div[1]/h6[1]/a/strong').click()
        self.selenium.find_element(By.XPATH, '/html/body/div/form/input[3]').click()
        follower = self.selenium.find_element(By.XPATH,'/html/body/div/h3[1]')
        self.assertEqual(follower.text, "Followers: 1")
        following = self.selenium.find_element(By.XPATH,'/html/body/div/h3[2]')
        self.assertEqual(following.text, "Following: 0")
        unfollower_button = self.selenium.find_element(By.XPATH, '/html/body/div/form/input[3]')
        self.assertEqual(unfollower_button.get_attribute('value'), "Unfollow")

        self.selenium.find_element(By.XPATH, '/html/body/nav/div/ul/li[1]/a/strong').click()
        profile_following_count = self.selenium.find_element(By.XPATH, '/html/body/div/h3[2]')
        self.assertEqual(profile_following_count.text, "Following: 1")
        profile_followers_count = self.selenium.find_element(By.XPATH, '/html/body/div/h3[1]')
        self.assertEqual(profile_followers_count.text, "Followers: 0")

        self.selenium.find_element(By.XPATH, '//*[@id="following_id"]').click()
        self.selenium.find_element(By.XPATH, '/html/body/div/div[1]/h6[1]/a/strong').click()
        self.selenium.find_element(By.XPATH, '/html/body/div/form/input[3]').click()
        unfollower = self.selenium.find_element(By.XPATH,'/html/body/div/h3[1]')
        self.assertEqual(unfollower.text, "Followers: 0")
        following_count = self.selenium.find_element(By.XPATH, '/html/body/div/h3[2]')
        self.assertEqual(following_count.text, "Following: 0")
    
        self.selenium.find_element(By.XPATH, '/html/body/nav/div/ul/li[1]/a').click()
        profile_following_count = self.selenium.find_element(By.XPATH, '/html/body/div/h3[2]')
        self.assertEqual(profile_following_count.text, "Following: 0")
        profile_followers_count_2 = self.selenium.find_element(By.XPATH,'/html/body/div/h3[1]')
        self.assertEqual(profile_followers_count_2.text, "Followers: 0")

    def test_search_users(self):
        self.login()
        self.selenium.get(f"{self.live_server_url}")
        self.selenium.find_element(By.XPATH, '//*[@id="users_page_id"]').click()
        user_input = self.selenium.find_element(By.XPATH, "/html/body/div/form/div/textarea")
        user_input.send_keys("hhh")
        self.selenium.find_element(By.XPATH, '/html/body/div/form/input').click()
        no_user_found = self.selenium.find_element(By.XPATH, '//*[@id="no_user"]')
        self.assertEqual(no_user_found.text, "No user found")

    def test_next_user_no_search(self):
        user_autobus = User.objects.create_superuser(username='autobus', password='bluebus', email='bluebus@tram.com', is_active=True)
        user_autobus.save()

        user_American = User.objects.create_superuser(username='American', password='amarican', email='american@tram.com', is_active=True)
        user_American.save()

        user_Salina = User.objects.create_superuser(username='Salina', password='bluetram', email='bluetram@tram.com', is_active=True)
        user_Salina.save()

        self.login()
        self.selenium.get(f"{self.live_server_url}")
        self.selenium.find_element(By.XPATH, '//*[@id="users_page_id"]').click()

        user_Amarican = self.selenium.find_element(By.XPATH, '/html/body/div/ul/li[1]/a/strong')
        self.assertEqual(user_Amarican.text, "American")

        user_auto = self.selenium.find_element(By.XPATH, '/html/body/div/ul/li[2]/a/strong')
        self.assertEqual(user_auto.text, "auto")

        user_autobus = self.selenium.find_element(By.XPATH, '/html/body/div/ul/li[3]/a/strong')
        self.assertEqual(user_autobus.text, "autobus")

        user_salina = self.selenium.find_element(By.XPATH, '/html/body/div/ul/li[4]/a/strong')
        self.assertEqual(user_salina.text, "Salina")


    def test_next_user_search(self):
        user_Autobus = User.objects.create_superuser(username='Autobus', password='bluebus', email='bluebus@tram.com', is_active=True)
        user_Autobus.save()

        user_American = User.objects.create_superuser(username='American', password='amarican', email='american@tram.com', is_active=True)
        user_American.save()

        user_salina = User.objects.create_superuser(username='salina', password='bluetram', email='bluetram@tram.com', is_active=True)
        user_salina.save()

        self.login()
        self.selenium.get(f"{self.live_server_url}")
        self.selenium.find_element(By.XPATH, '//*[@id="users_page_id"]').click()
        user_input = self.selenium.find_element(By.XPATH, "/html/body/div/form/div/textarea")
        user_input.send_keys("au")
        self.selenium.find_element(By.XPATH, '/html/body/div/form/input').click()

        user_auto = self.selenium.find_element(By.XPATH, '/html/body/div/ul/li[1]/a/strong')
        self.assertEqual(user_auto.text, "auto")

        user_Autobus = self.selenium.find_element(By.XPATH, '/html/body/div/ul/li[2]/a/strong')
        self.assertEqual(user_Autobus.text, "Autobus")

        





    





        


