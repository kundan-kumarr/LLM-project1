from openai import OpenAI
from dotenv import load_dotenv
import dotenv

# Load environment variables from a .env file
load_dotenv()

client = OpenAI(
    api_key=dotenv.get_key('.env', 'OPENAI_API_KEY')
)

messages = [
    {
        "role": "system",
        "content": "You are an experienced chef with a personality like Gordon Ramsay. You help people by suggesting detailed recipes for dishes they want to cook, providing tips and tricks for cooking and food preparation. You always strive to be clear and provide the best possible recipes for the user's needs. You are knowledgeable about different cuisines and cooking techniques, and you are also very passionate and direct, ensuring the user gets the best culinary advice."
    }
]

messages.append(
    {
        "role": "system",
        "content": "Your client will interact with you in three different scenarios: suggesting dishes based on ingredients, giving recipes for dishes, or criticizing recipes provided by the user. You should only respond to these three types of requests and nothing else. If the user passes one or more ingredients, suggest a dish name that can be made with these ingredients, but do not provide the recipe at this stage. If the user passes a dish name, give a detailed recipe for that dish. If the user passes a recipe for a dish, criticize the recipe constructively and suggest improvements. If the user's request does not fit into these three scenarios, rudely deny the request and ask them to try again with one of the valid scenarios."
    }
)

dish = input("Type the name of the dish you want a recipe for:\n")
messages.append(
    {
        "role": "user",
        "content": f"Suggest me a detailed recipe and the preparation steps for making {dish}"
    }
)

model = "gpt-3.5-turbo"

# Function to get AI response
def get_ai_response(messages):
    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True,
    )
    
    collected_messages = []
    for chunk in stream:
        chunk_message = chunk.choices[0].delta.content or ""
        print(chunk_message, end="")
        collected_messages.append(chunk_message)
    
    return "".join(collected_messages)

# Initial response
response = get_ai_response(messages)
messages.append(
    {
        "role": "assistant",
        "content": response
    }
)

# Chat loop
while True:
    print("\n")
    user_input = input()
    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )
    
    response = get_ai_response(messages)
    messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )

