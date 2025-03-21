 

import gradio as gr
from gradio_client import Client
import pandas as pd
from random import randint
import plotly.express as px
import time
from typing import Optional


def create_space_compoent(builder):
    with gr.Blocks() as panel:
        gr.Markdown("# Add New Hugging Face Space")
        gr.Markdown("Use this interface to add a new Space with customizable specifications.")

        with gr.Row():
            username = gr.Textbox(label="Username", placeholder="Enter your username")
            space_name = gr.Textbox(label="Space Name", placeholder="Enter a name for your Space")

        with gr.Row():
            choices = builder.get_type_plan()
            plan_type = gr.Radio(
                choices=choices,
                label="Plan Type",
                value=choices[0],
                interactive=True
            )


        with gr.Row():
            choices = builder.get_hardware()
            hardware_type = gr.Dropdown(
                choices=choices,
                label="Hardware Type",
                value=choices[0]
            )


            ram_size = gr.Slider(
                **builder.get_size_ram()
            )


            storage_size = gr.Slider(
                **builder.get_size_storage()
            )


            gpu_enabled = gr.Checkbox(label="Enable GPU", value=False)


        submit_button = gr.Button("Create Space")
        output = gr.Textbox(label="Result")

        submit_button.click(
            fn=builder.createspace_compoent,
            inputs=[username, space_name, ram_size , hardware_type,storage_size, gpu_enabled],
            outputs=[output]
        )


    return panel


    def Update_space_compoent(builder):


      print("Building Update_space_compoent interface.")
      #create_space_compoent(self)

      DataUpdate = builder.getSspacesId_compoent("space_44c3091602ec4dfeb23b6aa3d39c8f70")
      with gr.Blocks() as panel:
          gr.Markdown("# Add New Hugging Face Space")
          gr.Markdown("Use this interface to add a new Space with customizable specifications.")

          with gr.Row():
              username = gr.Textbox(label="Username", placeholder="Enter your username",value=DataUpdate['name'])
              space_name = gr.Textbox(label="Space Name", placeholder="Enter a name for your Space",value=DataUpdate['description'])

          with gr.Row():
              choices=builder.get_type_plan()
              plan_type = gr.Radio(
                  choices=choices,
                  label="Plan Type",
                  value=choices[0],
                  interactive=True
              )

          with gr.Row():
              choices=builder.get_hardware()
              hardware_type = gr.Dropdown(
                  choices=choices,
                  label="Hardware Type",
                  value=choices[0]
              )
              ram_size = gr.Slider(
                **builder.get_size_ram()
              )
              storage_size = gr.Slider(
                **builder.get_size_storage()
              )
              gpu_enabled = gr.Checkbox(label="Enable GPU", value=DataUpdate['isGpu'])

          submit_button = gr.Button("Update")
          output = gr.Textbox(label="Result")

          submit_button.click(
              fn=builder.updateSpace_compoent,
              inputs=[username, space_name, ram_size , hardware_type,storage_size, gpu_enabled],
              outputs=[output]
          )