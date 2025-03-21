
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

class TemplateTextToTextStudioBuilder:
    def __init__(self, url, token, isDev=True, data=None) -> None:
        self.msg_event = "Initialization started"
        self.status_code=444
        self.data=data
        self.Isdiv=isDev
        self.serviceId=""

        if isDev:
            self.builder = BuilderStudioModelAiSpeed(models_list)
            self.builderRequest = TemplateBuilderRequest(url, token, True)
            self.msg_event = "Development environment initialized"


        else:

            self.builder = BuilderStudioModelAiAPi(url,token)
            self.builderRequest = TemplateBuilderRequest(url, token, False)
            self.msg_event = "api  environment initialized"



        self.token = token

        self.url = url

        self.client = None

        print(f"Message event: {self.msg_event}")
        print(f"Status code: {self.status_code}")
    def get_data_chat_txt_model(self,data=[]):
       
           
            model_info = {
                "modelGateway": data.get("modelGateway", ""),
                "modelAi": data.get("modelAi", "wasmdashai/T2T"),
                "service": data.get("service", "/predict"),
                "token": data.get("token","AIzaSyC85_3TKmiXtOpwybhSFThZdF1nGKlxU5c"),
                "eventId": data.get("eventId", ""),
                "numberRequests": data.get("numberRequests", 0),
                "currentNumberRequests": data.get("currentNumberRequests", 0)
            }
            return model_info
         
         
    def handle_error(self, message, status_code):
        self.msg_event = message
        self.status_code = status_code
        if status_code >= 200 and status_code < 300:
            return {
                "status": "success",
                "message": message,
                "status_code": status_code
            }
        elif  status_code >= 400 and status_code < 500:
            self.builderRequest.send_event_request("string","string","failed")



            return {
                "status": "error",
                "message": message,
                "status_code": status_code
            }

        elif  status_code==602:
            print(f"Message event: {message}")
            print(f"Status code: {status_code}")

            return {
                "status": "error",
                "message": message,
                "status_code": status_code
            }
        elif status_code==11.1:
             print(f"Message event: {message}")
             print(f"Status code: {status_code}")
             return None
        elif status_code==33.1:
            return {
                "status": "error",
                "message": message,
                "status_code": status_code
            }




    def get_serviceId(self):
         if self.Isdiv:
            return "serv_3daa9b9b2f3a466eb15edecb415481af"
         else:

             #api_data = json.loads(self.data['api'])
             #service_ids = [api_data.get('ServiceId')]
             #return service_ids[0]

             return "serv_3daa9b9b2f3a466eb15edecb415481af"
    
    def ask_ai(self, message):

        if not message or message == "":

              self.msg_event = "Invalid input: Message is required"
              self.status_code = 11.1
              return self.handle_error(self.msg_event ,self.status_code)


        self.msg_event = "Request creation started"



        if not self.serviceId or self.serviceId == "":
             #self.msg_event = "Invalid input: serviceId is required"
             #self.status_code = 11.1
             #return self.handle_error(self.msg_event ,self.status_code)
             self.serviceId=self.get_serviceId()
        print(f"ServiceId: {self.serviceId}")

        request = self.builderRequest.Create_request(serviceId=self.serviceId)
        
        datarquest=self.get_data_chat_txt_model(data={})
        result = ""
        print(f"Request : {request}")
        print(f"msg_event: {self.builderRequest.msg_event}")



        if  request and request.get("status") == "success" and request.get("data")  :
            try:
                
                if self.client is None:

                    self.client = Client(datarquest['modelAi'])
                    self.msg_event = "Client initialized successfully"
                    self.status_code = 22.2
            except Exception as e:

                self.msg_event = f"Error initializing client: {e}"
                self.status_code = 22.3
                print(f"Error initializing client: {e}")
                self.client = Client(datarquest['modelAi'])

                #self.handle_error(f"Error initializing client: {e}", 22.3)

            try:

                result = self.client.predict(
                    #key=request["data"]["token"]
                    #api_name=request["data"]["service"]
                    text=message,
                    key=datarquest['token'],
                    api_name=datarquest['service']
                )


                if result!=None:
                    print(f"result: {result}")
                    self.msg_event = "predict completed successfully"
                    self.status_code = 222
                    event_id=request["data"]["eventId"]
                     
                    status=request["status"]



                    result_request=self.builderRequest.send_event_request(event_id,result,status)
                    print(f"result: {result_request}")
                    if result_request and result_request["status"]=="success":
                        self.msg_event = "predict completed successfully"
                        print(f"msg_event: {self.msg_event}")
                        print(self.msg_event)

                    else:
                        self.msg_event = "result send event request   None"
                        self.status_code =result_request['status_code']
                        print(f"msg_event: {self.msg_event}")
                        print(self.msg_event)
                        if self.Isdiv==False:
                            return self.handle_error(self.msg_event ,self.status_code)


                else:
                    self.msg_event = "result client predict None"
                    self.status_code =11.2
                    print(self.msg_event)
                    return self.handle_error(self.msg_event ,self.status_code)
            except Exception as e:

                self.msg_event = f"Error during prediction: {e}"
                self.status_code = 224
                print(f"Error during prediction: {e}")
                return self.handle_error(self.msg_event ,self.status_code)

        else:
            self.msg_event = "Request creation failed"
            self.status_code =request['status_code']
            return self.handle_error(self.msg_event ,self.status_code)


        #print(f"Event Status: {self.msg_event}")
        #print(f"Status code: {self.status_code}")




        return result



    def generate_audio(self,token,message):



        self.msg_event = "Audio generation started"
        self.status_code = 222
        try:
            client = Client("wasmdashai/RunTasking")
            result = client.predict(
                text=message,
                name_model="wasmdashai/vits-ar-sa-huba-v2",
                speaking_rate=0.8,
                api_name="/predict"
            )
            self.msg_event = "Audio generation completed successfully"
            self.status_code = 222
            return result
        except Exception as e:
            self.msg_event = f"Error during audio generation: {e}"
            self.status_code = 226
            print(f"Error during audio generation: {e}")
            self.handle_error(f"Error during audio generation: {e}", 226)
            return None






    # def add_message(self, history, message):
    #     for x in message["files"]:
    #         history.append({"role": "user", "content": {"path": x}})
    #     if message["text"] is not None:
    #         history.append({"role": "user", "content": message["text"]})
    #     return history, gr.MultimodalTextbox(value=None, interactive=False)

    def bot(self,message:str,model="",max_token=0.8,Temperature=1.0,streaming=True):

        self.msg_event = "Bot response generation started"
        response = self.ask_ai(message)
        if response is None:
            self.msg_event = "Bot response failed"
            print(f"Bot error event: {self.msg_event}")
            response=None
            return gr.MultimodalTextbox(interactive=False,value=None),None,bodyicon
        else:
        
          return gr.MultimodalTextbox(interactive=True,value=None),response,bodyicon
         


    def print_like_dislike(self, x: gr.LikeData, history):
        self.msg_event = f"Like/Dislike event triggered for index {x.index}"
        return self.generate_audio(history[x.index]["content"])
    
    def get_filter(self,FilterModelAI,returnName):
     
          if not FilterModelAI:
                  return None
              
          if returnName is None:
                    return None
          result=self.builder.get_filter(FilterModelAI,returnName)
          return result
 
    def update_languages(self, category):

        self.msg_event = f"Updating languages for category {category}"

        available_languages=self.get_filter(FilterModelAI(category=category),"language")
        return gr.update(choices=available_languages, value=[], visible=True)

    def update_dialects(self,category,language):

        self.msg_event = f"Updating dialects for language {language}"
        available_dialects=self.get_filter(FilterModelAI(category=category,language=language),"dialect")

        return gr.update(choices=available_dialects, value=[], visible=True)

    def update_models(self, category,language,dialect):
        self.msg_event = f"Updating models for dialect {dialect}"
        default_model=self.get_filter(FilterModelAI(category=category,language=language,dialect=dialect),"name")
        self.msg_event = f"Updating models for dialect {dialect}"

        first_value = default_model[0] if default_model and isinstance(default_model, list) else None
        return gr.update(choices=default_model, value=first_value,visible=True)


    def createapp(self, data=None, language="en"):

        self.msg_event = f"Creating app for language {language}"
        print(self.msg_event )
        self.data = data
        with gr.Column() as service_dashboard:
            createTextToText(self)
            #print(data)



        return service_dashboard





class TemplateTextToTextBuilder:
    def __init__(self, url, token, isDev=True, data=None) -> None:
        self.msg_event = "Initialization started"
        self.status_code=444
        self.data=data
        self.Isdiv=isDev
        self.serviceId=""

        if isDev:
            self.builder = BuilderStudioModelAiSpeed(models_list)
            self.builderRequest = TemplateBuilderRequest(url, token, True)
            self.msg_event = "Development environment initialized"


        else:

            self.builder = BuilderStudioModelAiAPi(url,token)
            self.builderRequest = TemplateBuilderRequest(url, token, False)
            self.msg_event = "api  environment initialized"



        self.token = token

        self.url = url

        self.client = None

        print(f"Message event: {self.msg_event}")
        print(f"Status code: {self.status_code}")
    def get_data_chat_txt_model(self,data=[]):
       
           
            model_info = {
                "modelGateway": data.get("modelGateway", ""),
                "modelAi": data.get("modelAi", "wasmdashai/T2T"),
                "service": data.get("service", "/predict"),
                "token": data.get("token","AIzaSyC85_3TKmiXtOpwybhSFThZdF1nGKlxU5c"),
                "eventId": data.get("eventId", ""),
                "numberRequests": data.get("numberRequests", 0),
                "currentNumberRequests": data.get("currentNumberRequests", 0)
            }
            return model_info
         
         
    def handle_error(self, message, status_code):
        self.msg_event = message
        self.status_code = status_code
        if status_code >= 200 and status_code < 300:
            return {
                "status": "success",
                "message": message,
                "status_code": status_code
            }
        elif  status_code >= 400 and status_code < 500:
            self.builderRequest.send_event_request("string","string","failed")



            return {
                "status": "error",
                "message": message,
                "status_code": status_code
            }

        elif  status_code==602:
            print(f"Message event: {message}")
            print(f"Status code: {status_code}")

            return {
                "status": "error",
                "message": message,
                "status_code": status_code
            }
        elif status_code==11.1:
             print(f"Message event: {message}")
             print(f"Status code: {status_code}")
             return None
        elif status_code==33.1:
            return {
                "status": "error",
                "message": message,
                "status_code": status_code
            }




    def get_serviceId(self):
         if self.Isdiv:
            return "serv_3daa9b9b2f3a466eb15edecb415481af"
         else:

             #api_data = json.loads(self.data['api'])
             #service_ids = [api_data.get('ServiceId')]
             #return service_ids[0]

             return "serv_3daa9b9b2f3a466eb15edecb415481af"
    
    def ask_ai(self, message):

        if not message or message == "":

              self.msg_event = "Invalid input: Message is required"
              self.status_code = 11.1
              return self.handle_error(self.msg_event ,self.status_code)


        self.msg_event = "Request creation started"



        if not self.serviceId or self.serviceId == "":
             #self.msg_event = "Invalid input: serviceId is required"
             #self.status_code = 11.1
             #return self.handle_error(self.msg_event ,self.status_code)
             self.serviceId=self.get_serviceId()
        print(f"ServiceId: {self.serviceId}")

        request = self.builderRequest.Create_request(serviceId=self.serviceId)
        
        datarquest=self.get_data_chat_txt_model(data={})
        result = ""
        print(f"Request : {request}")
        print(f"msg_event: {self.builderRequest.msg_event}")



        if  request and request.get("status") == "success" and request.get("data")  :
            try:
                
                if self.client is None:

                    self.client = Client(datarquest['modelAi'])
                    self.msg_event = "Client initialized successfully"
                    self.status_code = 22.2
            except Exception as e:

                self.msg_event = f"Error initializing client: {e}"
                self.status_code = 22.3
                print(f"Error initializing client: {e}")
                self.client = Client(datarquest['modelAi'])

                #self.handle_error(f"Error initializing client: {e}", 22.3)

            try:

                result = self.client.predict(
                    #key=request["data"]["token"]
                    #api_name=request["data"]["service"]
                    text=message,
                    key=datarquest['token'],
                    api_name=datarquest['service']
                )


                if result!=None:
                    print(f"result: {result}")
                    self.msg_event = "predict completed successfully"
                    self.status_code = 222
                    event_id=request["data"]["eventId"]
                     
                    status=request["status"]



                    result_request=self.builderRequest.send_event_request(event_id,result,status)
                    print(f"result: {result_request}")
                    if result_request and result_request["status"]=="success":
                        self.msg_event = "predict completed successfully"
                        print(f"msg_event: {self.msg_event}")
                        print(self.msg_event)

                    else:
                        self.msg_event = "result send event request   None"
                        self.status_code =result_request['status_code']
                        print(f"msg_event: {self.msg_event}")
                        print(self.msg_event)
                        if self.Isdiv==False:
                            return self.handle_error(self.msg_event ,self.status_code)


                else:
                    self.msg_event = "result client predict None"
                    self.status_code =11.2
                    print(self.msg_event)
                    return self.handle_error(self.msg_event ,self.status_code)
            except Exception as e:

                self.msg_event = f"Error during prediction: {e}"
                self.status_code = 224
                print(f"Error during prediction: {e}")
                return self.handle_error(self.msg_event ,self.status_code)

        else:
            self.msg_event = "Request creation failed"
            self.status_code =request['status_code']
            return self.handle_error(self.msg_event ,self.status_code)


        #print(f"Event Status: {self.msg_event}")
        #print(f"Status code: {self.status_code}")




        return result



    def generate_audio(self,token,message):



        self.msg_event = "Audio generation started"
        self.status_code = 222
        try:
            client = Client("wasmdashai/RunTasking")
            result = client.predict(
                text=message,
                name_model="wasmdashai/vits-ar-sa-huba-v2",
                speaking_rate=0.8,
                api_name="/predict"
            )
            self.msg_event = "Audio generation completed successfully"
            self.status_code = 222
            return result
        except Exception as e:
            self.msg_event = f"Error during audio generation: {e}"
            self.status_code = 226
            print(f"Error during audio generation: {e}")
            self.handle_error(f"Error during audio generation: {e}", 226)
            return None






    # def add_message(self, history, message):
    #     for x in message["files"]:
    #         history.append({"role": "user", "content": {"path": x}})
    #     if message["text"] is not None:
    #         history.append({"role": "user", "content": message["text"]})
    #     return history, gr.MultimodalTextbox(value=None, interactive=False)

    def bot(self,message:str,model="",max_token=0.8,Temperature=1.0,streaming=True):

        self.msg_event = "Bot response generation started"
        response = self.ask_ai(message)
        if response is None:
            self.msg_event = "Bot response failed"
            print(f"Bot error event: {self.msg_event}")
            response=None
            return gr.MultimodalTextbox(interactive=False,value=None),None,bodyicon
        else:
        
          return gr.MultimodalTextbox(interactive=True,value=None),response,bodyicon
         


    def print_like_dislike(self, x: gr.LikeData, history):
        self.msg_event = f"Like/Dislike event triggered for index {x.index}"
        return self.generate_audio(history[x.index]["content"])
    
    def get_filter(self,FilterModelAI,returnName):
     
          if not FilterModelAI:
                  return None
              
          if returnName is None:
                    return None
          result=self.builder.get_filter(FilterModelAI,returnName)
          return result
 
    def update_languages(self, category):

        self.msg_event = f"Updating languages for category {category}"

        available_languages=self.get_filter(FilterModelAI(category=category),"language")
        return gr.update(choices=available_languages, value=[], visible=True)

    def update_dialects(self,category,language):

        self.msg_event = f"Updating dialects for language {language}"
        available_dialects=self.get_filter(FilterModelAI(category=category,language=language),"dialect")

        return gr.update(choices=available_dialects, value=[], visible=True)

    def update_models(self, category,language,dialect):
        self.msg_event = f"Updating models for dialect {dialect}"
        default_model=self.get_filter(FilterModelAI(category=category,language=language,dialect=dialect),"name")
        self.msg_event = f"Updating models for dialect {dialect}"

        first_value = default_model[0] if default_model and isinstance(default_model, list) else None
        return gr.update(choices=default_model, value=first_value,visible=True)


    def createapp(self, data=None, language="en"):

        self.msg_event = f"Creating app for language {language}"
        print(self.msg_event )
        self.data = data
        with gr.Column() as service_dashboard:
            create_t2text(self)
            #print(data)



        return service_dashboard
