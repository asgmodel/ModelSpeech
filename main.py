from fastapi import FastAPI
import gradio as gr
from fastapi.responses import RedirectResponse
from gradio_client import Client
from pydantic import BaseModel
class ModelInput(BaseModel):
    model_name: str
    model_structure: str
    template_instructions: str

import t2speechmuit
import chataist
import audio_interface
import testc
app = FastAPI()

@app.get('/')
async def root():
    return 'Gradio app is running at /gradio', 200
@app.get("/redirect")
async def redirect_to_site():
    # إعادة التوجيه إلى موقع معين
    return RedirectResponse(url="http://lahja.runasp.net/services")




# نقطة النهاية لمعالجة الطلب
@app.post("/predict")
async def run_model(input_data: ModelInput):
    client = Client("wasmdashai/LAHJA-AI")
    result = client.predict(
            model_names_str=input_data.model_name,
            model_structure=input_data.model_structure,
            template_instructions=input_data.template_instructions,
            api_name="/render_outputs"
    )
    return {"result": result}





app = gr.mount_gradio_app(app, t2speechmuit.demo, path='/t2speechmuit')
app = gr.mount_gradio_app(app, testc.demo, path='/testc')
app = gr.mount_gradio_app(app, chataist.demo, path='/chat-pro')
app = gr.mount_gradio_app(app, audio_interface.demo, path='/studio-pro')



from apps.ui_apps import APPS
for uiapp,path in APPS:
    app = gr.mount_gradio_app(app, uiapp, path="/"+path)

from apps.api_routers import APIS
for router,path in  APIS:
     app.include_router(router, prefix=f"/api/{path}")

    
