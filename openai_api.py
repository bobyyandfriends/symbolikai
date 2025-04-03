from openai import OpenAI

client = OpenAI(
  api_key="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"
)

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  messages=[
    {"role": "user", "content": "write a haiku about ai"}
  ]
)

print(completion.choices[0].message);
