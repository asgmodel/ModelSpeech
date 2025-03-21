import pandas as pd
from random import randint
from .clients import *
from typing import List
 
from .seeds import  *
class BuilderDashAPI:
    def __init__(self, url, token, isDev=False) -> None:
        self.api = DashAPI(url, token)
        self.isDev = isDev

    def get_data_byservices(self):
        data = self.api.get_service_usage_data()
        labels = []
        values = []
        for i in data:
            labels.append(i["name"])
            values.append(i["usageCount"])
        return values, labels

    def get_model_ai_service_requests(self):
        data = self.api.get_model_ai_service_requests()
        labels = []
        values = []
        for i in data:
            labels.append(i["modelAi"])
            values.append(i["usageCount"])
        return values, labels






    def post_service_requests(self, request_data):
        request_data = {
                        "serviceType": "12345",
                        "dateTime": "67890",
                        "dateTimeFilter": "2025-03-01",

                      }
        return self.api.post_service_requests(request_data)

    def get_service_users_count(self):
        data = self.api.get_service_users_count()
        labels = []
        values = []
        for i in data:
            labels.append(i["serviceType"])
            values.append(i["count"])
        return values, labels

    # def  get_service_usage_and_remaining_plot(self):
    #       data=self.get_service_usage_and_remaining()
    #       transformed_data = []
    #       for item in data:
    #         transformed_data.append({"value": item["usageCount"], "TypeData": "requests", "service_type": item["name"]})
    #         transformed_data.append({"value": item["remaining"], "TypeData": "remaining", "service_type": item["name"]})



    #       labels_servs = {
    #                   "label_dropdown":"Type Service",
    #                   "Type": "TypeData",
    #                   "x": "value",
    #                   "y": "service_type"
    #               }
    #       return pd.DataFrame(transformed_data),labels_servs
    def get_service_usage_and_remaining_plot(self):
        try:
            data =self.api.get_service_usage_and_remaining()
            transformed_data = []
            for item in data:
                #transformed_data.append({"value": item["usageCount"], "TypeData": "requests", "service_type": item["name"]})
                transformed_data.append({"value":randint(5, 1000), "TypeData": "requests", "service_type": item["name"]})
                transformed_data.append({"value": item["remaining"], "TypeData": "remaining", "service_type": item["name"]})
                transformed_data.append({"value":randint(5, 100), "TypeData": "errors", "service_type": item["name"]})

            labels_servs = {
                "label_dropdown": "Type Service",
                "Type": "TypeData",
                "x": "value",
                "y": "service_type"
            }
            return pd.DataFrame(transformed_data), labels_servs
        except Exception as e:
            print(f"Error in get_service_usage_and_remaining_plot: {str(e)}")
            return pd.DataFrame(), {}  # إرجاع DataFrame فارغ وقاموس فارغ في حالة حدوث خطأ


    def get_service_usage_and_remaining(self):
        data = self.api.get_service_usage_and_remaining()
        labels = []
        values = []
        remainings=[]
        for i in data:
            labels.append(i["name"])
            values.append(i["usageCount"])
            remainings.append(i["remaining"])
        return values, labels,remainings





    def get_model_name_request_bytimee(self, serviceType="all", start="2025-02-14T23:07:29.795Z", end="2025-03-05T23:07:29.795Z", time="None"):
                  dataA = {
                      "serviceType": serviceType,
                      "startDate": start,
                      "endDate": end,
                      "dateTimeFilter":time
                  }


                  data = self.api.post_service_requests(dataA)


                  print(f"  data  : {data}")


                  if not isinstance(data, list):
                      #print("Unexpected data format:", data)
                      return pd.DataFrame(),[]

                  if not data:  # التحقق مما إذا كانت القائمة فارغة
                      print("No data received.")
                      return pd.DataFrame(),[]

                  print("Data received successfully.")


                  transformed_data = []
                  for item in data:

                        transformed_data.append({"value":item["value"], "TypeData": item["typeData"], "service_type": item["serviceType"]})
                        #transformed_data.append({"value": item["value"], "TypeData": "remaining", "service_type": item["name"]})
                        #transformed_data.append({"value":randint(5, 100), "TypeData": "errors", "service_type": item["name"]})

                      #if isinstance(entry, dict) and 'time' in entry:
                          #entry['time'] = pd.to_datetime(entry['time'])
                      #else:
                          #print(f"Skipping invalid entry: {entry}")



                  df = pd.DataFrame(transformed_data)
                  #df["time"]=pd.date_range("2025-01-01", end="2025-01-05", periods=len(df))



                  #df["time"]=pd.date_range("2025-01-01", end="2025-01-05", periods=len(df))
                  #df['requests'] = df['requests'].astype(int)
                  #df['errors'] = df['errors'].astype(int)

                  #df["time"]=pd.date_range("2025-01-01", end="2025-01-05", periods=len(df))
                  #df['requests'] = [randint(5, 20) for _ in range(len(df))]
                  #df['errors'] = [randint(0, 3) for _ in range(len(df))]


                  # if 'serviceType' in df.columns:
                  #     df['service_type'] = df['serviceType']
                  #     df.drop(columns=['serviceType'], inplace=True)


                  labels_service = {
                      "label_dropdown": "Type Service",
                      "Type": "service_type",
                      "x": "time",
                      "y":"requests"
                  }

                  return df, labels_service
    def get_model_name_request_bytime(self, serviceType="all", start="2025-02-14T23:07:29.795Z", end="2025-03-05T23:07:29.795Z", time="None"):
                  dataA = {
                      "serviceType": serviceType,
                      "startDate": start,
                      "endDate": end,
                      "dateTimeFilter":time
                  }


                  data = self.api.GetRequestsByDatetime(None)


                  print(f"  data  : {data}")


                  if not isinstance(data, list):
                      #print("Unexpected data format:", data)
                      return pd.DataFrame(),[]

                  if not data:  # التحقق مما إذا كانت القائمة فارغة
                      print("No data received.")
                      return pd.DataFrame(),[]

                  print("Data received successfully.")

                 



                   

                  df = pd.DataFrame(data)
                  df.rename(columns={'dateTime': 'time'}, inplace=True)
                  df.rename(columns={'name': 'service_type'}, inplace=True)

                  #df["time"]=
                  df["time"]=pd.date_range("2025-01-01", end="2025-01-05", periods=len(df))
                  df['requests'] = df['requests'].astype(int)
                  df['errors'] = df['errors'].astype(int)
                                    





                  #df['requests'] = df['requests'].astype(int)
                  #df['errors'] = df['errors'].astype(int)

                  #df["time"]=pd.date_range("2025-01-01", end="2025-01-05", periods=len(df))
                  #df['requests'] = [randint(5, 20) for _ in range(len(df))]
                  #df['errors'] = [randint(0, 3) for _ in range(len(df))]

                  # if 'dateTime' in df.columns:
                  #       df['time'] = df['dateTime']
                  #       df.drop(columns=['time'], inplace=True)
                  # else :
                  #       df['time'] = df['dateTime']
                  #       df.drop(columns=['time'], inplace=True)
                 
                  # if 'serviceType' in df.columns:
                  #       df['service_type'] = df['name']
                  #       df.drop(columns=['serviceType'], inplace=True)


                  labels_service = {
                      "label_dropdown":"Type Service",
                      "Type":"serviceType",
                      "x": "time",
                      "y": "requests"
                  } 

                  return df, labels_service
      





    def get_space_requests(self):
        data = self.api.get_space_requests()
        labels = []
        values = []
        for i in data:
            #labels.append(i["name"])
            labels.append(f"space{i}")
            values.append(i["usageCount"])
        return values, labels
