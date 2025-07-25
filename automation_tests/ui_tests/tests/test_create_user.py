import time
from tabnanny import check

from automation_tests.ui_tests.pages.pom import AdminPage
from automation_tests.ui_tests.tests.login import login


class Testcreate:
    def test_create_user_chrome(self,driver_setup_chrome,base_url,admin):
        login(driver_setup_chrome,admin,base_url)
        username = f'new_user{int(time.time())}'
        password = 'password'
        admin_mode=AdminPage(driver_setup_chrome,base_url)
        admin_mode.create_new_user(username,password)
        check_user=admin_mode.is_user_in_list(username)
        assert check_user==True,f"{username}未创建成功"
        admin_mode.click_popup_ok()
        admin_mode.delete_user(username)
        check_user_after_delete=admin_mode.is_user_in_list(username)
        assert check_user_after_delete==False,f"{username}删除失败"

    def test_create_user_edge(self,driver_setup_edge,base_url,admin):
        login(driver_setup_edge,admin,base_url)
        username = f'new_user{int(time.time())}'
        password = 'password'
        admin_mode=AdminPage(driver_setup_edge,base_url)
        admin_mode.create_new_user(username,password)
        check_user=admin_mode.is_user_in_list(username)
        assert check_user==True,f"{username}未创建成功"
        admin_mode.click_popup_ok()
        admin_mode.delete_user(username)
        check_user_after_delete=admin_mode.is_user_in_list(username)
        assert check_user_after_delete==False,f"{username}删除失败"

