import asyncio
import json

from fastapi.testclient import TestClient
from httpx import AsyncClient

# We mock settings before importing main
import os
os.environ["WHATSAPP_VERIFY_TOKEN"] = "test123token"

try:
    from main import app
    client = TestClient(app)

    print("✅ Fast API loaded successfully")

    # 1. Test GET /webhook/whatsapp verification endpoint
    response = client.get(
        "/webhook/whatsapp?hub.mode=subscribe&hub.verify_token=test123token&hub.challenge=challenge123"
    )
    if response.status_code == 200 and response.text == "challenge123":
        print("✅ Webhook GET Verification successful")
    else:
        print(f"❌ Webhook GET Verification failed: {response.status_code} - {response.text}")

    # 2. Test POST /webhook/whatsapp endpoint
    payload = {
        "entry": [{
            "changes": [{
                "value": {
                    "messages": [{
                        "from": "5511999999999",
                        "text": {"body": "Oi"}
                    }]
                }
            }]
        }]
    }
    response = client.post("/webhook/whatsapp", json=payload)
    if response.status_code == 200 and response.json() == {"status": "ok"}:
        print("✅ Webhook POST responds 200 immediately")
    else:
        print(f"❌ Webhook POST failed: {response.status_code} - {response.text}")

except Exception as e:
    print(f"❌ Failed to load or run app tests: {e}")
