import requests

class DashAPI:
    def __init__(self, base_url, token=None):
        """
        Initialize the DashAPI class.
        :param base_url: The base URL of the API.
        :param token: Optional token for authentication.
        """
        self.base_url = base_url
        self.headers = {
            "Authorization": f"{token}" if token else "",
            "Content-Type": "application/json"
        }

    def get_service_usage_data(self):
        url = f"{self.base_url}/api/Dashboard/ServiceUsageData"
        response = requests.get(url, headers=self.headers)
        return self._handle_response(response)

    def get_service_users_count(self):
        url = f"{self.base_url}/api/Dashboard/ServiceUsersCount"
        response = requests.get(url, headers=self.headers)
        return self._handle_response(response)
    def GetRequestsByDatetime(self,request_data):
        url = f"{self.base_url}/api/Dashboard/GetRequestsByDatetime"
        response = requests.get(url, headers=self.headers, json=request_data)
        print(response.json())
        return self._handle_response(response)

    def get_service_usage_and_remaining(self):
        url = f"{self.base_url}/api/Dashboard/ServiceUsageAndRemaining"
        response = requests.get(url, headers=self.headers)
        return self._handle_response(response)
    def get_ModelAi_Service_Requests(self):
        url = f"{self.base_url}/api/Dashboard/ModelAiServiceRequests"
        response = requests.get(url, headers=self.headers)
        return self._handle_response(response)
    def post_service_requests(self, request_data):
        url = f"{self.base_url}/api/Dashboard/ServiceRequests"
        response = requests.post(url, headers=self.headers, json=request_data)
        return self._handle_response(response)

    def get_model_ai_service_requests(self):
        url = f"{self.base_url}/api/Dashboard/ModelAiServiceRequests"
        response = requests.get(url, headers=self.headers)
        return self._handle_response(response)

    def get_space_requests(self):
        url = f"{self.base_url}/api/Dashboard/SpaceRequests"
        response = requests.get(url, headers=self.headers)
        return self._handle_response(response)

    def _handle_response(self, response):
        """
        Handle the API response.
        :param response: The response object from requests.
        :return: The JSON data or error details.
        """
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            return {"error": True, "status_code": response.status_code, "details": str(e)}
        except requests.exceptions.RequestException as e:
            return {"error": True, "details": str(e)}


