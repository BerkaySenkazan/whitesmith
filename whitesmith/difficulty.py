import os
import textacy.text_stats
import textstat
import spacy
import pandas as pd
import termcolor
import textacy

nlp = spacy.load("en_core_web_md")

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


def w_cefr_score(word, cefr):
    cefr_map = {"A1" : 0.1, "A2" : 0.2, "B1" : 0.4, "B2" : 0.6, "C1" : 0.8, "C2" : 1.0}

    cefr_level = get_cefr_data(word)
    termcolor.termcolor.cprint(cefr_level, "green")
    return cefr_map.get(cefr_level, cefr_map.get(cefr))


def s_fk_score(sentence, min = 0, max = 12):
    fk = textstat.textstat.flesch_kincaid_grade(sentence)
    normalized_score = (fk - min) / (max - min)
    return normalized_score

def s_complexity_score(sentence):
    doc = nlp(sentence)
    num_subordinate_clauses = sum(1 for token in doc if token.dep_ == "mark")
    termcolor.cprint(str(num_subordinate_clauses),"light_magenta")

    textacy.text_stats.diversity

    return min(1.0, max(0.0, num_subordinate_clauses / 5))

    
def algorithmic_difficulty(sentence):
    


    dc = textstat.textstat.dale_chall_readability_score_v2(sentence)
    ke = textstat.textstat.flesch_reading_ease(sentence)
    fk = textstat.textstat.flesch_kincaid_grade(sentence)
    
    cl = textstat.textstat.coleman_liau_index(sentence)
    gf = textstat.textstat.gunning_fog(sentence)

    normalized_ke = ((100 - ke) / 100) * 15

    weights = {
        "dale_chall": 0.3,
        "flesch_reading_ease": 0.25,
        "flesch_kincaid": 0.2,
        "coleman_liau": 0.15,
        "gunning_fog": 0.1,
    }

    combined_score = (
        weights["dale_chall"] * max(dc,0) +
        weights["flesch_reading_ease"] * max(normalized_ke,0) +
        weights["flesch_kincaid"] * max(fk, 0) +
        weights["coleman_liau"] * max(cl,0) +
        weights["gunning_fog"] * max(gf,0)
    )

    return {"ke" : normalized_ke, "dc": dc, "fk": fk, "cl": cl, "gf" : gf, "combined" : combined_score}


def diversity_score(sentence):
    words = sentence.split()
    unique_words = set(words)
    diversity = len(unique_words) / len(words)
    return min(1.0, max(0.0, 1 - diversity))


def w_total_score(word, cefr):

    w1, w2,  = 0.5, 0.5,

    w_freq = get_freq_data(word)
    w_cefr = w_cefr_score(word, cefr)



    score = (w1 * w_freq + w2 * w_cefr)

    return round(score,3)

def s_total_score(s , cefr):
    diverse_w, complex_w, fk_w, w_total_w = 0.25, 0.30, 0.20, 0.25

    sentence = nlp(s)
    total_w_score = 0
    for w in sentence:
        if w.pos_ not in {"PUNCT", "NUM", "SYM"}:
            lemma = w.lemma_
            total_w_score += w_total_score(w, cefr)
            print(total_w_score , lemma, w.text, w.pos_)
    avg_w_sc = total_w_score / len(sentence.doc)

    d_sc = diversity_score(s)
    c_sc = s_complexity_score(s)
    fk_sc = s_fk_score(s)

    total = diverse_w * d_sc + complex_w * c_sc + fk_w * fk_sc + w_total_w * avg_w_sc
    mapped_value = (total - 0.01) / (0.6 - 0.01)
    return round(mapped_value, 3)
        




