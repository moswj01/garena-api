import uvicorn
from typing import Union
from fastapi import FastAPI
from Termgame import Termgame
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os

class BuyRequest(BaseModel):
    app_id: int
    player_id: str
    item_id: int

class LoginRequest(BaseModel):
    username: str
    password: str
    setup_key: str

class UpdatePlayerIDLoginCookieRequest(BaseModel):
    cookies: str

class UpdatePreloginCookiesRequest(BaseModel):
    cookies: str

class UpdateGetPackagesSessionKeyRequest(BaseModel):
    cookies: str

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

username = os.getenv("GARENA_USERNAME")
password = os.getenv("GARENA_PASSWORD")
auth_key = os.getenv("GARENA_AUTH")

print(username, password, auth_key)

api = Termgame(username, password, auth_key, '_ga=GA1.1.1693857112.1761887450; _ga_1M7M9L6VPX=GS2.1.s1761887449$o1$g1$t1761887487$j22$l0$h0; token_session=05c2ebb6ccac4a0b6e4e855e5b96fa9a8413f143a129764c58e8b530ab2ac5a908be7fa6734c77020da3bc14c941d722; fb_state=906e1e8089584c3e9e51d0587f2423dd; google_state=1aea2d007dde4ba7b9202d3517649229; huawei_state=5105e6ff29fe4220b1480a96c98c51b6; line_state=fb15ec3223994483a765b1cb560649c0; twitter_state=26f40cd9100a486caebaaab5502263b3; vk_state=e54eae5ac7c84b76aadc21be8d55b4a7; _ga_XB5PSHEQB4=GS2.1.s1762276856$o4$g1$t1762276998$j60$l0$h0; datadome=AzQu0AtLaTapOKcpQg~HVsp7DS3q~z~DkYJtAGpTmBmyYIzLEXaYdhP2rGl3htQfQs4e0wZJt25_DQZsyDLL8dq52hmemuOn4cT38p4lcSy80CoOc8swS13TZVOZjihw')
api.login_garena()


def response_wrapper(response: Union[dict, str]):
    if isinstance(response, dict):
        return JSONResponse(content=response)
    else:
        return JSONResponse(content=response, status_code=400)


@app.post("/login")
async def login(login_request: LoginRequest):
    try:
        print("login_request", login_request)
        api.set_credentials(login_request.username,
                            login_request.password, login_request.setup_key)
        response = api.login_garena()
        print('login_garena', response)
        return response_wrapper(response)
    except Exception as e:
        print(e)
        return response_wrapper({
            "message": "ไม่สามารถเข้าสู่ระบบได้",
        })

@app.get("/account")
async def account():
    try:
        return response_wrapper(api.get_user_info())
    except Exception as e:
        print(e)
        return response_wrapper({
            "error": "ไม่สามารถดึงข้อมูลบัญชีได้",
        })

@app.post("/recharge")
async def recharge(buy_request: BuyRequest):
    print('recharge request', buy_request)
    player_id_login_app_ids = [api.DELTA_FORCE, api.GARENA_UNDAWN, api.HAIKYU_FLY_HIGH, api.CALL_OF_DUTY_MOBILE]
    packed_role_id = 0
    session_key = None
    if buy_request.app_id == api.ROV:
        packed_role_id = 786432

    if buy_request.app_id in player_id_login_app_ids:
        player_login_id_response = api.player_id_login(buy_request.app_id, buy_request.player_id)
        print('player_login_id_response', player_login_id_response)
        if player_login_id_response.get('error') or player_login_id_response.get('success') == False:
            return response_wrapper({'error': 'ข้อมูลไอดีผู้เล่นไม่ถูกต้อง'})
        else:
            session_key = player_login_id_response.get('session_key')
            if not session_key:
                return response_wrapper({'error': 'ไม่พบข้อมูลผู้เล่น'})

            player_info_response = api.get_user_info(session_key)
            print('player_info_response', player_info_response)
            garena_uid = player_info_response.get('player_id', {}).get('uid', None)
            if garena_uid is not None:
                print('This account is bind with Garena UID:', garena_uid)
                return response_wrapper({
                    "error": "บัญชีนี้ผูกกับบัญชี Garena ไม่สามารถเติมได้",
                })

            packed_role_response = api.get_roles(buy_request.app_id, session_key)
            print('packed_role_response', packed_role_response)

            try:
                packed_role_id = packed_role_response[str(buy_request.app_id)][0]['packed_role_id']
                print('packed_role_id', packed_role_id)
            except (KeyError, IndexError, TypeError) as e:
                print('Error accessing packed_role_id:', e)
                return response_wrapper({'error': 'ไม่พบข้อมูลสำหรับผู้เล่นนี้'})

    print('request params', buy_request.app_id, buy_request.player_id, buy_request.item_id, packed_role_id)
    response = api.buy(buy_request.app_id, buy_request.player_id, buy_request.item_id, packed_role_id, session_key)
    print('recharge response', response)
    if response.get('error') or response.get('result') != 'success':
        return response_wrapper({
            "error": response.get('error', response.get('result', 'ไม่สามารถดำเนินการสั่งซื้อได้')),
        })

    return response_wrapper(response)

@app.get("/packages")
async def packages(app_id: int):
    print('get_packages_request', app_id)
    response = api.get_packages(app_id)
    return response_wrapper({
        "packages": response
    })

@app.post("/update-player-id-login-cookie")
async def update_player_id_login_cookie(request: UpdatePlayerIDLoginCookieRequest):
    try:
        print("update_player_id_login_cookie", request)
        api.set_player_id_login_cookies(request.cookies)
        return response_wrapper({
            "message": "อัปเดตคุกกี้สำเร็จ",
        })
    except Exception as e:
        print(e)
        return response_wrapper({
            "message": "ไม่สามารถอัปเดตคุกกี้ได้",
        })

@app.post("/update-prelogin-cookies")
async def update_prelogin_cookies(request: UpdatePreloginCookiesRequest):
    try:
        print("update_prelogin_cookies", request)
        api.set_prelogin_cookies(request.cookies)
        return response_wrapper({
            "message": "อัปเดตคุกกี้สำเร็จ",
        })
    except Exception as e:
        print(e)
        return response_wrapper({
            "message": "ไม่สามารถอัปเดตคุกกี้ได้",
        })

@app.post("/update-get-packages-session-key")
async def update_get_packages_session_key(request: UpdateGetPackagesSessionKeyRequest):
    try:
        print("update_get_packages_session_key", request)
        api.set_get_packages_session_key(request.cookies)
        return response_wrapper({
            "message": "อัปเดตคุกกี้สำเร็จ",
        })
    except Exception as e:
        print(e)
        return response_wrapper({
            "message": "ไม่สามารถอัปเดตคุกกี้ได้",
        })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8100)
