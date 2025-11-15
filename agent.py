import asyncio
import os
from pathlib import Path
from agents import Agent, Runner, function_tool


# Path to the persisted artifacts file (same location used by the Streamlit app)
DATA_FILE = Path(__file__).parent / "data" / "string_list.json"


@function_tool
def get_artifact_details(artifact_name: str) -> str:
    """Return the raw contents of the persisted `string_list.json` or empty string."""
    try:
        return DATA_FILE.read_text(encoding="utf-8") if DATA_FILE.exists() else ""
    except Exception:
        return ""

SYSTEM_PROMPT = """
You are an archeologist agent that can access a list of artifacts.





"""

agent = Agent(
    name="Archeologist Agent",
    instructions=SYSTEM_PROMPT,
    tools=[get_artifact_details]
)


def run_agent(question: str = None) -> str:
    """Run the agent. If `question` is provided it will be appended to the system prompt.
    If the environment variable `DEFAULT_AGENT_MODEL` is set it will be passed to the Runner
    as an attempt to select a specific model/client (tries `model` then `client`).
    """
    try:
        result = asyncio.run(Runner.run(agent, input=question))
        return getattr(result, "final_output", str(result))
    except Exception as e:
        return f"Agent execution failed: {e}"
