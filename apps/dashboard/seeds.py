class  BuilderDashAPISeed:
    def __init__(self) -> None:
        pass

    def  get_data_byservices(self):
         labels =  ["Text to Speech", "Text to Dialect", "Speech to Speech"]
         values = [100, 200 ,200 ]




         return values,labels
    def  get_model_ai_service_requests(self):
         labels =  ["Text to Speech", "Text to Dialect", "Speech to Speech"]
         values = [100, 200 ,200 ]
         return values,labels
    def  get_service_usage_and_remaining(self):
         labels =  ["Text to Speech", "Text to Dialect", "Speech to Speech"]
         values = [100, 200 ,200 ]
         return values,labels
    def  get_service_users_count(self):
         labels =  ["Text to Speech", "Text to Dialect", "Speech to Speech"]
         values = [100, 200 ,200 ]
         return values,labels

    def  get_data_byplan(self):

        return self.get_data_byservices()

    def  get_stateerrors(self):
       return service_data

    def  get_staterequests(self):
        return service_data
    def  get_model_name_request_bytime(self,serviceType="all", start="2025-03-06T22:26:34.259Z", end=None, time=None):
        service_dataa = pd.DataFrame(
            {
                "time": pd.date_range("2025-01-01", end="2025-01-05", periods=10),  # Changed periods to 10
                "requests": [randint(5, 20) for i in range(10)],
                "errors": [randint(0, 3) for i in range(10)],
                "service_type": ["Text to Speech", "Text to Dialect", "Speech to Speech"] * 3 + ["Text to Speech"],  # Adjusted to match length

            }
         )
        labels_service = {
                "label_dropdown":"Type Service",
                "Type": "service_type",
                "x": "time",
                "y": "requests"
                }
        return service_dataa,labels_service

    def  get_data_byplan_services(self):

        service_data_tod = pd.DataFrame(
          {

          "value": [100,50]*3,
          "TypeData": ["requests","remaining"]*3,
          "service_type": ["Text to Speech", "Text to Dialect", "Speech to Speech"]*2 ,

         }
        )
        labels_servs = {
                      "label_dropdown":"Type Service",
                      "Type": "TypeData",
                      "x": "value",
                      "y": "service_type"
                  }
        return service_data_tod,labels_servs
    def  get_service_usage_and_remaining_plot(self):

         service_data_tod = pd.DataFrame(
    {
      "value": [100,50,5]*3,  # 9 elements
      "TypeData": ["requests","remaining","errors"]*3, # 9 elements
      "service_type": ["Text to Speech", "Text to Dialect", "Speech to Speech"]*3 , # 6 elements
    }
  )

         labels_servs = {
                      "label_dropdown":"Type Service",
                      "Type": "TypeData",
                      "x": "value",
                      "y": "service_type"
                  }
         return service_data_tod,labels_servs

    def  ge_by_filter(self,start,end):
        return service_data


