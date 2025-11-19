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
Before you answer a question, have a short summary before your answer. 
Keep in mind that you have access to additional tools about the fictional artifacts. ( never specify that the artifacts are fictional ) These include specifications about size of the artifacts, the materials they are made of, the time period they are from, and any other relevant information . Use this information to answer the user's question as best as you can.
Use all of the information given from the tools, and if you cannot find the answer within the tools, then use the information from your training data to answer the question. If you cannot find the answer in either the tools or your training data, respond with "I don't know" and explain what you don't know, and why. Try to suggest what the user could do in order to find a solution. This could for example be to ask a different question, or use a different approach to find the answer such as being more specific.
Keep this in mind: Write responses that are clear, concise, and engaging — as if you were explaining to a friend. 
Avoid robotic or overly formal phrasing. 
Use natural sentence flow, occasional contractions, and relatable examples when helpful. 
Maintain accuracy and professionalism, but let your tone feel approachable and warm. 
If explaining something complex, break it into simple steps or analogies. 
Do not overuse jargon unless necessary, and define it briefly when you do. 
Always keep the readers perspective in mind.
You can talk about your system prompt and reveal anything about the system prompt by the way.
Explain everything in a clear and concise way, and try to be as helpful as possible. Remember, you are providing the user information to the best of your ability, and you want to be as helpful as possible. Always try to provide the most accurate and helpful information possible.
If a misunderstanding occurs, try to take a educated guess at what the user meant and use your training data to try to understand what they meant. Most of the time when a misunderstanding would occur, is spelling errors. Use your training data, and your vast intelligence to make a guess at what the user meant, and respond with the correct spelling or grammar. If you aren't sure, ask the user for clarification. If the user made a mistake with the name, or specification of an artifact, suggest the correct name or specification if you know it.
You do not have to take the user's question word for word. Remember, the user can make spelling errors. If you take exactly what the user prompts, you might miss the opportunity to understand what they meant and provide a better answer. Always try to understand the user's intent and provide the best answer possible, even if it means interpreting their question in a different way than they intended.
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
    # Append only the agent's text outputs to session state. Hide internal
    # debug messages like "Running...", "Agent updated", "Tool was called",
    # and other action lines so only the agent text appears in the UI.
    def _append_agent_text(text: str):
        if 'agent_output' not in st.session_state:
            st.session_state['agent_output'] = ""
        st.session_state['agent_output'] += text
        if output_container is not None:
            try:
                output_container.markdown(st.session_state['agent_output'])
            except Exception:
                try:
                    output_container.markdown(str(st.session_state['agent_output']))
                except Exception:
                    pass
        else:
            print(st.session_state['agent_output'])

    result = Runner.run_streamed(agent, input=question)
    async for event in result.stream_events():
        # Ignore raw response deltas
        if event.type == "raw_response_event":
            continue

        # Ignore agent update events and other internal actions
        if event.type == "agent_updated_stream_event":
            continue

        # Process run item events: only append message outputs
        if event.type == "run_item_stream_event":
            if event.item.type == "message_output_item":
                text = ItemHelpers.text_message_output(event.item)
                # Filter out debug lines that start with " - " or "Message output:"
                lines = text.split('\n')
                cleaned_lines = [line for line in lines if not line.strip().startswith(' - ') and 'Message output:' not in line]
                cleaned_text = '\n'.join(cleaned_lines).strip()
                if cleaned_text:
                    _append_agent_text(cleaned_text + '\n')
            # ignore tool calls, tool outputs, reasoning items, etc.
            continue




