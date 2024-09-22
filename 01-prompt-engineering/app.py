import gradio as gr


def generate_question(text):
    return "What is the topic of this text?", ["A", "B", "C"], "A"


text = None
question = None
choices = []
correct_answer = 0

with gr.Blocks() as demo:
    text_box = gr.Textbox(label="Enter your text")
    answer_selector = gr.Radio(label="N/A", choices=choices, visible=False)
    result_lbl = gr.Markdown("N/A", visible=False)
    submit_btn = gr.Button("Submit")

    def submit(input_text, answer, _r):
        global text, question, choices, correct_answer
        if text != input_text:
            text = input_text
            question, choices, correct_answer = generate_question(text)
            return {
                answer_selector: gr.Radio(label=question, choices=choices, visible=True),
                result_lbl: result_lbl,
            }
        else:
            return {
                answer_selector: gr.Radio(label=question, choices=choices, visible=True),
                result_lbl: gr.Markdown("## Correct" if answer == correct_answer else "## Incorrect", visible=True),
            }

    submit_btn.click(
        submit,
        [text_box, answer_selector, result_lbl],
        [answer_selector, result_lbl],
    )

demo.launch()
