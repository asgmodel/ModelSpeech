
from .seeds import *
from .builders import *
import gradio as gr
from gradio_client import Client
import pandas as pd
from random import randint
import plotly.express as px
import time
from typing import Optional, Text
from .components import *

 

class TemplateSpacePlatformBuilder:
    def __init__(self, url, token, is_dev=True, data=None) -> None:
        self.msg_event = None
        self.status_code = None
        self.Is_Div = is_dev
        self.data = data

        if not url or not token:

            self._raise_error("URL and Token must be provided.", 11.1)

        try:
            self.builder = SpaceDev(token) if is_dev else builderSpace(url, token)
            print(f"Initialized with {'SpaceDev' if is_dev else 'SpaceAPI'}.")

        except Exception as e:
            self._raise_error(f"Error during initialization: {str(e)}", 500)


    def _raise_error(self, message, status_code):
        self.msg_event = message
        self.status_code = status_code
        print(f"Error: {message} (Status code: {status_code})")
        if status_code == 11.1:
            raise ValueError(message)

    def _raise_exception(self, message, status_code):
          return {
                "status": "failed",
                "data": None,
                "message":  message,
                "details":"",
                "status_code": status_code
            }



    def _validate_space_inputs(self, name, description, ram, cpu_cores, disk_space, bandwidth):
        validations = [
            (isinstance(name, str) and name, "Name must be a non-empty string."),
            (isinstance(description, str) and description, "Description must be a non-empty string."),
            (isinstance(ram, int) and 1 <= ram <= 64, "RAM must be an integer between 1 and 64 GB."),
            (isinstance(cpu_cores, str) and cpu_cores , "CPU cores must be a positive  ."),
            (isinstance(disk_space, int) and disk_space > 0, "Disk space must be a positive integer."),
            (isinstance(bandwidth, int) and bandwidth > 0, "Bandwidth must be a positive integer.")
        ]
        for valid, msg in validations:
            if not valid:
                self._raise_error(msg, 11.1)


    def get_subscriptionId(self):
        try:
            print("Fetching subscription ID.")
            return "sub_1QzOMiKMQ7LabgRTl3DwSxAa"
        except Exception as e:
            self._raise_error(f"Error fetching subscription ID: {str(e)}", 500)

    def get_token(self):
        try:
            print("Fetching token.")
            return "string"
        except Exception as e:
            self._raise_error(f"Error fetching token: {str(e)}", 500)



    def createspace_compoent(self, name="Azdeen", description="Azdeen talal", ram=20, cpu_cores=3, disk_space=4,
                     is_gpu=True, is_global=True, bandwidth=4):
        try:

            self._validate_space_inputs(name, description, ram, cpu_cores, disk_space, bandwidth)
            subscription_id = self.get_subscriptionId()
            token = self.get_token()

            if not subscription_id or not token:
                self._raise_error("Failed to fetch subscriptionId or token.", 11.1)

            data = {
                "name": name,
                "description": description,
                "ram": ram,
                "cpuCores": 3, # cpu_cores error
                "diskSpace": disk_space,
                "isGpu": is_gpu,
                "isGlobal": is_global,
                "bandwidth": bandwidth,
                "token": token,
                "subscriptionId": subscription_id
            }



            result = self.create_space(data)

            if result.get("status") == "success":
                print("Space created successfully.")
                return result['data']
            else:
                self._raise_error("Error creating space.", result.get("status_code", 500))

        except Exception as e:
            self._raise_error(f"Error creating space: {str(e)}", 500)

    def updateSpace_compoent(self, name="Azdeen", description="Azdeen talal", ram=20, cpu_cores=3, disk_space=4,
                     is_gpu=True, is_global=True, bandwidth=4):
              try:


                  self._validate_space_inputs(name, description, ram, cpu_cores, disk_space, bandwidth)

                  data = {
                      "name": name,
                      "description": description,
                      "ram": ram,
                      "cpuCores": 3, # cpu_cores error
                      "diskSpace": disk_space,
                      "isGpu": is_gpu,
                      "isGlobal": is_global,
                      "bandwidth": bandwidth

                  }

                  result = self.update_space(data)
                  print(result)

                  if result.get("status") == "success":
                      print("Space created successfully.")
                      return result['data']
                  else:
                      self._raise_error("Error update space.", result.get("status_code", 500))

              except Exception as e:
                  self._raise_error(f"Error creating space: {str(e)}", 500)

    def get_spacesId(self):
        try:
            print("Fetching spaces ID.")
            return "space_c55725b462c54fed88f1de4ae9dff548"
        except Exception as e:
            self._raise_error(f"Error fetching spaces ID: {str(e)}", 500)

    def update_space(self,data):
            try:


                spacesId=self.get_spacesId()
                if not spacesId:
                     return self._raise_exception(f"Error id None: {str(e)}",500)


                result = self.builder.update_space(
                    spacesId,
                     data
                )

                return result

            except Exception as e:

                 return self._raise_exception(f"Error update space: {str(e)}",500)

    def create_space(self,data):
        try:



            if not data:
                return self._raise_exception("Failed data None", 11.1)


            # data = {
            #     "name": name,
            #     "description": description,
            #     "ram": ram,
            #     "cpuCores": 3, # cpu_cores error
            #     "diskSpace": disk_space,
            #     "isGpu": is_gpu,
            #     "isGlobal": is_global,
            #     "bandwidth": bandwidth,
            #     "token": token,
            #     "subscriptionId": subscription_id
            # }

            result = self.builder.create_space(data)
            return result



        except Exception as e:
            return self._raise_exception(f"Error creating space: {str(e)}",500)
            #self._raise_error(f"Error creating space: {str(e)}", 500)





    def get_hardware(self):
        return ['cpu-basic', 'cpu-upgrade', 't4-small', 't4-medium', 'a10g-small', 'a10g-large', 'a100-large']

    def get_sdk_version(self):
        return ["latest"]

    def get_type_plan(self):
        return ["Free", "Paid"]

    def get_private(self):
        return [True, False]

    def get_size_ram(self):
        return {"minimum": 1, "maximum": 64, "step": 1, "label": "RAM Size (GB)", "value": 2}

    def get_size_storage(self):
        return {"minimum": 5, "maximum": 500, "step": 5, "label": "Storage Size (GB)", "value": 5}


    def getSspacesId_compoent(self,id):
        try:

           if not id:
            self._raise_error("Failed to fetch spaceId.", 11.1)
            print(f"Fetching data for space with ID: {id}.")
           else:
              result=self.get_data_space_by_id(id)
              if result.get("status") == "success":
                  print("Space created successfully.")
                  return result['data']
              else:
                  self._raise_error("Error creating space.", result.get("status_code", 500))

        except Exception as e:
            self._raise_error(f"Error fetching space data: {str(e)}", 500)




    def get_data_space_by_id(self,id):
        print(f"Fetching data for space with ID: {id}.")
        try:
           if not id:
             return self._raise_exception("Failed to fetch spaceId.", 11.1)
             print(f"Fetching data for space with ID: {id}.")
           else:
              return self.builder.get_data_space_by_id(id)
        except Exception as e:
            return self._raise_exception("Failed to fetch spaceId.", 11.1)
            #self._raise_error(f"Error fetching space data: {str(e)}", 500)




    def createapp(self, data=None, language="en"):
            try:
                with gr.Column() as service_dashboard:

                    print("Building Gradio service dashboard interface.")
                    create_space_compoent(self)


                    #Update_space_compoent(self)  # Assuming you will define this function to handle update space component.
                return service_dashboard
            except Exception as e:
                return f"Error creating Gradio app: {str(e)}"
