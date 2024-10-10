import os
from dotenv import load_dotenv

load_dotenv()

VK_LOGIN = os.getenv('VK_LOGIN')
VK_PASSWORD = os.getenv('VK_PASSWORD')
VK_APP_ID = os.getenv('VK_APP_ID')
VK_ACCESS_TOKEN = os.getenv('VK_ACCESS_TOKEN')
