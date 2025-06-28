import gradio as gr
from dotenv import load_dotenv
from research_manager import ResearchManager

load_dotenv(override=True)


async def run(query: str):
    async for chunk in ResearchManager().run(query):
        yield chunk


with gr.Blocks(theme=gr.themes.Default(primary_hue="sky")) as ui:
    gr.Markdown("# Búsqueda Profunda")
    query_textbox = gr.Textbox(label="¿Sobre qué tema te gustaría investigar?")
    run_button = gr.Button("Ejecutar", variant="primary")
    report = gr.Markdown(label="Informe")
    
    run_button.click(fn=run, inputs=query_textbox, outputs=report)
    query_textbox.submit(fn=run, inputs=query_textbox, outputs=report)

ui.launch(inbrowser=True)

