import os

import gradio as gr
import time

from utils.frame_utils.frame import Frame

os.environ["no_proxy"] = "localhost,127.0.0.1,::1"

FRAME = Frame()


def model_inference(input_text):
    outputs = [["chatbot", ""]]
    for token in FRAME.predict(question=input_text):
        outputs[0][1] += token
        yield outputs  # 流式返回


with gr.Blocks() as demo:
    gr.Markdown("## O1 Model Interaction")

    with gr.Row():
        input_text = gr.Textbox(label="Input Text", placeholder="Enter your text here...")
        submit_btn = gr.Button("Submit")

    output_chatbot = gr.Chatbot(label="Model Output")

    submit_btn.click(
        fn=model_inference,
        inputs=input_text,
        outputs=output_chatbot,
        api_name="infer"
    )

demo.launch(server_name="0.0.0.0",
            server_port=7860,
            share=False,
            )
