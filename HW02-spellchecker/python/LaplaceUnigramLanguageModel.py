import collections, math

class LaplaceUnigramLanguageModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.total = 0
    self.unigramCounts = collections.defaultdict(lambda: 1)
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model.
        Compute any counts or other corpus statistics in this function.
    """

    for sentence in corpus.corpus:
        for datum in sentence.data:
            token = datum.word
            self.unigramCounts[token] = self.unigramCounts[token] + 1
            self.total += 1

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the
        sentence using your language model. Use whatever data you computed in train() here.
    """
    score = 0
    for token in sentence:
        score += math.log(self.unigramCounts[token])
        score -= math.log(self.total + len(self.unigramCounts))

    return score
