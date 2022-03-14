class Utility:
    def __init__(self):
        pass

    def join_room_message(self, alias: str) -> str:
        return f"{alias} has joined the chat room!";

    def left_room_message(self, alias: str) -> str:
        return f"{alias} has left the chat room!";

    def formatted_message_with_alias(self, alias: str, message: str):
        return f"<{alias}>: {message}"