import collections, math, string

class CustomLanguageModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.unigramCounts = collections.defaultdict(lambda: 0)
    self.bigramCounts = collections.defaultdict(lambda: 0)
    self.trigramCounts = collections.defaultdict(lambda: 0)
    self.followingWords = collections.defaultdict(lambda: set())
    self.precedingWords = collections.defaultdict(lambda: set())
    self.total = 0
    self.discount = 0.75
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
            self.total += 1

        i = 0
        while i < len(sentence.data) - 1:
            token = str(cleanSentence.get(i))
            self.followingWords[token].add(str(cleanSentence.get(i+1)))
            i += 1

        i = 1
        while i < len(sentence.data):
            bigram = str(cleanSentence.get(i-1)) + " " + str(cleanSentence.get(i))
            self.bigramCounts[bigram] = self.bigramCounts[bigram] + 1

            self.precedingWords[str(cleanSentence.get(i))].add(str(cleanSentence.get(i-1)))
            i += 1
        self.precedingWordsTotal = sum(map(lambda x: len(x), self.precedingWords.values()))

        i = 2
        while i < len(sentence.data):
            trigram = str(cleanSentence.get(i-2)) + " " + str(cleanSentence.get(i-1)) + " " + str(cleanSentence.get(i))
            self.trigramCounts[trigram] = self.trigramCounts[trigram] + 1
            i += 1

    #print('precedingWords')
    #print(self.precedingWords)
    #print('followingWords')
    #print(self.followingWords)
    #print('unigrams')
    #print(self.unigramCounts)
    #print('bigrams')
    #print(self.bigramCounts)

        #self.discount(self.trigramCounts)
        #self.discount(self.bigramCounts)
        #self.discount(self.unigramCounts)


  def discount(self, counts):
      for token in counts:
        self.discountValue(counts[token])

  def discountValue(self, count):
      if count > 1:
        return count - 0.75
      elif count == 1:
        return count - 0.5
      else:
        return 0.00003

  def mainScore(self, sentence, i):
      bigram = string.join(sentence[i-1:i+1])
      return max(self.bigramCounts[bigram] - self.discount, 0) / float(self.unigramCounts[sentence[i-1]])

  def lambdaCoefficient(self, word):
      # print('followingWords', word, self.followingWords[word])
      return (self.discount / float(self.unigramCounts[word])) * len(self.followingWords[word])

  def pContinuation(self, word):
      # print('precedingWords', word, self.precedingWords[word])
      #return len(self.precedingWords[word]) / float(len(self.bigramCounts))
      return len(self.precedingWords[word]) / float(self.precedingWordsTotal)

  # Kneser-Ney smoothing with additional penalty for unknown words
  def score(self, sentence):
      i = 0
      score = 0
      # key factor to get 0.244 accuracy
      # if we apply fallback score twice, we lower score for unknown words,
      # because log of a fraction is negative
      # quite strange, but it works
      penalty = 2
      # fallback score taken from https://stats.stackexchange.com/a/168124
      # (without penalty)
      fallbackScore = penalty * math.log(self.discount / float(len(self.unigramCounts)))
      while i < len(sentence):
          if self.unigramCounts[sentence[i]] > 0 and self.unigramCounts[sentence[i-1]] > 0:
              mainScore = self.mainScore(sentence, i)
              lambdaCoefficient = self.lambdaCoefficient(sentence[i-1])
              pContinuation = self.pContinuation(sentence[i])
              wordScore = mainScore + lambdaCoefficient * pContinuation
              if wordScore > 0:
                #print(sentence[i-1], sentence[i], mainScore, lambdaCoefficient, pContinuation, wordScore, math.log(wordScore))
                score += math.log(wordScore)
              else:
                score += fallbackScore
          else:
              # print(sentence[i-1], sentence[i], self.unigramCounts[sentence[i-1]], self.unigramCounts[sentence[i]])
              score += fallbackScore
          i += 1
      return score

  # not so good
  def simpleDiscountScore(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the
        sentence using your language model. Use whatever data you computed in train() here.
    """
    #score = 0
    i = 1
    coeff3 = 0.6
    coeff2 = 0.3
    coeff1 = 0.1
    score = 0
    while i < len(sentence):
        trigram = str(sentence[i-2]) + " " + str(sentence[i-1]) + " " + str(sentence[i])
        bigram = str(sentence[i-1]) + " " + str(sentence[i])
        unigram = str(sentence[i])

        score += coeff3 * self.trigramCounts[trigram] / float(len(self.bigramCounts) + self.bigramCounts[sentence[i-1]])

        score += coeff2 * self.bigramCounts[bigram] / float(len(self.unigramCounts) + self.unigramCounts[sentence[i-1]])

        score += coeff1 * self.unigramCounts[unigram] / float(len(self.unigramCounts) + self.total)

        i += 1
    return math.log(score)
# not so good
def backoff():
  if self.trigramCounts.has_key(trigram):
      score += math.log(self.trigramCounts[trigram])
      score -= math.log(self.bigramCounts[sentence[i-1]])
  elif self.bigramCounts.has_key(bigram):
      score += math.log(self.bigramCounts[bigram])
      score -= math.log(self.unigramCounts[sentence[i-1]])
  else:
      score += coeff + math.log(self.unigramCounts[unigram])
      score -= math.log(self.total)
