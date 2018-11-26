import sys, nltk
from collections import defaultdict
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords


METHODS = ['simplified', 'best-avg', 'orig', 'leading']
stops = stopwords('english')


def getDocuments(paths):
    docs = []
    docs_tokens = []
    for path in paths:
        with open(path, 'r', encoding='utf8') as f:
            s = f.read()
            f.close()
        sents = sent_tokenize(s)
        tokens = [word_tokenize(sent) for sent in sents]
        docs.append(sents)
        docs_tokens.append(tokens)
    return docs, docs_tokens


def sumBasic(documents, docs_tokens, method='orig', length=100):
    # Get probs
    probs = defaultdict(int)
    sentprobs = defaultdict(int)
    result = ""

    if method == 'leading':
        sentences = [sen for doc in documents for sen in doc]
        num = 0
        while num < length:
            if len(sentences) == 0:
                return result
            result += sentences.pop() + "\n"
            num = len(word_tokenize(result))
        return result

    N = sum([len(tokens) for doc in docs_tokens for tokens in doc])

    for i in range(0, len(documents)): # i: doc
        doc = documents[i]
        for j in range(0, len(doc)): # j: sentence
            tokens = docs_tokens[i][j]
            for token in tokens:
                probs[token] += 1/N

    num = 0
    while num < length:
        # Score sentences
        for i in range(0, len(documents)):
            doc = documents[i]
            for j in range(0, len(doc)):
                sent = docs_tokens[i][j]
                for token in sent:
                    sentprobs[doc[j]] += probs[token]/len(sent)

        # most probable word
        most_prob_word = max(probs.items(), key=lambda k: k[1])[0]

        if method != METHODS[1]: # best-avg no word prob
            # sentences with that word
            sents = [documents[i][j] for i in range(0, len(documents)) for j in range(0, len(documents[i]))
                     if most_prob_word in docs_tokens[i][j]]
        else:
            # all sentences
            sents = [doc[i] for doc in documents for i in range(0, len(doc))]

        if len(sents) == 0:
            return result
        # max prob. sentence among candidates
        sent = max(sents, key=lambda k: sentprobs[k])
        sentprobs.pop(sent)
        for i in range(0, len(documents)):
            for j in range(0, len(documents[i])):
                if documents[i][j] == sent:
                    idx = (i,j)
                    documents[i].pop(j)
                    docs_tokens[i].pop(j)
                    break
        num += len(word_tokenize(sent))
        result += sent+"\n"

        if method != METHODS[0]: # simple no redundancy
            for word in word_tokenize(sent):
                probs[word] **= 2

        # print([len(doc) for doc in docs], docs)

    return result


if __name__ == '__main__':

    try:
        method = sys.argv[1]
        docpaths = sys.argv[2:]
    except IndexError as e:
        print("Expected at least two parameters: [method], [path1, path2, ...].")
        quit(1)

    docs, docs_tokens = getDocuments(docpaths)

    if method in METHODS:
        print(sumBasic(docs, docs_tokens, method=method).replace('\u200b', ''))
    else:
        print("Method must be one of 'best-avg', 'simplified', or 'orig', got {}.".format(method))
        quit(1)
