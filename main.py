from fastapi import FastAPI
import gradio as gr
from fastapi.responses import RedirectResponse

from gradio_ui import demo
import t2speech
import t2text
import chatbot
import dashboard
import t2speechmuit
import userspace
from ui import dash
import audio_interface
app = FastAPI()

@app.get('/')
async def root():
    return 'Gradio app is running at /gradio', 200
@app.get("/redirect")
async def redirect_to_site():
    # إعادة التوجيه إلى موقع معين
    return RedirectResponse(url="http://lahja.runasp.net/services")




# app = gr.mount_gradio_app(app, demo, path='/studio-t2speech')
# app = gr.mount_gradio_app(app, t2speech.demo, path='/t2speech')

# app = gr.mount_gradio_app(app, t2text.demo, path='/studio-t2text')

# app = gr.mount_gradio_app(app, dash.demo, path='/dash')

# app = gr.mount_gradio_app(app, chatbot.demo, path='/chatbot')
# app = gr.mount_gradio_app(app, dashboard.dashboard, path='/dashboard')
# app = gr.mount_gradio_app(app, t2speechmuit.demo, path='/t2speechmuit')
# app = gr.mount_gradio_app(app, userspace.app, path='/createspace')

# app = gr.mount_gradio_app(app, audio_interface.demo, path='/manger-audio')



from apps.ui_apps import APPS
for uiapp,path in APPS:
    app = gr.mount_gradio_app(app, uiapp, path="/"+path)

    
