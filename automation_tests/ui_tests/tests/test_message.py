
from automation_tests.ui_tests.pages.pom import MessagePage
from automation_tests.ui_tests.tests.login import login


class TestMessage_chrome:
    def test_message(self,driver_setup_chrome,base_url,user):

        login(driver_setup_chrome, user, base_url)

        message_page=MessagePage(driver_setup_chrome, base_url)
        original_message_to_send = "你好"
        message_page.send_message(original_message_to_send)
        user_last_message=message_page.get_last_user_message_text()
        assert original_message_to_send==user_last_message,"消息可能没有发送成功"

        try:
            message_ai_reply=message_page.get_last_ai_reply_text()
            if message_ai_reply and message_ai_reply.strip() != "":
                print(f'成功收到ai回复{message_ai_reply}')
        except Exception as e:
            print(f'未收到回复可能未配置api或者网络问题{e}')

class TestMessage_edge:
    def test_message(self,driver_setup_edge,base_url,user):

        login(driver_setup_edge, user, base_url)

        message_page=MessagePage(driver_setup_edge, base_url)
        original_message_to_send = "你好"
        message_page.send_message(original_message_to_send)
        user_last_message=message_page.get_last_user_message_text()
        assert original_message_to_send==user_last_message,"消息可能没有发送成功"

        try:
            message_ai_reply=message_page.get_last_ai_reply_text()
            if message_ai_reply and message_ai_reply.strip() != "":
                print(f'成功收到ai回复{message_ai_reply}')
        except Exception as e:
            print(f'未收到回复可能未配置api或者网络问题{e}')
