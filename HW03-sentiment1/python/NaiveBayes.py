# NLP Programming Assignment #3
# NaiveBayes
# 2012

#
# The area for you to implement is marked with TODO!
# Generally, you should not need to touch things *not* marked TODO
#
# Remember that when you submit your code, it is not run from the command line
# and your main() will *not* be run. To be safest, restrict your changes to
# addExample() and classify() and anything you further invoke from there.
#


import sys
import getopt
import os
import math
import collections
import matplotlib.pyplot as plt
import operator
import re

from shutil import copyfile

class BayesClassifier:
    def __init__(self, modelName):
        self.words = set()
        self.counts = { 'pos': collections.defaultdict(lambda: 1), 'neg': collections.defaultdict(lambda: 1) }
        self.docCount = collections.defaultdict(lambda: 0)
        self.documentModel = self.__getDocumentModel(modelName)

    class SimpleModel:
        def words(self, words):
            return words

    class BooleanNegationModel:
        def __init__(self):
            self.negation = BayesClassifier.NegationModel()
            self.boolean = BayesClassifier.BooleanModel()

        def words(self, words):
            return self.boolean.words(self.negation.words(words))

    class BooleanModel:
        def words(self, words):
            return list(set(words))

    class NegationModel:
        eos_pattern = re.compile('^[-.!?,;"\'():]$')
        negation_pattern = re.compile('(^not|n\'t|^no|^never|^nor|^neither|^none|^nothing|^non)$')

        def words(self, words):
            filtered = []
            negated = False
            for word in words:
                filtered.append(self._maybe_negate(word, negated))
                if not negated and self._is_negation(word):
                    negated = True
                if self._is_eos(word):
                    negated = False

            # print(words, filtered)
            return filtered


        def _maybe_negate(self, word, negate):
            if negate:
                return "NOT_%s" % word
            else:
                return word

        def _is_negation(self, word):
            return bool(self.negation_pattern.search(word))

        def _is_eos(self, word):
            return bool(self.eos_pattern.match(word))

    def __getDocumentModel(self, name):
        if name == 'simple':
            return self.SimpleModel()
        elif name == 'boolean':
            return self.BooleanModel()
        elif name == 'negation':
            return self.NegationModel()
        elif name == 'boolean_negation':
            return self.BooleanNegationModel()
        else:
            raise ValueError('Invalid document model name.')


    def classify(self, words):
        transformedWords = self.documentModel.words(words)
        probs = { 'pos': 0.0, 'neg': 0.0 }
        for klass in ['pos', 'neg']:
            wordProbs = {}
            totalCount = float(sum(self.counts[klass].values()) - len(self.counts[klass]) + len(self.words))
            for word in transformedWords:
                if not word in self.words:
                    continue
                prob = self.counts[klass][word] / totalCount
                wordProbs[word] = prob
                probs[klass] += math.log(prob)
            probs[klass] += math.log(self.docCount[klass]/float(sum(self.docCount.values())))

        sortedWordProbs = sorted(wordProbs.items(), key=lambda x:-x[1])
        res = max(probs.iteritems(), key=operator.itemgetter(1))[0]
        return res


    def addExample(self, klass, words):
        self.docCount[klass] += 1
        ww = self.documentModel.words(words)
        for word in ww:
            self.words.add(word)
            self.counts[klass][word] += 1

class NaiveBayes:
  class TrainSplit:
    """Represents a set of training/testing data. self.train is a list of Examples, as is self.test.
    """
    def __init__(self):
      self.train = []
      self.test = []

  class Example:
    """Represents a document with a label. klass is 'pos' or 'neg' by convention.
       words is a list of strings.
    """
    def __init__(self):
      self.klass = ''
      self.words = []
      self.filename = ''


  def __init__(self):
    """NaiveBayes initialization"""
    self.FILTER_STOP_WORDS = False
    self.stopList = set(self.readFile('../data/english.stop'))
    self.numFolds = 10

    #self.classifier = BayesClassifier('boolean_negation')
    #self.classifier = BayesClassifier('negation')
    #self.classifier = BayesClassifier('simple')
    self.classifier = BayesClassifier('boolean')


  def classify(self, words):
      return self.classifier.classify(words)

  def addExample(self, klass, words):
      return self.classifier.addExample(klass, words)

  def filterStopWords(self, words):
      return self.filterStopWordsDict(words)

  # results similar to no filtering, require changing the  main() code
  def filterStopWordsStats(self, words):
      maxCount = 0
      treshold = 0.9
      for w in words:
        count = self.totalCount(w)
        if count > maxCount:
            maxCount = count

      filtered = [w for w in words if self.totalCount(w) < 0.95 * maxCount]
      return filtered

  def totalCount(self, w):
    total = self.counts['pos'][w] + self.counts['neg'][w]
    return total

  def filterStopWordsDict(self, words):
       filtered = list(set(words) - self.stopList)
       return filtered


  def readFile(self, fileName):
    """
     * Code for reading a file.  you probably don't want to modify anything here,
     * unless you don't like the way we segment files.
    """
    contents = []
    f = open(fileName)
    for line in f:
      contents.append(line)
    f.close()
    result = self.segmentWords('\n'.join(contents))
    return result


  def segmentWords(self, s):
    """
     * Splits lines on whitespace for file reading
    """
    return s.split()


  def trainSplit(self, trainDir):
    """Takes in a trainDir, returns one TrainSplit with train set."""
    split = self.TrainSplit()
    posTrainFileNames = os.listdir('%s/pos/' % trainDir)
    negTrainFileNames = os.listdir('%s/neg/' % trainDir)
    for fileName in posTrainFileNames:
      example = self.Example()
      example.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
      example.klass = 'pos'
      split.train.append(example)
    for fileName in negTrainFileNames:
      example = self.Example()
      example.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
      example.klass = 'neg'
      split.train.append(example)
    return split

  def train(self, split):
    for example in split.train:
      words = example.words
      if self.FILTER_STOP_WORDS:
        words =  self.filterStopWords(words)
      self.addExample(example.klass, words)

  def crossValidationSplits(self, trainDir):
    """Returns a lsit of TrainSplits corresponding to the cross validation splits."""
    splits = []
    posTrainFileNames = os.listdir('%s/pos/' % trainDir)
    negTrainFileNames = os.listdir('%s/neg/' % trainDir)
    #for fileName in trainFileNames:
    for fold in range(0, self.numFolds):
      split = self.TrainSplit()
      for fileName in posTrainFileNames:
        example = self.Example()
        example.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
        example.klass = 'pos'
        if fileName[2] == str(fold):
          split.test.append(example)
        else:
          split.train.append(example)
      for fileName in negTrainFileNames:
        example = self.Example()
        example.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
        example.klass = 'neg'
        if fileName[2] == str(fold):
          split.test.append(example)
        else:
          split.train.append(example)
      splits.append(split)
    return splits


  def test(self, split):
    """Returns a list of labels for split.test."""
    labels = []
    for example in split.test:
      words = example.words
      if self.FILTER_STOP_WORDS:
        words =  self.filterStopWords(words)
      guess = self.classify(words)
      labels.append(guess)
    return labels

  def buildSplits(self, args):
    """Builds the splits for training/testing"""
    trainData = []
    testData = []
    splits = []
    trainDir = args[0]
    if len(args) == 1:
      print '[INFO]\tPerforming %d-fold cross-validation on data set:\t%s' % (self.numFolds, trainDir)

      posTrainFileNames = os.listdir('%s/pos/' % trainDir)
      negTrainFileNames = os.listdir('%s/neg/' % trainDir)
      for fold in range(0, self.numFolds):
        split = self.TrainSplit()
        for fileName in posTrainFileNames:
          example = self.Example()
          example.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
          example.klass = 'pos'
          example.fileName = fileName
          if fileName[2] == str(fold):
            split.test.append(example)
          else:
            split.train.append(example)
        for fileName in negTrainFileNames:
          example = self.Example()
          example.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
          example.klass = 'neg'
          example.fileName = fileName
          if fileName[2] == str(fold):
            split.test.append(example)
          else:
            split.train.append(example)
        splits.append(split)
    elif len(args) == 2:
      split = self.TrainSplit()
      testDir = args[1]
      print '[INFO]\tTraining on data set:\t%s testing on data set:\t%s' % (trainDir, testDir)
      posTrainFileNames = os.listdir('%s/pos/' % trainDir)
      negTrainFileNames = os.listdir('%s/neg/' % trainDir)
      for fileName in posTrainFileNames:
        example = self.Example()
        example.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
        example.klass = 'pos'
        example.fileName = fileName
        split.train.append(example)
      for fileName in negTrainFileNames:
        example = self.Example()
        example.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
        example.klass = 'neg'
        example.fileName = fileName
        split.train.append(example)

      posTestFileNames = os.listdir('%s/pos/' % testDir)
      negTestFileNames = os.listdir('%s/neg/' % testDir)
      for fileName in posTestFileNames:
        example = self.Example()
        example.words = self.readFile('%s/pos/%s' % (testDir, fileName))
        example.klass = 'pos'
        split.test.append(example)
      for fileName in negTestFileNames:
        example = self.Example()
        example.words = self.readFile('%s/neg/%s' % (testDir, fileName))
        example.klass = 'neg'
        split.test.append(example)
      splits.append(split)
    return splits

def main():
  nb = NaiveBayes()

  # default parameters: no stop word filtering, and
  # training/testing on ../data/imdb1
  if len(sys.argv) < 2:
      options = [('','')]
      args = ['../data/imdb1/']
  else:
      (options, args) = getopt.getopt(sys.argv[1:], 'f')
  if ('-f','') in options:
    nb.FILTER_STOP_WORDS = True

  splits = nb.buildSplits(args)
  avgAccuracy = 0.0
  fold = 0
  failed = []
  for split in splits:
    classifier = NaiveBayes()
    accuracy = 0.0
    for example in split.train:
      words = example.words
      if nb.FILTER_STOP_WORDS:
        words = classifier.filterStopWords(words)
      classifier.addExample(example.klass, words)

    for example in split.test:
      words = example.words
      if nb.FILTER_STOP_WORDS:
        words =  classifier.filterStopWords(words)
      guess = classifier.classify(words)
      if example.klass == guess:
        accuracy += 1.0
      else:
        failed.append(example)

    accuracy = accuracy / len(split.test)
    avgAccuracy += accuracy
    print '[INFO]\tFold %d Accuracy: %f' % (fold, accuracy)
    fold += 1
    #for e in failed:
    #    print(e.klass, e.fileName)
    #    copyfile(args[0] + '/' + e.klass + '/' + e.fileName, '../data/failed/' + e.klass + '/' + e.fileName)
  avgAccuracy = avgAccuracy / fold
  print '[INFO]\tAccuracy: %f' % avgAccuracy

if __name__ == "__main__":
    main()
