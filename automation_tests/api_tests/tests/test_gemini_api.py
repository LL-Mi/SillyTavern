import json

import pytest
import requests
from requests import Timeout


class TestGeminiApi:
    def test_GeminiApi(self,base_url):
        api_endpoint=f"{base_url}/api/backends/chat-completions/generate"

        headers={"Content-Type":"application/json",
                 "Cookie": "session-da8676fd=eyJjc3JmVG9rZW4iOiI2ZjAyOTQxZTlkMDRmNTEwNTlkM2RkMzc2MWJlZWM4YWEzZjMxYTgxNWVkOTJlOTY3ZDg0NDAyYmU1NWUxYTNhIiwiaGFuZGxlIjoic2FtIiwidG91Y2giOjE3NTMzNjU2MTU1ODB9; session-da8676fd.sig=MujUv2uVsTEo_L_8im1aIS5Sf0U",
                 "X-CSRF-Token": "6f02941e9d04f51059d3dd3761beec8aa3f31a815ed92e967d84402be55e1a3a",
                 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
                 }


        requests_body={

                "messages": [
                    {
                        "role": "system",
                        "content": "Write Assistant's next reply in a fictional chat between Assistant and 1."
                    },
                    {
                        "role": "system",
                        "content": "[Start a new Chat]"
                    },
                    {
                        "role": "user",
                        "content": "你好"
                    }
                ],
                "model": "gemini-2.0-flash",
                "temperature": 1,
                "frequency_penalty": 0,
                "presence_penalty": 0,
                "top_p": 1,
                "max_tokens": 300,
                "stream": False,
                "chat_completion_source": "makersuite",
                "user_name": "1",
                "char_name": "Assistant",
                "group_names": [],
                "include_reasoning": True,
                "reasoning_effort": "auto",
                "enable_web_search": False,
                "request_images": False,
                "custom_prompt_post_processing": "",
                "top_k": 0,
                "stop": [],
                "use_makersuite_sysprompt": True

        }

        # 发送 POST 请求并处理可能的网络异常
        try:
            print(f"发送 API 请求到: {api_endpoint}")
            response = requests.post(api_endpoint, headers=headers, json=requests_body,timeout=60)
            print(f"收到 API 响应，状态码: {response.status_code}")
        except ConnectionError as e:
            pytest.fail(f"无法连接到 API 端点 {api_endpoint}。请确保后端服务正在运行且网络畅通。错误: {e}")
        except Timeout as e:
            pytest.fail(f"API 请求超时 ({api_endpoint})。请检查 API 响应速度或增加超时时间。错误: {e}")
        except Exception as e:
            pytest.fail(f"发送 API 请求时发生未知错误: {e}")

        assert response.status_code == 200,f"API 请求失败。预期状态码200，实际: {response.status_code}。完整响应: {response.text}"


        # 断言响应体内容
        try:
            response_json = response.json()

        except json.JSONDecodeError as e:
            # 捕获响应体不是有效 JSON 格式的错误
            pytest.fail(f"API 响应不是有效的 JSON 格式。错误: {e}。响应文本: {response.text}")

        #验证ai回复
        assert "choices" in response_json, "API 响应中缺少 'choices' 字段。"
        assert isinstance(response_json["choices"], list) and len(response_json["choices"]) > 0, "'choices' 字段不是有效的非空列表。"

        first_choice  = response_json["choices"][0]
        assert "message" in first_choice , "第一个 choices 中缺少 'message' 字段。"

        message = first_choice["message"]
        assert "content" in message, "message 中缺少 'content' 字段 。"

        ai_reply_content = message["content"]

        # 验证回复文本不为空
        assert ai_reply_content is not None and ai_reply_content.strip() != "", \
            f"AI 回复内容为空或仅包含空白字符。实际回复: '{ai_reply_content}'"

        print(f"API 测试通过！成功收到有效 AI 回复 (前100字符): {ai_reply_content[:100]}...")
