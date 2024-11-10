import anthropic
import spacy
import os
import re
from nltk.corpus import wordnet as wn
from .difficulty import s_total_score

##API_KEY = os.getenv("ANTHROPIC")
API_KEY = "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"
nlp = spacy.load("en_core_web_md")

client = anthropic.Anthropic(
    api_key= API_KEY
)




def createQuestion(theme, level, pos):

    partspeech = spacy.explain(pos)


    if (len(API_KEY) == 0):
        print("Error generating Question: API Problems")
        return "api key not defined."

    try:
        message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=250,
        temperature=1,
        system="You are a sentence generator for English learners. Generate sentences based on given themes and levels. Only sentences, no commentary. Generate exactly two sentences, no more, no less.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Think of a ${theme}-related scenario suitable for a ${level} CEFR learner. Create two sentences: The first sentence introduces the scenario and includes a ${partspeech}. The second sentence provides additional context or detail, ensuring both sentences are connected and form a cohesive description."
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
    

def omitSimple(sentence, pos, detailed):

    modified_sentence = None
    correct_option = None
    tokens = nlp(sentence)

    if (detailed):
        for t in tokens:
            if t.tag_ == pos:
                correct_option = str(t)
                modified_sentence = re.sub(rf"\b{re.escape(str(t))}\b", "__________", sentence)
    else:
        for t in tokens:
            if t.pos_ == pos:
                correct_option = str(t)
                modified_sentence = re.sub(rf"\b{re.escape(str(t))}\b", "__________", sentence)

    return {"sentence" : modified_sentence, "correct" : correct_option}
    

def generateOptions(theme, pos, cefr, sentence):

    if(sentence == None):
        return {"generated_answers" : "nothing returned"}
    try:
        message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=250,
        temperature=1,
        system="You are a language assessment assistant. Generate varied distractors for vocabulary exercises. Give only the words, no commentary. Separate the words with ','",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"""First, identify the correct answer for the blank in '${sentence}'. Next, generate six ${theme}-related words at CEFR ${cefr} level for distractors. Include:
- Two words that are similar in meaning or sound to the correct answer but makes no sense (to increase confusion).
- Two words that are clearly unrelated to the context of the sentence.
Ensure that the distractors do not fit the blank grammatically or semantically.""",
                    }
                ]
            }
        ]
    )

    except Exception as e:
        print(f"Error generating Question. ${str(e)} ${API_KEY}")
    finally:


        response_text = message.content[0].text

        return {"generated_answers": response_text}

def generateDistractors(correct):
    distractors = []
    synsets = wn.synsets(correct)
    if not synsets:
        return distractors

    for syn in synsets:
        for lemma in syn.lemmas():
            if lemma.name().lower() != correct.lower():
                distractors.append(lemma.name().replace("_", " "))
    
    return list(set(distractors))

def make_fill_blanks(theme, cefr, pos, detailed):
    q_sentence = createQuestion(theme, cefr, pos)

    o_sentence = omitSimple(q_sentence, pos, detailed)
    question = o_sentence["sentence"]
    correct = o_sentence["correct"]
    print(correct)

    answers = generateOptions(theme,pos,cefr,o_sentence)
    answ = answers

    return {"question" : question, "answers": answ, "correct": correct}


def test():
    q = make_fill_blanks("Financial, positive, investing", "B2", "ADJ", False)

    print(s_total_score(q["question"]))

test()