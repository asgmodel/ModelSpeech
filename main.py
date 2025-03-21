from fastapi import FastAPI
import gradio as gr
from fastapi.responses import RedirectResponse


import t2speechmuit

import audio_interface
app = FastAPI()

@app.get('/')
async def root():
    return 'Gradio app is running at /gradio', 200
@app.get("/redirect")
async def redirect_to_site():
    # إعادة التوجيه إلى موقع معين
    return RedirectResponse(url="http://lahja.runasp.net/services")








app = gr.mount_gradio_app(app, t2speechmuit.demo, path='/t2speechmuit')


app = gr.mount_gradio_app(app, audio_interface.demo, path='/manger-audio')



from apps.ui_apps import APPS
for uiapp,path in APPS:
    app = gr.mount_gradio_app(app, uiapp, path="/"+path)

from apps.api_routers import APIS
for router,path in  APIS:
     app.include_router(router, prefix=f"/api/{path}")

    
