import asyncio
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
Tell me more details about the whispering crescent artifact.
"""

agent = Agent(
    name="Archeologist Agent",
    instructions="You are a helpful agent.",
    tools=[get_artifact_details]
)

def run_agent() -> str:
    try:
        result = asyncio.run(Runner.run(agent, input=SYSTEM_PROMPT))
        return getattr(result, "final_output", str(result))
    except Exception as e:
        return f"Agent execution failed: {e}"
