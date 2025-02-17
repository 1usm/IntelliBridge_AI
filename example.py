

from openai import OpenAI

client = OpenAI(api_key="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")


try:
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello, world!"}])
    print(response)
except Exception as e:
    print(f"Error: {e}")