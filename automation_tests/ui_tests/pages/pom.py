import time

from selenium.common import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url

    def _wait_for_presence(self, locator, timeout=10):
        """等待元素在DOM中出现"""
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))

    def _wait_for_visibility(self, locator, timeout=10):
        """等待元素可见"""
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))

    def _wait_for_clickable(self, locator, timeout=10):
        """等待元素可点击"""
        return WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))

    def _wait_for_invisibility(self, locator, timeout=10):
        """等待元素从DOM中消失或变得不可见"""
        return WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(locator))

class Login(BasePage):
    def __init__(self, driver, base_url):
        super().__init__(driver, base_url)
        self.username_field = (By.ID, 'userHandle')
        self.password_field = (By.ID, 'userPassword')
        self.login_button = (By.ID, 'loginButton')
        self.welcome_text = (By.CSS_SELECTOR, 'div.welcomeHeaderTitle')

        self.forgot_password_link = (By.ID, 'recoverPassword')
        self.recovery_code_input = (By.ID, 'recoveryCode')
        self.new_password_input = (By.ID, 'newPassword')
        self.forgot_password_message_display = (By.ID, 'recoverMessage')
        self.send_button_recovery = (By.ID, 'sendRecovery')
        self.cancel_button_recovery = (By.ID, 'cancelRecovery')

    def open(self):
        """封装打开登录页面的操作，并等待主要元素加载。"""
        self.driver.get(f"{self.base_url}/login")
        self._wait_for_visibility(self.username_field)
        self._wait_for_visibility(self.password_field)
        self._wait_for_clickable(self.login_button)

    def enter_username(self, username):
        """输入用户名。"""
        # self.driver.find_element(*self.username).send_keys(username)如果页面加载速度慢,可能失败
        self._wait_for_visibility(self.username_field).send_keys(username)

    def enter_password(self, password):
        """输入密码。"""
        self._wait_for_visibility(self.password_field).send_keys(password)

    def click_login_button(self):
        """点击登录按钮。"""
        self._wait_for_clickable(self.login_button).click()

    def click_forgot_password_link(self):
        """点击“忘记密码”链接，并等待密码恢复界面的关键元素出现。"""
        self._wait_for_clickable(self.forgot_password_link).click()
        self._wait_for_visibility(self.recovery_code_input)
        self._wait_for_visibility(self.send_button_recovery)
        self._wait_for_visibility(self.cancel_button_recovery)

    def perform_login(self, username, password):
        """执行完整的登录业务流程：输入用户名、密码并点击登录按钮。"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
        self._wait_for_presence(self.welcome_text)

    def initiate_password_recovery(self, username):
        """发起密码恢复流程：输入用户名并点击“忘记密码”链接。"""
        self.enter_username(username)
        self.click_forgot_password_link()

    def get_forgot_password_message_text(self):
        """获取密码恢复界面显示的提示消息文本 """
        return self._wait_for_visibility(self.forgot_password_message_display).text

    def is_recovery_interface_displayed_correctly(self):
        """判断密码恢复界面是否正确显示所有关键输入框和按钮。"""
        try:
            self._wait_for_visibility(self.recovery_code_input, timeout=3)
            self._wait_for_visibility(self.new_password_input, timeout=3)
            self._wait_for_clickable(self.send_button_recovery, timeout=3)
            self._wait_for_clickable(self.cancel_button_recovery, timeout=3)
            self._wait_for_visibility(self.forgot_password_message_display, timeout=3)
            return True
        except (TimeoutException, NoSuchElementException):
            return False

class AdminPage(BasePage):
    def __init__(self, driver, base_url):
        super().__init__(driver, base_url)
        self.user_setting_page_button = (By.ID, 'user-settings-button')
        self.admin_button = (By.ID, 'admin_button')
        self.header_text = (By.CSS_SELECTOR, 'h3 span[data-i18n="User Settings"]')

        self.new_user_button = (By.CSS_SELECTOR,'button.newUserButton')
        self.username_field = (By.CSS_SELECTOR,'input.createUserDisplayName')
        self.password_field = (By.CSS_SELECTOR, 'input.createUserPassword')
        self.confirm_password_field = (By.CSS_SELECTOR, 'input.createUserConfirmPassword')
        self.submit_button = (By.CSS_SELECTOR, 'button.newUserRegisterFinalizeButton')

        self.popup_ok_button = (By.CSS_SELECTOR, 'button.popup-button-ok')
        self.cancel_button = (By.CSS_SELECTOR, 'button.popup-button-cancel')

        self.manager_user_button = (By.CSS_SELECTOR, 'button.manageUsersButton')
        self.user_account_card  = (By.CSS_SELECTOR, 'div.userAccount')
        self.user_name_in_card  = (By.CSS_SELECTOR, 'h3.userName')
        self.user_delete_button_in_card  = (By.CSS_SELECTOR, 'button.userDelete')

        self.delete_user_name_input=(By.ID,'deleteUserHandle')
        self.delete_user_date=(By.ID,'deleteUserData')

        self.logout_button = (By.ID, 'logout_button')

    def logout(self):
        self._wait_for_clickable(self.logout_button).click()

    def click_manager_setting_page_button(self):
        self._wait_for_clickable(self.user_setting_page_button).click()
        self._wait_for_visibility(self.header_text)

    def click_admin_button(self):
        self._wait_for_clickable(self.admin_button).click()
        self._wait_for_visibility(self.new_user_button)
        self._wait_for_visibility(self.manager_user_button)

    def click_new_user_button(self):
        self._wait_for_clickable(self.new_user_button).click()
        self._wait_for_visibility(self.username_field)
        self._wait_for_visibility(self.password_field)

    def input_username(self, username):
        self._wait_for_presence(self.username_field).send_keys(username)

    def input_password(self, password):
        self._wait_for_presence(self.password_field).send_keys(password)

    def input_confirm_password(self, confirm_password):
        self._wait_for_presence(self.confirm_password_field).send_keys(confirm_password)

    def click_submit(self):
        self._wait_for_clickable(self.submit_button).click()
        self._wait_for_presence(self.manager_user_button)

    def create_new_user(self, username, password):
        self.click_manager_setting_page_button()
        self.click_admin_button()
        self.click_new_user_button()
        self.input_username(username)
        self.input_password(password)
        self.input_confirm_password(password)
        self.click_submit()

    def click_delete_button_for_user(self, username):
        self.click_manager_setting_page_button()
        self.click_admin_button()
        self._wait_for_clickable(self.manager_user_button).click()

        self._wait_for_visibility(self.user_account_card)
        user_cards=self.driver.find_elements(*self.user_account_card)

        found = False
        for card in user_cards:
            try:
                # 在每个用户卡片中查找用户名元素
                name_element = card.find_element(*self.user_name_in_card)
                if name_element.text == username:
                    # 在找到的卡片中，定位并点击删除按钮
                    delete_button = card.find_element(*self.user_delete_button_in_card)
                    self._wait_for_clickable(delete_button).click()
                    found = True
                    break
            except NoSuchElementException:
                continue  # 如果当前卡片没有用户名或删除按钮，则跳过

        if not found:
            raise NoSuchElementException(f"未找到名为 '{username}' 的用户或其删除按钮。")

    def confirm_delete_user(self, username):
        self._wait_for_presence(self.delete_user_name_input).send_keys(username)

    def click_delete_date(self):
        self._wait_for_presence(self.delete_user_date).click()

    def confirm_delete(self,username):
        self.click_delete_button_for_user(username)
        self.click_delete_date()
        self.confirm_delete_user(username)
        self._wait_for_clickable(self.popup_ok_button).click()
        self._wait_for_presence(self.manager_user_button)


class MessagePage(BasePage):
    def __init__(self, driver, base_url):
        super().__init__(driver, base_url)
        self.message_input_field = (By.ID, 'send_textarea')
        self.send_button = (By.ID, 'send_but')
        self.last_user_message_text_locator = (By.CSS_SELECTOR,
                                               "div.mes[is_user='true'] > .mes_block > .mes_text > p:last-child")
        self.last_ai_reply_text_locator = (By.CSS_SELECTOR,
                                           "div.mes[is_user='false'][ch_name='Assistant'] > .mes_block > .mes_text > p:last-child")


    def get_message_input_placeholder(self):
        """输入框信息"""
        return self._wait_for_visibility(self.message_input_field).get_attribute('placeholder')

    def enter_message_text(self, text):
        """在消息输入框中输入文本。"""
        self._wait_for_visibility(self.message_input_field).send_keys(text)

    def click_send_button(self):
        """点击发送按钮。"""
        self._wait_for_clickable(self.send_button).click()

    def send_message(self, text):
        """发送信息"""
        # self.check_textarea()
        self.enter_message_text(text)
        self.click_send_button()


    def get_last_user_message_text(self, timeout=50):
        """获取聊天历史中最新一条用户发送的消息文本。"""
        user_message_element = self._wait_for_visibility(self.last_user_message_text_locator, timeout=timeout)
        return user_message_element.text

    def get_last_ai_reply_text(self, timeout=60):
        try:
            ai_reply_element = self._wait_for_visibility(self.last_ai_reply_text_locator, timeout=timeout)
            return ai_reply_element.text
        except TimeoutException:
            raise TimeoutException(f"在{timeout}s内未收到回复")


class CharacterPage(BasePage):
    def __init__(self, driver, base_url):
        super().__init__(driver, base_url)

        # 角色列表/面板元素
        self.character_list_panel = (By.ID, 'rightNavHolder')
        self.character_list_button = (By.ID, 'rm_button_characters')
        self.create_new_character_button = (By.ID, 'rm_button_create')
        self.character_search_bar = (By.ID, 'character_search_bar')

        # 页面检查用
        self.character_page_header_text = (By.CSS_SELECTOR, 'div.hotswap')

        # 创建/编辑角色表单元素
        self.character_name_input_field = (By.ID, 'character_name_pole')
        self.character_description_textarea = (By.ID, 'description_textarea')
        self.character_first_message_textarea = (By.ID, 'firstmessage_textarea')
        self.create_character_submit_button = (By.ID, 'create_button_label')

        # 删除角色相关元素
        self.bulk_edit_mode_button = (By.ID, 'bulkEditButton')
        self.all_character_cards = (By.CSS_SELECTOR, '#rm_print_characters_block .character_select')
        self.selected_character_count_display = (By.ID, 'bulkSelectedCount')

        self.bulk_delete_button = (By.ID, 'bulkDeleteButton')
        self.delete_chat_history_checkbox = (By.ID, 'del_char_checkbox')
        self.confirm_delete_popup_ok_button = (By.CSS_SELECTOR, '.popup-button-ok')
        self.delete_popup_title = (By.CSS_SELECTOR, '.popup-body h3')

        # 用于定位特定名称的角色卡片容器
        self.character_card_by_name_locator_template = lambda name: (By.XPATH,
                                                                     f"//div[@id='rm_print_characters_block']//div[contains(@class, 'character_select') and .//span[@class='ch_name' and normalize-space(text())='{name}']]")
        # 用于定位特定名称角色卡片内部的复选框
        self.character_checkbox_in_card_template = lambda name: (By.XPATH,
                                                                 f"//div[@id='rm_print_characters_block']//div[contains(@class, 'character_select') and .//span[@class='ch_name' and normalize-space(text())='{name}']]")

    # 导航/打开面板方法
    def open_character_management_panel(self):
        self._wait_for_clickable(self.character_list_panel).click()
        self._wait_for_clickable(self.character_list_button).click()
        self._wait_for_visibility(self.create_new_character_button)
        self._wait_for_visibility(self.character_page_header_text)

    # 创建角色相关方法
    def click_create_new_character_button(self):
        self._wait_for_clickable(self.create_new_character_button).click()
        self._wait_for_visibility(self.character_name_input_field)

    def enter_character_name(self, name):
        self._wait_for_visibility(self.character_name_input_field).send_keys(name)

    def enter_character_description(self, description):
        self._wait_for_visibility(self.character_description_textarea).send_keys(description)

    def enter_character_first_message(self, text):
        self._wait_for_visibility(self.character_first_message_textarea).send_keys(text)

    def click_create_character_submit_button(self):
        self._wait_for_clickable(self.create_character_submit_button,timeout=30).click()
        self._wait_for_invisibility(self.character_name_input_field)

    def create_character(self, name, description, first_message):
        self.open_character_management_panel()
        self.click_create_new_character_button()
        self.enter_character_name(name)
        self.enter_character_description(description)
        self.enter_character_first_message(first_message)
        self.click_create_character_submit_button()

        try:
            if not self.is_character_displayed_in_list(name, timeout=45):
                raise TimeoutException(f"创建角色 '{name}' 后，未在 {45} 秒内出现在列表中。")
            print(f"DEBUG: 新创建角色 '{name}' 已在列表中可见。")
        except TimeoutException as e:
            raise e

    # 删除角色相关方法
    def click_bulk_edit_mode_button(self):
        self._wait_for_clickable(self.bulk_edit_mode_button).click()
        self._wait_for_visibility(self.selected_character_count_display)

    def select_character_by_name(self, character_name,timeout=30):
        # 遍历所有角色卡片，查找指定名称的角色，并点击其内部的复选框
        character_checkbox_locator = self.character_checkbox_in_card_template(character_name)

        try:
            checkbox_to_click = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(character_checkbox_locator)
            )
            checkbox_to_click.click()
            print(f"DEBUG: 成功点击了角色 '{character_name}' 的复选框。")
        except TimeoutException:
            raise NoSuchElementException(
                f"在 {timeout} 秒内未找到或无法点击角色 '{character_name}' 的复选框以进行选择。")
        except NoSuchElementException as e:
            raise NoSuchElementException(f"未找到角色 '{character_name}' 的复选框元素。错误: {e}")
        except Exception as e:
            print(f"DEBUG: 选择角色 '{character_name}' 的复选框时发生未知错误: {type(e).__name__}: {e}")
            raise

    def is_character_displayed_in_list(self, character_name, timeout=30):
        """
        验证指定名称的角色是否显示在列表中。
        """
        character_name_locator = (By.XPATH,
                                  f"//div[@id='rm_print_characters_block']//div[contains(@class, 'character_select')]//span[@class='ch_name' and normalize-space(text())='{character_name}']")

        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(character_name_locator)
            )
            print(f"DEBUG: 角色 '{character_name}' 在列表中可见。")
            return True
        except TimeoutException:
            print(f"DEBUG: 在 {timeout} 秒内未找到角色 '{character_name}' 或其不可见。")
            return False
        except Exception as e:
            print(f"DEBUG: 检查角色 '{character_name}' 时发生未知错误: {type(e).__name__}: {e}")
            return False

    def get_selected_character_count(self):
        return self._wait_for_visibility(self.selected_character_count_display).text

    def click_bulk_delete_button(self):
        self._wait_for_clickable(self.bulk_delete_button).click()
        self._wait_for_visibility(self.delete_popup_title)

    def check_delete_chat_history_checkbox(self):
        self._wait_for_clickable(self.delete_chat_history_checkbox).click()

    def confirm_delete_character_action(self):
        self._wait_for_clickable(self.confirm_delete_popup_ok_button).click()
        self._wait_for_invisibility(self.delete_popup_title)

    def delete_character(self, character_name, delete_chat_history=True):
        self.click_bulk_edit_mode_button()
        self.select_character_by_name(character_name)
        self.click_bulk_delete_button()
        if delete_chat_history:
            self.check_delete_chat_history_checkbox()

        self.confirm_delete_character_action()
        try:
            WebDriverWait(self.driver, 30).until(
                EC.invisibility_of_element_located(self.character_card_by_name_locator_template(character_name))
            )
            print(f"DEBUG: 角色 '{character_name}' 已从列表中消失。")
        except TimeoutException:
            raise TimeoutException(f"删除角色 '{character_name}' 后，未在 30 秒内从列表中消失。")


class PersonaManagementPage(BasePage):
    def __init__(self, driver, base_url):
        super().__init__(driver, base_url)

        self.persona_management_entry_button = (By.ID, 'persona-management-button')
        self.page_header_title_display = (By.CSS_SELECTOR, 'h3 span[data-i18n="Persona Management"]')

        self.create_new_persona_button = (By.ID, 'create_dummy_persona')
        self.all_persona_cards = (By.CSS_SELECTOR, '#user_avatar_block .avatar-container')
        self.persona_name_in_card = (By.CSS_SELECTOR, 'span.ch_name')
        self.current_persona_name_display = (By.ID, 'your_name')

        self.rename_persona_button = (By.ID, 'persona_rename_button')
        self.delete_persona_button = (By.ID, 'persona_delete_button')
        self.persona_description_textarea = (By.ID, 'persona_description')

        self.popup_content_locator = (By.CSS_SELECTOR, '.popup-content')
        self.popup_input_field = (By.CSS_SELECTOR, '.popup-input')
        self.popup_ok_button = (By.CSS_SELECTOR, '.popup-button-ok')
        self.popup_cancel_button = (By.CSS_SELECTOR, '.popup-button-cancel')

    # 弹出窗口
    def is_popup_displayed(self):
        """判断通用弹窗是否显示。"""
        try:
            self._wait_for_visibility(self.popup_content_locator, timeout=3)
            return True
        except TimeoutException:
            return False

    def enter_text_in_popup_input(self, text):
        """在弹窗的输入框中输入文本。"""
        input_element = self._wait_for_presence(self.popup_input_field)
        input_element.clear()  # 清空现有文本
        input_element.send_keys(text)

    def click_popup_ok_button(self):
        """点击弹窗的确认按钮 (OK)。"""
        self._wait_for_clickable(self.popup_ok_button).click()
        self._wait_for_invisibility(self.popup_content_locator)

    def click_popup_cancel_button(self):
        """点击弹窗的取消按钮 (Cancel)。"""
        self._wait_for_clickable(self.popup_cancel_button).click()
        self._wait_for_invisibility(self.popup_content_locator)

    # 名字筛选
    def select_persona_by_name(self, persona_name,timeout=30):

        all_persona_cards_css = (By.CSS_SELECTOR, "#user_avatar_block .avatar-container")

        start_time = time.monotonic()
        found_and_clicked = False  # 标志变量，表示是否找到并点击成功

        # 在整个超时时间内重试查找和点击
        while time.monotonic() < start_time + timeout and not found_and_clicked:
            try:
                # 1. 等待至少一个角色卡片出现并可见
                WebDriverWait(self.driver, 5).until(  # 短暂等待，确保列表区域已加载
                    EC.visibility_of_element_located(all_persona_cards_css)
                )

                # 2. 获取所有角色卡片 (每次循环都重新查找，防止 StaleElementReferenceException)
                all_cards = self.driver.find_elements(*all_persona_cards_css)

                # 3. 遍历每个卡片，在其内部查找名称并匹配
                for card_element in all_cards:
                    try:
                        # 在当前卡片内部查找名称 span
                        name_span_in_card = card_element.find_element(By.CSS_SELECTOR, "span.ch_name")
                        actual_name_text = name_span_in_card.text.strip()  # 获取文本并去除前后空格

                        if actual_name_text == persona_name:
                            # 4. 找到匹配的卡片了！等待它可点击，然后点击。
                            print(f"DEBUG: 找到包含名称 '{persona_name}' 的卡片。")
                            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(card_element))
                            card_element.click()
                            print(f"DEBUG: 成功点击了用户角色 '{persona_name}' 的卡片。")
                            found_and_clicked = True
                            break  # 找到并点击了，退出 for 循环
                    except NoSuchElementException:
                        # 当前 card_element 内部没有 span.ch_name 或其结构不匹配，跳过此卡片
                        continue

                # 如果内层循环找到并点击了，则退出外层 while 循环
                if found_and_clicked:
                    break

            except StaleElementReferenceException:
                print("DEBUG: 遇到陈旧元素引用，重新查找所有角色卡片。")
                time.sleep(0.1)
                continue
            except TimeoutException:
                print(f"DEBUG: 循环内短暂等待超时，将重试查找 '{persona_name}'。")
                time.sleep(0.5)
                continue
            except Exception as e:
                print(f"DEBUG: 选择角色时发生异常：{type(e).__name__}: {e}，将重试。")
                time.sleep(1)

        if not found_and_clicked:
            raise NoSuchElementException(f"在 {timeout} 秒内未找到或无法点击名为 '{persona_name}' 的角色以进行选择。")

        # 验证“当前角色显示名称”是否更新 (这部分逻辑保持不变)
        current_name_display_element = self._wait_for_visibility(self.current_persona_name_display)  # 👈 修正这里
        actual_current_persona_name = current_name_display_element.text.strip()  # 👈 现在就可以安全地调用 .text 了

        if actual_current_persona_name != persona_name:
                raise AssertionError(
                    f"选中角色后，当前角色显示名称不匹配。预期：'{persona_name}', 实际：'{actual_current_persona_name}'")
        print(f"DEBUG: 当前角色显示名称验证通过：'{actual_current_persona_name}'。")


    def is_persona_displayed_in_list(self, persona_name,timeout=60):
        """
        验证用户角色是否显示在列表中。
        """
        persona_name_css_selector = (By.CSS_SELECTOR, "#user_avatar_block .avatar-container .ch_name")

        try:
            # 查找所有角色卡片，检查其中是否有匹配名称的span
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(persona_name_css_selector))

            all_name_elements = self.driver.find_elements(*persona_name_css_selector)

            for element in all_name_elements:
                actual_name_text = element.text.strip()  # .strip() 移除前后空白符
                if actual_name_text == persona_name:
                    print(f"DEBUG: 用户角色 '{persona_name}' 文本匹配成功。")
                    return True
            print(f"DEBUG: 元素可见，但在 {60} 秒内未找到文本为 '{persona_name}' 的用户角色。")
            return False

        except TimeoutException:
            return False

    # 创建角色
    def open_persona_management_page(self):
        self._wait_for_clickable(self.persona_management_entry_button).click()
        self._wait_for_visibility(self.page_header_title_display)
        self._wait_for_visibility(self.create_new_persona_button)

    def click_create_new_persona_button(self):
        self._wait_for_clickable(self.create_new_persona_button).click()
        self._wait_for_visibility(self.popup_content_locator)

    def enter_persona_description(self, description_text):
        self._wait_for_visibility(self.persona_description_textarea).send_keys(description_text)


    def create_persona(self, persona_name, description=""):
        self.open_persona_management_page()
        self.click_create_new_persona_button()
        self.enter_text_in_popup_input(persona_name)
        self.click_popup_ok_button()

        self.select_persona_by_name(persona_name)
        self._wait_for_visibility(self.persona_description_textarea)
        if description:
            self.enter_persona_description(description)

    # 编辑角色
    def click_edit_persona_button(self):
        self._wait_for_clickable(self.rename_persona_button).click()
        self._wait_for_visibility(self.popup_content_locator)

    def edit_role(self, old_persona_name, new_persona_name):
        self.open_persona_management_page()
        self.select_persona_by_name(old_persona_name)
        self.click_edit_persona_button()
        self.enter_text_in_popup_input(new_persona_name)
        self.click_popup_ok_button()

    # 删除角色
    def click_delete_persona_button(self):
        self._wait_for_clickable(self.delete_persona_button).click()
        self._wait_for_visibility(self.popup_content_locator)

    def delete_persona(self, persona_name):
        self.open_persona_management_page()
        self.select_persona_by_name(persona_name)
        self.click_delete_persona_button()
        self.click_popup_ok_button()
