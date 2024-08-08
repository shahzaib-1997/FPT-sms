from fastapi import FastAPI, Form, status, Response
import time, json, requests

app = FastAPI()


def read_json_file(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def write_json_file(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


def get_access_token():
    token_file = "tokens.json"

    data = read_json_file(token_file)

    access_token = data["access_token"]
    expires_in = int(data["expires_in"])
    token_time = data["created_time"]

    if time.time() - token_time > expires_in:
        client_secret = "j4yC3G5MGCGC6OsB2AFe"
        client_id = "1726087278974764839"

        url = "http://sandbox.sms.fpt.net/oauth2/token"
        headers = {
            "Content-Type": "application/json",
        }
        data = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": "send_brandname_otp",
            "session_id": "5c22be0c0396440829c98d7ba124092020145753419"
        }

        tokens = requests.post(url, json=data, headers=headers).json()
        print(tokens)
        access_token = tokens["access_token"]
        tokens["created_time"] = time.time()

        write_json_file(token_file, tokens)
    return access_token


@app.post("/send/")
async def handle_form(
    phone: str = Form(...), body: str = Form(...), sender: str = Form(...)
):
    try:
        url = "http://sandbox.sms.fpt.net/api/push-brandname-international"
        access_token = get_access_token()
        headers = {
            "Content-Type": "application/json",
        }
        data = {
            "access_token": access_token,
            "session_id": "5c22be0c0396440829c98d7ba124092020145753419",
            "BrandName": "FTI",
            "Phone": phone,
            "Message": body,
        }
        return {"msg": "Message sent successfully"}
    except:
        return Response(
            content={"error": "Unable to send msg."},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@app.post("/validate/")
async def validate(generated_otp: str, user_otp: str):
    if generated_otp == user_otp:
        return True
    return False
