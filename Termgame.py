import requests
import pyotp
import time
import hashlib
import binascii
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from base64 import b64encode
import base64
import json

class Termgame:
    TERMGAME_ENDPOINT = "https://termgame.com"
    SSO_GARENA_ENDPOINT = "https://sso.garena.com"
    AUTHGOP_ENDPOINT = "https://authgop.garena.com"

    SSO_APP_ID = 10100
    AUTHGOP_APP_ID = 10017

    DELTA_FORCE = 100151
    FREE_FIRE = 100067
    ROV = 100055
    HAIKYU_FLY_HIGH = 100153
    CALL_OF_DUTY_MOBILE = 100082
    GARENA_UNDAWN = 100105

    def __init__(self, username: str = None, password: str = None, auth_key: str = None, prelogin_cookies: str = None):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_55_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
            'connection': 'keep-alive',
        })
        self.username = username
        self.password = password
        self.auth_key = auth_key
        self.datadome = self.initial_datadome()
        self.access_token = None
        self.garena_id = None
        self.player_id_login_cookies = 'source=pc; region=IN.TH; mspid2=02f8849803c509c8e792813e7271a6ef; language=th; _fbp=fb.1.1757340696850.641426515527115040; _ga=GA1.1.1903506881.1757340697; datadome=1FWIfm61mCz1yDqqLxnY1R5GHtfepBUSSQYH5iqr76301Y55yGa1xT3s6qzZUwvXiSQuHaUNzWnv0UyNUc1VJqkkb2L7HRCOPmTUTQ0o54eb2hdz7RpN6DB2dN79Kkcu; session_key=qzybn0lh67vexi7dn0hs34d1ynclgw7t; _ga_VRZ5RWC6GM=GS2.1.s1757340697$o1$g1$t1757340719$j38$l0$h0'
        self.prelogin_cookies = prelogin_cookies
        self.get_packages_session_key = 'h6p47vato27p2xd5zftf3he71wgbro66'
        self.session_key = None

    def set_credentials(self, username: str, password: str, auth_key: str):
        self.username = username
        self.password = password
        self.auth_key = auth_key

    def get_datadome(self):
        url = "https://dd.garena.com/js/"

        payload = 'jsData=%7B%22ttst%22%3A8.299999952316284%2C%22ifov%22%3Afalse%2C%22hc%22%3A10%2C%22br_oh%22%3A891%2C%22br_ow%22%3A1512%2C%22ua%22%3A%22Mozilla%2F5.0%20(Macintosh%3B%20Intel%20Mac%20OS%20X%2010_15_7)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F126.0.0.0%20Safari%2F537.36%22%2C%22wbd%22%3Afalse%2C%22dp0%22%3Atrue%2C%22tagpu%22%3A0.7381211959967529%2C%22wdif%22%3Afalse%2C%22wdifrm%22%3Afalse%2C%22npmtm%22%3Afalse%2C%22br_h%22%3A804%2C%22br_w%22%3A753%2C%22isf%22%3Afalse%2C%22nddc%22%3A1%2C%22rs_h%22%3A982%2C%22rs_w%22%3A1512%2C%22rs_cd%22%3A30%2C%22phe%22%3Afalse%2C%22nm%22%3Afalse%2C%22jsf%22%3Afalse%2C%22lg%22%3A%22en-US%22%2C%22pr%22%3A2%2C%22ars_h%22%3A891%2C%22ars_w%22%3A1512%2C%22tz%22%3A-420%2C%22str_ss%22%3Atrue%2C%22str_ls%22%3Atrue%2C%22str_idb%22%3Atrue%2C%22str_odb%22%3Afalse%2C%22plgod%22%3Afalse%2C%22plg%22%3A5%2C%22plgne%22%3Atrue%2C%22plgre%22%3Atrue%2C%22plgof%22%3Afalse%2C%22plggt%22%3Afalse%2C%22pltod%22%3Afalse%2C%22hcovdr%22%3Afalse%2C%22hcovdr2%22%3Afalse%2C%22plovdr%22%3Afalse%2C%22plovdr2%22%3Afalse%2C%22ftsovdr%22%3Afalse%2C%22ftsovdr2%22%3Afalse%2C%22lb%22%3Afalse%2C%22eva%22%3A33%2C%22lo%22%3Afalse%2C%22ts_mtp%22%3A0%2C%22ts_tec%22%3Afalse%2C%22ts_tsa%22%3Afalse%2C%22vnd%22%3A%22Google%20Inc.%22%2C%22bid%22%3A%22NA%22%2C%22mmt%22%3A%22application%2Fpdf%2Ctext%2Fpdf%22%2C%22plu%22%3A%22PDF%20Viewer%2CChrome%20PDF%20Viewer%2CChromium%20PDF%20Viewer%2CMicrosoft%20Edge%20PDF%20Viewer%2CWebKit%20built-in%20PDF%22%2C%22hdn%22%3Afalse%2C%22awe%22%3Afalse%2C%22geb%22%3Afalse%2C%22dat%22%3Afalse%2C%22med%22%3A%22defined%22%2C%22aco%22%3A%22probably%22%2C%22acots%22%3Afalse%2C%22acmp%22%3A%22probably%22%2C%22acmpts%22%3Atrue%2C%22acw%22%3A%22probably%22%2C%22acwts%22%3Afalse%2C%22acma%22%3A%22maybe%22%2C%22acmats%22%3Afalse%2C%22acaa%22%3A%22probably%22%2C%22acaats%22%3Atrue%2C%22ac3%22%3A%22%22%2C%22ac3ts%22%3Afalse%2C%22acf%22%3A%22probably%22%2C%22acfts%22%3Afalse%2C%22acmp4%22%3A%22maybe%22%2C%22acmp4ts%22%3Afalse%2C%22acmp3%22%3A%22probably%22%2C%22acmp3ts%22%3Afalse%2C%22acwm%22%3A%22maybe%22%2C%22acwmts%22%3Afalse%2C%22ocpt%22%3Afalse%2C%22vco%22%3A%22%22%2C%22vcots%22%3Afalse%2C%22vch%22%3A%22probably%22%2C%22vchts%22%3Atrue%2C%22vcw%22%3A%22probably%22%2C%22vcwts%22%3Atrue%2C%22vc3%22%3A%22maybe%22%2C%22vc3ts%22%3Afalse%2C%22vcmp%22%3A%22%22%2C%22vcmpts%22%3Afalse%2C%22vcq%22%3A%22%22%2C%22vcqts%22%3Afalse%2C%22vc1%22%3A%22probably%22%2C%22vc1ts%22%3Atrue%2C%22dvm%22%3A8%2C%22sqt%22%3Afalse%2C%22so%22%3A%22landscape-primary%22%2C%22wdw%22%3Atrue%2C%22cokys%22%3A%22bG9hZFRpbWVzY3NpYXBwL%3D%22%2C%22ecpc%22%3Afalse%2C%22lgs%22%3Atrue%2C%22lgsod%22%3Afalse%2C%22psn%22%3Atrue%2C%22edp%22%3Atrue%2C%22addt%22%3Atrue%2C%22wsdc%22%3Atrue%2C%22ccsr%22%3Atrue%2C%22nuad%22%3Atrue%2C%22bcda%22%3Atrue%2C%22idn%22%3Atrue%2C%22capi%22%3Afalse%2C%22svde%22%3Afalse%2C%22vpbq%22%3Atrue%2C%22ucdv%22%3Afalse%2C%22spwn%22%3Afalse%2C%22emt%22%3Afalse%2C%22bfr%22%3Afalse%2C%22dbov%22%3Afalse%2C%22cfpfe%22%3A%22ZnVuY3Rpb24oKXsKCnZhciBkYXRhID0gewoicmVzb3VyY2UiOiB7CiAgInZlcnNpb24iOiIxIiwKICAKICAibWFjcm9zIjpbeyJmdW5jdGlvbiI6Il9fZSJ9LHsiZnVuY3Rpb24iOiJfX2MiLCJ2dHBfdmFsdWUiOiJjIn1dLAogICJ0YWdzIjpbeyJmdW5jdGlvbiI6%22%2C%22stcfp%22%3A%22bWFuYWdlci5jb20vZ3RhZy9qcz9pZD1VQS0xMzc1OTc4MjctOSZsPWRhdGFMYXllciZjeD1jOjE1NTozNgogICAgYXQgaHR0cHM6Ly93d3cuZ29vZ2xldGFnbWFuYWdlci5jb20vZ3RhZy9qcz9pZD1VQS0xMzc1OTc4MjctOSZsPWRhdGFMYXllciZjeD1jOjQ5NDoz%22%2C%22ckwa%22%3Atrue%2C%22prm%22%3Atrue%2C%22tzp%22%3A%22Asia%2FBangkok%22%2C%22cvs%22%3Atrue%2C%22usb%22%3A%22defined%22%2C%22emd%22%3A%22k%3Aai%2Cvi%2Cao%22%2C%22glvd%22%3A%22Google%20Inc.%20(Apple)%22%2C%22glrd%22%3A%22ANGLE%20(Apple%2C%20ANGLE%20Metal%20Renderer%3A%20Apple%20M2%20Pro%2C%20Unspecified%20Version)%22%2C%22wwl%22%3Afalse%2C%22jset%22%3A1718263114%7D&eventCounters=%5B%5D&jsType=ch&cid=bWS~KjsGhP5sw_q~e8r8F3eP9z7trRjLxp3ktoVf26rlN~SYXJl6ybV2iPPC1qCeAXXBLg8plNKj4IN6b8skojnVENabj2h8JkoIE2icTTVlCA4r3FcaVMmQyAyQsT1g&ddk=AE3F04AD3F0D3A462481A337485081&Referer=https%253A%252F%252Ftermgame.com%252Fapp%252F%253Faccess_token%253Dedbab3b7b4f0f9b723de81f07507ab2dce8600be2bd41f463c7de3823f910bd1&request=%252Fapp%252F%253Faccess_token%253Dedbab3b7b4f0f9b723de81f07507ab2dce8600be2bd41f463c7de3823f910bd1&responsePage=origin&ddv=4.29.1'
        headers = {
            'content-type': 'application/x-www-form-urlencoded',
            'origin': self.TERMGAME_ENDPOINT,
            'referer': self.TERMGAME_ENDPOINT + "/"
        }

        response = self.session.post(url, headers=headers, data=payload)
        return response.json()

    def initial_datadome(self):
        response = self.get_datadome()['cookie']
        return response.split(";")[0].split("=")[1]

    def get_otp(self):
        opt_code = pyotp.HOTP(self.auth_key)
        return opt_code.at(int(time.time() / 180))

    def get_current_time(self):
        return int(time.time())

    def encrypt_password(self, password: str, v1: str, v2: str):
        password = hashlib.md5(password.encode('utf-8')).hexdigest()
        key = hashlib.sha256((hashlib.sha256((password + v1).encode()).hexdigest() + v2).encode()).hexdigest()
        key = binascii.unhexlify(key)
        password = binascii.unhexlify(password)

        # Create a cipher object with AES in ECB mode
        cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())

        # Encrypt the data without additional padding
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(password) + encryptor.finalize()

        # Encode the encrypted data as base64
        encrypted_base64 = b64encode(encrypted_data).decode()

        #encrypted_base64 to hex
        encrypted_hex = binascii.hexlify(base64.b64decode(encrypted_base64)).decode()

        return encrypted_hex

    def login_garena(self, proxies: dict = None):

        url = "{}/api/prelogin?app_id={}&account={}&format=json&id={}".format(
            self.SSO_GARENA_ENDPOINT, self.SSO_APP_ID, self.username, self.get_current_time())

        payload = {}
        headers = {
          'Accept': 'application/json, text/plain, */*',
          'Accept-Language': 'en-US,en;q=0.9,th;q=0.8',
          'Cache-Control': 'no-cache',
          'Connection': 'keep-alive',
          'Pragma': 'no-cache',
          'Referer': 'https://authgop.garena.com/universal/oauth?client_id=10017&redirect_uri=https%3A%2F%2Ftermgame.com%2F&response_type=token&platform=1&locale=th-TH&theme=light',
          'Sec-Fetch-Dest': 'empty',
          'Sec-Fetch-Mode': 'cors',
          'Sec-Fetch-Site': 'same-origin',
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
          'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"macOS"',
          'Cookie': self.prelogin_cookies
        }

        prelogin_response = self.session.get(url, headers=headers, data=payload, proxies=proxies)
        prelogin_response = prelogin_response.json()

        print('prelogin_response', prelogin_response)

        v1 = prelogin_response.get('v1')
        v2 = prelogin_response.get('v2')
        if not v1 or not v2:
            return {
                "success": False,
                "message": "ไม่สามารถเข้าสู่ระบบได้ (prelogin)",
            }

        password = self.encrypt_password(self.password, v1, v2)
        login_response = self.session.get("{}/api/login?app_id={}&account={}&password={}&redirect_uri=https%3A%2F%2Faccount.garena.com%2F&format=json&id={}".format(
            self.SSO_GARENA_ENDPOINT, self.SSO_APP_ID, self.username, password, self.get_current_time()), headers=headers, data=payload, proxies=proxies)

        print(login_response.json())
        if 'error' in login_response.json():
            return {
                "success": False,
                "message": login_response.json().get('error'),
            }


        sso_key = login_response.headers.get('Set-Cookie').split(";")[0].split("=")[1]
        grant_token_response = self.grant_token(sso_key)
        print('grant_token_response', grant_token_response)
        self.access_token = grant_token_response['access_token']
        inspect_token_response = self.inspect_token(self.access_token)
        print('inspect_token_response', inspect_token_response)
        self.garena_id = inspect_token_response['uid']
        return login_response.json()

    def grant_token(self, sso_key: str):
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9,th;q=0.8',
            'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'cookie': 'datadome={}; sso_key={}'.format(self.datadome, sso_key),
        }

        payload = 'client_id={}&response_type=token&redirect_uri=https%3A%2F%2Ftermgame.com%2Fapp%2F&format=json&id={}'.format(self.AUTHGOP_APP_ID, self.get_current_time())

        response = self.session.post(self.AUTHGOP_ENDPOINT + "/oauth/token/grant", headers=headers, data=payload)
        return response.json()

    def inspect_token(self, token: str):
        headers = {
            'accept': 'application/json',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9,th;q=0.8',
            'content-type': 'application/json',
            'x-datadome-clientid': self.datadome,
        }

        payload = json.dumps({
            'token': token,
        })

        response = self.session.post(self.TERMGAME_ENDPOINT + "/api/auth/inspect_token", headers=headers, data=payload)
        self.session_key = response.headers.get('Set-Cookie').split(";")[0].split("=")[1]
        return response.json()

    def get_user_info(self):
        headers = {
            'accept': 'application/json',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9,th;q=0.8',
            'content-type': 'application/json',
            'cookie': 'source=pc; session_key={}; datadome={}'.format(self.session_key, self.datadome),
            'x-datadome-clientid': self.datadome,
        }

        response = self.session.get(self.TERMGAME_ENDPOINT + "/api/auth/get_user_info/multi", headers=headers)
        return response.json()

    def prefight(self):
        headers = {
            'accept': 'application/json',
            'content-type': 'application/json',
            'cookie': 'source=pc; session_key={}; datadome={}'.format(self.session_key, self.datadome),
        }

        response = self.session.post(self.TERMGAME_ENDPOINT + "/api/preflight", headers=headers)
        return response.headers

    def get_roles(self, app_id: int, session_key: str = None):
        url = "https://termgame.com/api/shop/apps/roles?app_id=100151&region=IN.TH&language=th&source=pc"

        payload = {}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Cookie': 'session_key={}'.format(session_key),
        }

        response = requests.get(url, headers=headers, data=payload)
        if 'error' in response.json():
            return {
                "success": False,
                "message": response.json().get('error'),
            }

        return response.json()

    def buy(self, app_id: str, player_id: str, item_id: int, packed_role_id, custom_session_key: str = None):
        data = {
            "service": "mb",
            "app_id": app_id,
            "packed_role_id": packed_role_id,
            "channel_id": 207070,
            "item_id": item_id,
            "channel_data": {
                "otp_code": self.get_otp(),
                "garena_uid": self.garena_id
            },
            "player_id": player_id,
            "revamp_experiment": {
                "group": "treatment2",
                "service_version": "mshop_frontend_20241011",
                "source": "pc",
                "domain": "termgame.com"
            }
        }

        remove_player_id_apps = [self.DELTA_FORCE, self.HAIKYU_FLY_HIGH, self.CALL_OF_DUTY_MOBILE, self.GARENA_UNDAWN]
        if int(app_id) in remove_player_id_apps:
            data.pop('player_id')

        payload = json.dumps(data)

        preflight_response = self.prefight()
        preflight_cookie = preflight_response.get('Set-Cookie').split(";")[0].split("=")[1]

        if custom_session_key:
            handled_session_key = custom_session_key
        else:
            handled_session_key = self.session_key

        headers = {
            'Accept-Language': 'en-US,en;q=0.9,th;q=0.8',
            'Cookie': 'source=pc; __csrf__={}; session_key={}'.format(preflight_cookie, handled_session_key),
            'accept': 'application/json',
            'content-type': 'application/json',
            'x-csrf-token': preflight_cookie,
            'x-datadome-clientid': self.datadome,
        }

        response = self.session.post(self.TERMGAME_ENDPOINT + "/api/shop/pay/init?language=th&region=IN.TH", headers=headers, data=payload)
        print(response.json())
        return response.json()

    def player_id_login(self, app_id: int, player_id: str, proxies: dict = None):
        url = "https://termgame.com/api/auth/player_id_login"

        payload = json.dumps({
            "app_id": app_id,
            "login_id": player_id,
        })

        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9,th;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
            'Cookie': self.player_id_login_cookies,
        }

        response = requests.post(url, headers=headers, data=payload, proxies=proxies)
        if 'error' in response.json():
            return {
                "success": False,
                "message": response.json().get('error'),
            }

        if 'url' in response.json():
            return {
                "success": False,
                "message": "ต้องยืนยันตัวตนก่อน",
                "data": response.json()
            }

        response_headers = response.headers
        session_key = None
        if 'Set-Cookie' in response_headers:
            cookies = response_headers['Set-Cookie'].split(";")
            for cookie in cookies:
                if 'session_key' in cookie:
                    session_key = cookie.split("session_key=")[1]
                    break
        if not session_key:
            return {
                "success": False,
                "message": "ไม่สามารถเข้าสู่ระบบได้ (player_id_login)",
            }

        return {
            "success": True,
            "session_key": session_key,
            "data": response.json()
        }

    # def get_user_info(self, session_key: str):
    #     headers = {
    #         'accept': 'application/json',
    #         'accept-encoding': 'gzip, deflate, br',
    #         'accept-language': 'en-US,en;q=0.9,th;q=0.8',
    #         'content-type': 'application/json',
    #         'cookie': 'session_key={}'.format(session_key),
    #         'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
    #     }

    #     response = requests.get(self.TERMGAME_ENDPOINT + "/api/auth/get_user_info/multi", headers=headers)
    #     return response.json()

    def set_player_id_login_cookies(self, cookies: str):
        self.player_id_login_cookies = cookies

    def set_prelogin_cookies(self, cookies: str):
        self.prelogin_cookies = cookies

    def set_get_packages_session_key(self, session_key: str):
        self.get_packages_session_key = session_key

    def get_packages(self, app_id: int, channel_id = 207070):
        url = "{}/api/shop/apps/channels?app_id={}&packed_role_id=0&region=IN.TH&language=th&channel_id={}".format(self.TERMGAME_ENDPOINT, app_id, channel_id)
        payload = {}

        headers = {
            'Accept-Language': 'en-US,en;q=0.9,th;q=0.8',
            'Connection': 'keep-alive',
            'Referer': '{}/app'.format(self.TERMGAME_ENDPOINT),
            'accept': 'application/json',
            'content-type': 'application/json',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
            'cookie': 'session_key={}'.format(self.get_packages_session_key)
        }

        response = requests.get(url, headers=headers, data=payload)
        channel = response.json()['channels']
        return next((item for item in channel if item['channel'] == channel_id), None)['items']



