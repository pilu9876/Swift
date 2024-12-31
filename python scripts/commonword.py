from preprocess import textPreprocess

def findcommonword(query, liststring):
    string1 = textPreprocess([query])
    c=0
    for text in liststring:
        string2 = textPreprocess([text])
        words1 = set(string1[0].split())
        words2 = set(string2[0].split())
        common_words = words1.intersection(words2)
        if len(common_words)>1:
            c=1
            break
    if c==1:
        return text
    else:
        return "could not understand"