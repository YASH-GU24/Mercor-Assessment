def get_user_chat_history(chat_history):
    result = []
    for msg in chat_history:
        if msg["type"] == "user":
            result.append(msg["text"])
    return result
