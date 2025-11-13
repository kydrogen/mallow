import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool

load_dotenv()


@function_tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is snowing."


@function_tool
def get_artifact_details(artifact_name: str) -> str:
    """Return the raw contents of `data/string_list.json` (as text).

    If the file does not exist or cannot be read, return an empty string.
    """
    from pathlib import Path

    data_file = Path(__file__).parent / "data" / "string_list.json"
    if not data_file.exists():
        return ""

    try:
        return data_file.read_text(encoding="utf-8")
    except Exception:
        return ""


agent = Agent(
    name="Archeologist Agent",
    instructions="You are a helpful agent.",
    tools=[get_weather, get_artifact_details],
)



async def main():

    result = await Runner.run(agent, input="Tell me more details about the whispering crescent artifact.")
    print(result.final_output)
    # The weather in Tokyo is sunny.


if __name__ == "__main__":
    asyncio.run(main())