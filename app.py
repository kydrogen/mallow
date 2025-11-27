from dotenv import load_dotenv 
import asyncio
import streamlit as st

from agent import run_agent
from tools import (
	PREDEFINED_ARTIFACTS,
	load_persisted_list,
	persist_list
)

# ============================================================================
# CONFIGURATION
# ============================================================================
load_dotenv()
st.set_page_config(page_title="Archeologist Agent", layout="centered")


# ============================================================================
# HELPER FUNCTIONS & CLASSES
# ============================================================================
def make_toggle(artifact):
	"""Create a toggle callback for adding/removing artifacts."""
	def toggle():
		lst = st.session_state.get('string_list', [])
		if not isinstance(lst, list):
			lst = []
		exists = any(isinstance(it, dict) and it.get('name') == artifact['name'] for it in lst)
		if exists:
			st.session_state['string_list'] = [it for it in lst if not (isinstance(it, dict) and it.get('name') == artifact['name'])]
		else:
			st.session_state['string_list'].append(artifact)
		persist_list(st.session_state['string_list'])
	return toggle


def format_artifact_display():
	"""Format artifact list for display (first two lines only)."""
	lines = []
	for idx, a in enumerate(st.session_state['string_list'], start=1):
		if isinstance(a, dict):
			name = a.get('name', '')
			desc = a.get('description', '')
			lines.append(f"{idx}. {name}")
			if desc:
				desc_lines = desc.splitlines()
				if desc_lines:
					lines.append(desc_lines[0])
					if len(desc_lines) > 1:
						lines.append(desc_lines[1])
			lines.append("---")
		else:
			lines.append(f"{idx}. {str(a)}")
	return "\n".join(lines)


class BorderedOutputProxy:
	"""Proxy to wrap agent output in styled HTML div."""
	def __init__(self, delta):
		self._delta = delta

	def markdown(self, text, unsafe_allow_html=False, **kwargs):
		wrapped = f'<div class="agent-output">{text}</div>'
		return self._delta.markdown(wrapped, unsafe_allow_html=True, **kwargs)

	def write(self, *args, **kwargs):
		content = " ".join(str(a) for a in args)
		return self.markdown(content, **kwargs)

	def empty(self):
		return self._delta.empty()


def run_agent_callback(question, output_container):
	"""Run the agent and display output in Streamlit."""
	if question and question.strip():
		st.session_state['agent_output'] = ""
		asyncio.run(run_agent(question, output_container))
	else:
		st.session_state['agent_output'] = "Please enter a question before sending."


# ============================================================================
# STYLING
# ============================================================================
st.markdown(
	"""
	<style>
		/* Page background */
		.stApp, .reportview-container, .main {
			background-color: #cfbdae !important;
			min-height: 200vh;
		}
		/* Make all text black */
		body, p, h1, h2, h3, h4, h5, h6, span, label,.stText {
			color: #000000 !important;
		}
		/* Make form controls clearly visible */
		input, textarea, button {
			color: #000000 !important;
			background-color: #bba694 !important;
		}
		/* Target Streamlit textarea with all classes */
		textarea.st-ae, textarea.st-bd, textarea.st-be, textarea.st-bf, textarea.st-bg,
		textarea[class*="st-"], .stTextArea textarea {
			color: #000000 !important;
		}
		/* Override Streamlit's default text fill color for disabled textareas */
		.st-bx {
			-webkit-text-fill-color: #000000 !important;
		}
		/* Agent output styling */
		.agent-output {
			border: 2px solid #000000 !important;
			padding: 12px !important;
			border-radius: 6px !important;
			background-color: #bba694 !important;
			color: #000000 !important;
		}
	</style>
	""",
	unsafe_allow_html=True,
)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================
if 'string_list' not in st.session_state:
	st.session_state['string_list'] = load_persisted_list()

# ============================================================================
# UI: ARTIFACTS SECTION
# ============================================================================
st.title("Artifacts found at site")

# Quick-add buttons for predefined artifacts
cols = st.columns(3)
for i, art in enumerate(PREDEFINED_ARTIFACTS):
	cols[i].button(art['name'], on_click=make_toggle(art))

# Display artifact database
st.text_area("Database of known artifacts", value=format_artifact_display(), height=240, disabled=True)

# ============================================================================
# UI: AGENT SECTION
# ============================================================================
st.markdown("---")
st.header("Agent")

# Agent input form
with st.form(key="agent_form", clear_on_submit=False):
	col1, col2 = st.columns([4, 1], vertical_alignment="bottom")
	
	with col1:
		user_question = st.text_input(
			"Ask the agent:", 
			placeholder="Type your question here...", 
			key="agent_question_input"
		)
	
	with col2:
		send_clicked = st.form_submit_button("Send", use_container_width=True)

# Agent output container
_raw_output = st.empty()
output_container = BorderedOutputProxy(_raw_output)

# ============================================================================
# LOGIC: AGENT EXECUTION
# ============================================================================
# Handle form submission
if send_clicked:
	question = st.session_state.get('agent_question_input', '').strip()
	if question:
		st.session_state['agent_request'] = question
		st.session_state['should_run_agent'] = True

# Run agent if triggered
if st.session_state.get('should_run_agent'):
	st.session_state['should_run_agent'] = False
	user_question = st.session_state.get('agent_request', '')
	if user_question:
		run_agent_callback(user_question, output_container)
