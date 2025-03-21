from AppUI import create_api

from .chatbot.templates  import TemplateSpeechStudioBuilder
isDev=True
APIS=[
  (create_api(TemplateSpeechStudioBuilder,isDev),'/user')
]
