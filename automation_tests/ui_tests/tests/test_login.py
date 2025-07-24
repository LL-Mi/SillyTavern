import pytest
from selenium.webdriver.support.wait import WebDriverWait


from selenium.webdriver.support import expected_conditions as EC

from automation_tests.ui_tests.pages.pom import Login, MessagePage, AdminPage
from automation_tests.ui_tests.tests.login import login


class TestLogin_chrome:
    def test_successful_user_login(self, driver_setup_chrome,base_url,user):
        print("测试用户登录")

        login_page=Login(driver_setup_chrome,base_url)

        login_page.open()
        print(f"打开登录界面:{driver_setup_chrome.current_url}")

        username=user["username"]
        password=user["password"]
        login_page.perform_login(username,password)
        print(f"{username}登录中")

        expected_full_url_after_login="http://localhost:8000/"
        assert expected_full_url_after_login == driver_setup_chrome.current_url,f"登录后URL不正确。预期为 '{expected_full_url_after_login}', 实际为 '{driver_setup_chrome.current_url}'"

        try:
            message_page=MessagePage(driver_setup_chrome,base_url)
            placeholder_text=message_page.get_message_input_placeholder()
            assert placeholder_text is not None and placeholder_text != "",f"输入消息框显示:{placeholder_text}"
            print("登录成功，消息输入框可见")
        except Exception as e:
            pytest.fail(f"登录成功后未能正确跳转到消息页面或页面元素验证失败: {e}")

        print(f"测试成功登录：用户 '{username}' 已成功登录并跳转到仪表盘。当前 URL: {driver_setup_chrome.current_url}")

    def test_successful_logout(self, driver_setup_chrome,base_url,user):
        print("测试")

        login(driver_setup_chrome, user, base_url)

        logout_page = AdminPage(driver_setup_chrome, base_url)
        logout_page.click_manager_setting_page_button()
        print("执行退出操作")
        logout_page.logout()

        expected_contain_url_after_logout="/login"
        try:
            # 等待URL完全匹配
            WebDriverWait(driver_setup_chrome, 10).until(EC.url_contains(expected_contain_url_after_logout))
            print(f"登出后URL已跳转到：{driver_setup_chrome.current_url}")
        except Exception as e:
            pytest.fail(f"登出操作后未能在预期时间内跳转到登录页。当前URL: {driver_setup_chrome.current_url}. 错误: {e}")

        assert expected_contain_url_after_logout in driver_setup_chrome.current_url,f"实际为'{expected_contain_url_after_logout}'"

        login_page = Login(driver_setup_chrome, base_url)

        assert login_page._wait_for_visibility(login_page.username_field, timeout=5)

        print("退出测试成功")

    def test_successful_admin_login(self, driver_setup_chrome,base_url,admin):
        print("测试管理员登录")
        login_page=Login(driver_setup_chrome,base_url)
        login_page.open()
        print(f"打开登录界面:{driver_setup_chrome.current_url}")

        username=admin["username"]
        password=admin["password"]
        login_page.perform_login(username,password)

        expected_full_url_after_login = "http://localhost:8000/"
        assert expected_full_url_after_login == driver_setup_chrome.current_url, f"登录后URL不正确。预期为 '{expected_full_url_after_login}', 实际为 '{driver_setup_chrome.current_url}'"

        try:
            message_page = MessagePage(driver_setup_chrome, base_url)
            placeholder_text = message_page.get_message_input_placeholder()
            assert placeholder_text is not None and placeholder_text != "", f"输入消息框显示:{placeholder_text}"
            print("登录成功，消息输入框可见")
        except Exception as e:
            pytest.fail(f"登录成功后未能正确跳转到消息页面或页面元素验证失败: {e}")

        print(f"测试成功登录：用户 '{username}' 已成功登录并跳转到仪表盘。当前 URL: {driver_setup_chrome.current_url}")

class TestLogin_edge:
    def test_successful_user_login(self, driver_setup_edge,base_url,user):
        print("测试用户登录")

        login_page=Login(driver_setup_edge,base_url)

        login_page.open()
        print(f"打开登录界面:{driver_setup_edge.current_url}")

        username=user["username"]
        password=user["password"]
        login_page.perform_login(username,password)
        print(f"{username}登录中")

        expected_full_url_after_login="http://localhost:8000/"
        assert expected_full_url_after_login == driver_setup_edge.current_url,f"登录后URL不正确。预期为 '{expected_full_url_after_login}', 实际为 '{driver_setup_edge.current_url}'"

        try:
            message_page=MessagePage(driver_setup_edge,base_url)
            placeholder_text=message_page.get_message_input_placeholder()
            assert placeholder_text is not None and placeholder_text != "",f"输入消息框显示:{placeholder_text}"
            print("登录成功，消息输入框可见")
        except Exception as e:
            pytest.fail(f"登录成功后未能正确跳转到消息页面或页面元素验证失败: {e}")

        print(f"测试成功登录：用户 '{username}' 已成功登录并跳转到仪表盘。当前 URL: {driver_setup_edge.current_url}")

    def test_successful_logout(self, driver_setup_edge,base_url,user):
        print("执行测试")
        login(driver_setup_edge,user,base_url)
        logout_page = AdminPage(driver_setup_edge, base_url)
        logout_page.click_manager_setting_page_button()
        print("执行退出操作")
        logout_page.logout()

        expected_contain_url_after_logout="/login"
        try:
            # 等待URL完全匹配
            WebDriverWait(driver_setup_edge, 10).until(EC.url_contains(expected_contain_url_after_logout))
            print(f"登出后URL已跳转到：{driver_setup_edge.current_url}")
        except Exception as e:
            pytest.fail(f"登出操作后未能在预期时间内跳转到登录页。当前URL: {driver_setup_edge.current_url}. 错误: {e}")

        assert expected_contain_url_after_logout in driver_setup_edge.current_url,f"实际为'{expected_contain_url_after_logout}'"

        login_page = Login(driver_setup_edge, base_url)

        assert login_page._wait_for_visibility(login_page.username_field, timeout=5)

        print("退出测试成功")

    def test_successful_admin_login(self, driver_setup_edge,base_url,admin):
        print("测试管理员登录")
        login_page=Login(driver_setup_edge,base_url)
        login_page.open()
        print(f"打开登录界面:{driver_setup_edge.current_url}")

        username=admin["username"]
        password=admin["password"]
        login_page.perform_login(username,password)

        expected_full_url_after_login = "http://localhost:8000/"
        assert expected_full_url_after_login == driver_setup_edge.current_url, f"登录后URL不正确。预期为 '{expected_full_url_after_login}', 实际为 '{driver_setup_edge.current_url}'"

        try:
            message_page = MessagePage(driver_setup_edge, base_url)
            placeholder_text = message_page.get_message_input_placeholder()
            assert placeholder_text is not None and placeholder_text != "", f"输入消息框显示:{placeholder_text}"
            print("登录成功，消息输入框可见")
        except Exception as e:
            pytest.fail(f"登录成功后未能正确跳转到消息页面或页面元素验证失败: {e}")

        print(f"测试成功登录：用户 '{username}' 已成功登录并跳转到仪表盘。当前 URL: {driver_setup_edge.current_url}")







