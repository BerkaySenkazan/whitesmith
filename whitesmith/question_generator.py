import anthropic
import spacy
import os

API_KEY = os.getenv("ANTHROPIC")


client = anthropic.Anthropic(
    api_key= API_KEY
)




def createQuestion(theme, level):


    if (len(API_KEY) == 0):
        print("Error generating Question: API Problems")
        return "api key not defined."

    try:
        message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=250,
        temperature=0.4,
        system="You are a sentence generator. Create sentences of specified CEFR level. If specified, make it the specified domain. Only give the sentence, no commentary.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"create a ${theme} themed sentence in ${level} CEFR level."
                    }
                ]
            }
        ]
    )

    except Exception as e:
        print(f"Error generating Question. ${str(e)} ${API_KEY}")
    finally:

        response_text = message.content[0].text

        print(response_text)
        return response_text
    
