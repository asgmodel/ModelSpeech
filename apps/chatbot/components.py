
bodyiconchat = """
    <style>
      :root {
    --name: default;

    --primary-500: rgba(11, 186, 131, 1);
    }
      .shadow-primary {
        box-shadow: 0 4px 8px rgba(0, 123, 255, 0.25);
      }
      .icon-xxl {
        width: 170px;
        height: 170px;
        line-height: 6.8rem;
        align-items: center;
      }
      .icon-md, .icon-lg, .icon-xl, .icon-xxl {
        display: flex;
        justify-content: center;
        align-items: center;
        border-radius: 50%;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        background-color: #ffffff;
      }
      .flex-shrink-0 {
        flex-shrink: 0 !important;
      }
      .rounded-circle {
        border-radius: 50% !important;
      }
      .text-center {
        text-align: center;
      }
      .mud-icon-root.mud-svg-icon {
        fill: rgba(11,186,131,1);
      }
      .mud-icon-size-large {
        font-size: 4.25rem !important;
        width: 7.25rem !important;
        height: 7.25rem !important;
      }
      .mud-success-text {
        color: rgba(11,186,131,1);
      }
      .icon-cont-center {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;

      }
      .built-with.svelte-sar7eh.svelte-sar7eh.svelte-sar7eh {
        display:none !important;
      }
     footer.svelte-sar7eh.svelte-sar7eh.svelte-sar7eh {
    position: fixed;
    right: 20px;
    top: 0;
}
       .gap.svelte-vt1mxs {
    gap: 8px !important;
}
    </style>

"""
users = [("admin", "password123"), ("user", "userpass")]



from .data import *
from .models import *

import gradio as gr
from gradio_client import Client
import pandas as pd
from random import randint
import plotly.express as px
import time
from typing import Optional

def createchat(builder, lg="en"):
    try:
        print(f"Creating chat")
        #m_category=builder.get_filter(FilterModelAI(type="Chat"),"category")

        m_category = builder.builder.get_property("category")
        if m_category is None:
            m_category = []
         
        #m_category=None
        current_language = lg

        with gr.Blocks() as panel:
            with gr.Row():
                with gr.Column(scale=1):
                    with gr.Accordion(LANGUAGES[current_language]["options"]):
                        category_dropdown = gr.Dropdown(
                            choices=m_category,
                            label=LANGUAGES[current_language]["category"],
                            value=[],
                            info=LANGUAGES[current_language]["choose_category"]

                        )
                        language_dropdown = gr.Dropdown(
                            choices=[],
                            label=LANGUAGES[current_language]["language"],
                            value=[],
                            visible=False,
                            info=LANGUAGES[current_language]["choose_language"]
                        )
                        dialect_dropdown = gr.Dropdown(
                            choices=[],
                            label=LANGUAGES[current_language]["dialect"],
                            value=[],
                            visible=False,
                            info=LANGUAGES[current_language]["choose_dialect"]
                        )
                        model_dropdown = gr.Dropdown(

                            label=LANGUAGES[current_language]["model_name"],
                            value=[],
                            visible=False,
                            interactive=True,
                            info=LANGUAGES[current_language]["choose_model"]
                        )

                    with gr.Accordion(LANGUAGES[current_language]["settings"]):
                        temperature_slider = gr.Slider(
                            label=LANGUAGES[current_language]["temperature"],
                            minimum=0.1, maximum=5, step=0.1, value=0.7
                        )
                        speech_rate_slider = gr.Slider(
                            label=LANGUAGES[current_language]["max_token"],
                            minimum=50, maximum=120000, step=50, value=1024
                        )
                        streaming_toggle = gr.Checkbox(
                            label=LANGUAGES[current_language]["streaming"],
                            value=True
                        )

                with gr.Column(scale=3):
                    gr.HTML(bodyiconchat)
                    out_audio = gr.Audio(label=LANGUAGES[current_language]["voice_output"], autoplay=True, visible=False)

                    chatbot = gr.Chatbot(elem_id="chatbot", bubble_full_width=False, type="messages")

                    chat_input = gr.MultimodalTextbox(
                        interactive=True,
                        file_count="multiple",
                        placeholder=LANGUAGES[current_language]["enter_message"],
                        show_label=False,
                        sources=["microphone", "upload"],
                        lines=3,
                        max_lines=3
                    )

                    category_dropdown.change(
                        builder.update_languages, inputs=[category_dropdown], outputs=[language_dropdown]
                    )

                    language_dropdown.change(
                        builder.update_dialects, inputs=[category_dropdown,language_dropdown], outputs=[dialect_dropdown]
                    )
                    dialect_dropdown.change(
                        builder.update_models, inputs=[category_dropdown,language_dropdown,dialect_dropdown], outputs=[model_dropdown]
                    )

                    chat_msg = chat_input.submit(
                        builder.add_message, [chatbot, chat_input], [chatbot, chat_input]
                    )
                    bot_msg = chat_msg.then(builder.bot, chatbot, chatbot, api_name="bot_response")
                    bot_msg.then(lambda: gr.MultimodalTextbox(interactive=True), None, [chat_input])

        return panel

    except Exception as e:
        print(f"An error occurred: {e}")
        #print(f"Error message: {str(Builder.builder.)}"
        # هنا يمكن إضافة معالجة خطأ إضافية أو إرسال رسالة خطأ خاصة
        return None  # إعادة None في حال حدوث استثناء

