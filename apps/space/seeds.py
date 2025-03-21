
class SpaceDev:
    def __init__(self, token):
        """Initialize the SpaceDev class with a token"""
        self.token = token

    def create_space(self,data):
        try:
            # Validate input types (add more validation if necessary)


            # # Prepare the data
            # data = {
            #     "name": name,
            #     "description": description,
            #     "ram": ram,
            #     "cpuCores": cpu_cores,
            #     "diskSpace": disk_space,
            #     "isGpu": is_gpu,
            #     "isGlobal": is_global,
            #     "bandwidth": bandwidth,
            #     "token": self.token,  # Use instance token
            #     "subscriptionId": subscription_id
            # }

            # Return success response
            return {
                "status": "success",
                "data": data,
                "message": "Space created successfully.",
                "status_code": 200
            }


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
        """Update space details and return a structured response"""
        try:


            # Update logic (for demo, we'll return the same data)
            return {
                "status": "success",
                "data": data,
                "message": f"Space with ID {space_id} updated successfully.",
                "status_code": 200
            }

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


            # Sample data for demonstration purposes
            data = {
                "name": "ggg",
                "description": "string",
                "ram": 0,
                "cpuCores": 0,
                "diskSpace": 0,
                "isGpu": True,
                "isGlobal": True,
                "bandwidth": 0
            }

            return {
                "status": "success",
                "data": data,
                "message": f"Space data for ID {space_id} retrieved successfully.",
                "status_code": 200
            }

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
