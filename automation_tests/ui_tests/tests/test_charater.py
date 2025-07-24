import time

from automation_tests.ui_tests.pages.pom import CharacterPage
from automation_tests.ui_tests.tests.login import login


class Test_charater_chrome:
    def test_charater(self,driver_setup_chrome,base_url,user):
       login(driver_setup_chrome, user,base_url)
       character=CharacterPage(driver_setup_chrome, base_url)
       character_name = f'测试角色_{int(time.time())}'
       character_description=description='这是一个测试角色'
       character_message='测试'
       character.create_character(character_name,character_description,character_message)
       is_created_and_displayed = character.is_character_displayed_in_list(character_name)
       assert is_created_and_displayed == True, f"角色 '{character_name}' 创建后未在列表中显示。"
       print(f" 角色 '{character_name}' 已成功创建并显示在列表中。")


       character.delete_character(character_name)
       check_create = character.is_character_displayed_in_list(character_name)
       assert check_create is False, f"未删除成功"


class Test_charater_edge:
    def test_charater(self,driver_setup_edge,base_url,user):
       login(driver_setup_edge, user,base_url)
       character=CharacterPage(driver_setup_edge, base_url)
       character_name = f'测试角色_{int(time.time())}'
       character_description=description='这是一个测试角色'
       character_message='测试'
       character.create_character(character_name,character_description,character_message)
       is_created_and_displayed = character.is_character_displayed_in_list(character_name)
       assert is_created_and_displayed == True, f"角色 '{character_name}' 创建后未在列表中显示。"
       print(f" 角色 '{character_name}' 已成功创建并显示在列表中。")


       character.delete_character(character_name)
       check_create = character.is_character_displayed_in_list(character_name)
       assert check_create is False, f"未删除成功"

