import streamlit as st
import sys
import os

# Get absolute path to backend folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND_PATH = os.path.join(BASE_DIR, "backend")

sys.path.append(BACKEND_PATH)

from monitor import list_containers, get_container_details
from agent.ai import analyze_container
from executor import execute_action, decide_action
from agent.graph import graph

st.set_page_config(page_title="Docker AI Doctor", layout="wide")

st.title("🧠 Docker AI Doctor")
st.write("Monitor and auto-heal your containers")

# Auto-Fix Toggle (Sidebar)
auto_fix = st.sidebar.toggle("⚡ Auto Fix", value=False)
if auto_fix:
    st.info("⚡ Auto-Fix is ENABLED")
else:
    st.warning("Auto-Fix is DISABLED")

# Show Agent Pipeline (Visual Explanation)
st.subheader("🧠 Agent Pipeline")

st.write("""
🔍 Investigator -> 🧠 Diagnoser -> 🛠 Planner -> ⚖️ Decider -> ⚡ Executor  
""")

# List all containers with their status
containers = list_containers()
print("DOCKER_AI_DOCTOR: Containers List:", containers)

st.subheader("📦 Containers")

for c in containers:
    col1, col2, col3 = st.columns([3, 2, 2])

    col1.write(f"**{c['name']}**")
    # col2.write(c["status"])

    status_map = {
        "running": "🟢 Running",
        "exited": "🔴 Exited",
        "restarting": "🟡 Restarting"
    }

    col2.write(status_map.get(c["status"], c["status"]))

    if c["status"] != "running":
        col3.warning("Needs Attention")
    else:
        col3.success("Healthy")

# Allow user to select a container to analyze
container_names = [c["name"] for c in containers]
print("DOCKER_AI_DOCTOR: Container Names:", container_names)

selected = st.selectbox("Select Container", container_names)

# Show details and logs of the selected container
details = get_container_details(selected)
print("DOCKER_AI_DOCTOR: Container Details:", details)

st.subheader("📜 Logs")
st.code(details.get("logs", "No logs available"), language="bash")

button_label = "⚡ Execute Agent" if auto_fix else "🧠 Analyze with AI"
run_clicked = st.button(button_label)
# Detect issues and show AI analysis
if run_clicked:
    with st.spinner("Analyzing..."):
        # result = analyze_container(
        #     selected,
        #     details.get("status"),
        #     details.get("logs")
        # )
        result = graph.invoke({
            "container_name": selected,
            "status": details.get("status"),
            "logs": details.get("logs"),
            "auto_fix": auto_fix   # 🔥 pass toggle here
        })
    print("DOCKER_AI_DOCTOR: Graph Invoke:", result)
    st.session_state["last_result"] = result

    st.subheader("🧠 AI Diagnosis")

    st.write(f"**Cause:** {result.get('root_cause')}")

    severity = result.get("severity")
    if severity == "High":
        st.error(f"Severity: {severity}")
    elif severity == "Medium":
        st.warning(f"Severity: {severity}")
    else:
        st.success(f"Severity: {severity}")

    st.write(f"**Fix:** {result.get('fix')}")
    st.write(f"**Action:** {result.get('action')}")
    if auto_fix:
        st.success(f"Executed: {result.get('action')}")

    # action = decide_action(result)

    # if action:
    #     st.write(f"**Suggested Action:** {action}")

# Allow user to apply the suggested fix
apply_clicked = st.button(
    "⚡ Apply Fix",
    disabled=auto_fix  # 🔥 disable when auto-fix is ON
)
if apply_clicked:
    # result = analyze_container(
    #     selected,
    #     details.get("status"),
    #     details.get("logs")
    # )

    # action = decide_action(result) if 'result' in locals() else None
    result = st.session_state.get("last_result")
    if not result:
        st.warning("Please run analysis first")
    else:
        action = result.get("action")
        if action and action != "none":
            execute_action(action, selected)
            st.success(f"Executed: {action}")
        else:
            st.warning("No safe action found")

# Auto Refresh
if st.sidebar.button("🔄 Refresh"):
    st.rerun()