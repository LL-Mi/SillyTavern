import os
import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService

from webdriver_manager.microsoft import EdgeChromiumDriverManager

from automation_tests.ui_tests.tests.login import login

load_dotenv()

@pytest.fixture(scope="module")
def base_url():
    return os.getenv('BASE_URL',"http://localhost:8000")

@pytest.fixture(scope="module")
def driver_setup_chrome():
    print('浏览器初始化中')
    chrome_driver_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'drivers', 'chromedriver.exe'))
    service = ChromeService(chrome_driver_path)  # 使用本地路径
    driver=webdriver.Chrome(service=service)

    driver.maximize_window()#最大化窗口
    driver.implicitly_wait(10)#隐式等待

    yield driver

    print('关闭浏览器')
    driver.quit()

@pytest.fixture(scope="module")
def driver_setup_edge():
    print('浏览器初始化中')

    edge_driver_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'drivers', 'msedgedriver.exe'))
    service = EdgeService(edge_driver_path)  # 使用本地路径

    driver = webdriver.Edge(service=service)

    driver.maximize_window()  # 最大化窗口
    driver.implicitly_wait(10)  # 隐式等待

    yield driver

    print('关闭浏览器')
    driver.quit()

@pytest.fixture(scope="session")
def user():
    username=os.getenv('TEST_USERNAME')
    password=os.getenv('TEST_PASSWORD')
    if not username or not password:
        pytest.fail("错误：未设置 TEST_USERNAME 或 TEST_PASSWORD 环境变量。请检查 .env 文件或系统环境变量。")

    return {"username": username, "password": password}

@pytest.fixture(scope="session")
def admin():
    username=os.getenv('TEST_ADMIN_NAME')
    password=os.getenv('TEST_ADMIN_PASSWORD')
    if not username or not password:
        pytest.fail("错误：未设置 TEST_ADMIN_NAME 或 TEST_ADMIN_PASSWORD 环境变量。请检查 .env 文件或系统环境变量。")

    return {"username": username, "password": password}

