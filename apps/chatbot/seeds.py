from .models import *


LANGUAGES = {
    "ar": {
        "options": "الخيارات",
        "category": "التصنيف",
         "model_name":"الموديل",
        "choose_model":"اختر موديل",
        "choose_category": "اختر تصنيفًا",
        "language": "اللغة",
        "choose_language": "اختر لغة",
        "dialect": "اللهجة",
        "choose_dialect": "اختر لهجة",
        "settings": "الإعدادات",
        "temperature": "درجة الحرارة",
        "max_token": "أقصى عدد من الرموز",
        "streaming": "البث",
        "voice_output": "الإخراج الصوتي",
        "enter_message": "أدخل الرسالة أو قم بتحميل ملف..."
    },
    "en": {
        "options": "Options",
        "category": "Category",
         "model_name":"model name",
        "choose_model":"Choose a Model",
        "choose_category": "Choose a category",
        "language": "Language",
        "choose_language": "Choose a language",
        "dialect": "Dialect",
        "choose_dialect": "Choose a dialect",
        "settings": "Settings",
        "temperature": "Temperature",
        "max_token": "Max Token",
        "streaming": "Streaming",
        "voice_output": "Voice Output",
        "enter_message": "Enter message or upload file..."
    }
}



class BuilderDataModelAi:
    def __init__(self, models: List[ModelAiCreate]):
        self.models = models



    def get_unique_values(self, field_name: str) -> List[str]:
        unique_values = {getattr(model, field_name) for model in self.models if getattr(model, field_name) is not None}
        return list(unique_values)




    def filter_models(self, filter_criteria: FilterModelAI) -> List[ModelAiCreate]:
        unique_results: Set[tuple] = set()
        filtered_models = []

        for m in self.models:
            if (filter_criteria.name is None or filter_criteria.name.lower() in m.name.lower()) and \
               (filter_criteria.category is None or filter_criteria.category == m.category) and \
               (filter_criteria.language is None or filter_criteria.language == m.language) and \
               (filter_criteria.isStandard is None or filter_criteria.isStandard == m.isStandard) and \
               (filter_criteria.gender is None or filter_criteria.gender == m.gender) and \
               (filter_criteria.dialect is None or filter_criteria.dialect == m.dialect) and \
               (filter_criteria.Type is None or filter_criteria.Type == m.Type):

                model_key = (m.name, m.category, m.language, m.isStandard, m.gender, m.dialect, m.Type)

                if model_key not in unique_results:
                    unique_results.add(model_key)
                    filtered_models.append(m)

        return filtered_models


models_list = [
    ModelAiCreate(name="AI Model 5", AbsolutePath="", category="General", language="Arabic", isStandard=True, gender="Female", dialect="Najdi Dialect", Type="chat"), # Added AbsolutePath=""
    ModelAiCreate(name="AI Model 2", AbsolutePath="", category="News", language="English", isStandard=False, gender="Female", dialect="American Dialect", Type="chat"), # Added AbsolutePath=""
    ModelAiCreate(name="AI Model 3", AbsolutePath="", category="General", language="Arabic", isStandard=True, gender="Female", dialect="Hijazi Dialect", Type="chat"), # Added AbsolutePath=""
    ModelAiCreate(name="AI Model 1", AbsolutePath="", category="General", language="Arabic", isStandard=True, gender="Male", dialect="Najdi Dialect", Type="chat"), # Added AbsolutePath=""
              ]





class BuilderStudioModelAiSpeed:
    def __init__(self,models_list):

        self.Builder = BuilderDataModelAi(models_list)
    def get_filter(self,FilterModelAI,returnName):
         models=self.Builder.filter_models(FilterModelAI)
         unique_values = {getattr(model, returnName) for model in models if getattr(model, returnName) is not None}
         return list(unique_values)

    def get_property(self, field_name: str) -> List[str]:
         return self.Builder.get_unique_values(field_name)


class RequestDev:
    def __init__(self, max_requests: int):
        """  Simulate requests in development mode"""
        self.max_requests = max_requests
        self.request_count = 0
    def  send_event_request(self,data):
         return  None
    def send_event_request(self, eventId, status, message):
        """Send an event request to the API"""
        dataa = {
                "eventId":"aaaaaaaagsdhghghghghgg",
                "status": status,
                "message": message
               }
        return {
                "status": "success",
                "data": dataa,
                "message": "success to connect to API",
                "details":"",
                "status_code":200
            }

    def create_request(self, data):
        """  Create a mock request"""
        data_return = {
            "modelGateway": "string",
            "modelAi": "wasmdashai/T2T",
            "service": "string",
            "token": "AIzaSyC85_3TKmiXtOpwybhSFThZdF1nGKlxU5c",
            "eventId": "string",
            "numberRequests": self.max_requests,
            "currentNumberRequests": self.request_count + 1
        }



        if self.request_count < self.max_requests:
            self.request_count += 1
            return {
                "status": "success",
                "data":data_return,
                "message": "success to connect to API",
                "details":"",
                "status_code":200
            }
            return data_return
        else:
             return {
                "status":"failed",
                "data":None,
                "message": "success to connect to API",
                "details":"",
                "status_code":602
            }



