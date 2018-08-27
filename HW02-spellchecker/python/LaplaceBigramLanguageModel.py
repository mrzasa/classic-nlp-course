import collections, math

class LaplaceBigramLanguageModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.total = 0
    self.unigramCounts = collections.defaultdict(lambda: 0)
    self.bigramCounts = collections.defaultdict(lambda: 1)
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model.
        Compute any counts or other corpus statistics in this function.
    """
    for sentence in corpus.corpus:
        cleanSentence = sentence.cleanSentence()
        for datum in cleanSentence.data:
            token = datum.word
            self.unigramCounts[token] = self.unigramCounts[token] + 1

        i = 1
        while i < len(sentence.data):
            bigram = str(cleanSentence.get(i-1)) + " " + str(cleanSentence.get(i))
            self.bigramCounts[bigram] = self.bigramCounts[bigram] + 1
            self.total += 1
            i += 1

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the
        sentence using your language model. Use whatever data you computed in train() here.
    """
    score = 0
    i = 1
    while i < len(sentence):
        bigram = str(sentence[i-1]) + " " + str(sentence[i])
        score += math.log(self.bigramCounts[bigram])
        score -= math.log(self.total + self.unigramCounts[sentence[i-1]])
        i += 1

    return score
