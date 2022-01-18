from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import os
import zipfile
import time


manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
"""

class ManualDriver:
    def get_background_js(self, proxy):
        proxy = proxy.split(":")
        PROXY_USER = proxy[2]
        PROXY_PASS = proxy[3]
        PROXY_HOST = proxy[0]
        PROXY_PORT = proxy[1]
        return """
    var config = {
            mode: "fixed_servers",
            rules: {
              singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
              },
              bypassList: ["localhost"]
            }
          };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

    def get_chromedriver(self, proxy, use_proxy=False, user_agent=None):
        path = os.path.dirname(os.path.abspath(__file__))
        chrome_options = webdriver.ChromeOptions()
        if use_proxy:
            pluginfile = 'proxy_auth_plugin.zip'
            background_js = self.get_background_js(proxy)
            with zipfile.ZipFile(pluginfile, 'w') as zp:
                zp.writestr("manifest.json", manifest_json)
                zp.writestr("background.js", background_js)
            chrome_options.add_extension(pluginfile)
        if user_agent:
            chrome_options.add_argument('--user-agent=%s' % user_agent)
        driver = webdriver.Chrome(
            ChromeDriverManager().install(),
            chrome_options=chrome_options)
        return driver

    def drive(self, email, password, token, proxy):
        driver = self.get_chromedriver(proxy, use_proxy=True)
        driver.get('https://discord.com/login')
        email_input = driver.find_element_by_name("email")
        password_input = driver.find_element_by_name("password")
        email_input.send_keys(email)
        password_input.send_keys(password)
        driver.find_element_by_xpath("//button[@type='submit']").click()
        captcha_solver = input("Captcha y/n? \n ")
        if captcha_solver == "y":
            driver.execute_script(
                """function login(token) {
  setInterval(() => {
    document.body.appendChild(document.createElement`iframe`)
                 .contentWindow.localStorage.token = `"${token}"`;
  }, 50);
  setTimeout(() => {
    location.reload();
  }, 2500);
}

          login("%s")
          console.log
          """
                % token
            )

        finished = input("Press Enter to go to next account")
        driver.close()