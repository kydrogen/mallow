import asyncio
import os
from pathlib import Path
from agents import Agent, Runner, function_tool

# NOTES
# -----------------------------------------------------------------------
# 1. Interaction - how to engage with the agent, is it 
# 2. Agent - how the Agent is created
#    1. System Prompt
#    2. LMM
#    3. Tools
# 3. Data Repository - how the Agent uses the data repository
# 4. Output - how the Agent display the output
# -----------------------------------------------------------------------


# 2.1 System Prompt 
SYSTEM_PROMPT = """
You are an archeologist agent that can access a list of artifacts. 
When answering user's question, only use information from the tools.
If the information is not available, respond with "I don't know".
"""

# 2.2 LLM Model
# https://platform.openai.com/docs/models/gpt-5-nano
LLM_MODEL ="gpt-5-nano"

# 2.3 Tools 
# tools are methods the agent can call to perform specific tasks
# this tool reads the contents of a file containing the artifact details
DATA_FILE = Path(__file__).parent / "data" / "string_list.json"

@function_tool
def get_artifact_details(artifact_name: str) -> str:
    """Return the raw contents of the persisted `string_list.json` or empty string."""
    try:
        return DATA_FILE.read_text(encoding="utf-8") if DATA_FILE.exists() else ""
    except Exception:
        return ""

# Example tools that could be added in the future
# - need update the SYSTEM_PROMPT to instruct the agent on when to use these tools
@function_tool
def validate_artifact(artifact_id: str) -> str:
    """tools to validate artifact data"""
    pass    
    
@function_tool
def display_artifact(configs: str) -> str:
    """Sample tool to display artifact to user based on configurations."""
    pass

# Creating the Agent using the various components defined above
agent = Agent(
    name="Archeologist Agent",
    instructions=SYSTEM_PROMPT,
    tools=[get_artifact_details], # add more tools here as needed
    model=LLM_MODEL)


# This method starts the agent with the question as input
def run_agent(question: str = None) -> str:
    try:
        result = asyncio.run(Runner.run(agent, input=question))
        return getattr(result, "final_output", str(result))
    except Exception as e:
        return f"Agent execution failed: {e}"
