from pydantic import BaseModel, create_model
from typing import Any, Dict, List, Union
import json

class DataDynamicModel:
    def __init__(self, data: str):
        self.data = data
        self.parsed_data = self.parse_data(data)
        
    def parse_data(self, data: str) -> Dict[str, Any]:
     
        try:
            return json.loads(data)
        except Exception as e:
            raise ValueError(f"Error parsing data: {str(e)}")

    def generate_dynamic_model(self, data_dict: Dict[str, Any]) -> BaseModel:
        
        model_fields = {}
        
        for key, value in data_dict.items():
            if isinstance(value, dict):
                # إذا كانت القيمة قواميس أخرى، ننشئ نموذجًا فرعيًا لها.
                model_fields[key] = (self.generate_dynamic_model(value), ...)
            elif isinstance(value, list):
                # إذا كانت القيمة قائمة، ننشئ نوعًا يمكن أن يحتوي على عناصر ديناميكية.
                if value and isinstance(value[0], dict):
                    # قائمة تحتوي على قواميس، ننشئ نموذجًا لها.
                    model_fields[key] = (List[self.generate_dynamic_model(value[0])], ...)
                else:
                    # إذا كانت قائمة تحتوي على أنواع أخرى.
                    model_fields[key] = (List[Any], ...)
            else:
                # بالنسبة للأنواع الأخرى، نستخدم النوع العام Any.
                model_fields[key] = (Any, ...)

        # إنشاء النموذج الديناميكي
        DynamicModel = create_model("DynamicModel", **model_fields)
        return DynamicModel

    def convert_to_dynamic_model(self) -> BaseModel:
       
        dynamic_model = self.generate_dynamic_model(self.parsed_data)
        return dynamic_model(**self.parsed_data)
