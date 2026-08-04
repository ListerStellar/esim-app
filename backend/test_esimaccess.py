import os
import json
import time
import uuid
import hmac
import hashlib
import httpx

ACCESS_CODE = "091c8ebf9e89467693e88305c405469f"
SECRET_KEY = "7f8e8a8743be4a3bade45ae375368328"
BASE_URL = "https://api.esimaccess.com/api/v1/open"

def generate_headers(body_str=""):
    timestamp = str(int(time.time() * 1000))
    req_id = str(uuid.uuid4())
    sign_str = timestamp + req_id + ACCESS_CODE + body_str
    signature = hmac.new(SECRET_KEY.encode(), sign_str.encode(), hashlib.sha256).hexdigest().upper()
    
    return {
        "RT-AccessCode": ACCESS_CODE,
        "RT-RequestID": req_id,
        "RT-Timestamp": timestamp,
        "RT-Signature": signature,
        "Content-Type": "application/json"
    }

async def test_api():
    async with httpx.AsyncClient() as client:
        # 1. Test destinations/locations
        body = json.dumps({})
        headers = generate_headers(body)
        print("Fetching destinations...")
        try:
            res = await client.post(f"{BASE_URL}/location/list", data=body, headers=headers)
            print("Location HTTP Status:", res.status_code)
            print("Location JSON:", json.dumps(res.json(), indent=2)[:500])
        except Exception as e:
            print("Location list error:", e)
            
        print("-" * 50)
        
        # 2. Test packages
        body = json.dumps({"locationCode": "FR"})
        headers = generate_headers(body)
        print("Fetching packages for FR...")
        try:
            res = await client.post(f"{BASE_URL}/package/list", data=body, headers=headers)
            print("Package HTTP Status:", res.status_code)
            print("Package JSON:", json.dumps(res.json(), indent=2)[:500])
        except Exception as e:
            print("Package list error:", e)

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_api())
