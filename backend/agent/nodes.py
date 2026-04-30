import os
import json
import re
from dotenv import load_dotenv
from openai import OpenAI
from executor import execute_action
from agent.memory.vector_store import search_memory, add_memory

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# Node 1 — Investigator
def investigator(state):
    logs = state["logs"][-2000:]
    print("DOCKER_AI_DOCTOR: *====Orchestration Started====*")
    print("DOCKER_AI_DOCTOR: Investigator Logs:", logs)

    return {
        "logs": logs
    }

def extract_json(text):
    text = re.sub(r"```json|```", "", text).strip()
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group(0) if match else "{}"

def safe_parse_json(content):
    try:
        return json.loads(content)
    except:
        print("⚠️ JSON parse failed:", content)
        return {
            "root_cause": "Unknown",
            "severity": "Low",
            "fix": "Parsing failed"
        }
    
def normalize_severity(severity):
    severity = str(severity).lower()
    if severity in ["high", "critical", "error"]:
        return "High"
    elif severity in ["medium", "warning"]:
        return "Medium"
    return "Low"

# Node 2 — Diagnoser
def diagnoser(state):
    logs = state["logs"]

    # 🔍 Retrieve similar past issues
    similar_cases = search_memory(logs)

    prompt = f"""
    You are a DevOps expert.

    Here are similar past issues and their fixes:
    {similar_cases}

    Use them as reference, but validate against current logs.

    Current logs:
    {logs}

    Return JSON:
    root_cause, severity, fix
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    
    content = response.choices[0].message.content
    print("\n🔍 RAW LLM OUTPUT:\n", content) 
    clean_json = extract_json(content) 
    result = safe_parse_json(clean_json)
    result["severity"] = normalize_severity(result.get("severity"))
    print("DOCKER_AI_DOCTOR: Diagnoser Result:", result)
    # result = json.loads(content)

    # result = json.loads(response.choices[0].message.content)

    return result

# Node 3 — Planner
def planner(state):
    fix = state["fix"].lower()

    if "restart" in fix:
        action = "restart"
    elif "stop" in fix:
        action = "stop"
    else:
        action = "none"
    print("DOCKER_AI_DOCTOR: Planner Action:", action)

    return {"action": action}

# Node 4 — Decision (Safety Layer)
def decision(state):
    if state["severity"] == "High" and state["action"] != "none" and state.get("auto_fix"):
        print("DOCKER_AI_DOCTOR: Decision Execute: True")
        return {"execute": True}
    print("DOCKER_AI_DOCTOR: Decision Execute: False")
    return {"execute": False}

# Node 5 — Executor
def executor_node(state):
    executed = False
    if state.get("auto_fix") and state.get("execute"):
        execute_action(state["action"], state["container_name"])
        executed = True

    print("DOCKER_AI_DOCTOR: Executor: Executed:", executed)
    # ✅ Save semantic memory
    entry = {
        "logs_snippet": state["logs"][:500],
        "root_cause": state["root_cause"],
        "severity": state["severity"],
        "fix": state["fix"],
        "action": state["action"],
        "executed": executed
    }

    if state["severity"] == "High":
        add_memory(entry)
    print("DOCKER_AI_DOCTOR: Executor: Success")
    print("DOCKER_AI_DOCTOR: *====Orchestration Ended====*")

    return {}