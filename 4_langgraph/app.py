import gradio as gr
from sidekick import Sidekick


async def setup():
    sidekick = Sidekick()
    await sidekick.setup()
    return sidekick

async def process_message(sidekick, message, success_criteria, history):
    results = await sidekick.run_superstep(message, success_criteria, history)
    return results, sidekick
    
async def reset():
    new_sidekick = Sidekick()
    await new_sidekick.setup()
    return "", "", None, new_sidekick

def free_resources(sidekick):
    print("Limpiando recursos")
    try:
        if sidekick:
            sidekick.free_resources()
    except Exception as e:
        print(f"Excepción durante la limpieza: {e}")


with gr.Blocks(title="Sidekick", theme=gr.themes.Default(primary_hue="emerald")) as ui:
    gr.Markdown("## Sidekick Compañero de Trabajo Personal")
    sidekick = gr.State(delete_callback=free_resources)
    
    with gr.Row():
        chatbot = gr.Chatbot(label="Sidekick", height=300, type="messages")
    with gr.Group():
        with gr.Row():
            message = gr.Textbox(show_label=False, placeholder="Tu solicitud al Sidekick")
        with gr.Row():
            success_criteria = gr.Textbox(show_label=False, placeholder="¿Cuáles son tus criterios de éxito?")
    with gr.Row():
        reset_button = gr.Button("Reiniciar", variant="stop")
        go_button = gr.Button("Ir!", variant="primary")
        
    ui.load(setup, [], [sidekick])
    message.submit(process_message, [sidekick, message, success_criteria, chatbot], [chatbot, sidekick])
    success_criteria.submit(process_message, [sidekick, message, success_criteria, chatbot], [chatbot, sidekick])
    go_button.click(process_message, [sidekick, message, success_criteria, chatbot], [chatbot, sidekick])
    reset_button.click(reset, [], [message, success_criteria, chatbot, sidekick])

    
ui.launch(inbrowser=True)