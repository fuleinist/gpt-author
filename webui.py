import gradio as gr
import json
from gpt_author_v2 import create_fantasy_novel
from ebook_to_text import epub_2_txt_file

INPUT_GUIDANCES = {
    'prompt': "Enter a brief scenario, question, or concept that encapsulates the primary idea or situation your novel will explore. This could be a conflict, a mystery, a setting, or a character's predicament.",
    'writing_style': "Describe the writing style for your novel. Consider aspects like sentence structure, tone, and lexicon. Examples might include 'concise and to-the-point', 'flowery and descriptive', or 'casual and conversational'.",
    'extra_guideline': "Include any additional instructions, preferences, or guidelines that are pertinent to the writing of your novel. This could encompass specific do's or don'ts, thematic considerations, or particular elements to include or avoid.",
    'plot_design': "Outline the main events and turning points in your novel. Consider how conflicts will arise and be resolved, and how the story will progress from beginning to end.",
    'world_building': "Describe the setting of your novel, including the physical environment, cultures, and social norms. Consider how the world's unique characteristics will impact the story and character development.",
    'character_depth': "Detail the main characters of your novel, including their backgrounds, motivations, and development arcs. Consider how their individual stories will intersect with and drive the overall plot."
}

# Function to be used in Gradio UI
def generate_and_save_novel(prompt, num_chapters, writing_style, extra_guideline, plot_design, world_building, character_depth, template_file):
    if template_file is not None:
        print('Loading inputs from template')
        template = load_template(template_file)
        print(template['prompt'])
    title = create_fantasy_novel((template['prompt'] or prompt), int(template['num_chapters'] or num_chapters), (template['writing_style'] or writing_style), (template['extra_guideline'] or extra_guideline), (template['plot_design'] or plot_design), (template['world_building'] or world_building), (template['character_depth'] or character_depth))
    file_path = f"content/{title}.epub"
    return file_path

def load_template(template_file):
    """
    Load parameters from a JSON template file.

    Parameters:
    - template_file: file object, the uploaded JSON file

    Returns:
    dict with parameter values
    """
    try:
        # Attempt to load the JSON data
        template_file.seek(0)  # Ensure we're at the start of the file again before reading as JSON
        file_content = template_file.read()
        template = json.loads(file_content)
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        template = {}
    return template

# Gradio UI
def gradio_ui():
    iface1 = gr.Interface(
        fn=generate_and_save_novel,
        inputs=[
            gr.inputs.Textbox(lines=3, label="Prompt", placeholder=INPUT_GUIDANCES['prompt']),
            gr.inputs.Slider(minimum=1, maximum=100, default=15, label="Number of Chapters"),
            gr.inputs.Textbox(lines=3, label="Writing Style", placeholder=INPUT_GUIDANCES['writing_style']),
            gr.inputs.Textbox(lines=3, label="Extra Guideline", placeholder=INPUT_GUIDANCES['extra_guideline'], optional=True),
            gr.inputs.Textbox(lines=3, label="Plot Design", placeholder=INPUT_GUIDANCES['plot_design'], optional=True),
            gr.inputs.Textbox(lines=3, label="World Building", placeholder=INPUT_GUIDANCES['world_building'], optional=True),
            gr.inputs.Textbox(lines=3, label="Character Depth", placeholder=INPUT_GUIDANCES['character_depth'], optional=True),
            gr.inputs.File(label="Template File", type="file", optional=True)  # Adding template file input
        ],
        outputs=gr.outputs.File(label="Download Generated Novel"),
        live=False, # This means the function will only be called when the user presses the "Submit" button
    )

    # Interface 2: EPUB to TXT Conversion
    iface2 = gr.Interface(
        fn=epub_2_txt_file,
        inputs=gr.inputs.File(label="Upload EPUB File"),
        outputs=gr.outputs.File(label="Download TXT File"),
        live=False
    )

    app = gr.TabbedInterface([iface1, iface2], ["Generate Novel", "Convert EPUB to TXT"])

    app.launch()

# Run the Gradio UI
gradio_ui()