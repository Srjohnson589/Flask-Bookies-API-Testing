from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful librarian."},
    {"role": "user", "content": "I like mysteries"},
    {"role": "system", "content": "Sure! Mystery is a great genre. Do you have any preferences, like a specific setting or time period, or do you prefer a particular type of detective or amateur sleuth? Let me know if you have any preferences so I can recommend a mystery book that suits your tastes."},
    {"role": "user", "content": "I like the Victorian era"}
  ]
)

print(completion.choices[0].message)