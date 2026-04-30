import subprocess

retry_count = {}
ALLOWED_ACTIONS = ["restart", "stop", "none"]

def restart_container(name):
    print(f"🔄 Restarting {name}")
    subprocess.run(["docker", "restart", name])
    print("DOCKER_AI_DOCTOR: Restart Container: Success")


def stop_container(name):
    print(f"⛔ Stopping {name}")
    subprocess.run(["docker", "stop", name])
    print("DOCKER_AI_DOCTOR: Stop Container: Success")

def decide_action(ai_result):
    action = ai_result.get("action")
    if action not in ALLOWED_ACTIONS:
        return None
    return action

def execute_action(action, container_name):
    if action == "restart":
        restart_container(container_name)
    elif action == "stop":
        stop_container(container_name)
    else:
        print("DOCKER_AI_DOCTOR: Execute Action: No Safe Action Mapped")
        print("⚠️ No safe action mapped")

def is_safe_to_fix(ai_result):
    return ai_result.get("severity") == "High"

def can_retry(name):
    retry_count[name] = retry_count.get(name, 0) + 1
    return retry_count[name] <= 3

def fallback_action(status):
    if status == "exited":
        return "restart"
    return None