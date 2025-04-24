import base64
import os
import uuid

import gradio as gr
import modelscope_studio.components.antd as antd
import modelscope_studio.components.antdx as antdx
import modelscope_studio.components.base as ms
import modelscope_studio.components.pro as pro
from modelscope_studio.components.pro.chatbot import (ChatbotActionConfig,
                                                      ChatbotBotConfig,
                                                      ChatbotUserConfig,
                                                      ChatbotWelcomeConfig)
from modelscope_studio.components.pro.multimodal_input import \
  MultimodalInputUploadConfig
from openai import OpenAI
bodyicon = """
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

    </style>
    <div class="icon-cont-center  ">
    <div id="logo-icon-static-id" class="icon-xxl text-center shadow-primary rounded-circle flex-shrink-0">
        <svg class="mud-icon-root mud-svg-icon mud-success-text mud-icon-size-large" style="direction:ltr !important;margin:8px !important" focusable="false" viewBox="0 0 24 24" aria-hidden="true" role="img">
            <title>API</title>
            <path d="M0 0h24v24H0z" fill="none"></path>
            <path d="M6 13c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1zm0 4c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1zm0-8c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1zm-3 .5c-.28 0-.5.22-.5.5s.22.5.5.5.5-.22.5-.5-.22-.5-.5-.5zM6 5c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1zm15 5.5c.28 0 .5-.22.5-.5s-.22-.5-.5-.5-.5.22-.5.5.22.5.5.5zM14 7c.55 0 1-.45 1-1s-.45-1-1-1-1 .45-1 1 .45 1 1 1zm0-3.5c.28 0 .5-.22.5-.5s-.22-.5-.5-.5-.5.22-.5.5.22.5.5.5zm-11 10c-.28 0-.5.22-.5.5s.22.5.5.5.5-.22.5-.5-.22-.5-.5-.5zm7 7c-.28 0-.5.22-.5.5s.22.5.5.5.5-.22.5-.5-.22-.5-.5-.5zm0-17c.28 0 .5-.22.5-.5s-.22-.5-.5-.5-.5.22-.5.5.22.5.5.5zM10 7c.55 0 1-.45 1-1s-.45-1-1-1-1 .45-1 1 .45 1 1 1zm0 5.5c-.83 0-1.5.67-1.5 1.5s.67 1.5 1.5 1.5 1.5-.67 1.5-1.5-.67-1.5-1.5-1.5zm8 .5c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1zm0 4c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1zm0-8c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1zm0-4c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1zm3 8.5c-.28 0-.5.22-.5.5s.22.5.5.5.5-.22.5-.5-.22-.5-.5-.5zM14 17c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1zm0 3.5c-.28 0-.5.22-.5.5s.22.5.5.5.5-.22.5-.5-.22-.5-.5-.5zm-4-12c-.83 0-1.5.67-1.5 1.5s.67 1.5 1.5 1.5 1.5-.67 1.5-1.5-.67-1.5-1.5-1.5zm0 8.5c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1zm4-4.5c-.83 0-1.5.67-1.5 1.5s.67 1.5 1.5 1.5 1.5-.67 1.5-1.5-.67-1.5-1.5-1.5zm0-4c-.83 0-1.5.67-1.5 1.5s.67 1.5 1.5 1.5 1.5-.67 1.5-1.5-.67-1.5-1.5-1.5z"></path>
        </svg>
    </div>
    </div>
"""
# =========== Configuration

# API KEY
# MODELSCOPE_ACCESS_TOKEN = os.getenv('MODELSCOPE_ACCESS_TOKEN')

client = None
model = "LAHJA-AI"

save_history = False

# =========== Configuration

DEFAULT_PROMPTS = [{
    "label":
    "📅 Make a plan",
    "children": [{
        "description": "Help me with a plan to start a business",
    }, {
        "description": "Help me with a plan to achieve my goals",
    }]
}, {
    "label":
    "🖋 Help me write",
    "children": [{
        "description": "SHelp me write a story with a twist ending",
    }, {
        "description": "Help me write a blog post on mental health",
    },
       
    ]
}]

DEFAULT_SUGGESTIONS = [{
    "label":
    'Make a plan',
    "value":
    "Make a plan",
    "children": [{
        "label": "Start a business",
        "value": "Help me with a plan to start a business"
    }, {
        "label": "Achieve my goals",
        "value": "Help me with a plan to achieve my goals"
    }, {
        "label": "Successful interview",
        "value": "Help me with a plan for a successful interview"
    }]
}, {
    "label":
    'Help me write',
    "value":
    "Help me write",
    "children": [{
        "label": "Story with a twist ending",
        "value": "Help me write a story with a twist ending"
    }, {
        "label": "Blog post on mental health",
        "value": "Help me write a blog post on mental health"
    }, {
        "label": "Letter to my future self",
        "value": "Help me write a letter to my future self"
    }]
}]

DEFAULT_LOCALE = 'en_US'

DEFAULT_THEME = {
    "token": {
        "colorPrimary": "rgba(11, 186, 131, 1)",
    }
}


def user_config(disabled_actions=None):
    return ChatbotUserConfig(actions=[
        "copy", "edit",
        ChatbotActionConfig(
            action="delete",
            popconfirm=dict(title="Delete the message",
                            description="Are you sure to delete this message?",
                            okButtonProps=dict(danger=True)))
    ],
                             disabled_actions=disabled_actions)


def bot_config(disabled_actions=None):
    return ChatbotBotConfig(
        actions=[
            "copy", "like", "dislike", "edit",
            ChatbotActionConfig(
                action="retry",
                popconfirm=dict(
                    title="Regenerate the message",
                    description=
                    "Regenerate the message will also delete all subsequent messages.",
                    okButtonProps=dict(danger=True))),
            ChatbotActionConfig(action="delete",
                                popconfirm=dict(
                                    title="Delete the message",
                                    description=
                                    "Are you sure to delete this message?",
                                    okButtonProps=dict(danger=True)))
        ],
        avatar="https://mdn.alipayobjects.com/huamei_iwk9zp/afts/img/A*s5sNRo5LjfQAAAAAAAAAAAAADgCCAQ/fmt.webp",
        disabled_actions=disabled_actions)

from gradio_client import Client
client = Client("wasmdashai/T2T")
def ask_ai(message ):
     
        
     
     result = client.predict(
         text=message,
         key="AIzaSyC85_3TKmiXtOpwybhSFThZdF1nGKlxU5c",
         api_name="/predict"
     )
     return result
class Gradio_Events:

    @staticmethod
    def submit(state_value):
        # Define your code here
        # The best way is to use the image url.
        def image_to_base64(image_path):
            with open(image_path, "rb") as image_file:
                encoded_string = base64.b64encode(
                    image_file.read()).decode('utf-8')
            return f"data:image/jpeg;base64,{encoded_string}"

        def format_history(history):
            messages = [{
                "role": "system",
                "content": "You are a helpful and harmless assistant.",
            }]
            for item in history:
                if item["role"] == "user":
                    messages.append({
                        "role":
                        "user",
                        "content": [{
                            "type": "image_url",
                            "image_url": image_to_base64(file)
                        } for file in item["content"][0]["content"]
                                    if os.path.exists(file)] +
                        [{
                            "type": "text",
                            "text": item["content"][1]["content"]
                        }]
                    })
                elif item["role"] == "assistant":
                    messages.append({
                        "role": "assistant",
                        "content": item["content"]
                    })
            return messages

        history = state_value["conversations_history"][
            state_value["conversation_id"]]
        history_messages = format_history(history)

        history.append({
            "role": "assistant",
            "content": "",
            "loading": True,
            "status": "pending"
        })

        yield {
            chatbot: gr.update(value=history),
            state: gr.update(value=state_value),
        }
        try:
            response = ask_ai(history_messages)
            for chunk in response:
                history[-1]["content"] += chunk
                history[-1]["loading"] = False
                yield {
                    chatbot: gr.update(value=history),
                    state: gr.update(value=state_value)
                }
            history[-1]["status"] = "done"
            yield {
                chatbot: gr.update(value=history),
                state: gr.update(value=state_value),
            }
        except Exception as e:
            history[-1]["loading"] = False
            history[-1]["status"] = "done"
            history[-1]["content"] = "Failed to respond, please try again."
            yield {
                chatbot: gr.update(value=history),
                state: gr.update(value=state_value)
            }
            raise e

    @staticmethod
    def add_user_message(input_value, state_value):
        if not state_value["conversation_id"]:
            random_id = str(uuid.uuid4())
            history = []
            state_value["conversation_id"] = random_id
            state_value["conversations_history"][random_id] = history
            state_value["conversations"].append({
                "label": input_value["text"],
                "key": random_id
            })

        history = state_value["conversations_history"][
            state_value["conversation_id"]]
        history.append({
            "role":
            "user",
            "content": [{
                "type": "file",
                "content": [f for f in input_value["files"]]
            }, {
                "type": "text",
                "content": input_value["text"]
            }]
        })
        return gr.update(value=state_value)

    @staticmethod
    def preprocess_submit(clear_input=True):

        def preprocess_submit_handler(state_value):
            history = state_value["conversations_history"][
                state_value["conversation_id"]]
            return {
                **({
                    input:
                    gr.update(value=None, loading=True) if clear_input else gr.update(loading=True),
                } if clear_input else {}),
                conversations:
                gr.update(active_key=state_value["conversation_id"],
                          items=list(
                              map(
                                  lambda item: {
                                      **item,
                                      "disabled":
                                      True if item["key"] != state_value[
                                          "conversation_id"] else False,
                                  }, state_value["conversations"]))),
                add_conversation_btn:
                gr.update(disabled=True),
                clear_btn:
                gr.update(disabled=True),
                conversation_delete_menu_item:
                gr.update(disabled=True),
                chatbot:
                gr.update(value=history,
                          bot_config=bot_config(
                              disabled_actions=['edit', 'retry', 'delete']),
                          user_config=user_config(
                              disabled_actions=['edit', 'delete'])),
                state:
                gr.update(value=state_value),
            }

        return preprocess_submit_handler

    @staticmethod
    def postprocess_submit(state_value):
        history = state_value["conversations_history"][
            state_value["conversation_id"]]
        return {
            input:
            gr.update(loading=False),
            conversation_delete_menu_item:
            gr.update(disabled=False),
            clear_btn:
            gr.update(disabled=False),
            conversations:
            gr.update(items=state_value["conversations"]),
            add_conversation_btn:
            gr.update(disabled=False),
            chatbot:
            gr.update(value=history,
                      bot_config=bot_config(),
                      user_config=user_config()),
            state:
            gr.update(value=state_value),
        }

    @staticmethod
    def cancel(state_value):
        history = state_value["conversations_history"][
            state_value["conversation_id"]]
        history[-1]["loading"] = False
        history[-1]["status"] = "done"
        history[-1]["footer"] = "Chat completion paused"
        return Gradio_Events.postprocess_submit(state_value)

    @staticmethod
    def delete_message(state_value, e: gr.EventData):
        index = e._data["payload"][0]["index"]
        history = state_value["conversations_history"][
            state_value["conversation_id"]]
        history = history[:index] + history[index + 1:]

        state_value["conversations_history"][
            state_value["conversation_id"]] = history

        return gr.update(value=state_value)

    @staticmethod
    def edit_message(state_value, chatbot_value, e: gr.EventData):
        index = e._data["payload"][0]["index"]
        history = state_value["conversations_history"][
            state_value["conversation_id"]]
        history[index]["content"] = chatbot_value[index]["content"]
        return gr.update(value=state_value)

    @staticmethod
    def regenerate_message(state_value, e: gr.EventData):
        index = e._data["payload"][0]["index"]
        history = state_value["conversations_history"][
            state_value["conversation_id"]]
        history = history[:index]
        state_value["conversations_history"][
            state_value["conversation_id"]] = history
        # custom code
        return gr.update(value=history), gr.update(value=state_value)

    @staticmethod
    def select_suggestion(input_value, e: gr.EventData):
        input_value["text"] = input_value["text"][:-1] + e._data["payload"][0]
        return gr.update(value=input_value)

    @staticmethod
    def apply_prompt(input_value, e: gr.EventData):
        input_value["text"] = e._data["payload"][0]["value"]["description"]
        return gr.update(value=input_value)

    @staticmethod
    def new_chat(state_value):
        if not state_value["conversation_id"]:
            return gr.skip()
        state_value["conversation_id"] = ""
        return gr.update(active_key=state_value["conversation_id"]), gr.update(
            value=None), gr.update(value=state_value)

    @staticmethod
    def select_conversation(state_value, e: gr.EventData):
        active_key = e._data["payload"][0]
        if state_value["conversation_id"] == active_key or (
                active_key not in state_value["conversations_history"]):
            return gr.skip()
        state_value["conversation_id"] = active_key
        return gr.update(active_key=active_key), gr.update(
            value=state_value["conversations_history"][active_key]), gr.update(
                value=state_value)

    @staticmethod
    def click_conversation_menu(state_value, e: gr.EventData):
        conversation_id = e._data["payload"][0]["key"]
        operation = e._data["payload"][1]["key"]
        if operation == "delete":
            del state_value["conversations_history"][conversation_id]

            state_value["conversations"] = [
                item for item in state_value["conversations"]
                if item["key"] != conversation_id
            ]

            if state_value["conversation_id"] == conversation_id:
                state_value["conversation_id"] = ""
                return gr.update(
                    items=state_value["conversations"],
                    active_key=state_value["conversation_id"]), gr.update(
                        value=None), gr.update(value=state_value)
            else:
                return gr.update(
                    items=state_value["conversations"]), gr.skip(), gr.update(
                        value=state_value)
        return gr.skip()

    @staticmethod
    def clear_conversation_history(state_value):
        if not state_value["conversation_id"]:
            return gr.skip()
        state_value["conversations_history"][
            state_value["conversation_id"]] = []
        return gr.update(value=None), gr.update(value=state_value)

    @staticmethod
    def update_browser_state(state_value):

        return gr.update(value=dict(
            conversations=state_value["conversations"],
            conversations_history=state_value["conversations_history"]))

    @staticmethod
    def apply_browser_state(browser_state_value, state_value):
        state_value["conversations"] = browser_state_value["conversations"]
        state_value["conversations_history"] = browser_state_value[
            "conversations_history"]
        return gr.update(
            items=browser_state_value["conversations"]), gr.update(
                value=state_value)


css = """
#chatbot {
  height: calc(100vh - 32px - 21px - 16px);
}

#chatbot .chatbot-conversations {
  height: 100%;
  background-color: var(--ms-gr-ant-color-bg-layout);
}

#chatbot .chatbot-conversations .chatbot-conversations-list {
  padding-left: 0;
  padding-right: 0;
}

#chatbot .chatbot-chat {
  padding: 32px;
  height: 100%;
}

@media (max-width: 768px) {
  #chatbot .chatbot-chat {
      padding: 0;
  }
}
                
  
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
#chatbot .chatbot-chat .chatbot-chat-messages {
  flex: 1;
}
"""


def logo():
    with antd.Typography.Title(level=1,
                               elem_style=dict(fontSize=24,
                                               padding=8,
                                               margin=0)):
        with antd.Flex(align="center", gap="small", justify="center"):
            antd.Image(
                "https://mdn.alipayobjects.com/huamei_iwk9zp/afts/img/A*eco6RrQhxbMAAAAAAAAAAAAADgCCAQ/original",
                preview=False,
                alt="logo",
                width=24,
                height=24)
            ms.Span("Chatbot")

def   getChatPro():
      # with gr.Blocks(css=css, fill_width=True) as demo:
          state = gr.State({
              "conversations_history": {},
              "conversations": [],
              "conversation_id": "",
          })

          with ms.Application(), antdx.XProvider(
                  theme=DEFAULT_THEME, locale=DEFAULT_LOCALE), ms.AutoLoading() as app:
              with antd.Row(gutter=[20, 20], wrap=False, elem_id="chatbot"):
                  # Left Column
                  antd.Tree.DirectoryTree(
                      draggable=True,
                      multiple=True,
                      default_expand_all=True,
                      tree_data=tree_data
                  )
                  with antd.Col(md=dict(flex="0 0 260px", span=24, order=0),
                                span=0,
                                order=1,
                                elem_classes="chatbot-conversations"):
                      with antd.Flex(vertical=True,
                                    gap="small",
                                    elem_style=dict(height="100%")):
                          # Logo
                          logo()

                          # New Conversation Button
                          with antd.Button(value=None,
                                          color="primary",
                                          variant="filled",
                                          block=True) as add_conversation_btn:
                              ms.Text("New Conversation")
                              with ms.Slot("icon"):
                                  antd.Icon("PlusOutlined")

                          # Conversations List
                          with antdx.Conversations(
                                  elem_classes="chatbot-conversations-list",
                          ) as conversations:
                              with ms.Slot('menu.items'):
                                  with antd.Menu.Item(
                                          label="Delete", key="delete", danger=True
                                  ) as conversation_delete_menu_item:
                                      with ms.Slot("icon"):
                                          antd.Icon("DeleteOutlined")
                          antd.Divider("Settings")

                                      # Settings Area
                          with antd.Space(size="small",
                                                      wrap=True,
                                                      elem_id="settings-area"):
                                          system_prompt_btn = antd.Button(
                                              "⚙️ Set System Prompt", type="default")
                                          history_btn = antd.Dropdown.Button(
                                              "📜 History",
                                              type="default",
                                              elem_id="history-btn",
                                              menu=dict(items=[{
                                                  "key": "clear",
                                                  "label": "Clear History",
                                                  "danger": True
                                              }]))
                  # Right Column
                  with antd.Col(flex=1, elem_style=dict(height="100%")):
                      with antd.Flex(vertical=True, elem_classes="chatbot-chat"):
                          gr.HTML(bodyicon)
                          # Chatbot
                          chatbot = pro.Chatbot(
                              elem_classes="chatbot-chat-messages",
                              welcome_config=ChatbotWelcomeConfig(
                                  variant="borderless",
                                  icon=
                                  "https://mdn.alipayobjects.com/huamei_iwk9zp/afts/img/A*s5sNRo5LjfQAAAAAAAAAAAAADgCCAQ/fmt.webp",
                                  title=f"Hello, I'm {model}",
                                  description=
                                  "You can upload images and text to get started.",
                                  prompts=dict(
                                      title="How can I help you today?",
                                      styles={
                                          "list": {
                                              "width": '100%',
                                          },
                                          "item": {
                                              "flex": 1,
                                          },
                                      },
                                      items=[{
                                          "label":
                                          "🖋 Make a plan",
                                          "children": [{
                                              "description":
                                              "Help me with a plan to start a business"
                                          },]
                                      }, {
                                          "label":
                                          "📅 Help me write",
                                          "children": [{
                                              "description":
                                              "Help me write a story with a twist ending"
                                          }]
                                      }]),
                              ),
                              user_config=user_config(),
                              bot_config=bot_config())
                          # Input
                          with antdx.Suggestion(
                                  items=DEFAULT_SUGGESTIONS,
                                  # onKeyDown Handler in Javascript
                                  should_trigger="""(e, { onTrigger, onKeyDown }) => {
                            switch(e.key) {
                              case '/':
                                onTrigger()
                                break
                              case 'ArrowRight':
                              case 'ArrowLeft':
                              case 'ArrowUp':
                              case 'ArrowDown':
                                break;
                              default:
                                onTrigger(false)
                            }
                            onKeyDown(e)
                          }""") as suggestion:
                              with ms.Slot("children"):
                                  with pro.MultimodalInput(
                                          placeholder="Enter / to get suggestions",
                                          upload_config=MultimodalInputUploadConfig(
                                              upload_button_tooltip=
                                              "Upload Attachments",
                                              allow_speech=True, allow_paste_file=True,
                                              max_count=6,
                                              
                                              accept="image/*",
                                              multiple=True)) as input:
                                      with ms.Slot("prefix"):
                                          # Clear Button
                                          with antd.Tooltip(
                                                  title="Clear Conversation History"
                                          ):
                                              with antd.Button(
                                                      value=None,
                                                      type="text") as clear_btn:
                                                  with ms.Slot("icon"):
                                                      antd.Icon("ClearOutlined")
          browser_state = gr.BrowserState(
                  {
                      "conversations_history": {},
                      "conversations": [],
                  },
                  storage_key="ms_chatbot_storage")
          # Events Handler
          if save_history:
              
              state.change(fn=Gradio_Events.update_browser_state,
                          inputs=[state],
                          outputs=[browser_state])

              # demo.load(fn=Gradio_Events.apply_browser_state,
              #           inputs=[browser_state, state],
              #           outputs=[conversations, state])

          add_conversation_btn.click(fn=Gradio_Events.new_chat,
                                    inputs=[state],
                                    outputs=[conversations, chatbot, state])
          conversations.active_change(fn=Gradio_Events.select_conversation,
                                      inputs=[state],
                                      outputs=[conversations, chatbot, state])
          conversations.menu_click(fn=Gradio_Events.click_conversation_menu,
                                  inputs=[state],
                                  outputs=[conversations, chatbot, state])
          chatbot.welcome_prompt_select(fn=Gradio_Events.apply_prompt,
                                        inputs=[input],
                                        outputs=[input])

          clear_btn.click(fn=Gradio_Events.clear_conversation_history,
                          inputs=[state],
                          outputs=[chatbot, state])

          suggestion.select(fn=Gradio_Events.select_suggestion,
                            inputs=[input],
                            outputs=[input])
          chatbot.delete(fn=Gradio_Events.delete_message,
                        inputs=[state],
                        outputs=[state])
          chatbot.edit(fn=Gradio_Events.edit_message,
                      inputs=[state, chatbot],
                      outputs=[state])

          regenerating_event = chatbot.retry(
              fn=Gradio_Events.regenerate_message,
              inputs=[state],
              outputs=[chatbot, state
                      ]).then(fn=Gradio_Events.preprocess_submit(clear_input=False),
                              inputs=[state],
                              outputs=[
                                  input, clear_btn, conversation_delete_menu_item,
                                  add_conversation_btn, conversations, chatbot,
                                  state
                              ]).then(fn=Gradio_Events.submit,
                                      inputs=[state],
                                      outputs=[chatbot, state])

          submit_event = input.submit(
              fn=Gradio_Events.add_user_message,
              inputs=[input, state],
              outputs=[state
                      ]).then(fn=Gradio_Events.preprocess_submit(clear_input=True),
                              inputs=[state],
                              outputs=[
                                  input, clear_btn, conversation_delete_menu_item,
                                  add_conversation_btn, conversations, chatbot,
                                  state
                              ]).then(fn=Gradio_Events.submit,
                                      inputs=[state],
                                      outputs=[chatbot, state])
          regenerating_event.then(fn=Gradio_Events.postprocess_submit,
                                  inputs=[state],
                                  outputs=[
                                      input, conversation_delete_menu_item,
                                      clear_btn, conversations, add_conversation_btn,
                                      chatbot, state
                                  ])
          submit_event.then(fn=Gradio_Events.postprocess_submit,
                            inputs=[state],
                            outputs=[
                                input, conversation_delete_menu_item, clear_btn,
                                conversations, add_conversation_btn, chatbot, state
                            ])
          input.cancel(fn=Gradio_Events.cancel,
                      inputs=[state],
                      outputs=[
                          input, conversation_delete_menu_item, clear_btn,
                          conversations, add_conversation_btn, chatbot, state
                      ],
                      cancels=[submit_event, regenerating_event],
                      queue=False)
          return app,conversations,browser_state,state
import gradio as gr
import modelscope_studio.components.antd as antd
import modelscope_studio.components.base as ms

# دالة لتحويل JSON إلى صيغة tree_data
def convert_to_tree(data):
    def build_node(key, value):
        if isinstance(value, list):
            return {
                "title": key,
                "key": key,
                "children": [
                    {"title": v, "key": f"{key}-{v}", "isLeaf": True} if isinstance(v, str)
                    else build_node(f"{key}-{i}", v)
                    for i, v in enumerate(value)
                ]
            }
        elif isinstance(value, dict):
            return {
                "title": key,
                "key": key,
                "children": [build_node(k, v) for k, v in value.items()]
            }
        return {"title": str(value), "key": f"{key}-{value}", "isLeaf": True}

    tree = []
    for k, v in data.items():
        tree.append(build_node(k, v))
    return tree

# البيانات الأصلية بصيغة JSON
your_json_data = {
    "Controllers": ["Api", "Auth", "Admin"],
    "Repositories": ["Base", "Builder", "Share"],
    "Services": ["Email", "Logging"],
    "DyModels": [
        {
            "VM": [],
            "Dto": {
                "Build": ["Request", "Response", "ResponseFilter"],
                "Share": ["Request", "Response", "ResponseFilter"]
            },
            "Dso": ["Request", "Response", "ResponseFilter"]
        }
    ],
    "Config": ["Mappers", "Scopes", "Singletons", "Transients"],
    "Models": [],
    "Builders": ["Db"],
    "Helper": [],
    "Data": [],
    "Enums": [],
    "Validators": ["Conditions"],
    "Schedulers": []
}

# تحويل البيانات لصيغة الشجرة
tree_data = convert_to_tree(your_json_data)
import base64
import os
import re

import gradio as gr
import modelscope_studio.components.antd as antd
import modelscope_studio.components.base as ms
from openai import OpenAI

# =========== Configuration

# API KEY

client = None

model = "Qwen/Qwen2.5-Coder-32B-Instruct"
# =========== Configuration

DEFAULT_SYSTEM_PROMPT = """You are a web development engineer, writing web pages according to the instructions below. You are a powerful code editing assistant capable of writing code and creating artifacts in conversations with users, or modifying and updating existing artifacts as requested by users.
All code is written in a single code block to form a complete code file for display, without separating HTML and JavaScript code. An artifact refers to a runnable complete code snippet, you prefer to integrate and output such complete runnable code rather than breaking it down into several code blocks. For certain types of code, they can render graphical interfaces in a UI window. After generation, please check the code execution again to ensure there are no errors in the output.
Output only the HTML, without any additional descriptive text."""

EXAMPLES = [
    {
        "title":
        "LAHJA Start！",
        "description":
        "Help me design an interface with a purple button that says 'LAHJA, Start!'. When the button is clicked, display a countdown from 5 in a very large font for 5 seconds.",
    },
    {
        "title":
        "Spam with emojis!",
        "description":
        "Write code in a single HTML file: Capture the click event, place a random number of emojis at the click position, and add gravity and collision effects to each emoji."
    },
    {
        "title":
        "TODO list",
        "description":
        "I want a TODO list that allows me to add tasks, delete tasks, and I would like the overall color theme to be purple."
    },
]

DEFAULT_LOCALE = 'en_US'

DEFAULT_THEME = {
    "token": {
        "colorPrimary": "rgba(11, 186, 131, 1)",
    }
}


class GradioEvents:

    @staticmethod
    def generate_code(input_value, system_prompt_input_value, state_value):
        # Define your code here

        def remove_code_block(text):
            pattern = r'```html\n(.+?)\n```'
            match = re.search(pattern, text, re.DOTALL)
            if match:
                return match.group(1).strip()
            else:
                return text.strip()

        def send_to_sandbox(code):
            encoded_html = base64.b64encode(
                code.encode('utf-8')).decode('utf-8')
            data_uri = f"data:text/html;charset=utf-8;base64,{encoded_html}"
            return f"<iframe src=\"{data_uri}\" width=\"100%\" height=\"100%\"></iframe>"

        yield {
            output_loading: gr.update(spinning=True),
            state_tab: gr.update(active_key="loading"),
            output: gr.update(value=None)
        }

        if input_value is None:
            input_value = ''

        messages = [{
            'role': "system",
            'content': system_prompt_input_value
        }] + state_value["history"]

        messages.append({'role': "user", 'content': input_value})

        generator = client.chat.completions.create(model=model,
                                                   messages=messages,
                                                   stream=True)
        response = ""
        for chunk in generator:
            content = chunk.choices[0].delta.content
            response += content
            if chunk.choices[0].finish_reason == 'stop':
                state_value["history"] = messages + [{
                    'role': "assistant",
                    'content': response
                }]
                # Completed
                yield {
                    output:
                    gr.update(value=response),
                    download_content:
                    gr.update(value=remove_code_block(response)),
                    state_tab:
                    gr.update(active_key="render"),
                    output_loading:
                    gr.update(spinning=False),
                    sandbox:
                    gr.update(
                        value=send_to_sandbox(remove_code_block(response))),
                    state:
                    gr.update(value=state_value)
                }

            else:
                # Generating
                yield {
                    output: gr.update(value=response),
                    output_loading: gr.update(spinning=False),
                }

    @staticmethod
    def select_example(example: dict):
        return lambda: gr.update(value=example["description"])

    @staticmethod
    def close_modal():
        return gr.update(open=False)

    @staticmethod
    def open_modal():
        return gr.update(open=True)

    @staticmethod
    def disable_btns(btns: list):
        return lambda: [gr.update(disabled=True) for _ in btns]

    @staticmethod
    def enable_btns(btns: list):
        return lambda: [gr.update(disabled=False) for _ in btns]

    @staticmethod
    def update_system_prompt(system_prompt_input_value, state_value):
        state_value["system_prompt"] = system_prompt_input_value
        return gr.update(value=state_value)

    @staticmethod
    def reset_system_prompt(state_value):
        return gr.update(value=state_value["system_prompt"])

    @staticmethod
    def render_history(statue_value):
        return gr.update(value=statue_value["history"])

    @staticmethod
    def clear_history(e: gr.EventData, state_value):
        item = e._data["payload"][0]["key"]
        if item == "clear":
            gr.Success("History Cleared.")
            state_value["history"] = []
            return gr.update(value=state_value)
        return gr.skip()


css = """
#coder-artifacts .output-empty,.output-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  min-height: 680px;
}

#coder-artifacts .output-html {
  display: flex;
  flex-direction: column;
  width: 100%;
  min-height: 680px;
}

#coder-artifacts .output-html > iframe {
  flex: 1;
}

#code-artifacts-code-drawer .output-code {
  flex:1;
}
#code-artifacts-code-drawer .output-code .ms-gr-ant-spin-nested-loading {
  min-height: 100%;
}
"""
def  getStuido():
     # with gr.Blocks(css=css) as demo:
          # Global State
     state = gr.State({"system_prompt": DEFAULT_SYSTEM_PROMPT, "history": []})
     with ms.Application(elem_id="coder-artifacts") as app:
              with antd.ConfigProvider(theme=DEFAULT_THEME, locale=DEFAULT_LOCALE):
                  #  Header
                  with antd.Flex(justify="center", align="center", gap="middle"):
                      antd.Typography.Title("Studio-LAHJA",
                                            level=1,
                                            elem_style=dict(fontSize=24))
                  with ms.AutoLoading():
                      with antd.Row(gutter=[32, 12],
                                    elem_style=dict(marginTop=20),
                                    align="stretch"):
                          # Left Column
                          with antd.Col(span=24, md=8):
                              with antd.Flex(vertical=True, gap="middle", wrap=True):
                                  # Input
                                  input = antd.Input.Textarea(
                                      size="large",
                                      allow_clear=True,
                                      auto_size=dict(minRows=2, maxRows=6),
                                      placeholder=
                                      "Describe the web application you want to create",
                                      elem_id="input-container")
                                  # Input Notes
                                  with antd.Flex(align="center",
                                                justify="space-between"):
                                      antd.Typography.Text(
                                          "Note: The model supports multi-round dialogue.",
                                          strong=True,
                                          type="warning")

                                      tour_btn = antd.Button("Usage Tour",
                                                            variant="filled",
                                                            color="default")
                                  # Submit Button
                                  submit_btn = antd.Button("Submit",
                                                          type="primary",
                                                          block=True,
                                                          size="large",
                                                          elem_id="submit-btn")

                                  antd.Divider("Settings")

                                  # Settings Area
                                  with antd.Space(size="small",
                                                  wrap=True,
                                                  elem_id="settings-area"):
                                      system_prompt_btn = antd.Button(
                                          "⚙️ Set System Prompt", type="default")
                                      history_btn = antd.Dropdown.Button(
                                          "📜 History",
                                          type="default",
                                          elem_id="history-btn",
                                          menu=dict(items=[{
                                              "key": "clear",
                                              "label": "Clear History",
                                              "danger": True
                                          }]))
                                  

                                  antd.Divider("Examples")

                                  # Examples
                                  with antd.Flex(gap="small", wrap=True):
                                      for example in EXAMPLES:
                                          with antd.Card(
                                                  elem_style=dict(
                                                      flex="1 1 fit-content"),
                                                  hoverable=True) as example_card:
                                              antd.Card.Meta(
                                                  title=example['title'],
                                                  description=example['description'])

                                          example_card.click(
                                              fn=GradioEvents.select_example(
                                                  example),
                                              outputs=[input])

                          # Right Column
                          with antd.Col(span=24, md=16):
                              with antd.Card(title="Output",
                                            elem_style=dict(height="100%"),
                                            styles=dict(body=dict(height="100%")),
                                            elem_id="output-container"):
                                  # Output Container Extra
                                  with ms.Slot("extra"):
                                      with ms.Div(elem_id="output-container-extra"):
                                          with antd.Button(
                                                  "Download HTML",
                                                  type="link",
                                                  href_target="_blank",
                                                  disabled=True,
                                          ) as download_btn:
                                              with ms.Slot("icon"):
                                                  antd.Icon("DownloadOutlined")
                                          download_content = gr.Text(visible=False)

                                          view_code_btn = antd.Button(
                                              "🧑‍💻 View Code", type="primary")
                                  # Output Content
                                  with antd.Tabs(
                                          active_key="empty",
                                          render_tab_bar="() => null") as state_tab:
                                      with antd.Tabs.Item(key="empty"):
                                          antd.Empty(
                                              description=
                                              "Enter your request to generate code",
                                              elem_classes="output-empty")
                                      with antd.Tabs.Item(key="loading"):
                                          with antd.Spin(
                                                  tip="Generating code...",
                                                  size="large",
                                                  elem_classes="output-loading"):
                                              # placeholder
                                              ms.Div()
                                      with antd.Tabs.Item(key="render"):
                                          sandbox = gr.HTML(
                                              elem_classes="output-html")

                          # Modals and Drawers
                          with antd.Modal(open=False,
                                          title="System Prompt",
                                          width="800px") as system_prompt_modal:
                              system_prompt_input = antd.Input.Textarea(
                                  DEFAULT_SYSTEM_PROMPT,
                                  size="large",
                                  placeholder="Enter your system prompt here",
                                  allow_clear=True,
                                  auto_size=dict(minRows=4, maxRows=14))

                          with antd.Drawer(
                                  open=False,
                                  title="Output Code",
                                  placement="right",
                                  get_container=
                                  "() => document.querySelector('.gradio-container')",
                                  elem_id="code-artifacts-code-drawer",
                                  styles=dict(
                                      body=dict(display="flex",
                                                flexDirection="column-reverse")),
                                  width="750px") as output_code_drawer:
                              with ms.Div(elem_classes="output-code"):
                                  with antd.Spin(spinning=False) as output_loading:
                                      output = gr.Code(elem_classes="output-code")

                          with antd.Drawer(
                                  open=False,
                                  title="Chat History",
                                  placement="left",
                                  get_container=
                                  "() => document.querySelector('.gradio-container')",
                                  width="750px") as history_drawer:
                              history_output = gr.Chatbot(
                                  show_label=False,
                                  type="messages",
                                  height='100%',
                                  elem_classes="history_chatbot")
                          # Tour
                          with antd.Tour(open=False) as usage_tour:
                              antd.Tour.Step(
                                  title="Step 1",
                                  description=
                                  "Describe the web application you want to create.",
                                  get_target=
                                  "() => document.querySelector('#input-container')")
                              antd.Tour.Step(
                                  title="Step 2",
                                  description="Click the submit button.",
                                  get_target=
                                  "() => document.querySelector('#submit-btn')")
                              antd.Tour.Step(
                                  title="Step 3",
                                  description="Wait for the result.",
                                  get_target=
                                  "() => document.querySelector('#output-container')"
                              )
                              antd.Tour.Step(
                                  title="Step 4",
                                  description=
                                  "Download the generated HTML here or view the code.",
                                  get_target=
                                  "() => document.querySelector('#output-container-extra')"
                              )
                              antd.Tour.Step(
                                  title="Additional Settings",
                                  description=
                                  "You can change the system prompt or chat history here.",
                                  get_target=
                                  "() => document.querySelector('#settings-area')")
              # Event Handler
              gr.on(fn=GradioEvents.close_modal,
                    triggers=[usage_tour.close, usage_tour.finish],
                    outputs=[usage_tour])
              tour_btn.click(fn=GradioEvents.open_modal, outputs=[usage_tour])

              system_prompt_btn.click(fn=GradioEvents.open_modal,
                                      outputs=[system_prompt_modal])

              system_prompt_modal.ok(GradioEvents.update_system_prompt,
                                    inputs=[system_prompt_input, state],
                                    outputs=[state]).then(fn=GradioEvents.close_modal,
                                                          outputs=[system_prompt_modal])

              system_prompt_modal.cancel(GradioEvents.close_modal,
                                        outputs=[system_prompt_modal]).then(
                                            fn=GradioEvents.reset_system_prompt,
                                            inputs=[state],
                                            outputs=[system_prompt_input])
              output_code_drawer.close(fn=GradioEvents.close_modal,
                                      outputs=[output_code_drawer])
              history_btn.menu_click(fn=GradioEvents.clear_history,
                                    inputs=[state],
                                    outputs=[state])
              history_btn.click(fn=GradioEvents.open_modal,
                                outputs=[history_drawer
                                        ]).then(fn=GradioEvents.render_history,
                                                inputs=[state],
                                                outputs=[history_output])
              history_drawer.close(fn=GradioEvents.close_modal, outputs=[history_drawer])

              download_btn.click(fn=None,
                                inputs=[download_content],
                                js="""(content) => {
                  const blob = new Blob([content], { type: 'text/html' })
                  const url = URL.createObjectURL(blob)
                  const a = document.createElement('a')
                  a.href = url
                  a.download = 'output.html'
                  a.click()
          }""")
              view_code_btn.click(fn=GradioEvents.open_modal,
                                  outputs=[output_code_drawer])
              submit_btn.click(
                  fn=GradioEvents.open_modal,
                  outputs=[output_code_drawer],
              ).then(fn=GradioEvents.disable_btns([submit_btn, download_btn]),
                    outputs=[submit_btn, download_btn]).then(
                        fn=GradioEvents.generate_code,
                        inputs=[input, system_prompt_input, state],
                        outputs=[
                            output, state_tab, sandbox, download_content,
                            output_loading, state
                        ]).then(fn=GradioEvents.enable_btns([submit_btn, download_btn]),
                                outputs=[submit_btn, download_btn
                                          ]).then(fn=GradioEvents.close_modal,
                                                  outputs=[output_code_drawer])
              return app


                                      

def  AppProAI(inputs=[],outputs=[]):
     with gr.Blocks() as demo:
          state=gr.State(value=None)

          @gr.render()
          def main(request: gr.Request):
               with antd.ConfigProvider(theme=DEFAULT_THEME, locale=DEFAULT_LOCALE):
              #  with antd.Col(span=24):
              #  antd.Text("Welcome to AppProAI - Your AI Solution", style={"fontSize": "24px", "fontWeight": "bold", "textAlign": "center"})
              
                    with antd.Row(gutter=[32, 12],
                                          elem_style=dict(marginTop=20),
                                          align="stretch"):
                                          # Left Column
                          with antd.Col(span=24, md=6):
                                with antd.Flex(vertical=True, gap="middle", wrap=True):
                        
                                      antd.Tree.DirectoryTree(
                                          draggable=True,
                                          multiple=True,
                                          default_expand_all=True,
                                          tree_data=tree_data
                                      )
                                      # Right Column
                          with antd.Col(span=24, md=18):

                                with antd.Tabs(default_active_key='1'):
                                    with antd.Tabs.Item(key="1", label="Genratre"):
                                          getStuido()
                                    with antd.Tabs.Item(key="2", label="ChatBot"):
                                          app,conversations,browser_state,state=getChatPro()
                                    
          demo.load(fn=main, inputs=[],
                                          outputs=[])
                               

                        
              #




     return demo

         
    
demo=AppProAI()
