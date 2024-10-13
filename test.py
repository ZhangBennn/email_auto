import gradio as gr

def greet(name):
    return f"Hello {name}!"

with gr.Blocks() as demo:
    name_input = gr.Textbox(label="Your Name", placeholder="Enter your full name here", value="sss")
    output_text = gr.Textbox(label="Greeting")
    btn = gr.Button("Greet")
    
    btn.click(fn=greet, inputs=name_input, outputs=output_text)

demo.launch()