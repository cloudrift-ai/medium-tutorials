from ollama import Client
import os
import gradio as gr

LLM_SERVER_IP_ADDRESS = os.environ.get('LLM_SERVER_IP_ADDRESS')
if LLM_SERVER_IP_ADDRESS is None:
    raise Exception("Please set the LLM_SERVER_IP_ADDRESS environment variable to the IP address of the LLM server.")


def generate_question(context):
    # supply text to the model and get the context
    prompt = f"""{context}"""
    client = Client(host=f"http://{LLM_SERVER_IP_ADDRESS}:11434")
    context = client.generate(model='deepseek-r1:32b', prompt=prompt)['context']

    # generate a question based on the context
    prompt = f"""
    Generate one question with several answer choices based on the aforementioned text.
    Separate the question and answer choices with a newline.
    Do not provide any hints, explanations, or additional information.
    Use asterisk "*" to denote the correct answer inline.
    Don't use asterisk anywhere else and don't repeat the answer to simplify parsing.
    """
    response = client.generate(model='deepseek-r1:32b', prompt=prompt, context=context)['response']
    print("LLM Response:\n", response)

    # Parse the response
    lines = response.split('\n')
    think_mode = False
    question = None
    choices = []
    correct_answer = 0
    for i, line in enumerate(lines):
        line = line.strip()
        if line == '<think>':
            think_mode = True
        elif line == '</think>':
            think_mode = False
        elif line == '' or think_mode:
            continue
        elif question is None:
            question = line
        else:
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
    # an input text box
    text_box = gr.Textbox(label="Enter your text")
    # radio buttons for the answer choices, we populate choices later
    answer_selector = gr.Radio(label="N/A", choices=choices, visible=False)
    # a button to submit the answer
    submit_btn = gr.Button("Submit")
    # a label to display the result: correct or incorrect
    result_lbl = gr.Markdown("N/A", visible=False)

    def submit(input_text, answer, _r):
        global text, question, choices, correct_answer
        # if running for the first time or the input text has changed - generate a new question
        if text != input_text:
            text = input_text
            question, choices, correct_answer = generate_question(text)
            return {
                answer_selector: gr.Radio(label=question, choices=choices, visible=True),
                result_lbl: result_lbl,
            }
        # if the answer is submitted - check if it's correct
        else:
            result = "## Correct" if answer == choices[correct_answer] else "## Incorrect"
            return {
                answer_selector: gr.Radio(label=question, choices=choices, visible=True),
                result_lbl: gr.Markdown(result, visible=True),
            }

    # bind the submit button to the submit function
    submit_btn.click(
        submit,
        [text_box, answer_selector, result_lbl],
        [answer_selector, result_lbl],
    )

demo.launch()
