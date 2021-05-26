
from tda import auth
from src.model import config
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class td_authenticator:
    def __init__(self):
        pass

    @staticmethod
    def authenticate():
        try:
            c = auth.client_from_token_file(config.TOKEN_PATH, config.API_KEY)
        except FileNotFoundError:
            with webdriver.Chrome(ChromeDriverManager().install()) as driver:
                c = auth.client_from_login_flow(
                    driver, config.API_KEY, config.REDIRECT_URI, config.TOKEN_PATH)