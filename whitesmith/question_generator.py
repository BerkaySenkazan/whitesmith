import anthropic
import spacy
import os

client = anthropic.Anthropic(
    api_key= os.getenv("API_KEY")
)


def createQuestion(q_type, ex_type):

    try:
        message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=250,
        temperature=0.4,
        system="You are a question generator specialized in creating questions compatible with Turkish YDS, YDT, and YÖKdil formats with four options. Produce only the following components without commentary or line breaks separated by \"$\":\n\nThe question text\nAn English instruction (e.g., \"Choose the correct answer.\")\nThe answer choices (without labels like A, B, C) each answer is separated by \"%\" (eg. opt1 % opt2) \n if there's a \"/\" in the options, keep them as is.  \nThe answer choice",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Create a question for {ex_type}, Evaluate {q_type} knowledge. Have only one blank. Randomize correct answers."
                    }
                ]
            }
        ]
    )

    except:
        print("Error generating Question.")
    finally:

        response_text = message.content[0].text

        print(response_text)
        return response_text