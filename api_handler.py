import requests
import json
import time  # Don't forget to import the time module for the sleep function

class APIHandler:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = "https://api.openai.com/v1/engines/davinci-codex/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def build_payload(self, prompt, max_tokens=100):
        return json.dumps({
            "prompt": prompt,
            "max_tokens": max_tokens,
        })

    def send_request(self, payload):
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                data=payload
            )

            # Handle rate limiting first
            if response.status_code == 429:
                retry_after = response.headers.get("Retry-After")
                if retry_after:
                    time.sleep(int(retry_after))
                    return self.send_request(payload)
                else:
                    return {"error": {"message": "Rate limited. Please try again later."}}

            response.raise_for_status()  # Check for other HTTP errors

            jsonResponse = response.json()
            if "error" in jsonResponse:
                raise Exception(jsonResponse["error"]["message"])

            return jsonResponse

        except requests.exceptions.RequestException as e:
            return {"error": {"message": str(e)}}
        except Exception as e:
            return {"error": {"message": str(e)}}

    def get_text_from_response(self, response):
        try:
            return response["choices"][0]["text"].strip()
        except KeyError:
            if "error" in response:
                return response["error"]["message"]
            return "Error: Could not extract text from response."

if __name__ == '__main__':
    api_handler = APIHandler("your_api_key_here")
    prompt = "Translate the following English text to French: '{}'"
    payload = api_handler.build_payload(prompt.format("Hello, world"))
    response = api_handler.send_request(payload)
    generated_text = api_handler.get_text_from_response(response)
    print(generated_text)