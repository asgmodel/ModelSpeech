from AppUI import create_app
from .chatbot.templates  import TemplateSpeechStudioBuilder
isDev=False
APPS=[
      (create_app(TemplateSpeechStudioBuilder,isDev),'chatbot'),
      (create_app(TemplateSpeechStudioBuilder,isDev),'chatbot2'),
      
]




