import ollama
import gradio as gr


def generate_question(text):
    prompt = f"""{text}"""
    context = ollama.generate(model='llama3.1', prompt=prompt)['context']

    prompt = f"""
    Generate a question and several answer choices based on the aforementioned text.
    Separate the question and answer choices with a newline.
    Use asterisk to denote the correct answer.
    Do not provide any hints, explanations, or additional information.
    """
    response = ollama.generate(model='llama3.1', prompt=prompt, context=context)['response']
    print("LLM Response:\n", response)

    # Parse the response
    lines = response.split('\n')
    question = lines[0]
    choices = []
    correct_answer = 0
    for i, line in enumerate(lines[1:]):
        line = line.strip()
        if line == '':
            continue
        if '*' in line:
            correct_answer = len(choices)
            line = line.replace('*', '')
        choices.append(line)

    return question, choices, correct_answer


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
                result_lbl: gr.Markdown("## Correct" if answer == choices[correct_answer] else "## Incorrect", visible=True),
            }

    submit_btn.click(
        submit,
        [text_box, answer_selector, result_lbl],
        [answer_selector, result_lbl],
    )

demo.launch()
