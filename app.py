import json
import os
from pathlib import Path
from dotenv import load_dotenv 

import streamlit as st

load_dotenv()
st.set_page_config(page_title="String List Manager")

# File used to persist the list so other processes (like agent.py) can read it
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)
DATA_FILE = DATA_DIR / "string_list.json"


def load_persisted_list():
	if DATA_FILE.exists():
		try:
			data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
			# Backwards-compat: if file contains a list of strings, convert to objects
			if isinstance(data, list) and data and isinstance(data[0], str):
				converted = []
				for s in data:
					name = s.splitlines()[0] if s else ""
					converted.append({"name": name, "description": s})
				# persist normalized structure
				try:
					DATA_FILE.write_text(json.dumps(converted, ensure_ascii=False, indent=2), encoding="utf-8")
				except Exception:
					pass
				return converted
			return data
		except Exception:
			return []
	return []


def persist_list(lst):
	try:
		DATA_FILE.write_text(json.dumps(lst, ensure_ascii=False, indent=2), encoding="utf-8")
	except Exception:
		# best-effort persistence; Streamlit UI shouldn't break if disk write fails
		pass


if 'string_list' not in st.session_state:
	st.session_state['string_list'] = load_persisted_list()




# Predefined artifacts for quick add/remove
PREDEFINED_ARTIFACTS = [
	{
		"name": "The Whispering Crescent",
		"description": (
			"The Whispering Crescent is a longbow of ethereal beauty, seemingly carved from moonlight itself. "
			"Its limbs are forged from pale silverwood that glows faintly under the night sky, veined with lines "
			"of sapphire light that pulse like a heartbeat. The bowstring is spun from the hair of a fallen star — "
			"thin as spider silk, yet impossibly strong. When drawn, faint whispers echo from the air around it, "
			"as though spirits or memories are stirred by the tension."
		),
	},
	{
		"name": "The Ember Chalice",
		"description": (
			"A goblet of blackened iron that never cools. Mithril filigree runs along its rim, and embers glow "
			"within as if a small hearth burns inside. Legends say a draught from the chalice heals.")
	},
	{
		"name": "The Silent Diadem",
		"description": (
			"A delicate circlet of woven silver and onyx. Wearing it grants clarity but muffles the wearer's voice, "
			"leaving a hush in crowded halls.")
	},
]


def make_toggle(artifact):
	def toggle():
		# Toggle presence by name
		lst = st.session_state.get('string_list', [])
		# normalize existing to list
		if not isinstance(lst, list):
			lst = []
		exists = any(isinstance(it, dict) and it.get('name') == artifact['name'] for it in lst)
		if exists:
			# remove matching
			st.session_state['string_list'] = [it for it in lst if not (isinstance(it, dict) and it.get('name') == artifact['name'])]
		else:
			st.session_state['string_list'].append(artifact)
		# persist
		persist_list(st.session_state['string_list'])
	return toggle



# UI Layout
st.title("String List Manager")
st.write("Use the buttons below to add or remove predefined artifacts.")

# Quick-add buttons for predefined artifacts (click to add; click again to remove)
cols = st.columns(3)
for i, art in enumerate(PREDEFINED_ARTIFACTS):
	cols[i].button(art['name'], on_click=make_toggle(art))

# Display the complete list in a read-only panel (formatted)
lines = []
for idx, a in enumerate(st.session_state['string_list'], start=1):
	if isinstance(a, dict):
		lines.append(f"{idx}. {a.get('name','')}")
		desc = a.get('description','')
		if desc:
			lines.append(desc)
		lines.append("---")
	else:
		# fallback for older string entries
		lines.append(f"{idx}. {str(a)}")

current = "\n".join(lines)
st.text_area("Current artifacts (read-only)", value=current, height=240, disabled=True)


# --- Embedded agent UI and tools -------------------------------------------------
import asyncio
from agents import Agent, Runner, function_tool


@function_tool
def get_weather(city: str) -> str:
	return f"The weather in {city} is snowing."


@function_tool
def get_artifact_details(artifact_name: str) -> str:
	"""Return the raw contents of the persisted `string_list.json` or empty string."""
	try:
		return DATA_FILE.read_text(encoding="utf-8") if DATA_FILE.exists() else ""
	except Exception:
		return ""


agent = Agent(
	name="Archeologist Agent",
	instructions="You are a helpful agent.",
	tools=[get_weather, get_artifact_details],
)



HARDCODED_PROMPT = "Tell me more details about the whispering crescent artifact."


def run_agent_callback():
	"""Run the agent with a hardcoded prompt and store the final output."""
	prompt = HARDCODED_PROMPT
	try:
		result = asyncio.run(Runner.run(agent, input=prompt))
		st.session_state['agent_output'] = getattr(result, 'final_output', str(result))
	except Exception as e:
		st.session_state['agent_output'] = f"Agent execution failed: {e}"


st.markdown("---")
st.header("Agent")
st.button("Run agent", on_click=run_agent_callback)
st.text_area("Agent output", value=st.session_state.get('agent_output', ''), height=200)


