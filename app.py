import json
import os
from pathlib import Path
from dotenv import load_dotenv 

import streamlit as st

load_dotenv()
st.set_page_config(page_title="String List Manager")

# Ensure core UI is visible and inputs are readable (debugging layout issues)
st.markdown(
		"""
		<style>
			/* Page background */
			.stApp, .reportview-container, .main {
				background-color: #cfbdae !important;
				min-height: 200vh;
			}
			/* Make all text black and bold */
			body, p, h1, h2, h3, h4, h5, h6, div, span, label,.stText, .stMarkdown {
				color: #000000 !important;
				font-weight: bold !important;
			}
			/* Make form controls clearly visible */
			input, textarea, button {
				color: #000000 !important;
				background-color: #bba694 !important;
				font-weight: bold !important;
			}
			/* Target Streamlit textarea with all classes */
			textarea.st-ae, textarea.st-bd, textarea.st-be, textarea.st-bf, textarea.st-bg,
			textarea[class*="st-"],
			.stTextArea textarea {
				color: #000000 !important;
				font-weight: bold !important;
			}
		</style>
		""",
		unsafe_allow_html=True,
)

# Small visible debug banner so users can confirm the app rendered
st.markdown("<div style='padding:6px;background:#ffffffaa;border-radius:6px;'>UI loaded — debug banner</div>", unsafe_allow_html=True)

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
		"name": " The Celestial Obsidian Lens",
		"description": """The Celestial Obsidian Lens is an oval-shaped, finely polished lens of deep black obsidian, measuring 12.6 cm in length, 8.4 cm in width, and 1.7 cm in thickness, discovered in 1911 during a joint excavation by the Metropolitan Museum of Art and the Oriental Institute at Tello (ancient Girsu) in southern Mesopotamia, found in a sealed chamber adjacent to Temple E2, a large administrative and ceremonial precinct; stratigraphic and radiocarbon dating place the lens within the Late Ur III period, c. 2100–2000 BCE, coinciding with a time of intense administrative organization, early scientific experimentation, and ritual innovation in Sumerian city-states. Geological analysis confirms that the obsidian originates from the Nemrut Dağ volcanic region in eastern Anatolia, indicating sophisticated trade networks capable of transporting high-value materials over hundreds of kilometers. The lens features a convex top surface and flat underside, with microscopic striations consistent with careful grinding using abrasives such as emery or fine sand, and residues of vegetable oils, iron oxides, and traces of ochre embedded in microgrooves suggest repeated handling and possible ceremonial coating to enhance optical clarity or symbolic brilliance. The chamber also contained bronze fittings, miniature ceramic vessels with plant-based pigments, and fragments of cuneiform tablets referencing solar, lunar, and planetary observations, implying that the lens was part of a composite device potentially used for astronomical observation, ritualized illumination, divination, or as a symbolic object representing divine insight, with some scholars suggesting it may have functioned to align sunlight with sacred architectural features during solstices or equinoxes. Historical documentation notes that sunlight transmitted through the lens could focus on small surfaces with enough intensity to char thin organic materials, a phenomenon confirmed by optical simulations conducted at Oxford University in 1985, which measured a focal length of approximately 28 cm and confirmed highly uniform light transmission across the surface; experimental archaeology replication projects have successfully demonstrated that the lens can concentrate light to precise points under varying angles, supporting hypotheses of intentional design for either practical or ceremonial purposes. Interpretations of the lens’s function are diverse: some scholars, including Dr. Ingrid F. Müller, propose it was an astronomical instrument used to track celestial movements or lunar cycles, while others, such as Dr. Robert C. Lang, argue it held primarily symbolic or ritual significance as the “eye of the gods,” potentially used to mediate divine knowledge or illuminate sacred spaces during temple ceremonies. Microscopic analysis reveals minor wear along edges consistent with repeated placement in mounts or frames, while chemical analysis of residues also detected traces of animal fat and plant resin, suggesting the lens may have been handled with ritual oils or integrated into a complex ceremonial practice. The lens’s optical properties have been studied extensively in modern times, including photometric measurements, laser interferometry, refractive index analysis, and structural stress testing, which confirmed its unusually high transparency, uniform curvature, and precise focus—remarkable engineering for the period, exceeding the craftsmanship of other known contemporaneous Near Eastern artifacts. Catalogued as Tello-1911/OB-3, the lens is preserved in climate-controlled storage, with environmental monitoring implemented to prevent microfracturing or surface deterioration. Scholarly debates persist regarding whether the lens’s primary function was ritual, instructional, astronomical, symbolic, or a combination of these roles; hypotheses range from its use in temple light alignment, ceremonial solar observation, or as a training tool for scribes in early optical techniques, to more speculative interpretations suggesting its employment as a medium to visually communicate cosmological or divine principles to the priestly elite. Further interdisciplinary studies include archaeo-optical experimentation, material science analysis, Sumerological interpretation, comparison with other Late Ur III artifacts, and experimental replication using obsidian with similar chemical and structural properties; these studies have sought to understand not only the lens’s functional properties but also its broader cultural, ritual, and symbolic significance within Sumerian society. The Celestial Obsidian Lens represents an unparalleled combination of technical sophistication, ritual significance, and optical precision, offering scholars an extraordinary window into the intersection of early science, sacred practice, material craftsmanship, and symbolic thought, and despite over a century of intensive study, its full purpose remains unresolved, ensuring that it continues to challenge researchers and captivates both historical and scientific imagination."""
		
		,
	},
	{
		"name": "The Basalt Resonance Tablet",
		"description": """The Basalt Resonance Tablet is a rectangular slab of magnetite-rich basalt, recovered in 1904 from Tell Brak, one of the largest Early and Late Bronze Age sites in northeastern Syria, specifically from Structure 27, a multi-room administrative and ceremonial complex that shows evidence of continuous occupation from the Mitanni period, c. 1500–1300 BCE; petrographic and isotopic analysis confirm that the basalt originated from the upper Jebel Abd al-Aziz volcanic fields, indicating either the acquisition of high-quality ceremonial materials through long-distance trade or the deliberate selection of a stone with particular acoustic properties, and the tablet measures 31.4 cm in length, 18.7 cm in width, and 3.2 cm in thickness, with a total weight of approximately 6.3 kilograms. Its surface is intricately carved with a series of intersecting linear grooves forming a precise geometric grid, believed to correspond with harmonic ratios preserved in surviving Hurrian musical texts, while a series of shallow hemispherical depressions along one edge appear to serve as acoustic nodes capable of selectively modulating vibrations; microscopic examination reveals wear patterns consistent with repeated, controlled tapping using wooden mallets or other implements, suggesting that the object was not merely symbolic but actively used to produce sound during rituals or musical instruction. Excavators noted that when struck lightly with a wooden implement, the tablet produced a series of pure, resonant tones, a phenomenon confirmed in 1932 during controlled testing at the British Museum, which measured consistent frequency intervals between 415 Hz and 480 Hz, aligning closely with reconstructed pitches from Hurrian ceremonial hymns; additional nearby finds included clay tablets inscribed with cuneiform referencing the “measure of the breath of the sky god Teshub,” miniature ceramic vessels containing burnt plant matter, and bronze fittings that may have been used as resonators, supports, or tuning aids, suggesting a multi-functional role combining music, ritual, and symbolic meaning. Residue analysis conducted in 1979 by the University of Chicago’s Oriental Institute Laboratory revealed traces of pine resin, burnt juniper, and traces of iron oxides, substances historically associated with Mitanni purification and sacred ceremonial activities, reinforcing the interpretation of the tablet as both functional and ritualistically significant. Acoustic modeling using 3D laser scanning and vibrational analysis indicates that the magnetite distribution within the basalt creates distinct vibration pathways, amplifying certain tonal frequencies while dampening others, a property that modern materials scientists classify as an accidental but highly effective form of early acoustic engineering, implying that the Mitanni culture may have recognized and exploited specific physical properties of stone for ceremonial sound production. The tablet was catalogued as OIM A.1904.77 and placed in controlled storage due to surface flaking and minor microfractures, with ongoing preservation studies monitoring environmental humidity, temperature, and vibration exposure. Scholarly debates surrounding the tablet include its primary purpose, whether as a ceremonial instrument invoking divine favor, a reference standard for Mitanni court musicians, an instructional device for training young performers in harmonic intervals, or a symbolic object measuring cosmic or divine principles through sound; additional hypotheses suggest it could have functioned as a combination of these roles, integrating ritual, education, and symbolic meaning into a single, multi-purpose artifact. Experimental archaeology has recreated the tablet using basalt with comparable density and magnetite content, demonstrating that, when struck with replica implements at various angles, it reproduces the tonal patterns recorded in Hurrian hymns, supporting interpretations of intentional musical design; further interdisciplinary studies include chemical analysis of residues, 3D modeling of the grooves and nodes, cross-referencing acoustic data with surviving texts, and examination of wear patterns to reconstruct historical usage, while comparative analysis with similar Mitanni artifacts has shown that few contemporary objects exhibit equivalent technical sophistication, making the Basalt Resonance Tablet one of the most acoustically intriguing, technically advanced, and culturally significant artifacts recovered from the Mitanni sphere and providing unparalleled insight into the intersection of music, ritual, and material science in Bronze Age Syria. Modern research also considers the tablet’s potential symbolic and cosmological significance, including speculation that the resonances represented celestial harmonics or encoded cosmological principles, that its use in temple ceremonies could have marked ritual timing or transitions, and that it may have served as a tangible link between sound, space, and the sacred, reflecting the Mitanni’s sophisticated understanding of acoustic phenomena as a medium of cultural and religious expression; despite over a century of study, its precise role remains debated, ensuring that the Basalt Resonance Tablet continues to challenge researchers and remains a unique example of prehistoric musical, ritual, and engineering ingenuity."""
			
	},
	{
		"name": "The Echo Prism (Accession A-2097-EP)",
		"description": """The Echo Prism is a triangular quartzite artifact first uncovered in 1892 during the British Museum’s systematic excavation of the Nineveh Province in northern Iraq, specifically at Site N-14, located southeast of the ancient Assyrian city of Nimrud, where it was found 2.3 meters below a collapsed ceremonial chamber, which had suffered centuries of structural decay yet preserved a microclimate that contributed to the exceptional preservation of its material; stratigraphic analysis dates the prism’s last period of use to between 850–600 BCE, situating it within the late Neo-Assyrian Empire, a period noted for monumental architecture, sophisticated administration, and the codification of ceremonial and religious practice. The prism measures 14.2 cm at its base, 9.8 cm in height, approximately 5.1 cm in thickness, and weighs 220 grams, carved from exceptionally pure quartzite whose isotopic fingerprint matches deposits in the Zagros Mountains, indicating either long-distance trade networks or the transport of specialized materials to centers of power in Assyria, and detailed microscopic analysis reveals an intricate lattice of reflective planes, micro-fissures, and resonance filaments precisely aligned along axes that do not correspond with natural fracture patterns, indicating deliberate geometric design likely intended to manipulate both light and sound in controlled ways. Field notes from lead archaeologist Dr. Charles Hawthorne document that the prism emitted faint tonal vibrations when first exposed to sunlight, creating subtle, fluctuating hums that appeared to correspond to the angle of incoming light; subsequent controlled experiments conducted throughout the 20th century by scholars at the British Institute for the Study of Iraq and University College London produced similar acoustic responses when specific resonant frequencies were applied, although these responses were inconsistent under differing environmental conditions. The chamber also contained multiple related artifacts, including clay tablets (BM 1893,1121.45–58) with Akkadian inscriptions referencing ceremonial recitations, oaths, and “the stone that carries the final breath,” as well as administrative seals linked to the reign of Ashurbanipal, implying both ritualistic and practical uses, possibly to amplify speech during formal oaths, record ceremonial declarations, or facilitate long-distance acoustic communication within palace complexes or temple chambers; wear patterns along the edges and surface suggest repeated handling, and chemical analyses performed in 1974 revealed traces of cedar oil, bitumen, and burnt ash, substances commonly associated with Neo-Assyrian purification and ritual practices. Interpretations of the prism’s function range from mnemonic tool for oral declarations, ceremonial object demonstrating authority or divine favor, to proto-acoustic amplifier intended to manipulate perception of voice within enclosed spaces, with acoustic spectroscopy in 1961 confirming selective amplification of mid-range sound frequencies when positioned at approximately 37 degrees relative to a hard surface; modern geophysical and optical studies of the lattice and reflective planes demonstrate unexpectedly sophisticated understanding of light refraction and sound resonance, suggesting a highly specialized class of Assyrian craftspeople, possibly the priestly “Resonant Scholars,” were responsible for its creation. The prism has been preserved with minor microcracks noted in 1987, catalogued as N-14.QZ.1892, and is stored in climate-controlled conditions, remaining one of the most intensively studied artifacts from Neo-Assyria, featuring in publications across archaeology, geology, acoustics, and Assyriology; contemporary scholarly debates continue over its primary function—ritual, practical, mnemonic, symbolic, or part of a larger system—while further hypotheses include educational use for training scholars in voice modulation, acoustic signaling in palace or temple corridors, or symbolic representation of authority or divine communication, and modern studies include photometric modeling, acoustic simulations, chemical analysis, and experimental replication attempts, highlighting its intersection across material science, ritual practice, historical acoustics, and Near Eastern political and ceremonial traditions, securing its reputation as one of the most enigmatic and technically sophisticated Neo-Assyrian artifacts."""
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
from agent import run_agent, debug_run_agent
def run_agent_callback(question):
	"""Run the agent using the helper in `agent.py` and store the final output."""
	if question and question.strip():
		# Pass the user's question into the agent helper
		st.session_state['agent_output'] = run_agent(question)
		# also capture debug info for diagnostics
		try:
			st.session_state['agent_debug'] = debug_run_agent(question)
		except Exception:
			st.session_state['agent_debug'] = {"error": "failed to produce debug info"}
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

st.text_area("Agent output", value=st.session_state.get('agent_output', ''), height=200, disabled=True)

# Optional debug view (hidden unless enabled)
if st.checkbox("Show agent debug info"):
	debug_info = st.session_state.get('agent_debug')
	st.text_area("Agent debug (repr/type/attrs)", value=str(debug_info), height=300)
