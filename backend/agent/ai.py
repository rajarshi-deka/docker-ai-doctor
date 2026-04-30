from openai import OpenAI
from .prompts import SYSTEM_PROMPT
import os
import json
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def analyze_container(name, status, logs):

    context = f"""
    Container Name: {name}
    Status: {status}

    Recent Logs:
    {logs[-2000:]}

    Observation:
    The container is currently NOT running.

    Task:
    1. Identify root cause
    2. Suggest fix
    3. Choose action (restart if container is stopped)
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": context}
        ]
    )

    output = response.choices[0].message.content

    try:
        return json.loads(output)
    except:
        return {"error": output}