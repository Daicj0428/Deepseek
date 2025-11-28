from openai import OpenAI
import os

def deepseek1(message, stream=True):
    client = OpenAI(
        base_url=os.getenv("DEEPSEEK_API_URL", "https://api.deepseek.com/"),
        api_key=os.getenv("DEEPSEEK_API_KEY")
    )
    
    completion = client.chat.completions.create(
        model=os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
        messages=message,
        stream=stream
    )
    
    if stream:
        for chunk in completion:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    else:
        return completion.choices[0].message.content
