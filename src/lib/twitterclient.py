class TwitterClient:
    def __init__(self, bearer_token: str):
        self.__headers = {"Authorization": f"Bearer {bearer_token}"}
