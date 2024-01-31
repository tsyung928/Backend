import openai

openai.api_key = '<YOUR_API_KEY>'

completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "說句話吧"}
    ]
)

print(completion)