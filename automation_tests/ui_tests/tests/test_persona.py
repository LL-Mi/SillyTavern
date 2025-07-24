import time

from automation_tests.ui_tests.pages.pom import PersonaManagementPage
from automation_tests.ui_tests.tests.login import login


class TestPersona_chrome:
    def test_persona(self,driver_setup_chrome,base_url,user):
        login(driver_setup_chrome,user,base_url)
        persona=PersonaManagementPage(driver_setup_chrome,base_url)
        persona_name = f'ST-persona_test_{int(time.time())}'
        persona_description='用户角色创建测试'
        persona.create_persona(persona_name,persona_description)
        persona_in_list=persona.is_persona_displayed_in_list(persona_name)
        assert persona_in_list == True, f'{persona_name} 不在表中，创建失败'

        persona.open_persona_management_page()
        persona_new_name=f'New-ST-persona_test_{int(time.time())}'
        persona.edit_role(persona_name,persona_new_name)
        new_persona_in_list = persona.is_persona_displayed_in_list(persona_new_name)
        assert new_persona_in_list==True, f'{persona_new_name} 不在表内，未修改成功'

        persona.open_persona_management_page()
        persona_delete = persona.delete_persona(persona_new_name)
        after_delete = persona.is_persona_displayed_in_list(persona_new_name)
        assert after_delete is False, f'{persona_name} 还在表内，删除失败'


class TestPersona_edge:
    def test_persona(self,driver_setup_edge,base_url,user):
        login(driver_setup_edge,user,base_url)
        persona=PersonaManagementPage(driver_setup_edge,base_url)
        persona_name = f'ST-persona_test_{int(time.time())}'
        persona_description='用户角色创建测试'
        persona.create_persona(persona_name,persona_description)
        persona_in_list=persona.is_persona_displayed_in_list(persona_name)
        assert persona_in_list == True, f'{persona_name} 不在表中，创建失败'

        persona.open_persona_management_page()
        persona_new_name=f'New-ST-persona_test_{int(time.time())}'
        persona.edit_role(persona_name,persona_new_name)
        new_persona_in_list = persona.is_persona_displayed_in_list(persona_new_name)
        assert new_persona_in_list==True, f'{persona_new_name} 不在表内，未修改成功'

        persona.open_persona_management_page()
        persona_delete = persona.delete_persona(persona_new_name)
        after_delete = persona.is_persona_displayed_in_list(persona_new_name)
        assert after_delete is False, f'{persona_name} 还在表内，删除失败'
