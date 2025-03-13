from AppUI import create_app
from chatbot.tamplates  import TemplateSpeechStudioBuilder
isDev=True

demo_chatbot=create_app(TemplateSpeechStudioBuilder,isDev)




