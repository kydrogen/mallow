import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool

load_dotenv()


@function_tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is snowing."


@function_tool
def get_artifact_details(artifact_name: str) -> str:
    return """
        Name: The Whispering Crescent
        Appearance:

        The Whispering Crescent is a longbow of ethereal beauty, seemingly carved from moonlight itself. Its limbs are forged from pale silverwood that glows faintly under the night sky, veined with lines of sapphire light that pulse like a heartbeat. The bowstring is spun from the hair of a fallen star — thin as spider silk, yet impossibly strong. When drawn, faint whispers echo from the air around it, as though spirits or memories are stirred by the tension.
        The tips of the bow curl inward like crescent moons, and when an arrow is nocked, faint runes along the limbs ignite, tracing constellations in pale blue fire. The weapon feels both ancient and alive, resonating with the will of its bearer.
    """


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