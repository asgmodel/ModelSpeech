from fastapi import APIRouter

class UserHandler:
    def __init__(self,builder):
        self.router = APIRouter()
        self.__builder=builder
    

        @self.router.get("/users")
        def get_users():
            return {"message": "List of users"}

        @self.router.get("/users/{user_id}")
        def get_user(user_id: int):
            return {"message": f"User {user_id}"}

    def  get_router(self):
    
           return self.router
