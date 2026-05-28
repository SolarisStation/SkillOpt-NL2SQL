import openai
import os
import threading
import time

_lock = threading.Lock()
_optimizer_client = None
_target_client = None

def get_optimizer_client(cfg):
    global _optimizer_client
    with _lock:
        if _optimizer_client is None:
            _optimizer_client = openai.OpenAI(
                api_key=cfg["api_key"],
                base_url=cfg["endpoint"]
            )
        return _optimizer_client

def get_target_client(cfg):
    global _target_client
    with _lock:
        if _target_client is None:
            _target_client = openai.OpenAI(
                api_key=cfg["api_key"],
                base_url=cfg["endpoint"]
            )
        return _target_client

def chat(client, model, system, user, max_tokens, retries=5):
    for attempt in range(retries):
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user}
                ],
                max_completion_tokens=max_tokens,
                temperature=0.0
            )
            return resp.choices[0].message.content, {}
        except Exception as e:
            if attempt == retries - 1:
                raise e
            time.sleep(2 ** attempt)
