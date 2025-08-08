import json
import requests
from urllib.parse import parse_qs
from mybyte import Encrypt_ID, encrypt_api

def handler(event, context):
    try:
        query = parse_qs(event.get("queryStringParameters") or "")
        token = query.get("token", [None])[0]
        uid = query.get("uid", [None])[0]

        if not token or not uid:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing token or uid"}, ensure_ascii=False)
            }

        uid = int(uid)
        id_encrypted = Encrypt_ID(uid)
        data0 = "08c8b5cfea1810" + id_encrypted + "18012008"
        data = bytes.fromhex(encrypt_api(data0))

        url = "https://clientbp.ggblueshark.com/GetBackpack"
        headers = {
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9; ASUS_Z01QD Build/PI)',
            'Connection': 'Keep-Alive',
            'Expect': '100-continue',
            'Authorization': f'Bearer {token}',
            'X-Unity-Version': '2018.4.11f1',
            'X-GA': 'v1 1',
            'ReleaseVersion': 'OB50',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        response = requests.post(url, headers=headers, data=data, verify=False)

        if response.status_code == 200:
            return {
                "statusCode": 200,
                "body": json.dumps({"status": "success", "message": "Friend removed or action completed!"}, ensure_ascii=False)
            }
        else:
            return {
                "statusCode": 500,
                "body": json.dumps({
                    "status": "failed",
                    "code": response.status_code,
                    "response": response.text
                }, ensure_ascii=False)
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}, ensure_ascii=False)
        }
