import httpx
import json
import time
BASE_URL = "http://127.0.0.1:8000/api/chat/"
def test_chat(message, history=[]):
    print(f"\nUser: {message}")
    payload = {
        "message": message,
        "history": history
    }
    try:
        response = httpx.post(BASE_URL, json=payload, timeout=60.0)
        if response.status_code == 200:
            data = response.json()
            print(f"Agent: {data['message']}")
            print(f"Action: {data.get('action')}")
            if data.get('data'):
                print(f"Data: {data.get('data')}")
            return data
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Request failed: {e}")
        return None
def main():
    print("--- Testing Agent Interactivity ---")
    print("\n--- Test 1: Research Company ---")
    history = []
    resp1 = test_chat("Research Microsoft", history)
    if resp1:
        history.append({"role": "user", "content": "Research Microsoft"})
        history.append({"role": "assistant", "content": resp1['message']})
    print("\n--- Test 2: Specific Question (Deep Dive) ---")
    time.sleep(1)
    resp2 = test_chat("What is their AI strategy?", history)
    if resp2:
        history.append({"role": "user", "content": "What is their AI strategy?"})
        history.append({"role": "assistant", "content": resp2['message']})
    print("\n--- Test 3: Context Switch ---")
    time.sleep(1)
    resp3 = test_chat("What about Google?", history)
if __name__ == "__main__":
    main()