"""
CV Interactivo — Interfaz Terminal Matrix
Ángel Nácar Jiménez — AI Agent Profile

Reemplaza la función launch() al final de chat_optimized.py con este módulo,
o impórtalo directamente: from ui import launch_ui
"""

import gradio as gr

# ── Paleta y variables CSS ──────────────────────────────────────────────────

_CSS = """
/* ══════════════════════════════════════════════════════════════
   IMPORTS & RESET
══════════════════════════════════════════════════════════════ */
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&display=swap');

:root {
    --matrix-black:    #000000;
    --matrix-dark:     #050f05;
    --matrix-mid:      #0a1a0a;
    --matrix-panel:    #0d1f0d;
    --matrix-border:   #1a4a1a;
    --matrix-green:    #00ff41;
    --matrix-green-2:  #00cc33;
    --matrix-green-3:  #008f11;
    --matrix-green-dim:#003b00;
    --matrix-amber:    #ffaa00;
    --matrix-red:      #ff3333;
    --matrix-white:    #e0ffe0;
    --font-mono:       'Share Tech Mono', 'Courier New', monospace;
    --font-display:    'Orbitron', monospace;
    --scanline-opacity: 0.03;
    --glow-sm: 0 0 6px var(--matrix-green), 0 0 12px rgba(0,255,65,0.3);
    --glow-md: 0 0 10px var(--matrix-green), 0 0 25px rgba(0,255,65,0.4), 0 0 50px rgba(0,255,65,0.1);
    --glow-lg: 0 0 15px var(--matrix-green), 0 0 40px rgba(0,255,65,0.5), 0 0 80px rgba(0,255,65,0.2);
}

/* ══════════════════════════════════════════════════════════════
   BASE — fondo, tipografía, scanlines
══════════════════════════════════════════════════════════════ */

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body, .gradio-container, #root {
    background: var(--matrix-black) !important;
    color: var(--matrix-green) !important;
    font-family: var(--font-mono) !important;
    min-height: 100vh;
}

/* Scanlines overlay */
.gradio-container::before {
    content: '';
    position: fixed;
    inset: 0;
    background: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 2px,
        rgba(0,255,65, var(--scanline-opacity)) 2px,
        rgba(0,255,65, var(--scanline-opacity)) 4px
    );
    pointer-events: none;
    z-index: 9999;
    animation: scanRoll 8s linear infinite;
}

@keyframes scanRoll {
    from { background-position: 0 0; }
    to   { background-position: 0 400px; }
}

/* Vignette */
.gradio-container::after {
    content: '';
    position: fixed;
    inset: 0;
    background: radial-gradient(ellipse at center,
        transparent 50%,
        rgba(0,0,0,0.7) 100%
    );
    pointer-events: none;
    z-index: 9998;
}

/* ══════════════════════════════════════════════════════════════
   LAYOUT PRINCIPAL
══════════════════════════════════════════════════════════════ */

.main-container {
    max-width: 920px;
    margin: 0 auto;
    padding: 24px 16px;
    position: relative;
}

/* ══════════════════════════════════════════════════════════════
   HEADER — título + avatar + status
══════════════════════════════════════════════════════════════ */

.terminal-header {
    border: 1px solid var(--matrix-border);
    background: var(--matrix-panel);
    padding: 20px 24px;
    margin-bottom: 16px;
    position: relative;
    overflow: hidden;
}

.terminal-header::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg,
        transparent, var(--matrix-green), var(--matrix-green-2), transparent
    );
    animation: borderScan 3s ease-in-out infinite;
}

@keyframes borderScan {
    0%, 100% { opacity: 0.3; }
    50%       { opacity: 1; box-shadow: var(--glow-sm); }
}

.header-inner {
    display: flex;
    align-items: center;
    gap: 24px;
}

/* Avatar */
.avatar-frame {
    flex-shrink: 0;
    width: 90px;
    height: 90px;
    border: 2px solid var(--matrix-green-3);
    position: relative;
    box-shadow: var(--glow-sm);
    background: var(--matrix-dark);
    overflow: hidden;
}

.avatar-frame::before,
.avatar-frame::after {
    content: '';
    position: absolute;
    width: 12px; height: 12px;
    border-color: var(--matrix-green);
    border-style: solid;
    z-index: 2;
}
.avatar-frame::before { top: -1px; left: -1px; border-width: 2px 0 0 2px; }
.avatar-frame::after  { bottom: -1px; right: -1px; border-width: 0 2px 2px 0; }

/* Placeholder avatar — iniciales con estilo matrix */
.avatar-placeholder {
    width: 100%; height: 100%;
    display: flex; align-items: center; justify-content: center;
    font-family: var(--font-display);
    font-size: 28px;
    font-weight: 900;
    color: var(--matrix-green);
    text-shadow: var(--glow-md);
    background: linear-gradient(135deg, var(--matrix-dark), var(--matrix-mid));
    letter-spacing: 2px;
    animation: avatarPulse 4s ease-in-out infinite;
}

@keyframes avatarPulse {
    0%, 100% { text-shadow: var(--glow-sm); }
    50%       { text-shadow: var(--glow-lg); }
}

.avatar-frame img {
    width: 100%; height: 100%;
    object-fit: cover;
    object-position: center top;
    filter: sepia(0.2) hue-rotate(80deg) saturate(1.5) brightness(0.9);
    display: none; /* se activa por JS si existe avatar real */
}

/* Info del header */
.header-info { flex: 1; }

.header-title {
    font-family: var(--font-display);
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--matrix-green);
    text-shadow: var(--glow-sm);
    letter-spacing: 3px;
    text-transform: uppercase;
    line-height: 1.2;
}

.header-subtitle {
    font-family: var(--font-mono);
    font-size: 0.75rem;
    color: var(--matrix-green-3);
    letter-spacing: 2px;
    margin-top: 4px;
    text-transform: uppercase;
}

.header-status {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-top: 12px;
    font-size: 0.7rem;
    color: var(--matrix-green-3);
    letter-spacing: 1px;
}

.status-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: var(--matrix-green);
    box-shadow: var(--glow-sm);
    animation: blink 1.2s step-start infinite;
}

@keyframes blink {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0; }
}

.header-meta {
    text-align: right;
    font-size: 0.65rem;
    color: var(--matrix-green-dim);
    letter-spacing: 1px;
    line-height: 1.8;
}

/* ══════════════════════════════════════════════════════════════
   VENTANA DE CHAT
══════════════════════════════════════════════════════════════ */

/* Wrapper del chatbot */
.chat-wrapper {
    border: 1px solid var(--matrix-border);
    background: var(--matrix-dark);
    position: relative;
}

/* Barra de título estilo terminal */
.terminal-bar {
    background: var(--matrix-panel);
    border-bottom: 1px solid var(--matrix-border);
    padding: 7px 14px;
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 0.65rem;
    color: var(--matrix-green-3);
    letter-spacing: 2px;
    text-transform: uppercase;
}

.terminal-bar-dots { display: flex; gap: 6px; }
.terminal-bar-dot  { width: 8px; height: 8px; border-radius: 50%; }
.dot-red    { background: var(--matrix-red);   box-shadow: 0 0 4px var(--matrix-red); }
.dot-amber  { background: var(--matrix-amber); box-shadow: 0 0 4px var(--matrix-amber); }
.dot-green  { background: var(--matrix-green); box-shadow: 0 0 4px var(--matrix-green); }

.terminal-bar-title { flex: 1; text-align: center; }

/* Chatbot Gradio */
#angel-chat {
    background: var(--matrix-dark) !important;
    border: none !important;
    border-radius: 0 !important;
}

/* Área de mensajes */
#angel-chat .message-wrap,
#angel-chat > div:first-child {
    background: transparent !important;
    padding: 16px !important;
}

/* Scrollbar */
#angel-chat ::-webkit-scrollbar { width: 4px; }
#angel-chat ::-webkit-scrollbar-track { background: var(--matrix-dark); }
#angel-chat ::-webkit-scrollbar-thumb {
    background: var(--matrix-green-3);
    box-shadow: var(--glow-sm);
}

/* ── Burbujas de mensajes ── */

/* Usuario */
#angel-chat .user {
    background: transparent !important;
    border: 1px solid var(--matrix-green-3) !important;
    border-radius: 0 !important;
    color: var(--matrix-green-2) !important;
    font-family: var(--font-mono) !important;
    font-size: 0.85rem !important;
    padding: 10px 14px !important;
    margin-bottom: 12px !important;
    position: relative;
}

#angel-chat .user::before {
    content: '> USER:';
    display: block;
    font-size: 0.65rem;
    color: var(--matrix-green-3);
    letter-spacing: 2px;
    margin-bottom: 4px;
}

/* Bot */
#angel-chat .bot {
    background: var(--matrix-panel) !important;
    border: 1px solid var(--matrix-green-dim) !important;
    border-left: 3px solid var(--matrix-green) !important;
    border-radius: 0 !important;
    color: var(--matrix-white) !important;
    font-family: var(--font-mono) !important;
    font-size: 0.85rem !important;
    padding: 10px 14px !important;
    margin-bottom: 12px !important;
    box-shadow: inset 0 0 20px rgba(0,255,65,0.02);
    line-height: 1.7;
}

#angel-chat .bot::before {
    content: '> ANGEL.exe:';
    display: block;
    font-size: 0.65rem;
    color: var(--matrix-green);
    letter-spacing: 2px;
    margin-bottom: 4px;
    text-shadow: var(--glow-sm);
}

/* Typing indicator */
#angel-chat .thinking,
#angel-chat .generating {
    color: var(--matrix-green-3) !important;
    font-family: var(--font-mono) !important;
    font-size: 0.8rem !important;
    animation: cursorBlink 0.8s step-start infinite;
}

@keyframes cursorBlink {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.3; }
}

/* ══════════════════════════════════════════════════════════════
   INPUT Y BOTÓN
══════════════════════════════════════════════════════════════ */

.input-zone {
    border: 1px solid var(--matrix-border);
    border-top: none;
    background: var(--matrix-panel);
    padding: 12px;
    display: flex;
    gap: 10px;
    align-items: flex-end;
}

.input-prompt-label {
    font-family: var(--font-mono);
    font-size: 0.85rem;
    color: var(--matrix-green);
    padding-bottom: 12px;
    flex-shrink: 0;
    text-shadow: var(--glow-sm);
    white-space: nowrap;
}

/* Textarea */
#angel-input textarea,
#angel-input input {
    background: var(--matrix-dark) !important;
    border: 1px solid var(--matrix-green-3) !important;
    border-radius: 0 !important;
    color: var(--matrix-green) !important;
    font-family: var(--font-mono) !important;
    font-size: 0.85rem !important;
    caret-color: var(--matrix-green);
    padding: 10px 12px !important;
    resize: none !important;
    outline: none !important;
    transition: border-color 0.2s, box-shadow 0.2s;
}

#angel-input textarea:focus,
#angel-input input:focus {
    border-color: var(--matrix-green) !important;
    box-shadow: var(--glow-sm) !important;
}

#angel-input textarea::placeholder,
#angel-input input::placeholder {
    color: var(--matrix-green-dim) !important;
    font-style: italic;
}

/* Botón submit */
#angel-submit {
    background: transparent !important;
    border: 1px solid var(--matrix-green) !important;
    border-radius: 0 !important;
    color: var(--matrix-green) !important;
    font-family: var(--font-display) !important;
    font-size: 0.65rem !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    padding: 10px 16px !important;
    cursor: pointer;
    transition: all 0.15s;
    min-width: 80px;
    white-space: nowrap;
}

#angel-submit:hover {
    background: var(--matrix-green-dim) !important;
    box-shadow: var(--glow-sm) !important;
    color: var(--matrix-green) !important;
}

#angel-submit:active {
    background: rgba(0,255,65,0.2) !important;
}

/* Botón clear */
#angel-clear {
    background: transparent !important;
    border: 1px solid var(--matrix-green-dim) !important;
    border-radius: 0 !important;
    color: var(--matrix-green-3) !important;
    font-family: var(--font-mono) !important;
    font-size: 0.65rem !important;
    letter-spacing: 2px !important;
    padding: 8px 12px !important;
    cursor: pointer;
    transition: all 0.15s;
}

#angel-clear:hover {
    border-color: var(--matrix-red) !important;
    color: var(--matrix-red) !important;
}

/* ══════════════════════════════════════════════════════════════
   FOOTER — sistema info
══════════════════════════════════════════════════════════════ */

.terminal-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0;
    font-size: 0.6rem;
    color: var(--matrix-green-dim);
    letter-spacing: 1.5px;
    border-top: 1px solid var(--matrix-green-dim);
    margin-top: 8px;
}

.footer-left   { display: flex; gap: 16px; }
.footer-pulse  { animation: blink 2s step-start infinite; }

/* ══════════════════════════════════════════════════════════════
   RAIN CANVAS — lluvia matrix de fondo
══════════════════════════════════════════════════════════════ */

#matrix-rain {
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    z-index: -1;
    opacity: 0.08;
    pointer-events: none;
}

/* ══════════════════════════════════════════════════════════════
   HIDE GRADIO CHROME innecesario
══════════════════════════════════════════════════════════════ */

.gradio-container .prose h1,
footer.svelte-1rjryqp,
.built-with { display: none !important; }

/* Override Gradio defaults agresivos */
.gradio-container button,
.gradio-container input,
.gradio-container textarea {
    font-family: var(--font-mono) !important;
}

/* Eliminar bordes redondeados globales de Gradio */
.gradio-container .block,
.gradio-container .form {
    border-radius: 0 !important;
    border-color: var(--matrix-border) !important;
    background: transparent !important;
}
"""

# ── HTML extra (canvas rain + JS) ──────────────────────────────────────────

_HEADER_HTML = """
<canvas id="matrix-rain"></canvas>

<div class="main-container">
  <div class="terminal-header">
    <div class="header-inner">

      <div class="avatar-frame" id="avatar-frame">
        <!-- Imagen real: descomenta y pon la ruta a tu foto -->
         <img src="/file=assets/avatar.jpg" id="avatar-img" alt="Ángel Nácar"> 
        <div class="avatar-placeholder" id="avatar-placeholder">ÁN</div>
      </div>

      <div class="header-info">
        <div class="header-title">Ángel Nácar Jiménez</div>
        <div class="header-subtitle">Senior Software Developer &amp; Scrum Master</div>
        <div class="header-status">
          <span class="status-dot"></span>
          <span>SYSTEM ONLINE</span>
          <span style="margin-left:12px; color:var(--matrix-green-dim)">|</span>
          <span style="margin-left:12px">MADRID, ES</span>
        </div>
      </div>

      <div class="header-meta">
        <div>Java · Cloud · IA</div>
        <div>9+ YRS EXP</div>
        <div style="color:var(--matrix-green-3); margin-top:4px">AWS CERTIFIED</div>
      </div>

    </div>
  </div>
</div>

<script>
// ── Matrix rain ──────────────────────────────────────────────
(function(){
  const canvas = document.getElementById('matrix-rain');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*()アイウエオカキクケコサシスセソタチツテトナニヌネノ';
  let cols, drops;

  function resize(){
    canvas.width  = window.innerWidth;
    canvas.height = window.innerHeight;
    cols  = Math.floor(canvas.width / 16);
    drops = Array(cols).fill(1);
  }

  function draw(){
    ctx.fillStyle = 'rgba(0,0,0,0.05)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    for (let i = 0; i < cols; i++){
      const ch = chars[Math.floor(Math.random() * chars.length)];
      // Primer carácter de cada columna más brillante
      const isHead = drops[i] * 16 < 32;
      ctx.fillStyle = isHead ? '#ffffff' : (Math.random() > 0.1 ? '#00ff41' : '#00cc33');
      ctx.font = '14px "Share Tech Mono", monospace';
      ctx.fillText(ch, i * 16, drops[i] * 16);

      if (drops[i] * 16 > canvas.height && Math.random() > 0.975){
        drops[i] = 0;
      }
      drops[i]++;
    }
  }

  resize();
  window.addEventListener('resize', resize);
  setInterval(draw, 45);
})();

// ── Avatar: muestra imagen real si carga correctamente ──────
(function(){
  const img = document.getElementById('avatar-img');
  const placeholder = document.getElementById('avatar-placeholder');
  if (!img || !placeholder) return;
  img.onload  = () => { img.style.display = 'block'; placeholder.style.display = 'none'; };
  img.onerror = () => { img.style.display = 'none';  placeholder.style.display = 'flex'; };
})();
</script>
"""

_TERMINAL_BAR_HTML = """
<div class="terminal-bar">
  <div class="terminal-bar-dots">
    <div class="terminal-bar-dot dot-red"></div>
    <div class="terminal-bar-dot dot-amber"></div>
    <div class="terminal-bar-dot dot-green"></div>
  </div>
  <div class="terminal-bar-title">angel_cv.exe — INTERACTIVE TERMINAL v2.0</div>
</div>
"""

_FOOTER_HTML = """
<div class="terminal-footer">
  <div class="footer-left">
    <span>SYS: ACTIVE</span>
    <span>MODEL: KIMI-K2</span>
    <span>EVAL: ENABLED</span>
  </div>
  <div>
    <span class="footer-pulse">█</span>
    <span style="margin-left:6px">AGUARDANDO INPUT...</span>
  </div>
</div>
"""

# ── Construcción de la interfaz ─────────────────────────────────────────────

def build_ui(chat_fn):
    """
    Construye y retorna el gr.Blocks con la interfaz Matrix.

    Uso:
        from ui import build_ui
        from chat_optimized import chat
        app = build_ui(chat)
        app.launch()
    """
    with gr.Blocks(
        css=_CSS,
        title="Ángel Nácar — CV Interactivo",
        theme=gr.themes.Base(
            primary_hue="green",
            neutral_hue="green",
            font=gr.themes.GoogleFont("Share Tech Mono"),
        ),
    ) as demo:

        # Header con canvas y rain
        gr.HTML(_HEADER_HTML)

        # Barra de título estilo terminal
        gr.HTML(_TERMINAL_BAR_HTML)

        # Ventana de chat
        chatbot = gr.Chatbot(
            elem_id="angel-chat",
            #type="messages",
            height=420,
            show_label=False,
            avatar_images=(
                 None,                         # usuario — sin avatar
                #  None,                         # bot — sin avatar (usamos ::before CSS)
                # Para habilitar tu foto real descomenta:
                 "assets/avatar.jpg",
            ),
            #bubble_full_width=True,
            #show_copy_button=False,
            placeholder=(
                "<div style='text-align:center; color:var(--matrix-green-3); "
                "font-family:var(--font-mono); padding:40px; letter-spacing:2px;'>"
                "[ SISTEMA LISTO — INICIANDO SESIÓN... ]<br><br>"
                "Pregúntame sobre mi experiencia, proyectos o stack tecnológico."
                "</div>"
            ),
        )

        # Zona de input
        with gr.Row(elem_classes=["input-zone"]):
            gr.HTML("<div class='input-prompt-label'>$&gt;&nbsp;</div>")

            msg_input = gr.Textbox(
                elem_id="angel-input",
                placeholder="Escribe tu mensaje y pulsa ENTER o SEND...",
                show_label=False,
                lines=1,
                max_lines=4,
                scale=10,
                submit_btn=False,
                autofocus=True,
            )

            send_btn = gr.Button(
                "SEND",
                elem_id="angel-submit",
                scale=1,
                min_width=70,
            )

            clear_btn = gr.Button(
                "CLR",
                elem_id="angel-clear",
                scale=1,
                min_width=50,
            )

        # Footer
        gr.HTML(_FOOTER_HTML)

        # ── Lógica de interacción ──────────────────────────────

        def respond(message: str, history: list):
            if not message or not message.strip():
                return history, ""
            history = history or []
            # Añadir mensaje del usuario
            history.append({"role": "user", "content": message})
            # Llamar al agente
            reply = chat_fn(message, history[:-1])
            history.append({"role": "assistant", "content": reply})
            return history, ""

        send_btn.click(
            fn=respond,
            inputs=[msg_input, chatbot],
            outputs=[chatbot, msg_input],
        )

        msg_input.submit(
            fn=respond,
            inputs=[msg_input, chatbot],
            outputs=[chatbot, msg_input],
        )

        clear_btn.click(
            fn=lambda: ([], ""),
            outputs=[chatbot, msg_input],
        )

    return demo


# ── Ejecución directa ───────────────────────────────────────────────────────

if __name__ == "__main__":
    # Importa el agente real
    try:
        from chat_optimized_Hybrid import chat
    except ImportError:
        # Stub para probar la UI de forma aislada
        def chat(message: str, history: list) -> str:
            return (
                f"[STUB] Recibido: {message!r}\n"
                "Conecta chat_optimized_Hybrid.py para activar el agente real."
            )

    app = build_ui(chat)
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        show_api=False,
    )
