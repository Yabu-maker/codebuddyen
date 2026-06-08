import sys
import os
import json
import time
import datetime
import hmac
import hashlib
import subprocess
from urllib.parse import urlparse

TOKEN_PATH = "/Users/vinyaliu/Documents/programs/codebuddyen/token.txt"
SAVE_PATH = "/Users/vinyaliu/Documents/programs/codebuddyen/resouce/images/dog.jpg"

def _sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def _hmac_sha256(key: bytes, msg: bytes) -> bytes:
    return hmac.new(key, msg, hashlib.sha256).digest()

def _sign_request(
    secret_id: str,
    secret_key: str,
    service: str,
    action: str,
    version: str,
    region: str,
    host: str,
    payload: str,
    timestamp=None,
) -> dict:
    if timestamp is None:
        timestamp = int(time.time())
    date = datetime.datetime.fromtimestamp(
        timestamp, tz=datetime.timezone.utc
    ).strftime("%Y-%m-%d")

    http_request_method = "POST"
    canonical_uri = "/"
    canonical_querystring = ""
    content_type = "application/json; charset=utf-8"
    signed_headers = "content-type;host;x-tc-action"
    canonical_headers = (
        f"content-type:{content_type}\n"
        f"host:{host}\n"
        f"x-tc-action:{action.lower()}\n"
    )
    hashed_payload = _sha256_hex(payload.encode("utf-8"))

    canonical_request = (
        f"{http_request_method}\n"
        f"{canonical_uri}\n"
        f"{canonical_querystring}\n"
        f"{canonical_headers}\n"
        f"{signed_headers}\n"
        f"{hashed_payload}"
    )

    algorithm = "TC3-HMAC-SHA256"
    credential_scope = f"{date}/{service}/tc3_request"
    hashed_canonical = _sha256_hex(canonical_request.encode("utf-8"))
    string_to_sign = (
        f"{algorithm}\n"
        f"{timestamp}\n"
        f"{credential_scope}\n"
        f"{hashed_canonical}"
    )

    secret_date = _hmac_sha256(
        ("TC3" + secret_key).encode("utf-8"), date.encode("utf-8")
    )
    secret_service = _hmac_sha256(secret_date, service.encode("utf-8"))
    secret_signing = _hmac_sha256(secret_service, b"tc3_request")

    signature = hmac.new(
        secret_signing, string_to_sign.encode("utf-8"), hashlib.sha256
    ).hexdigest()

    authorization = (
        f"{algorithm} "
        f"Credential={secret_id}/{credential_scope}, "
        f"SignedHeaders={signed_headers}, "
        f"Signature={signature}"
    )

    headers = {
        "Authorization": authorization,
        "Content-Type": content_type,
        "Host": host,
        "X-TC-Action": action,
        "X-TC-Version": version,
        "X-TC-Region": region,
        "X-TC-Timestamp": str(timestamp),
    }
    return headers

def call_api_via_curl(action: str, body: dict, token: str) -> dict:
    endpoint = "https://copilot.tencent.com/agenttool/v1/tcproxy"
    provider = "hy-image-v3"
    service = "hunyuan"
    version = "2023-09-01"
    region = "ap-guangzhou"
    
    secret_id = f"{provider}.{token}"
    secret_key = "codebuddy"

    parsed = urlparse(endpoint)
    host = parsed.hostname
    payload = json.dumps(body, ensure_ascii=False)

    headers = _sign_request(
        secret_id=secret_id,
        secret_key=secret_key,
        service=service,
        action=action,
        version=version,
        region=region,
        host=host,
        payload=payload,
    )

    # Prepare curl command
    curl_cmd = ["curl", "-s", "-X", "POST", endpoint]
    for k, v in headers.items():
        curl_cmd.append("-H")
        curl_cmd.append(f"{k}: {v}")
    curl_cmd.append("-d")
    curl_cmd.append(payload)

    # Run via subprocess
    res = subprocess.run(curl_cmd, capture_output=True)
    if res.returncode != 0:
        print(f"Curl failed with return code {res.returncode}")
        print(res.stderr.decode(errors="ignore"))
        return {}

    try:
        return json.loads(res.stdout.decode("utf-8"))
    except Exception as e:
        print("Failed to parse API JSON response:", e)
        print("Raw output:", res.stdout.decode(errors="ignore"))
        return {}

def download_file(url: str, output_path: str):
    print(f"Downloading {url} to {output_path}...")
    res = subprocess.run(["curl", "-s", "-o", output_path, url])
    if res.returncode == 0:
        print("Download successful!")
    else:
        print("Download failed.")

def main():
    if not os.path.exists(TOKEN_PATH):
        print(f"Error: Token file {TOKEN_PATH} not found.")
        sys.exit(1)
        
    with open(TOKEN_PATH, "r") as f:
        token = f.read().strip()

    if not token:
        print(f"Error: Token file {TOKEN_PATH} is empty.")
        sys.exit(1)

    prompt = "一只极度可爱的小白狗，穿着蓝白条纹水手服，坐在松软的阳光草坪上，水汪汪的大眼睛看着镜头，特写，超清画质，电影级光影，景深"
    print(f"Submitting image generation with prompt: '{prompt}'")
    
    # 1. Submit
    res = call_api_via_curl("SubmitHunyuanImageJob", {"Prompt": prompt}, token)
    
    if "error" in res:
        print("\n[API Error] Service returned:", res["error"])
        if "token" in res["error"].lower() or "expired" in res["error"].lower():
            print("\n💡 提示：您的 CodeBuddy 账户 Session 已过期。请在 IDE 中重新登录，或运行 'Developer: Reload Window' 重新载入窗口刷新会话，然后重试。")
        sys.exit(1)

    response_data = res.get("Response", {})
    if "Error" in response_data:
        print("Error submitting job:", response_data["Error"].get("Message"))
        sys.exit(1)
        
    job_id = response_data.get("JobId")
    if not job_id:
        print("No JobId found in response:", res)
        sys.exit(1)
        
    print(f"Job successfully submitted! JobId: {job_id}")
    
    # 2. Poll
    for i in range(30):
        print(f"Polling status {i+1}/30 (next check in 5s)...")
        time.sleep(5)
        
        poll_res = call_api_via_curl("QueryHunyuanImageJob", {"JobId": job_id}, token)
        poll_data = poll_res.get("Response", {})
        
        if "Error" in poll_data:
            print("Error polling job status:", poll_data["Error"].get("Message"))
            break
            
        status = poll_data.get("Status")
        status_code = poll_data.get("JobStatusCode")
        print(f"Current Job Status: {status} (Code: {status_code})")
        
        if status == "DONE" or status_code == 5:
            img_url = poll_data.get("ResultImageUrl") or poll_data.get("ResultUrl")
            if img_url:
                print(f"Job complete! Image URL: {img_url}")
                # Ensure parent dir exists
                os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
                download_file(img_url, SAVE_PATH)
            else:
                print("Error: Job marked DONE but no image URL returned.")
            break
        elif status == "FAIL" or status_code == 4:
            print("Job failed:", poll_data.get("JobErrorMsg") or poll_data.get("ErrorMessage"))
            break

if __name__ == "__main__":
    main()
