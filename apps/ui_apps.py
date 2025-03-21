from AppUI import create_app
from .chatbot.templates  import TemplateSpeechStudioBuilder
from .space.templates  import TemplateSpacePlatformBuilder
from .dashboard.templates  import TamplateDashBuilder
from .t2text.templates  import TemplateTextToTextStudioBuilder,TemplateTextToTextBuilder
from .t2speech.templates  import TemplateTextToSpeechStudioBuilder,TemplateTextToSpeechBuilder
isDev=False

APPS=[
      (create_app(TamplateDashBuilder,isDev),'dashboard'),
      (create_app(TemplateSpeechStudioBuilder,isDev),'chatbot'),
      (create_app(TemplateTextToSpeechStudioBuilder,isDev),'studio-t2text'),
      (create_app(TemplateSpacePlatformBuilder,isDev),'createspace'),
      (create_app(TemplateTextToTextStudioBuilder,isDev),'studio-t2speech'),
      (create_app(TemplateTextToSpeechBuilder,isDev),'t2speech'),
      (create_app(TemplateTextToTextBuilder,isDev),'t2text'),

      
]




