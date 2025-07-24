from automation_tests.ui_tests.pages.pom import Login


def login(driver,user,base_url):
        login_page = Login(driver, base_url)

        login_page.open()
        print(f"打开登录界面:{driver.current_url}")

        username = user["username"]
        password = user["password"]
        login_page.perform_login(username, password)
        print(f"{username}登录中")

        expected_full_url_after_login = "http://localhost:8000/"
        assert expected_full_url_after_login == driver.current_url, f"登录后URL不正确。预期为 '{expected_full_url_after_login}', 实际为 '{driver.current_url}'"
