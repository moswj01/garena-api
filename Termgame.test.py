from Termgame import Termgame

api = Termgame("junebikoadmin1", "Junebiko123.", "6BL3T5TVJ5IY4Z4A", '_ga_1M7M9L6VPX=GS2.1.s1757040020$o18$g0$t1757040020$j60$l0$h0; _gid=GA1.2.1706402335.1757335196; _ga_KE3SY7MRSD=GS2.1.s1757335195$o1$g1$t1757335204$j51$l0$h0; _ga_RF9R6YT614=GS2.1.s1757335195$o1$g0$t1757335204$j51$l0$h0; _ga=GA1.1.1129761749.1749566646; token_session=e96cd88a6711237ffd6fcb065e13f06986b40fc0021795541b60bd25f96ddfe247b84b3d128a675d5f911a5b30bf7937; fb_state=28c995fa3c2a41f3b19e4e3d44711c60; google_state=24a8b7cbb672433e8c14aac1930f8b46; huawei_state=4066916e204740389fe2957f04c786f3; line_state=ed097738de554c62a7bff1a35b99deaa; twitter_state=ce3895c38f044303a5a09c924b274e31; vk_state=b673194c72cd42bdaef8256c4cc0b02c; _ga_XB5PSHEQB4=GS2.1.s1757385599$o21$g0$t1757385599$j60$l0$h0; datadome=f~KK9KbnYsaM0dQKfriXcB7p9Ad807seLmqiR2u1Lb7Y~3NcLTnIWgj~9NtCHFpj_~gGFsnU6se7yDMOtEL768mLIFUffRop5yhsqJyE7SnWv1DuidPeCUk1EV3ncPqf')  # Garena Account here
response = api.login_garena()
print('login_garena', response)

# print("DELTA_FORCE")
# player_id_login = api.player_id_login(api.DELTA_FORCE, "54963782192811737868")
# print(player_id_login)

# print("ROV")
# player_id_login = api.player_id_login(api.ROV, "475658971186290")
# print(player_id_login)

# print("FREEFIRE")
# player_id_login = api.player_id_login(api.FREE_FIRE, "19225432")
# print(player_id_login)

# print("UNDAWN")
# player_id_login = api.player_id_login(api.GARENA_UNDAWN, "12011163357")
# print(player_id_login)

response = api.buy(api.FREE_FIRE, "19225432", 80, 0)
print('สำเร็จ', response)
# {'error': 'invalid_id'}
# {'display_id': '14149741438725956850', 'error_data': None, 'result': 'success', 'exec': {'display_id': '14149741438725956850'}}

# response = api.buy(api.ROV, "475658971186290", 1)
# print('สำเร็จ', response)

# player_id_login = api.player_id_login(api.BLACK_CLOVER_M, "ZAIQ2666468406")
# response = api.buy(api.BLACK_CLOVER_M, "ZAIQ2666468406", 502, player_id_login['session_key'])
# print('สำเร็จ', response)

# # garena shell account must be TH region and undawn must not login by garena account
# player_id_login = api.player_id_login(api.UNDAWN, "12011163357")
# response = api.buy(api.UNDAWN, "12011163357", 40010, player_id_login['session_key'])
# print('สำเร็จ', response)
