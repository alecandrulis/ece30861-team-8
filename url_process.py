from typing import Literal
from classes.llm_child_api import GenAiChatApi

url_type = Literal["model", "dataset", "code", "invalid"]

def identify_urltype(url: str, api_key: str) -> url_type:

    # Set prompt
    prompt = f"""
        Given this url, classify if it leads to a
        - ML/AI model
        - A dataset used to train a ML/AI model
        - The code to an ML/AI model
        - None of the Above

        URL: {url}

        Answer only one word corresponding to your answer with one of the following:
        (model, dataset, code, invalid)
    """
    # Initialize the client
    chat_api = GenAiChatApi(
        base_url="https://genai.rcac.purdue.edu",
        model="llama3.1:latest"
    )

    # Set the token
    chat_api.set_bearer_token(api_key)

    # Ask for response
    response = chat_api.get_chat_completion(prompt)
    
    #Formatting response (precautionary) and return
    formatted_response = response.strip().lower()
    if formatted_response in ["model", "dataset", "code", "invalid"]:
        return formatted_response
    return False
