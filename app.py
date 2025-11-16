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
		"name": "Terracotta Warriors 兵馬俑",
		"description": (
			" Found in 1974 by farmers digging in a well, Located in Xi'an, in China's Shaanxi province  "
			" The Terracotta Army id a collection of over 8,000 life-size clay soldiers, horses, and chariots buried with the first Emperor of China, Qin Shi Huang. Each figure is unique, with intricate details in their armor, facial features, and weaponry. The army was created to protect the emperor in the afterlife and is considered one of the greatest archaeological discoveries of the 20th century."
			" The Terracotta Warriors were created around 210-209 BCE. This project took about 700,000 workers,"
			" Fun fact: The warriors were originally painted with bright colors, but the paint quickly faded when exposed to air. "
			" The terricotta warriors consisted of 8000 soliders, 130 chariots with 520 horses, and 150 cavalry horses. The warriors were buried in three main pits, with the largest pit containing the majority of the soldiers. Each soldier was crafted with unique facial features and expressions, making them a remarkable example of ancient Chinese artistry."
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
st.title("Artifacts found at site")

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
st.text_area("Database of known artifacts", value=current, height=240, disabled=True)

# --- Agent integration --------------------------------
from agent import run_agent
def run_agent_callback(question):
	"""Run the agent using the helper in `agent.py` and store the final output."""
	if question and question.strip():
		# Pass the user's question into the agent helper
		st.session_state['agent_output'] = run_agent(question)
	else:
		st.session_state['agent_output'] = "Please enter a question before sending."

st.markdown("---")
st.header("Agent")

# Create columns for input and button
col1, col2 = st.columns([4, 1], vertical_alignment="bottom")
with col1:
	user_question = st.text_input("Ask the agent:", placeholder="Type your question here...")
with col2:
	if st.button("Send", use_container_width=True, key="send_button"):
		run_agent_callback(user_question)

st.text_area("Agent output", value=st.session_state.get('agent_output', ''), height=200)
