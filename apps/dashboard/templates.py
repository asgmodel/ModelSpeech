from .seeds import *
from .data import *
from .builders import *
import gradio as gr
from gradio_client import Client
import pandas as pd
from random import randint
import plotly.express as px
import time
from typing import Optional, Text
from .components import *

class TamplateDashBuilder:
    __translation__ = {}

    def __init__(self, url, token, isDev=False) -> None:
        print("Initializing TamplateDashBuilder...")
        try:
            if isDev:
                self.builder = BuilderDashAPISeed()
            else:
                self.builder = BuilderDashAPI(url, token)
            self.token = token
            print("Builder initialized successfully.")
        except Exception as e:
            print(f"Error initializing builder: {e}")
            raise

    def get_data_byservices(self):
        print("Fetching data by services...")
        try:
            value, label = self.builder.get_data_byservices()
            return value, label
            #return plotpie(value, label)
        except Exception as e:
            print(f"Failed to fetch service data: {e}")

    def get_model_ai_service_requests(self):
        print("Fetching AI service requests...")
        try:
            value, label = self.builder.get_model_ai_service_requests()
            return value, label
            #return plotpie(value, label)
        except Exception as e:
            print(f"Failed to fetch AI service requests: {e}")

    def get_space_requests(self):
        print("Fetching space requests...")
        try:
            return self.builder.get_space_requests()
        except Exception as e:
            print(f"Failed to fetch space requests: {e}")

    def get_service_users_count(self):
        print("Fetching service users count...")
        try:
            value, label = self.builder.get_service_users_count()
            return value, label
        except Exception as e:
            print(f"Failed to fetch service users count: {e}")

    def get_service_usage_and_remaining(self):
        print("Fetching service usage and remaining data...")
        try:
            value, label, remaining = self.builder.get_service_usage_and_remaining()
            return value, label
            #return plotpie(value, label)
        except Exception as e:
            print(f"Failed to fetch service usage data: {e}")

    def get_data_byplan_services(self):
        print("Fetching data by plan services...")
        try:
            return self.builder.get_data_byplan_services()
        except Exception as e:
            print(f"Failed to fetch plan services data: {e}")


    def get_model_name_request_bytime(self, serviceType="all", start="2025-02-14T23:07:29.795Z", end="2025-03-05T23:07:29.795Z", time="None"):
        print(f"Fetching model name requests from {start} to {end or 'now'}...")
        try:
            return self.builder.get_model_name_request_bytime(serviceType, start, end, time)
        except Exception as e:
            print(f"Failed to fetch model requests by time: {e}")

    def post_service_requests(self, request_data):
        print("Posting service request...")
        try:
            return self.builder.post_service_requests(request_data)
        except Exception as e:
            print(f"Failed to post service request: {e}")

    def get_staterequests(self):
        print("Fetching state requests...")
        try:
            return self.builder.get_staterequests()
        except Exception as e:
            print(f"Failed to fetch state requests: {e}")

    def get_stateerrors(self):
        print("Fetching state errors...")
        try:
            return self.builder.get_stateerrors()
        except Exception as e:
            print(f"Failed to fetch state errors: {e}")

    def get_service_usage_and_remaining_plot(self):
        print("Fetching and plotting service usage and remaining data...")
        try:
            return self.builder.get_service_usage_and_remaining_plot()

        except Exception as e:
            print(f"Failed to fetch and plot service usage data: {e}")

    def ge_by_filter(self, start, end):
        print(f"Fetching data by filter from {start} to {end}...")
        try:
            return self.builder.ge_by_filter(start, end)
        except Exception as e:
            print(f"Failed to fetch filtered data: {e}")



    def createapp(self, data=None, language="en"):
        print("Creating the dashboard app...")
        try:
            labels = TRANSLATIONS[language]
            gr.HTML(Style)
            with gr.Column() as service_dashboard:
                create_section_state(self, labels)

                create_section_bytime(self, labels)
                create_section_by_all_services(self, labels)
            print("Dashboard app created successfully.")
            return service_dashboard
        except Exception as e:
            print(f"Failed to create dashboard app: {e}")
            raise
