from dotenv import load_dotenv 
import asyncio
from datetime import datetime
import html
import json
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
			# Add artifact with timestamp
			artifact_with_timestamp = artifact.copy()
			artifact_with_timestamp['discovered_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			st.session_state['string_list'].append(artifact_with_timestamp)
		persist_list(st.session_state['string_list'])
	return toggle


class BorderedOutputProxy:
	"""Proxy to wrap agent output in styled HTML div."""
	def __init__(self, delta):
		self._delta = delta

	def markdown(self, text, unsafe_allow_html=False, **kwargs):
		# Escape HTML to maintain safety, then preserve newlines for readability
		html_content = html.escape(text).replace("\n", "<br>")
		scroll_script = """
		<script>
			window.scrollTo(0, document.body.scrollHeight);
		</script>
		"""
		wrapped = f'<div class="agent-output">{html_content}</div>{scroll_script}'
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
		/* Make centered layout wider */
		.block-container {
			max-width: 1000px !important;
			padding: 2rem 1rem !important;
			background-color: #cfbdae !important;
			overflow: visible !important;
		}
		/* Page background */
		.stApp, .reportview-container, .main {
			background-color: #cfbdae !important;
		}
		/* Remove white backgrounds from containers */
		[data-testid="stAppViewContainer"] {
			background-color: #cfbdae !important;
			overflow: visible !important;
		}
		[data-testid="stHeader"] {
			background-color: #cfbdae !important;
		}
		section[data-testid="stSidebar"] {
			background-color: #cfbdae !important;
		}
		/* Fix scrollbar styling - single scrollbar only */
		html {
			scrollbar-color: #bba694 #cfbdae;
			scrollbar-width: thin;
		}
		body {
			overflow-y: scroll !important;
			overflow-x: hidden !important;
		}
		/* Prevent nested scrolling */
		.stApp {
			overflow: visible !important;
		}
		.stMainBlockContainer {
			overflow: visible !important;
		}
		::-webkit-scrollbar {
			width: 12px;
			height: 12px;
		}
		::-webkit-scrollbar-track {
			background: #cfbdae;
		}
		::-webkit-scrollbar-thumb {
			background: #bba694;
			border-radius: 6px;
		}
		::-webkit-scrollbar-thumb:hover {
			background: #a89683;
		}
		/* Prevent webkit scrollbars on children */
		.block-container ::-webkit-scrollbar {
			display: none;
		}
		/* Streamlit element spacing */
		[data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] {
			margin-bottom: 3rem !important;
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
			border: 2px solid #cccccc !important;
			padding: 12px !important;
			border-radius: 6px !important;
			background-color: #bba694 !important;
			color: #000000 !important;
			margin: 1.5rem 0 !important;
		}
		/* JSON component styling */
		[data-testid="stJson"] .react-json-view {
			background-color: #bba694 !important;
		}
		/* Expander styling to avoid flashing black */
		[data-testid="stExpander"] {
			background-color: #bba694 !important;
			border: 0 !important;
			margin: 1rem 0 !important;
		}
		[data-testid="stExpander"] button {
			background-color: #bba694 !important;
			color: #000000 !important;
		}
		[data-testid="stExpander"] div {
			background-color: #bba694 !important;
		}
		/* Artifact card styling */
		.artifact-card {
			background-color: #bba694;
			border: 2px solid #8c7862;
			border-radius: 8px;
			padding: 20px;
			margin-bottom: 1.5rem;
			margin-top: 1rem;
			box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
			color: #000000;
		}
		.artifact-card * {
			color: #000000 !important;
		}
		.artifact-card p {
			margin: 0.25rem 0;
		}
		.info-card {
			background-color: #bba694;
			border: 2px solid #8c7862;
			border-radius: 8px;
			padding: 16px 20px;
			color: #000000;
			margin-top: 1rem;
			margin-bottom: 1.5rem;
		}
		.artifact-title {
			font-size: 1rem;
		}
		.artifact-details details {
			margin-top: 0.75rem;
			background-color: #bba694;
			border: 1px solid #8c7862;
			border-radius: 6px;
			padding: 0.5rem 0.75rem;
		}
		.artifact-details summary {
			font-weight: 600;
			cursor: pointer;
			list-style: none;
		}
		.artifact-details summary::-webkit-details-marker {
			display: none;
		}
		.artifact-details summary::after {
			content: "▸";
			float: right;
			transition: transform 0.2s ease;
		}
		.artifact-details details[open] summary::after {
			transform: rotate(90deg);
		}
		.artifact-description {
			margin-top: 0.5rem;
		}
		.artifact-metadata-block {
			margin-top: 0.75rem;
			border-top: 1px solid #8c7862;
			padding-top: 0.5rem;
		}
		.artifact-metadata-title {
			font-weight: 600;
			margin-bottom: 0.25rem;
		}
		.artifact-metadata-block pre {
			background: none;
			border: none;
			margin: 0;
		}
		.ai-prototype-title {
			text-align: center;
			font-size: 2.7rem;
			font-weight: 700;
			margin-bottom: 1rem;
			margin-top: 0;
		}
		/* Section spacing */
		.section-header {
			margin-top: 3rem !important;
			margin-bottom: 1.5rem !important;
		}
		/* Agent section container */
		.agent-section {
			margin-bottom: 3.5rem !important;
		}
		/* Button row spacing */
		.artifact-buttons-row {
			margin-bottom: 2rem !important;
		}
		/* Instructions panel styling */
		.instructions-panel {
			background-color: #bba694 !important;
			padding: 20px !important;
			border-radius: 8px !important;
			border: 2px solid #8c7862 !important;
			margin-bottom: 3rem !important;
		}
		/* How to use button - top right corner */
		.how-to-use-btn {
			position: fixed;
			top: 120px;
			right: 20px;
			background-color: #bba694 !important;
			color: #000000 !important;
			border: 2px solid #8c7862;
			border-radius: 6px;
			padding: 8px 16px;
			font-weight: 600;
			cursor: pointer;
			z-index: 1000;
		}
		.how-to-use-btn:hover {
			background-color: #a89683 !important;
		}
		/* Hide default form submit hint and replace with custom text */
		form small {
			display: none !important;
		}
		form::after {
			content: "Press Enter to ask the agent a question!";
			display: block;
			font-size: 0.75rem;
			color: #666;
			margin-top: 0.5rem;
			text-align: right;
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

if 'show_instructions' not in st.session_state:
	st.session_state['show_instructions'] = False

# ============================================================================
# UI: HOW TO USE BUTTON
# ============================================================================
st.markdown('<div style="height: 2rem;"></div>', unsafe_allow_html=True)
col1, col2 = st.columns([0.85, 0.15])
with col2:
	if st.button("How To Use", use_container_width=True, key="how_to_use_btn"):
		st.session_state['show_instructions'] = not st.session_state['show_instructions']

# Display instructions panel if button is clicked
if st.session_state['show_instructions']:
	st.markdown("""
	<div class="instructions-panel">
	
	### How to Use
	
	**How to use our app!**
	
	1. **Add Artifacts**: Click the artifact buttons (Laufen Lens, Hohenfeld Basalt Slab, Altbrunn Prism) to add them to the data repository below. You can also click the button again to remove an artifact. The data repository is the box under the 3 buttons.
	
	2. **View Database**: The artifacts you add will appear in the database section. It will show the name of the discovered artifact, the date discovered, and a short description of the artifact. You can click on the "Details" section to see more about the artifact.
	
	3. **Ask Questions**: Type a question in the text box and click "Send" to ask the agent about the artifacts. (The AI agent can only answer questions regarding the 3 artifacts given)
	
	4. **Agent Responses**: To ask the agent another question, delete the question you asked originally, then type another question for the agent to answer!
	</div>
	""", unsafe_allow_html=True)

# ============================================================================
# UI: AGENT SECTION
# ============================================================================
st.markdown('<h2 class="ai-prototype-title">AI prototype</h2>', unsafe_allow_html=True)
st.markdown('<h2 class="section-header">Agent Interaction</h2>', unsafe_allow_html=True)

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

st.markdown('<div style="margin-bottom: 3.5rem;"></div>', unsafe_allow_html=True)

# ============================================================================
# UI: ARTIFACTS SECTION
# ============================================================================
st.markdown('<h2 class="section-header">Artifacts Data Repository</h2>', unsafe_allow_html=True)

# Quick-add buttons for predefined artifacts (evenly spaced)
col1, col2, col3 = st.columns(3)
for col, art in zip([col1, col2, col3], PREDEFINED_ARTIFACTS):
	col.button(art['name'], on_click=make_toggle(art), use_container_width=True)

# Display artifact database
st.subheader("Database of Artifacts at Site")
artifact_list = st.session_state['string_list']

if not artifact_list:
	st.markdown(
		'<div class="info-card">No artifacts added yet. Use the quick-add buttons above to populate the repository.</div>',
		unsafe_allow_html=True,
	)
else:
	with st.container():
		for idx, artifact in enumerate(artifact_list, start=1):
			if not isinstance(artifact, dict):
				st.warning(f"Entry {idx} is not formatted correctly and was skipped.")
				continue

			name = artifact.get('name', 'Unnamed Artifact')
			discovered = artifact.get('discovered_date', 'Date unknown')
			details = artifact.get('details') or {}
			description = details.get('description') or artifact.get('description') or "No description provided."
			summary = details.get('summary')
			location = details.get('location')
			metadata = artifact.get('metadata', {})

			title_html = html.escape(f"{idx}. {name}")
			discovered_html = html.escape(discovered)
			location_html = f"<p><em>Location:</em> {html.escape(location)}</p>" if location else ""
			summary_html = ""
			if summary:
				summary_with_ellipsis = summary.rstrip().rstrip('.') + '...'
				summary_html = f"<p class=\"artifact-summary\"><em>{html.escape(summary_with_ellipsis)}</em></p>"
			description_html = html.escape(description).replace("\n", "<br>")
			metadata_html = ""
			if metadata:
				pretty_metadata = html.escape(json.dumps(metadata, indent=2))
				metadata_html = f"""
				<div class=\"artifact-metadata-block\">
					<div class=\"artifact-metadata-title\">Metadata</div>
					<pre>{pretty_metadata}</pre>
				</div>
				"""
			details_block = f"""<details style="background-color: #bba694; border: 1px solid #8c7862; border-radius: 6px; padding: 0.75rem; margin-top: 0.75rem;"><summary style="font-weight: 600; cursor: pointer; list-style: none;">▶ Details</summary><div style="margin-top: 0.5rem;">{description_html}</div>{metadata_html}</details>"""

			card_html = f"""
			<div class=\"artifact-card\">
				<p class=\"artifact-title\"><strong>{title_html}</strong></p>
				<p><em>Discovered:</em> {discovered_html}</p>
				{location_html}
				{summary_html}
				{details_block}
			</div>
			"""

			st.markdown(card_html, unsafe_allow_html=True)
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
