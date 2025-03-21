import requests
import logging

class SpaceAPI:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.headers = {
            "accept": "text/plain",
            "Content-Type": "application/json",
            "Authorization": f"{token}"
        }
        logging.basicConfig(level=logging.INFO)

    def get_spaces(self):
        """ Fetch all spaces """
        try:
            url = f"{self.base_url}/api/Space"
            response = requests.get(url, headers=self.headers)

            return self._handle_response(response)

        except requests.exceptions.RequestException as e:
            logging.error(f"Error during GET request to {self.base_url}/api/Space: {e}")
            return self._handle_error(e)

    def get_data_space_by_id(self, space_id):
        """ Fetch a single space by ID """
        try:
            url = f"{self.base_url}/api/Space/{space_id}"
            response = requests.get(url, headers=self.headers)

            return self._handle_response(response)

        except requests.exceptions.RequestException as e:
            logging.error(f"Error during GET request to {self.base_url}/api/Space/{space_id}: {e}")
            return self._handle_error(e)

    def create_space(self, data):
        """ Create a new space """
        try:
            url = f"{self.base_url}/api/Space"
            response = requests.post(url, json=data, headers=self.headers)

            return self._handle_response(response)

        except requests.exceptions.RequestException as e:
            logging.error(f"Error during POST request to {self.base_url}/api/Space: {e}")
            return self._handle_error(e)

    def update_space(self, space_id, data):
        """ Update space data """
        try:
            url = f"{self.base_url}/api/Space/{space_id}"
            response = requests.put(url, json=data, headers=self.headers)

            return self._handle_response(response)

        except requests.exceptions.RequestException as e:
            logging.error(f"Error during PUT request to {self.base_url}/api/Space/{space_id}: {e}")
            return self._handle_error(e)

    def delete_space(self, space_id):
        """ Delete a space """
        try:
            url = f"{self.base_url}/api/Space/{space_id}"
            response = requests.delete(url, headers=self.headers)

            return self._handle_response(response)

        except requests.exceptions.RequestException as e:
            logging.error(f"Error during DELETE request to {self.base_url}/api/Space/{space_id}: {e}")
            return self._handle_error(e)

    def _handle_response(self, response):
        """ Handle API responses and format output """
        if response.status_code in [200, 201]:
            return {
                "status": "success",
                "data": response.json(),
                "message": "Request processed successfully.",
                "details": "",
                "status_code": response.status_code
            }

        return self._handle_error(response)

    def _handle_error(self, error):
        """ Handle errors and format the response """
        if isinstance(error, requests.exceptions.RequestException):
            return {
                "status": "failed",
                "data": None,
                "message": "An error occurred while connecting to the server.",
                "details": str(error),
                "status_code": 0
            }

        # Error messages for specific HTTP status codes
        error_messages = {
            400: "Bad Request: Check the submitted data.",
            401: "Unauthorized: Check your token or permissions.",
            403: "Forbidden: You don't have access to this resource.",
            404: "Not Found: The requested resource does not exist.",
            429: "Too Many Requests: Rate limit exceeded. Try again later.",
            500: "Internal Server Error: Something went wrong on the server."
        }

        if isinstance(error, requests.models.Response):
            # Handle HTTP error codes
            return {
                "status": "failed",
                "data": None,
                "message": error_messages.get(error.status_code, "Unexpected Error"),
                "details": error.text,
                "status_code": error.status_code
            }

        # If we receive an unexpected error type, log and return a general failure
        logging.error(f"Unexpected error: {error}")
        return {
            "status": "failed",
            "data": None,
            "message": "An unexpected error occurred.",
            "details": str(error),
            "status_code": 0
        }
