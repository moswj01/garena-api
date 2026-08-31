# garena-api

FastAPI service that wraps the Garena / termgame.com recharge flow. It runs on
port `8100` (see `docker-compose.yml`).

## Login

`POST /login` authenticates a Garena account. It runs the full Garena SSO login
chain internally (prelogin → password encryption → login → grant token →
inspect token) using the credentials in the request body.

### Request body

| Field       | Type   | Description                                              |
| ----------- | ------ | -------------------------------------------------------- |
| `username`  | string | Garena account username                                 |
| `password`  | string | Garena account password (encrypted server-side)         |
| `setup_key` | string | Garena TOTP/2FA **setup key** (not a 6-digit OTP code)   |

### curl

```bash
curl -X POST http://localhost:8100/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your_garena_username",
    "password": "your_garena_password",
    "setup_key": "your_2fa_setup_key"
  }'
```

Replace `localhost` with the host/IP where the container runs if calling it
remotely (the service binds `0.0.0.0:8100`).

### Responses

- **Success** — the Garena login response JSON.
- **Failure** — `{"message": "ไม่สามารถเข้าสู่ระบบได้"}` with HTTP `400`.

## Other endpoints

| Method | Path                              | Description                          |
| ------ | --------------------------------- | ------------------------------------ |
| GET    | `/account`                        | Current account info                 |
| POST   | `/recharge`                       | Buy / recharge an item               |
| GET    | `/packages?app_id=<id>`           | List packages for an app             |
| POST   | `/update-player-id-login-cookie`  | Update player-id login cookie        |
| POST   | `/update-prelogin-cookies`        | Update prelogin cookies              |
| POST   | `/update-get-packages-session-key`| Update the get-packages session key  |
