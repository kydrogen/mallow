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
		}
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
			border: 2px solid #cccccc !important;
			padding: 12px !important;
			border-radius: 6px !important;
			background-color: #bba694 !important;
			color: #000000 !important;
		}
		/* JSON component styling */
		[data-testid="stJson"] .react-json-view {
			background-color: #bba694 !important;
		}
		/* Expander styling to avoid flashing black */
		[data-testid="stExpander"] {
			background-color: #bba694 !important;
			border: 0 !important;
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
			padding: 16px;
			margin-bottom: 12px;
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
			padding: 12px 16px;
			color: #000000;
			margin-top: 0.75rem;
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
			margin-bottom: 0.25rem;
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
# UI: AGENT SECTION
# ============================================================================
st.markdown('<h2 class="ai-prototype-title">AI prototype</h2>', unsafe_allow_html=True)
st.header("Agent Interaction")

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

st.markdown("---")

# ============================================================================
# UI: ARTIFACTS SECTION
# ============================================================================
st.header("Artifacts Data Repository")

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
			details_block = f"""
			<div class=\"artifact-details\">
				<details>
					<summary>Details</summary>
					<div class=\"artifact-description\">{description_html}</div>
					{metadata_html}
				</details>
			</div>
			"""

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
