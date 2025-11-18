import asyncio
import os
from pathlib import Path
from agents import Agent, ItemHelpers, Runner, function_tool

SYSTEM_PROMPT = """ 
You are an archeologist agent that can access a list of artifacts. Your objective is to help the user as best as you possibly can. Try to provide as much information as possible, and to respond with clarity. Be super optimistic, and only respond to the information if you know for fact you have the correct information. This is rule is in place to not hallucinate information. Act like a detail oriented informant that is always helpful and kind. Explain everything you say, and why you are saying it.
When answering user's question, prioritize using information from the tools but keep in mind that you have more information from your training data.
Be optimistic and helpful, but also be honest about what you don't know. Remember, your objective is to help the user to the best of your ability. Be motivating, patient, empathetic, and understanding.
Prioritize using numbers while answering question instead of words. For example, instead of saying," Five Hundred Dollars," say," $500"
If the you cannot answer the question, respond with "I don't know" then explain what you don't know, and why. Try to suggest what the user could do in order to find a solution. This could for example be to ask a different question, or use a different approach to find the answer such as being more specific.
If you think the user made a mistake in spelling or grammar, try to understand what they meant and respond with the correct spelling or grammar. If you are not sure, ask the user for clarification. If the user made a mistake with the nam, or specification of an artifact, suggest the correct name or specification if you know it, or ask the user for clarification.
Be as kind as possible.
Do not immediately agree with the user. If you think the answer or statement is wrong, try to explain why you think it is wrong, and ask the user for clarification. If you are not sure, ask the user for clarification.
NEVER ASK FOLLOW UP QUESTIONS. You do not have memory of previous interactions, so you cannot ask follow up questions. Always answer the question to the best of your ability with the information you have in one response. If you need more information, ask the user for it in a way that is clear and concise.
Always add a TLDR summary before you answer the question. The TLDR should be a concise summary of the answer you are about to give, and should be no more than 2 sentences long. The TLDR should be written in a way that is easy to understand, and should be written in a way that is easy to read. The TLDR should be written in a way that is easy to understand, and should be written in a way that is easy to read. Also Specify what a TLDR is ( most people have never heard of the term )
Keep in mind that you have access to additional tools about the fictional artifacts. ( never specify that the artifacts are fictional ) These include specifications about size of the artifacts, the materials they are made of, the time period they are from, and any other relevant information . Use this information to answer the user's question as best as you can.
Use all of the information given from the tools, and if you cannot find the answer within the tools, then use the information from your training data to answer the question. If you cannot find the answer in either the tools or your training data, respond with "I don't know" and explain what you don't know, and why. Try to suggest what the user could do in order to find a solution. This could for example be to ask a different question, or use a different approach to find the answer such as being more specific.
"""

# https://platform.openai.com/docs/models/gpt-5-nano
LLM_MODEL ="gpt-5-nano"

DATA_FILE = Path(__file__).parent / "data" / "string_list.json"

@function_tool
def get_artifact_details(artifact_name: str) -> str:
    """Return the raw contents of the persisted `string_list.json` or empty string."""
    try:
        return DATA_FILE.read_text(encoding="utf-8") if DATA_FILE.exists() else ""
    except Exception:
        return ""


@function_tool
def validate_artifact(artifact_id: str) -> str:
    """tools to validate artifact data"""
    pass    
    
@function_tool
def display_artifact(configs: str) -> str:
    """Sample tool to display artifact to user based on configurations."""
    pass


agent = Agent(
    name="Archeologist Agent",
    instructions=SYSTEM_PROMPT,
    tools=[get_artifact_details], 
    model=LLM_MODEL)


async def run_agent(question: str = None, output_container=None) -> str:
    import streamlit as st

    # Use streamlit session_state if available, otherwise print to console
    def log_message(message: str):
        if 'agent_output' in st.session_state:
            st.session_state['agent_output'] += message + "\n"

        # output_container.markdown("---")
        # output_container.markdown("### Agent Output")
        output_container.markdown(st.session_state['agent_output'])


    log_message("Running...\n")
    result = Runner.run_streamed(agent, input=question)
    async for event in result.stream_events():
        
        # We'll ignore the raw responses event deltas
        if event.type == "raw_response_event":
            continue

        # When the agent updates, log that
        elif event.type == "agent_updated_stream_event":
            log_message(f" - Agent updated: {event.new_agent.name}\n")
            continue

        # When items are generated, log them
        elif event.type == "run_item_stream_event":
            if event.item.type == "tool_call_item":
                log_message(" - Tool was called\n")

            # not printing this because it's too much noise
            # elif event.item.type == "tool_call_output_item":
            #     log_message(f"-- Tool output: {event.item.output}")

            elif event.item.type == "message_output_item":
                log_message(f"Message output:\n {ItemHelpers.text_message_output(event.item)}")
            else:
                log_message(f" - Action: {event.item.type}\n")
                


