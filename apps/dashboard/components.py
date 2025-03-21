 

import gradio as gr
from gradio_client import Client
import pandas as pd
from random import randint
import plotly.express as px
import time
from typing import Optional


from .data import *
import pandas as pd
from random import randint
import gradio as gr
import plotly.express as px
Style = """
    <style>
      :root {
    --name: default;

    --primary-500: rgba(11, 186, 131, 1);
    }
    """
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
        "TypeData": ["requests","remaining"]*3,
        "service_type": ["Text to Speech", "Text to Dialect", "Speech to Speech"]*2 ,

    }
)
import plotly.express as px
import gradio as gr

def change_filter(service_type, data, name_type="Type"):
    try:
        print(name_type)
        if service_type == "all":
            return data
        else:
            return data[data[name_type] == service_type]
    except Exception as e:
        print(f"Error in change_filter: {str(e)}")
        return data  # إرجاع البيانات الأصلية في حالة حدوث خطأ

def createPlotCard(data, labels, type_chart="bar"):
    try:
        if type_chart == "bar":
            return gr.BarPlot(data, x=labels["x"], y=labels["y"], color=labels["Type"])
        else:
            return gr.LinePlot(data, x=labels["x"], y=labels["y"], color=labels["Type"])
    except Exception as e:
        print(f"Error in createPlotCard: {str(e)}")
        return None  # في حالة حدوث خطأ، لا يتم إرجاع أي مخطط

def BarServiceCard(data, labels=None, titel="Bar Service", type_chart="bar"):
    try:
        if data is None or data.empty:
            print("Warning: Data is empty or None in BarServiceCard")
            return gr.Accordion(titel), None, None

        if labels is None:
            labels = {
                "label_dropdown": "Type",
                "Type": "Type",
                "x": "x",
                "y": "y"
            }

        with gr.Accordion(titel) as panel:
            dropdownchart = gr.Radio(["bar", "line"], value=type_chart, label="Chart Type")

            if labels["Type"] in data.columns and not data[labels["Type"]].empty:
                dropdown_choices = ["all"] + list(data[labels["Type"]].unique())
            else:
                dropdown_choices = ["all"]

            dropdown = gr.Dropdown(choices=dropdown_choices, label=labels["label_dropdown"])

            dashplot = createPlotCard(data, labels, type_chart)

            dropdown.change(
                fn=lambda service_type: change_filter(service_type, data, labels["Type"]) if data is not None else None,
                inputs=dropdown,
                outputs=dashplot
            )

            dropdownchart.change(
                fn=lambda type_chart: createPlotCard(data, labels, dropdownchart) if data is not None else None,
                inputs=dropdownchart,
                outputs=dashplot
            )

        return panel, dashplot, dropdown
    except Exception as e:
        print(f"Error in BarServiceCard: {str(e)}")
        return None, None, None  # في حالة حدوث خطأ، إرجاع عناصر فارغة





def plotpie(values, labels, title="Plan Requests Distribution",
            hole=0.4,
            color_discrete_sequence=["rgba(11, 186, 131, 1)", "#99CCFF"],
            height=300):
    try:
        fig = px.pie(
            names=labels,
            values=values,
            title=title,
            hole=hole,
            color_discrete_sequence=color_discrete_sequence,
            height=height,
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='black'
        )
        return fig
    except Exception as e:
        print(f"Error in plotpie: {str(e)}")
        return None  # إرجاع `None` في حالة حدوث خطأ



def creatBarplotgroup(data, labels,plot_type="BarPlot"):
    try:
        with gr.Row():
            # مخطط الطلبات
            
            if plot_type =="LinePlot":
                requests_by_time = gr.LinePlot(
                    data,
                    x="time",
                    y="requests",
                    title=labels["requests_by_time_title"]
                )
                errors_by_time = gr.LinePlot(
                data,
                x="time",
                y="errors",
                title=labels["errors_by_time_title"]
            )
            elif plot_type == "BarPlot":
                  requests_by_time = gr.BarPlot(
                    data,
                    x="time",
                    y="requests",
                    title=labels["requests_by_time_title"]
                )
                  errors_by_time = gr.BarPlot(
                data,
                x="time",
                y="errors",
                title=labels["errors_by_time_title"]
            )
            else:
                    raise ValueError(f"Unsupported plot type: {plot_type}")
           
               
                

          

        return requests_by_time, errors_by_time



    except Exception as e:
        print(f"Error in creatBarplotgroup: {str(e)}")
        return None, None 
       
import gradio as gr

def create_section_state(builder, labels):
    def check_and_plot(value, label,name ,error_message="البيانات الخاصة بالخدمة غير موجودة أو فارغة."):
        if not value or not label:
            raise ValueError(error_message)
        return plotpie(value, label, labels[name])

    try:
        with gr.Accordion(labels["PlanRequestsVisualization"]) as plan:
            with gr.Row():
                with gr.Column(scale=1):
                    value, label = builder.get_service_users_count()
                    data_byservices = check_and_plot(value, label,"total_requests")
                    plotservice = gr.Plot(data_byservices)

                with gr.Column(scale=1):
                    value, label = builder.get_model_ai_service_requests()
                    model_ai_service_requests = check_and_plot(value, label,"remaining_requests")
                    plotpiereq = gr.Plot(model_ai_service_requests)

                with gr.Column(scale=1):
                    value, label = builder.get_service_users_count()
                    service_users_count = check_and_plot(value, label,"total_requests")
                    gr.Plot(service_users_count)
                # with gr.Column(scale=1):
                #     value, label = builder.get_space_requests()
                #     service_users_count = check_and_plot(value, label,"total_requests")
                #     gr.Plot(service_users_count)

        return plan
    except Exception as e:
        print(f"حدث خطأ: {e}")
        return f"حدث خطأ أثناء تحميل البيانات: {e}"

options = ["all","Space","Service", "Model"]


optionservice=["All","service1", "service2"]
optionsmodel=["all","Requests", "Errors"]

def show_description(selected_item):
     if selected_item == "all":
          return gr.update(visible=False,choices=[])
     else:
        return gr.update(visible=True,choices=optionservice)

def create_section_bytime(builder, labels):
    try:

        with gr.Accordion(labels["apply_btn"]) as panel:
            try:


                with gr.Row():
                    start = gr.DateTime("2025-01-01 00:00:00", label=labels["start_date"])
                    end = gr.DateTime("2025-01-05 00:00:00", label=labels["end_date"])
                    combox_spce = gr.Dropdown(
                      interactive=True, 
                      choices=options, 
                      label="Select from the Space",
                        
                      
                  )
                    


                    combox_services = gr.Dropdown(
                        choices=options, 
                        visible=False,
                        label="Select from the services",
                        interactive=True,  
                        
                    )
                    combox_models= gr.Dropdown(
                        choices=options, 
                        visible=False,
                        label="Select from the models",
                        interactive=True,  
                        

                    )
               
                    apply_btn = gr.Button(labels["apply_btn"], scale=0)

                with gr.Row():
                    group_by = gr.Radio(
                        [labels["none"], labels["30m"], labels["1h"], labels["4h"], labels["1d"]],
                        value=labels["none"], label=labels["group_by"]
                    )
                    aggregate = gr.Radio(
                        ["sum", "mean", "median", "min", "max"],
                        value="sum", label=labels["aggregation"]
                    )
            except Exception as e:
                print(f" Error in creating UI components: {str(e)}")

            try:
                data, labels_service = builder.get_model_name_request_bytime()

                requests_by_time, errors_by_time = creatBarplotgroup(data, labels,plot_type="BarPlot")



                labels_service = {
                      "label_dropdown": "Type Service",
                      "Type": "service_type",
                      "x": "time",
                      "y": "requests"
                  }
                panel, dashplot, dropdowntypeservce = BarServiceCard(data, labels_service, labels["requests_by_time_title"])

                labels_servicee = {
                      "label_dropdown": "Type Service",
                      "Type": "service_type",
                      "x": "time",
                      "y": "errors"
                  }

                panel1, dashplot1, dropdowntypeservce1 = BarServiceCard(data, labels_servicee, labels["requests_by_time_title"])

                time_graphs = [requests_by_time, errors_by_time]



            except Exception as e:
                print(f" Error in fetching and processing data: {str(e)}")

            def change_group_by(group):
                try:
                    return [gr.LinePlot(x_bin=None if group == labels["none"] else group)] * len(time_graphs)
                except Exception as e:
                    print(f" Error in change_group_by: {str(e)}")
                    return time_graphs

            group_by.change(fn=change_group_by, inputs=[group_by], outputs=time_graphs)

            def change_aggregate_by(y_aggregate):
                try:
                    return [gr.LinePlot(y_aggregate=y_aggregate)] * len(time_graphs)
                except Exception as e:
                    print(f" Error in change_aggregate_by: {str(e)}")
                    return time_graphs

            aggregate.change(fn=change_aggregate_by, inputs=[aggregate], outputs=time_graphs)

            def rescale(select: gr.SelectData):
                try:
                    return select.index
                except Exception as e:
                    print(f" Error in rescale: {str(e)}")
                    return None

            try:
                rescale_evt = gr.on([plot.select for plot in time_graphs], rescale, None, [start, end])
            except Exception as e:
                print(f" Error in rescale event setup: {str(e)}")

            def filter_data(start, end):
                try:
                    filtered_data = builder.ge_by_filter(start, end)

                    
                    return [
                        gr.LinePlot(filtered_data, x="time", y="errors", title=labels["errors_by_time_title"]),
                        gr.LinePlot(filtered_data, x="time", y="requests", title=labels["requests_by_time_title"])
                           ]
                except Exception as e:
                    print(f" Error in filter_data: {str(e)}")
                    return time_graphs

            apply_btn.click(filter_data, inputs=[start, end], outputs=time_graphs)
            combox_spce.change(show_description, inputs=[combox_spce], outputs=[combox_services])
            

            try:
                for trigger in [apply_btn.click, rescale_evt.then]:
                    trigger(
                        lambda start, end: [gr.LinePlot(x_lim=[start, end])] * len(time_graphs),
                        [start, end],
                        time_graphs
                    )
            except Exception as e:
                print(f" Error in setting event triggers: {str(e)}")

    except Exception as e:
        print(f" Fatal error in create_section_bytime: {str(e)}")

def create_section_by_all_services(builder, labels):
    try:
        with gr.Accordion(labels["requests_by_service"]) as panel2:
            data, labels_servs = builder.get_service_usage_and_remaining_plot()
            panel5 = BarServiceCard(data, labels_servs, type_chart="bar")
    except Exception as e:
        print(f"Error in create_section_by_all_services: {str(e)}")
#
