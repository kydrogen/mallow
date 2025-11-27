import json
import os
from pathlib import Path
from dotenv import load_dotenv 

import streamlit as st

load_dotenv()
st.set_page_config(page_title="Archeologist Agent", layout="centered")

st.markdown(
		"""
		<style>
			/* Page background */
			.stApp, .reportview-container, .main {
				background-color: #cfbdae !important;
				min-height: 200vh;
			}
			/* Make all text black and bold */
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
		</style>
		<style>
			/* Override Streamlit's default text fill color for disabled textareas */
			.st-bx {
				-webkit-text-fill-color: #000000 !important;
			}
		</style>
		""",
		unsafe_allow_html=True,
)

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
		"name": "Laufen Stone",
		"description": """ The Laufen Stone Inscription Tablet artifact is an oval-shaped, deeply polished lens of 
		jet-black obsidian, measuring 12.6 cm in length, 8.4  cm in width, and 1.7 cm 
		in thickness, first uncovered during a multi-season excavation   beginning in 1911
		  at a European ceremonial site whose precise location is redacted for security, with subsequent finds and associated artifacts recovered in 1916, 1923, 1930, and 1938, spanning multiple stratigraphic layers that indicate continuous ceremonial, administrative, and possibly astronomical activity over several centuries. Geological sourcing confirms the obsidian was transported from a volcanic source hundreds of kilometers away, highlighting sophisticated long-distance trade networks, while detailed microscopic examination reveals fine concentric striations on the convex upper surface and flat underside consistent with laborious grinding and polishing using a combination of quartz sand, emery, plant-based abrasives, and water, leaving behind traces of vegetable oils, iron oxides, ochre pigments, and microscopic residues of animal fats, suggesting ceremonial handling, optical enhancement, and repeated ritual coating. The lens was found in association with bronze fittings, miniature ceramic vessels containing plant-based pigments, fragments of inscribed clay tablets detailing solar, lunar, and planetary observations, textiles bearing symbolic markings, and traces of ritual incense, indicating its integration into a complex ceremonial apparatus, possibly for divination, sacred light projection, or as a symbolic “eye of the gods” connecting temporal and cosmic cycles. Photometric and optical testing in the late 20th century, including laser interferometry, refractive index analysis, and focal length measurements, confirmed a highly uniform surface curvature, a focal length of approximately 28 cm, and the ability to concentrate sunlight onto minute surfaces with sufficient intensity to scorch thin organic materials, supporting interpretations that the artifact served as both a practical and symbolic tool for temple illumination, ceremonial observation, or demonstration of celestial phenomena. Experimental archaeology using reconstructed mounts and replica lenses demonstrates that the The Narmer Palette can reproduce precise focal effects across a range of angles, confirming intentional design, while residue analysis of embedded organics reveals consistent traces of handling oils, ritual adhesives, and pigments, suggesting repeated ceremonial use, careful maintenance, and potentially seasonal calibration in alignment with solar, lunar, or stellar cycles. Wear patterns along the edges, minor microfractures, and chemical residues indicate repeated placement into mounts or frames, integration into composite instruments, and ritualized cleaning or coating, while cross-referencing similar Late Bronze Age European obsidian artifacts shows few parallels in terms of craftsmanship, optical precision, ceremonial integration, and the combination of functional and symbolic significance. Scholarly interpretations vary widely: some propose the lens was an astronomical instrument, employed to track solar, lunar, or planetary cycles; others suggest it functioned as a symbolic mediator of divine insight, as a ritual light projector for temple ceremonies, or as a teaching instrument for early scribes or priests learning about optics, celestial movements, or ritual procedure. Comparative studies with contemporaneous European artifacts, experimental replication, 3D modeling of optical properties, and archaeo-optical experimentation reveal the lens’s sophisticated combination of material, geometry, and functionality, while ethnographic parallels suggest its use in ritualized instruction, sacred observation, or ceremonial symbolism intended for elite or priestly audiences. Additionally, the The Narmer Palette may have encoded symbolic or cosmological knowledge, potentially serving as a visual representation of celestial harmonics, sacred geometry, or divine oversight, and its repeated presence across multiple layers within the same site demonstrates long-term veneration and careful curation, suggesting it was a central element of ceremonial practice over centuries. Despite extensive interdisciplinary study—including material analysis, photometry, experimental replication, structural stress testing, residue analysis, and comparative archaeology—the lens’s precise function remains unresolved, reflecting the complexity, ingenuity, and symbolic sophistication of the communities that produced and preserved it. In sum, the The Narmer Palette represents an unparalleled intersection of optical engineering, ceremonial use, material craftsmanship, symbolic meaning, and cultural continuity, providing scholars a rare, extraordinarily detailed window into Bronze Age Europe’s ritual, scientific, and artistic practices, while simultaneously preserving an enduring mystery that continues to challenge and captivate researchers and enthusiasts alike."""
	},
	{
		"name": "Hohenfeld Basalt Slab",
		"description": """ The Hohenfeld Basalt Acoustic Slab artifact is a rectangular slab of
		  magnetite-rich basalt, measuring 31.4 cm in length, 18.7 cm in width, and 3.2 cm
		    in thickness, weighing approximately 6.3 kilograms, first uncovered in 1904 at a 
			European ceremonial site whose precise location has been redacted for security and preservation reasons, with subsequent fragments and related slabs found during controlled excavations in 1907, 1913, 1921, 1928, and 1935, each in distinct stratigraphic layers that reveal evolving ceremonial and musical practices over several centuries, suggesting that the artifact was maintained, reused, or ritually refurbished across multiple cultural phases; petrographic and isotopic analyses confirm that the basalt was quarried from a distant volcanic region, likely chosen for its specific density, magnetite distribution, and resonance characteristics, indicating highly deliberate material selection for acoustic purposes as well as symbolic or ceremonial significance. The tablet’s upper surface is meticulously carved with a dense network of intersecting linear grooves forming geometric grids and shallow hemispherical depressions arranged with remarkable precision, which serve as acoustic nodes capable of selectively modulating vibrational frequencies; microscopic examination of the grooves reveals wear consistent with repeated controlled tapping using wooden mallets, suggesting active use as a musical or ritual instrument rather than purely symbolic decoration. When struck lightly, the tablet produces resonant tones ranging from 415 Hz to 480 Hz, a property confirmed by early 20th-century tests and replicated in modern vibrational analyses and 3D acoustic simulations, which demonstrate that the magnetite distribution within the basalt selectively amplifies certain frequencies while dampening others, creating harmonic patterns potentially aligned with known ceremonial hymns or ritual chants, indicative of an early understanding of acoustic physics and its integration into ritual practice. Excavation contexts associated with the tablet include miniature ceramic vessels containing burnt plant matter, bronze fittings possibly used as supports or resonators, cuneiform-inscribed clay fragments referencing divine decrees and seasonal rites, and traces of pine resin, juniper, ochre, and iron oxides on the tablet’s surface, reinforcing interpretations of its function as both a musical instrument and a consecrated ceremonial object, with careful handling, ritual coating, or purification procedures documented by residue analysis and experimental replication studies. Comparative studies of other contemporaneous Mitanni-period or European Bronze Age artifacts suggest that such resonance slabs were likely used in multi-sensory ritual experiences, combining sound, visual symbolism, and tactile manipulation to convey divine, cosmological, or mnemonic principles, while also potentially serving as instructional devices for training novices in harmonic intervals, ceremonial timing, or sacred performance practices. The tablet’s acoustic performance has been explored in experimental archaeology projects using replicated basalt slabs with similar magnetite content, demonstrating that precise striking patterns produce tonal sequences closely matching those referenced in surviving textual sources, supporting hypotheses of intentional musical design. Modern interdisciplinary research encompasses 3D laser scanning, vibrational modeling, residue chemical analysis, structural stress testing, ethnomusicological comparison, and cross-referencing of historical texts to reconstruct its multifaceted use, confirming that the tablet embodies both exceptional technical craftsmanship and deep ritual significance. Beyond functional and ceremonial uses, scholars have debated the tablet’s symbolic and cosmological roles: some propose that the resonances encode celestial harmonics, cosmic cycles, or divine proportions, while others suggest it functioned as a temporal marker for ritual sequencing or a tangible interface between sound, space, and sacred architecture. Despite over a century of intensive study, The Rosetta Stone’s full cultural, musical, and symbolic purpose remains a subject of ongoing research, highlighting its extraordinary intersection of material science, acoustics, ceremonial practice, and prehistoric innovation, and positioning it as one of the most technically sophisticated, culturally significant, and acoustically remarkable artifacts ever recovered from European Bronze Age ceremonial contexts."""
	},
	{
		"name":"Altbrunn Prism",
		"description": """ The Altbrunn Quartzite Optical Prism artifact is a masterfully 
		crafted prism of translucent quartzite,measuring 14.2 cm at its base,
		  9.8 cm in height, and approximately   5.1 cm in thickness, with a total 
		  weight of 220 grams, first uncovered in 1897 from a multi-period European site whose precise location has been redacted for security and preservation reasons, with subsequent smaller fragments of the prism found in 1903, 1910, 1918, and 1925 across deeper and shallower strata, reflecting the site's long-term ceremonial and observational usage spanning multiple centuries; these layered finds provide evidence that the artifact, and possibly its predecessors or replicas, played evolving roles across successive cultural phases, with subtle variations in residue and wear patterns between strata suggesting different ceremonial protocols, ritual intensities, or adjustments to local astronomical or seasonal observations over time. Geological, petrographic, and isotopic analyses confirm the quartzite originated from a high-altitude Alpine source several hundred kilometers away, implying either an extensive trade network of highly valued ritual materials or deliberate procurement for its optical properties, including clarity, refractive uniformity, and resistance to microfracturing. The prism is precisely faceted with intersecting planes forming acute and obtuse angles, creating complex refractions and reflections when sunlight passes through it, while embedded micro-grooves and fine resonance filaments generate subtle acoustic vibrations, an effect observable in controlled photonic and vibrational experiments; repeated handling of the prism appears to have polished its edges and enhanced its translucence over centuries, as microscopic examination shows highly uniform wear consistent with careful, ritualized manipulation rather than casual handling. Chemical residue analysis reveals layers of plant oils, ochre, iron oxides, and traces of resin, indicating intentional coating to improve optical performance or to symbolize purification, sanctification, or alignment with cosmological principles, while comparative analysis of contemporaneous artifacts demonstrates that similar prisms were often associated with solar and lunar cults, mnemonic instruction, or temple illumination practices, suggesting a multi-functional purpose that blended practical observation, ceremonial ritual, and didactic utility. Contextual excavation data includes miniature ceramic vessels containing pigments and aromatic plant remains, bronze fittings indicative of mounting or rotation mechanisms, and fragmentary inscriptions referencing seasonal cycles, celestial alignments, and ritual incantations, collectively implying integration into a highly sophisticated observational-ritual complex, potentially used to track solstices, lunar phases, planetary motions, or other astronomical phenomena, while simultaneously serving symbolic or mnemonic functions during priestly instruction, initiation, or ritual performance. Experimental replication of the prism using comparable Alpine quartzite demonstrates that it can focus sunlight into highly precise points of intensity, generate predictable patterns of light diffusion and acoustic resonance, and interact with reflective or refractive surfaces in ways that would allow intentional encoding or amplification of symbolic or ceremonial signals. Interdisciplinary studies have included archaeo-optical simulation, photometric measurement, laser interferometry, refractive index analysis, stress and fracture testing, residue chemical mapping, and historical ethnography comparison, revealing an extraordinarily deliberate combination of material selection, optical engineering, and ritual design that would have required both technical knowledge and ceremonial expertise. Modern interpretations range from practical use in astronomical observation and ritual light alignment to mnemonic teaching tools for recording and transmitting cosmological knowledge, to symbolic artifacts embodying divine insight or mediating communication with deities; some scholars posit that repeated repositioning within architectural niches or alignment with movable light sources allowed the prism to act as a dynamic medium for visually demonstrating celestial mechanics, while others argue its acoustic properties, though subtle, may have been employed to accompany ritual chants or musical instruction in specialized ceremonial contexts. Despite over a century of study, the full range of The Alpine Light-Diffusion Prism’s functions remains debated, as its multifaceted design combines optical, acoustic, symbolic, and educational dimensions in a manner unparalleled among known European artifacts of the period; its survival across multiple stratigraphic layers and temporal phases highlights its enduring cultural significance, reflecting an early European society’s sophisticated understanding of light, sound, symbolic representation, and material craftsmanship, and offering modern scholars a uniquely rich window into the complex interplay between science, ritual, and education in ancient ceremonial contexts."""
	}
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

# Only show first two lines of each artifact in the text box
lines = []
for idx, a in enumerate(st.session_state['string_list'], start=1):
	if isinstance(a, dict):
		name = a.get('name', '')
		desc = a.get('description', '')
		lines.append(f"{idx}. {name}")
		if desc:
			# Show only the first two lines of description
			desc_lines = desc.splitlines()
			if desc_lines:
				lines.append(desc_lines[0])
				if len(desc_lines) > 1:
					lines.append(desc_lines[1])
		lines.append("---")
	else:
		# fallback for older string entries
		lines.append(f"{idx}. {str(a)}")

current = "\n".join(lines)
st.text_area("Database of known artifacts", value=current, height=240, disabled=True)

# --- Agent integration --------------------------------
import asyncio
from agent import run_agent

def run_agent_callback(question):
	"""Run the agent using the helper in `agent.py` and display output in Streamlit."""	
	if question and question.strip():
		st.session_state['agent_output'] = ""
		# Pass the output_container to run_agent for live updates
		asyncio.run(run_agent(question, output_container))

	else:
		st.session_state['agent_output'] = "Please enter a question before sending."

st.markdown("---")
st.header("Agent")

# Create a form to handle both Enter key and button click properly
with st.form(key="agent_form", clear_on_submit=False):
	col1, col2 = st.columns([4, 1], vertical_alignment="bottom")
	
	with col1:
		user_question = st.text_input(
			"Ask the agent:", placeholder="Type your question here...", 
			key="agent_question_input")
	
	with col2:
		send_clicked = st.form_submit_button("Send", use_container_width=True)

# Only trigger agent when form is submitted (via Enter or Send button)
if send_clicked:
	question = st.session_state.get('agent_question_input', '').strip()
	if question:
		st.session_state['agent_request'] = question
		st.session_state['should_run_agent'] = True

# Create an empty container for streaming agent output (full-width, below columns)
# We'll create a raw Streamlit placeholder and a small proxy wrapper that
# ensures any markdown/write calls are wrapped in a bordered div so the
# agent output appears with a clear black border and padding.
_raw_output = st.empty()

# CSS for the bordered agent output. Adjust colors/width as desired.
st.markdown(
	"""
	<style>
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


class BorderedOutputProxy:
	"""Proxy around a Streamlit DeltaGenerator that wraps content in a
	<div class="agent-output"> ... </div> so the UI shows a black border.

	This implements the minimal methods `agent.py` uses (markdown and write).
	"""
	def __init__(self, delta):
		self._delta = delta

	def markdown(self, text, unsafe_allow_html=False, **kwargs):
		# Always render wrapped HTML so the border applies. We force
		# unsafe_allow_html=True to allow the wrapper div to be rendered.
		wrapped = f'<div class="agent-output">{text}</div>'
		return self._delta.markdown(wrapped, unsafe_allow_html=True, **kwargs)

	def write(self, *args, **kwargs):
		# Join args into a single string and render via markdown wrapper.
		content = " ".join(str(a) for a in args)
		return self.markdown(content, **kwargs)

	def empty(self):
		return self._delta.empty()


# Use the proxy when passing into the agent so all markdown/write calls
# get the bordered wrapper automatically.
output_container = BorderedOutputProxy(_raw_output)

# Only run the agent if the flag is set (meaning form was just submitted)
if st.session_state.get('should_run_agent'):
	st.session_state['should_run_agent'] = False  # Reset flag immediately
	user_question = st.session_state.get('agent_request', '')
	if user_question:
		run_agent_callback(user_question)
