# agents.py

"""
Unified Agents Implementation:
- If AutoGen is available → agents extend AssistantAgent but STILL accept tool argument safely.
- If AutoGen not available → normal Python agent functionality is used.
"""

from typing import Any

# Try AutoGen
try:
    from autogen import AssistantAgent  # type: ignore

    class ReporterAgent(AssistantAgent):
        def __init__(self, name: str = "Reporter", tool: Any = None):
            # store tool (even if AutoGen doesn't use it directly)
            super().__init__(name=name)
            self.tool = tool

        def handle_input(self, topic: str) -> str:
            # Tool-based fetch (fallback: when AutoGen manager is NOT running)
            if callable(self.tool):
                data = self.tool(topic)
                return f"{self.name} fetched: {data}"
            return f"{self.name} received topic '{topic}' (AutoGen mode)"

    class EditorAgent(AssistantAgent):
        def __init__(self, name: str = "Editor"):
            super().__init__(name=name)

        def handle_input(self, reporter_output: str) -> str:
            try:
                content = reporter_output.split(":", 1)[1].strip()
            except:
                content = reporter_output

            return (
                f"{self.name} summary: Based on the report → \"{content}\" — "
                f"final intro: 'Recent signals indicate positive momentum.'"
            )

except Exception:
    # Pure Python fallback (no AutoGen installed)
    class ReporterAgent:
        def __init__(self, name: str = "Reporter", tool: Any = None):
            self.name = name
            self.tool = tool

        def handle_input(self, topic: str) -> str:
            if callable(self.tool):
                data = self.tool(topic)
            else:
                data = f"(no tool) simulated data for {topic}"
            return f"{self.name} fetched: {data}"

    class EditorAgent:
        def __init__(self, name: str = "Editor"):
            self.name = name

        def handle_input(self, reporter_output: str) -> str:
            try:
                content = reporter_output.split(":", 1)[1].strip()
            except:
                content = reporter_output

            return (
                f"{self.name} summary: Based on the report → \"{content}\" — "
                f"final intro: 'Recent signals indicate positive momentum.'"
            )
