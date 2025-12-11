# main.py
"""
Main runner. Uses AutoGen GroupChat/Manager if available, otherwise runs a manual
sequential pipeline between Reporter and Editor.

Run:
    python main.py
"""

import time
from typing import Optional

# Import agents and tool
from agents import ReporterAgent, EditorAgent
from tools import fetch_live_data, USING_AUTOGEN_TOOL

# Attempt to use AutoGen orchestration (GroupChat/GroupChatManager). If not available,
# fall back to a simple sequential pipeline.
USE_AUTOGEN_MANAGER = False
try:
    from autogen import GroupChat, GroupChatManager  # type: ignore
    USE_AUTOGEN_MANAGER = True
except Exception:
    USE_AUTOGEN_MANAGER = False


def run_with_autogen(topic: str) -> str:
    """
    When AutoGen is installed and available this will create two AssistantAgents
    (Reporter and Editor), send a task, and let the GroupChatManager handle turns.
    Note: actual AutoGen behaviour depends on the installed version.
    """
    # create agents
    reporter = ReporterAgent(name="Reporter")
    editor = EditorAgent(name="Editor")

    # Create GroupChat expecting the manager to route messages sequentially.
    # The exact constructor may differ per autogen version; this is a common pattern.
    chat = GroupChat(
        agents=[reporter, editor],
        messages=[],
        max_round=3,
    )

    manager = GroupChatManager(groupchat=chat)

    # Instruction: ask reporter to fetch then ask editor to summarize.
    prompt = (
        "Task: 1) Reporter: fetch live data for the topic provided using the registered tool "
        "fetch_live_data(topic). 2) Editor: when reporter finishes, summarize and produce a "
        "short newsletter intro (approx. 2-3 sentences). Topic: " + topic
    )

    print("Starting AutoGen GroupChat run...")
    result = manager.run(prompt)
    return result


def run_sequential_pipeline(topic: str) -> str:
    """
    Simple sequential pipeline (fallback when AutoGen not present).
    Reporter -> Editor. Returns a combined log string.
    """

    # initialize reporter with tool
    reporter = ReporterAgent(name="Reporter", tool=fetch_live_data)
    editor = EditorAgent(name="Editor")

    # Run pipeline
    log_lines = []
    log_lines.append("=== RUN LOG START ===")
    t0 = time.strftime("%Y-%m-%d %H:%M:%S")
    log_lines.append(f"Run start: {t0}")

    reporter_out = reporter.handle_input(topic)
    log_lines.append(f"Reporter Output: {reporter_out}")

    editor_out = editor.handle_input(reporter_out)
    log_lines.append(f"Editor Output: {editor_out}")

    t1 = time.strftime("%Y-%m-%d %H:%M:%S")
    log_lines.append(f"Run end: {t1}")
    log_lines.append("=== RUN LOG END ===")

    return "\n".join(log_lines)


def main(topic: Optional[str] = None):
    if topic is None:
        topic = "AI Stock Trends"

    print(f"Topic: {topic}\n")

    if USE_AUTOGEN_MANAGER and USING_AUTOGEN_TOOL:
        try:
            output = run_with_autogen(topic)
            print(output)
            return
        except Exception as e:
            print("AutoGen orchestration failed or API mismatch:", e)
            print("Falling back to sequential pipeline...\n")

    # Fallback
    output = run_sequential_pipeline(topic)
    print(output)


if __name__ == "__main__":
    main()
