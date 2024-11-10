import math
import os
import termcolor.termcolor
import textstat
import spacy
import pandas as pd
import termcolor

nlp = spacy.load("en_core_web_sm")

cefr_ds_path = os.path.join(os.path.dirname(__file__), "data", "level_dataset.csv")
freq_ds_path = os.path.join(os.path.dirname(__file__), "data", "rank_freq.csv")

cefr_ds = pd.read_csv(cefr_ds_path)
freq_ds = pd.read_csv(freq_ds_path)

def get_freq_data(word):

    result_lemma = freq_ds[freq_ds["word"] == word.lemma_]
    result = freq_ds[freq_ds["word"] == word.text]
    if not result.empty:
        return result["inverted_frequency_score"].values[0]
    elif not result_lemma.empty and result.empty:
        termcolor.termcolor.cprint("returned " + word.lemma_ + " with " + str(result_lemma["inverted_frequency_score"].values[0]) + " freq value", "light_blue")
        return result_lemma["inverted_frequency_score"].values[0]
        
    else:
        return 0.4

def get_cefr_data(word):

    result_lemma = cefr_ds[cefr_ds["headword"] == word.lemma_]
    result = cefr_ds[cefr_ds["headword"] == word.text]
    if not result.empty:
        return result["CEFR"].values[0]
    elif not result_lemma.empty and result.empty:
        termcolor.termcolor.cprint("returned " + word.lemma_ + " with " + result_lemma["CEFR"].values[0] + " level", "light_red")
        return result_lemma["CEFR"].values[0]
        
    else: 
        return None


def w_cefr_score(word):
    cefr_map = {"A1" : 0.1, "A2" : 0.2, "B1" : 0.4, "B2" : 0.6, "C1" : 0.8, "C2" : 1.0}

    cefr_level = get_cefr_data(word)
    termcolor.termcolor.cprint(cefr_level, "green")
    return cefr_map.get(cefr_level, 0.5)


def s_fk_score(sentence, min = 0, max = 12):
    fk = textstat.textstat.flesch_kincaid_grade(sentence)
    normalized_score = (fk - min) / (max - min)
    return normalized_score

def s_complexity_score(sentence):
    doc = nlp(sentence)
    num_subordinate_clauses = sum(1 for token in doc if token.dep_ == "mark")
    return min(1.0, max(0.0, num_subordinate_clauses / 5))

def diversity_score(sentence):
    words = sentence.split()
    unique_words = set(words)
    diversity = len(unique_words) / len(words)
    return min(1.0, max(0.0, 1 - diversity))


def w_total_score(word):

    w1, w2,  = 0.5, 0.5,

    w_freq = get_freq_data(word)
    w_cefr = w_cefr_score(word)



    score = (w1 * w_freq + w2 * w_cefr)

    return round(score,3)

def s_total_score(s):
    diverse_w, complex_w, fk_w, w_total_w = 0.25, 0.30, 0.20, 0.25

    sentence = nlp(s)
    total_w_score = 0
    for w in sentence:
        if w.pos_ not in {"PUNCT", "NUM", "SYM"}:
            lemma = w.lemma_
            total_w_score += w_total_score(w)
            print(total_w_score , lemma, w.text, w.pos_)
    avg_w_sc = total_w_score / len(sentence.doc)

    d_sc = diversity_score(s)
    c_sc = s_complexity_score(s)
    fk_sc = s_fk_score(s)

    return round(diverse_w * d_sc + complex_w * c_sc + fk_w * fk_sc + w_total_w * avg_w_sc, 3)
        

# word = "The enthusiastic young investor carefully studied the stock market trends before making her first investment. After six months of disciplined saving and smart decisions, she was thrilled to see her portfolio grow by fifteen percent."

# def trial():
#     return s_total_score(word)


# print(trial())

