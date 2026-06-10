import gradio as gr
from query import ask

EXAMPLES = [
    "What do students say about Melissa Lynch's grading in CSCI160?",
    "Is Maryash good for CSCI135 if you have no C++ experience?",
    "How important is attendance for Shostak's CSCI260?",
    "What do students say about Mneimneh's teaching style in CSCI150?",
    "Do recent reviews recommend taking St. John for CSCI127?",
    "Who is easier for CSCI150, Mneimneh or Epstein?",
    "What do students say about exams in CSCI260?",
    "Is Tong Yi a good professor for CSCI135?",
    "What are the most common complaints about CSCI160 professors?",
    "Which CSCI127 professor do students recommend more?",
]

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700&display=swap');
body, * { font-family: 'Nunito', sans-serif !important; }
.gradio-container { max-width: 820px !important; margin: 0 auto !important; }
#title { text-align: center; }
#subtitle { text-align: center; }
"""


def handle_query(question):
    if not question.strip():
        return "", ""
    result = ask(question)
    sources = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], sources


with gr.Blocks(title="The Unofficial Guide") as demo:
    gr.Markdown("# The Unofficial Guide", elem_id="title")
    gr.Markdown(
        "Student-powered answers about CS professors at Hunter College, sourced from Rate My Professors reviews.",
        elem_id="subtitle",
    )

    inp = gr.Textbox(
        label="Ask a question",
        placeholder="e.g. Is Maryash good for CSCI135 if you have no C++ experience?",
        lines=2,
    )
    btn = gr.Button("Ask", variant="primary")

    with gr.Row():
        answer = gr.Textbox(label="Answer", lines=10, scale=3)
        sources = gr.Textbox(label="Sources", lines=10, scale=1)

    gr.Markdown("#### Try one of these:")
    gr.Examples(examples=[[q] for q in EXAMPLES], inputs=inp, label="")

    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])


if __name__ == "__main__":
    demo.launch(theme=gr.themes.Soft(), css=CSS)
