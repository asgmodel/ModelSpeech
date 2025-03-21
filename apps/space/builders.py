
from .clients import *
from typing import List
 
 

class builderSpace:

    def __init__(self,urlapi,token):


        self.buider=SpaceAPI(urlapi,token)

    def create_space(self,data):

        try:

            result=self.buider.create_space(data)
            if result!=None:

                return result
            else:
                print("Error creating space.")
                return None

            return result

        except ValueError as e:
            return {
                "status": "failed",
                "data": None,
                "message": str(e),
                "status_code": 400
            }

        except Exception as e:
            return {
                "status": "failed",
                "data": None,
                "message": "An error occurred while creating the space.",
                "details": str(e),
                "status_code": 500
            }


    def update_space(self, space_id, data):

        try:



            result=self.buider.update_space(space_id,data)
            if result!=None:
                return result
            else:
                print("Error updating space.")
                return None


        except ValueError as e:
            return {
                "status": "failed",
                "data": None,
                "message": str(e),
                "status_code": 400
            }

        except Exception as e:
            return {
                "status": "failed",
                "data": None,
                "message": "An error occurred while updating the space.",
                "details": str(e),
                "status_code": 500
            }

    def get_data_space_by_id(self, space_id):
        """Retrieve space data by ID and return a structured response"""
        try:

            result=self.buider.get_data_space_by_id(space_id)
            if result!=None:
                return result
            else:
                print("Error retrieving space data.")
                return None

        except ValueError as e:
            return {
                "status": "failed",
                "data": None,
                "message": str(e),
                "status_code": 400
            }

        except Exception as e:
            return {
                "status": "failed",
                "data": None,
                "message": "An error occurred while retrieving the space data.",
                "details": str(e),
                "status_code": 500
            }
