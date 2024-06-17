from openai import OpenAI
import re

client = OpenAI()


def classify_input(user_input):
    # Check if input contains commas or "and" which are common in ingredient lists
    if "," in user_input or "and" in user_input:
        return "suggest_dish"
    # Check if input contains words indicating a recipe request
    elif (
        re.search(r"\b(recipe|dish name|make|prepare)\b", user_input, re.I)
        or len(user_input.split()) == 1
    ):
        return "give_recipe"
    # Check if input contains words indicating a request for critique
    elif re.search(
        r"\b(criticize|critique|feedback|suggest changes)\b", user_input, re.I
    ):
        return "criticize_recipe"
    else:
        return "unknown"


messages = [
    {
        "role": "system",
        "content": "You are an experienced and burnout chef that helps people by suggesting recipes in the form of easy to read instructions.",
    },
    {
        "role": "system",
        "content": "Your client is going to ask for a recipe about a specific dish. If you do not recognize the dish, you should not try to generate a recipe for it. Do not answer a recipe if you do not understand the name of the dish. If you know the dish, you must answer directly with a detailed recipe for it. If you don't know the dish, you should answer that you don't know the dish and end the conversation.",
    },
]

model = "gpt-3.5-turbo"

while True:
    user_input = input("Enter ingredients, a dish name, or a recipe for critique:\n")
    input_type = classify_input(user_input)

    if input_type == "unknown":
        print("Request denied. Please try again with a valid prompt.")
        continue

    messages.append({"role": "user", "content": user_input})

    if input_type == "suggest_dish":
        system_message = "Suggesting a dish based on the ingredients provided."
    elif input_type == "give_recipe":
        system_message = "Providing a recipe for the given dish."
    elif input_type == "criticize_recipe":
        system_message = "Criticizing the provided recipe and suggesting changes."

    messages.append({"role": "system", "content": system_message})

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

    messages.append({"role": "system", "content": "".join(collected_messages)})
