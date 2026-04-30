# This connects the Python app directly to Docker daemon.

import docker
import time

from agent.graph import graph
from agent.ai import analyze_container
from executor import can_retry, execute_action, decide_action, fallback_action, is_safe_to_fix

AUTO_FIX = True

analyzed_cache = set()

try:
    client = docker.DockerClient(
    base_url='npipe:////./pipe/docker_engine',
    timeout=120)
    print(client.version())
except Exception as e:
    print("ERROR:", e)

def list_containers():

    # List all containers, including stopped ones.

    containers = client.containers.list(all=True)

    data = []
    for c in containers:
        data.append({
            "id": c.id[:12],
            "name": c.name,
            "status": c.status,
            "image": c.image.tags
        })

    return data

def get_container_details(name):

    # Get details of a specific container by name. This includes its status and recent logs.

    try:
        container = client.containers.get(name)

        return {
            "name": container.name,
            "status": container.status,
            "logs": container.logs(tail=20).decode("utf-8", errors="ignore")
        }

    except Exception as e:
        return {"error": str(e)}
    
def detect_issues(container):

    # Simple heuristic to detect common issues based on container status.

    if container["status"] == "exited":
        return "Container has stopped unexpectedly"
    elif container["status"] == "restarting":
        return "Container is stuck in restart loop"
    return None

def get_logs_if_failed(name, status):

    # If a container is not running, fetch its recent logs to help diagnose the issue.

    if status != "running":
        return get_container_details(name)["logs"]
    return None

def should_analyze(status):
    return status in ["exited", "restarting"]
    
def monitor_loop():

    # This function continuously monitors the status of all containers and 
    # prints it to the console every 10 seconds.

    while True:
        containers = list_containers()

        print("\n=== Container Status ===")
        for c in containers:
            container_key = f"{c['name']}-{c['status']}"
            print(f"{c['name']} → {c['status']}")

            issue = detect_issues(c)
            if issue:
                print(f"\n=== ⚠️ ISSUE in {c['name']}: {issue} ===")

                logs = get_logs_if_failed(c["name"], c["status"])
                print("\n=== Logs ===")
                print(logs)

                if should_analyze(c["status"]) and container_key not in analyzed_cache:
                    print("\n=== 🧠 AI Diagnosis: ===")

                    # result = analyze_container(c["name"], c["status"], logs)

                    result = graph.invoke({
                        "container_name": c["name"],
                        "status": c["status"],
                        "logs": logs
                    })

                    print(f"Cause: {result.get('root_cause')}")
                    print(f"Severity: {result.get('severity')}")
                    print(f"Fix: {result.get('fix')}")

                    action = decide_action(result)
                    if not action:
                        action = fallback_action(c["status"])

                    print(f"\n=== ⚙️ Decided Action: {action} ===")

                    if AUTO_FIX and action:
                        if is_safe_to_fix(result) and can_retry(c["name"]):
                            execute_action(action, c["name"])
                        else:
                            print("⚠️ Skipping auto-fix (safety rules)")

                    analyzed_cache.add(container_key)

        time.sleep(10)