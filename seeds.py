
translations = {
    "ar": {
        "start_date": "تاريخ البدء",
        "end_date": "تاريخ الانتهاء",
        "apply_btn": "تطبيق الفلتر",
        "group_by": "تجميع البيانات بواسطة",
        "aggregation": "طريقة التجميع",
        "requests_by_time_title": "الطلبات حسب الوقت",
        "errors_by_time_title": "الأخطاء حسب الوقت",
        "requests_by_service_title": "الطلبات حسب نوع الخدمة",
        "total_requests": "إجمالي الطلبات في الخطة الحالية",
        "remaining_requests": "الطلبات المتبقية",
        "none": "لا شيء",
        "30m": "30 دقيقة",
        "1h": "ساعة",
        "4h": "4 ساعات",
        "1d": "يوم",
        "requests_by_service": "الطلبات حسب نوع الخدمة",
        "errors_by_service": "الأخطاء حسب نوع الخدمة",
        "PlanRequestsVisualization":"أحصائية الخطة "
    },
    "en": {
        "start_date": "Start Date",
        "end_date": "End Date",
        "apply_btn": "Apply Filter",
        "group_by": "Group Data By",
        "aggregation": "Select Aggregation Method",
        "requests_by_time_title": "Requests Over Time",
        "errors_by_time_title": "Errors Over Time",
        "requests_by_service_title": "Requests by Service Type Over Time",
        "total_requests": "Total Requests in Current Plan",
        "remaining_requests": "Remaining Requests",
        "none": "None",
        "30m": "30 minutes",
        "1h": "1 hour",
        "4h": "4 hours",
        "1d": "1 day",
        "requests_by_service": "Requests by Service Type",
        "errors_by_service": "Errors by Service Type",
        "PlanRequestsVisualization": "Plan  Visualization"
    }
}
import pandas as pd
from random import randint
import gradio as gr
import plotly.express as px
from  typing import List

def plot_plan_data_services():

    labels =  ["Text to Speech", "Text to Dialect", "Speech to Speech"]
    values = [100, 200 ,200 ]

    # إنشاء المخطط باستخدام plotly
    fig = px.pie(
        names=labels,
        values=values,
        title="Service Usage and Status",
        hole=0.4,  # مخطط دائري مجوف
        color_discrete_sequence=["rgba(11, 186, 131, 1)", "#99CCFF","#559CCF"],
        height=300,
    )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',  # خلفية الورقة
        plot_bgcolor='rgba(0,0,0,0)',  # خلفية الرسم
        font_color='black'  # النص الأسود للوضع العادي (يتغير حسب الوضع الليلي)
    )
    return fig

def plot_plan_data():
    labels = ["Used Requests", "Remaining Requests"]
    values = [plan_data["current_plan_requests"], plan_data["remaining_requests"]]

    # إنشاء المخطط باستخدام plotly
    fig = px.pie(
        names=labels,
        values=values,
        title="Plan Requests Distribution",
        hole=0.4,  # مخطط دائري مجوف
        color_discrete_sequence=["rgba(11, 186, 131, 1)", "#99CCFF"],
        height=300,
    )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',  # خلفية الورقة
        plot_bgcolor='rgba(0,0,0,0)',  # خلفية الرسم
        font_color='black'  # النص الأسود للوضع العادي (يتغير حسب الوضع الليلي)
    )
    return fig


plan_data = {
    "current_plan_requests": 300,
    "remaining_requests": 150
}

service_data = pd.DataFrame(
    {
        "time": pd.date_range("2025-01-01", end="2025-01-05", periods=200),
        "requests": [randint(5, 20) for i in range(200)],
        "errors": [randint(0, 3) for i in range(200)],
        "service_type": ["Text to Speech", "Text to Dialect", "Speech to Speech"] * 66 + ["Text to Speech"] * 2,

    }
)
service_data_tod = pd.DataFrame(
    {

        "value": [100,50]*3,
        "TypeData": ["requests","errors"]*3,
        "service_type": ["Text to Speech", "Text to Dialect", "Speech to Speech"]*2 ,

    }
)

class  BuilderDashAPISeed:
    def __init__(self) -> None:
        pass

    def  get_data_byservices(self):
         labels =  ["Text to Speech", "Text to Dialect", "Speech to Speech"]
         values = [100, 200 ,200 ]




         return values,labels



    def  get_data_byplan(self):

        return self.get_data_byservices()

    def  get_stateerrors(self):
       return service_data

    def  get_staterequests(self):
        return service_data

    def  get_data_byplan_services(self):
        labels_servs = {
                      "label_dropdown":"Type Service",
                      "Type": "TypeData",
                      "x": "value",
                      "y": "service_type"
                  }
        return service_data_tod,labels_servs

    def  ge_by_filter(self,start,end):
        return service_data


