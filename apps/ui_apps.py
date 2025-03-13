from AppUI import create_app
from chatbot.tamplates  import TemplateSpeechStudioBuilder
isDev=True
APPS=[
      (create_app(TemplateSpeechStudioBuilder,isDev),'chatbot'),
      (create_app(TemplateSpeechStudioBuilder,isDev),'chatbot2'),
      
]




