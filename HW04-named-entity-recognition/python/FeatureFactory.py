import json, sys, re
import base64
from Datum import Datum

class FeatureFactory:
    """
    Add any necessary initialization steps for your features here
    Using this constructor is optional. Depending on your
    features, you may not need to intialize anything.
    """
    def __init__(self):
        self.insideSingleQuote = False
        self.insideDoubleQuote = False


    """
    Words is a list of the words in the entire corpus, previousLabel is the label
    for position-1 (or O if it's the start of a new sentence), and position
    is the word you are adding features for. PreviousLabel must be the
    only label that is visible to this method.
    """

    def computeFeatures(self, words, previousLabel, position):
        features = []
        currentWord = words[position]
        if position > 0:
            previousWord = words[position-1]
        else:
            previousWord = ' '

        if position > 1:
            previous2Word = words[position-2]
        else:
            previous2Word = ' '

        if position < (len(words) - 1):
            nextWord = words[position+1]
        else:
            nextWord = ' '

        if position < (len(words) - 2):
            next2Word = words[position+2]
        else:
            next2Word = ' '

        """ Baseline Features """
        features.append("word=" + currentWord)
        features.append("prevLabel=" + previousLabel)
        #features.append("word=" + currentWord + ", prevLabel=" + previousLabel)

        """
        Warning: If you encounter "line search failure" error when
        running the program, considering putting the baseline features
	back. It occurs when the features are too sparse. Once you have
        added enough features, take out the features that you don't need.
	"""

        if currentWord == "\'":
            self.insideSingleQuote = not self.insideSingleQuote
        elif currentWord == "\'":
            self.insideDoubleQuote = not self.insideDoubleQuote

        #if currentWord[0].isupper():
        #    features.append("case=Title")
        #    if previousWord == '.':
        #        features.append("case=Title" + ", beginningOfSentence=True")
        #    if self.isShortWord(currentWord):
        #        features.append("shortCapitalized=True")

        #if self.shortCapitalizedCluster(previousWord, currentWord, nextWord):
        #    features.append("shortCapitalizedCluster=True")


        #if self.insideDoubleQuote or self.insideSingleQuote:
        #    features.append("insideQuote=True")

        # features.append("2previous=" + previous2Word + " " + previousWord)
        # features.append("2next=" + nextWord + " " + next2Word)

        #features.append("previous=" +  previousWord)
        #features.append("next=" + nextWord)

        if currentWord[0].isupper():
            features.append("case=Title")

        #if previousWord[0].isupper():
        #    features.append("previousCase=Title")
        #if nextWord[0].isupper():
        #    features.append("nextCase=Title")

        if currentWord.lower()[0] == 'x':
            features.append("startsWithX=True")

        shape = self.shape(currentWord)
        features.append("shape=" + shape)
        features.append("simpleShape=" + self.simplifyShape(shape))
        # features.append("simpleShapePrev=" + self.simplifyShape(self.shape(previousWord)))
        # features.append("simpleShapeNext=" + self.simplifyShape(self.shape(nextWord)))
        # features.append("shapePrevious=" + self.shape(previousWord))
        # features.append("shapeNext=" + self.shape(nextWord))
        #features.append("prevLenght= %d" % len(previousWord))
        features.append("lenght=%d" % len(currentWord))
        #features.append("nextLenght= %d" % len(nextWord))
        #features.append("last6=" + currentWord[-6:])
        features.append("last5=" + currentWord[-5:])
        features.append("last4=" + currentWord[-4:])
        features.append("last3=" + currentWord[-3:])
        features.append("last2=" + currentWord[-2:])
        #features.append("last1=" + currentWord[-1:])

        #features.append("first6=" + currentWord[:6])
        features.append("first5=" + currentWord[:5])
        features.append("first4=" + currentWord[:4])
        features.append("first3=" + currentWord[:3])
        features.append("first2=" + currentWord[:2])
        #features.append("first1=" + currentWord[:1])

        features.append("stopWord=" + str(self.isStopWord(currentWord)))
        features.append("prevStopWord=" + str(self.isStopWord(previousWord)))
        #features.append("nextStopWord=" + str(self.isStopWord(nextWord)))
        features.append("personPrep=" + str(self.isPersonPrep(currentWord)))
        features.append("prevPersonPrep=" + str(self.isPersonPrep(previousWord)))
        #features.append("nextPersonPrep=" + str(self.isPersonPrep(nextWord)))
        #features.append("prevImprobable=" + str(self.isImprobablePrevious(previousWord)))

        #if self.upperCaseInside(currentWord):
        #    features.append("upperCaseInside=True")

        #features.append('nonLetters=' + self.nonLetters(currentWord))

        #for c in self.uppers(currentWord):
        #    features.append("upper_" + c + "=True")


        #if re.match(r'\d\.$', previousWord):
        #    features.append("numberedList=True")

        if currentWord[0].isupper() and not previousWord == '.':
            if self.isSaying(previousWord) or self.isSaying(nextWord):
                features.append("capitalizedSaying=True")
            if self.isSaying(previousWord):
                features.append("capitalizedPrevSaying=True")
            if self.isSaying(nextWord):
                features.append("capitalizedNextSaying=True")

            if nextWord in ['accuse', 'accused', 'quote', 'quoted', 'agree', 'agreed' ]:
                features.append("capitalizedNextSaying=True")

            if re.match(r'sa(id|ys?|ying)$', nextWord):
                features.append("capitalizedNextSaid=True")

            if self.isVerb(nextWord): # or nextWord in ['watch', 'watched', 'look', 'looked']:
                features.append("capitalizedNextVerb=True")


            #if nextWord in ['said', '\'s', 'b']:
            #    features.append('nextFrequentPERSON=True')

            #if nextWord == 'b':
            #    features.append('nextB=True')

            #if previousWord == 'b':
            #    features.append('prevB=True')

            #if nextWord == '.':
            #    features.append('nextDot=True')

            #if self.isInitial(previousWord):
            #    features.append("capitalizedPreviousInitial=True" )
            #features.append("capitalizedPrevPersonPrep=" + str(self.isPersonPrep(previousWord)))

            #if 'uu' in currentWord:
            #    features.append("uu=True")

            #if 'ao' in currentWord:
            #    features.append("ao=True")


            #if len(currentWord) == 3 or len(currentWord) == 4:
            #    if self.clusteredVowelRatio(currentWord) > 0.5:
            #        features.append("shortWithManyVowels=True")



            #if self.isShortCapitalized(currentWord):
            #    features.append("shortCapitalized=True")

            #if previousWord in ['Minister']:
            #    features.append("jobTitleBefore=True")

            #if re.match(r'.*er$', previousWord):
            #    features.append("previousEndsWithEr=True")


            #if previousWord == ',':#, or nextWord == ',':
            #    features.append('capitalNearComma=True')

            #features.append("capitalizedPrevPersonPrep=" + str(self.isPersonPrep(previousWord)))


            #if self.isBeing(previousWord) or self.isBeing(nextWord):
            #    features.append("capitalizedBeing=True")
            #if self.isBeing(previousWord):
            #    features.append("capitalizedPrevBeing=True")
            #if self.isBeing(nextWord):
            #    features.append("capitalizedNextBeing=True")


            #if self.isSaxon(nextWord):
            #    features.append("capitalizedNextSaxon=True")


        vowelClusters = self.vowelClusters(currentWord, 2)
        for cluster in vowelClusters:
            features.append("vowelCluster_" + cluster  + '=True')

        #consonantClusters = self.consonantClusters(currentWord, 3)
        #for cluster in consonantClusters:
        #    features.append("consonantCluster_" + cluster  + '=True')

        #if self.isShortCapitalized(currentWord):
        #    features.append("shortCapitalized=True")
        #    features.append("shortCapitalizedVowelRatio=%f" % self.vowelRatio(currentWord))


        #for quadrigram in self.ngrams(currentWord, 4):
        #    features.append("quadrigram_" + quadrigram  + '=True')

        for trigram in self.ngrams(currentWord, 3):
            features.append("trigram_" + trigram  + '=True')

        #for bigram in self.ngrams(currentWord, 2):
        #    features.append("bigram_" + bigram  + '=True')

        halves = self.halves(currentWord)
        features.append("firstHalf=" + halves[0])
        #features.append("secondHalf=" + halves[1])

        #previousHalves = self.halves(previousWord)
        #features.append("prevFirstHalf=" + previousHalves[0])
        #features.append("prevSecondHalf=" + previousHalves[1])
        #features.append("prevEnding=" + previousWord[-3:])

        if "O'" in currentWord:
            features.append("OApostrophe=True")

        #if self.isNoble(currentWord) and (nextWord[0].isupper() or previousWord[0].isupper()):
        #    features.append("noble=True")

        if '-' in currentWord and currentWord != '-':
            features.append("currentHyphnated=True")

                # (not re.findall(r'-{2,}', currentWord)) and \
                # (len(re.findall(r'-', currentWord)) < 3):
                # and \
            #if  False and (not re.findall(r'[A-Z]{2,}', currentWord)) and \
            #    (not re.findall(r'(ed|born|style|bound|ion|held|made|ing)$', currentWord)) and \
            #    (not re.findall(r'Israeli|American|German|France|Croat|Serb|Russian|Yemen', currentWord)) and \
            #    (not re.findall(r'[\d.]', currentWord)):
            #    features.append('potentialPersonHyphen=True')

        if nextWord == '(':
            features.append('nextBracket=True')

        if self.isDictionaryName(currentWord):
            features.append('dictName=True')
        if self.isNotAPerson(currentWord):
            features.append('notAPerson=True')


        #if nextWord in ['(', ',', 'said', '\'s', '.', '']:
        #    features.append('nextFrequentPERSON=True')
        #if nextWord in ['.', ',', 'the', 'of', 'in', 'to', 'a', ')', 'and', '"', 'on']:
        #    features.append('nextFrequentO=True')

        #if previousWord in ['(', '.', ',']: # , ')','-', '--', '"']:
        #    features.append('prevSpecial=True')

        #if nextWord == '.':
        #    features.append('nextDot=True')

#        if nextWord == ')':
#            features.append('nextClosingBracket=True')

#        if previousWord == '(':
#            features.append('prevBracket=True')

#        if re.match(r'\d+', nextWord):
#            features.append('nextStartsWithDigits=True')

#        if re.match(r'\d+', previousWord):
#            features.append('prevStartsWithDigits=True')

        #if nextWord == ',':
        #    features.append('nextComma=True')

        #if self.isRomanNumber(currentWord) and previousLabel == 'PERSON':
        #    features.append("romanNumber=True")

        #if '.' in currentWord and currentWord != '.':
        #    features.append("currentDotted=True")

        #if self.isNoble(previousWord):
        #    features.append("prevNoble=True")
        #if self.isNoble(nextWord):
        #    features.append("nextNoble=True")
        #if self.isNoble(currentWord) or self.isNoble(previousWord) or self.isNoble(nextWord):
        #    features.append("nobleCluster=True")

        letterStats = self.letterStats(currentWord)
        for letter, count in letterStats.items():
            features.append('lettersCount_' + letter + '=%d' % count)

        #features.append('mostFrequentLetter=' + sorted(letterStats, key=letterStats.get)[0])

        #if len(vowelClusters) > 0:
        #    features.append("maxLenVowelCluster=%d"%max(map(lambda x: len(x), vowelClusters)))
        #    features.append("countVowelCluster=%d"%len(vowelClusters))

        #features.append("soundShape=" + self.soundShape(currentWord))

        #if self.isInitial(nextWord):
        #    features.append("nextInitial=True" )

        if self.isInitial(currentWord):
            features.append("currentInitial=True" )

        if self.isInitial(previousWord):
            features.append("previousInitial=True" )

        #if self.endsWithS(nextWord):
        #    features.append("nextPotentialVerb=True" )

        if self.strangeClusters(currentWord):
            features.append("StrangeClusters=True" )

        #if self.anyPersonWordsInWindow(self.window(words, position, 1)):
        #    features.append("PersonWordInWindow1=True" )

        #if self.anyPersonWordsInWindow(self.window(words, position, 2)):
        #    features.append("PersonWordInWindow2=True" )

        #if self.notAlpha(previousWord):
        #    features.append("prevNotAlpha=True")

        #if self.numberedList(words, position):
        #    features.append("numberedList=True")

        #if self.pointsNext(words, position):
        #    features.append("pointsNext=True")


        return features

    def isSaying(self, word):
        if  re.match(r'sa(id|ys?|ying)$', word) or \
            re.match(r't(ells?|old|elling)$', word) or \
            re.match(r'express(ed)?$', word) or \
            re.match(r'agreed?$', word) or \
            re.match(r'proposed?$', word):
            return True

    def isHaving(self, word):
        if re.match(r'ha(d|s)$', word):
            return True

    def isLooking(self, word):
        if re.match(r'look(s|ed)$', word):
            return True

    def isBeing(self, word):
        if re.match(r'w(ere|as|ill)$', word): # or re.match(r'is$', word):
            return True

    def isDoing(self, word):
        if re.match(r'd(o|oes|id)$', word):
            return True

    def isModal(self, word):
        if re.match(r'should$', word):
            return True

    def isVerb(self, word):
        #return self.isHaving(word) or self.isBeing(word) or self.isDoing(word) or self.isLooking(word) or self.isSaying(word)
        return self.isDoing(word) or self.isHaving(word) or self.isBeing(word)#  or self.isModal(word)
        #return self.isLooking(word)

    def isSaxon(self, word):
        return word == "'s"

    def endsWithS(self, word):
        return word[-1] == 's'

    def isShortCapitalized(self, word):
        return self.isShortWord(word) and word[0].isupper()

    def shortCapitalizedCluster(self, previousWord, currentWord, nextWord):
        return (self.isShortCapitalized(currentWord) and (self.isShortCapitalized(nextWord) or self.isShortCapitalized(previousWord)))

    def isShortWord(self, word):
        return len(word) < 4 and len(word) > 1

    def isPersonPrep(self, word):
        #words = ['for', 'with', 'of', 'to', 'by', 'between', 'over', 'under', 'on', 'from', 'about']
        words = ['for', 'with', 'of', 'to', 'by', 'between', 'over', 'on', 'from', 'about']
                 #, 'after', 'like', 'without']
        if word in words:
            return True
        else:
            return False

    def isStopWord(self, word):
        stopWords = ['a', 'an', 'the', 'in', 'up', 'in', 'one', 'at', 'is',# 'be'
                     # 'had', 'has', 'was', 'am', 'are', 'have', 'is',
                     'or', 'two', 'he', 'she', 'it', 'we', 'you',
                     'they', 'I', 'me', 'our', 'your', 'them', 'their',
                     'who', 'whom', 'which', 'ever', 'how', '\'s', 'and', 'or', 'nor', 'not', 'neither',
                     'either', 'though', 'however', 'still',
                     'becasue', 'cause', 'therefore', 'there', 'those', 'this', 'these',
                     'but', 'so', 'yet',
                     'although', 'despite', 'though', 'whereas', 'while',
                     'across', 'away', 'along'
                     #'nonetheless', 'nevertheless', 'otherwise', 'likewise'
                     #'once', 'twice', 'three'
                     #'due', 'order', 'spite'
                     #'since',  'till', 'until'
                     #'even', 'hence', 'also'
                     #'however', 'thus', 'anyway',
                     #'where', 'when', 'why', 'what'
                     ]
        if word.lower() in stopWords:
            return True
        else:
            return False

    def isImprobablePrevious(self, word):
        improbableWords = ['a', 'an', 'the',
                     'two', 'he', 'she', 'it', 'we', 'you'
                     'they', 'i', 'me', 'our', 'your', 'them', 'their',
                     'who', 'whom', 'how', '\'s',
                     ]
        if word.lower() in improbableWords:
            return True
        else:
            return False

    def isDictionaryName(self, word):
        names = [
            'Rachel', 'Paul', 'Pauline', 'Paulo', 'Mark', 'Jacob', 'Jack', 'James', 'Peter', 'John', 'Mike', 'Tom',
            'Thomas', 'Tim', 'Jonathan', 'Adam', 'Ross', 'Severine'
            'Severine', 'Xiao', 'Chen', 'Fidel', 'Suu',
            'Mao', 'Vera'
            'Jordan',
        ]
        return word in names

    def isNotAPerson(self, word):
        words = [
            'Nato', 'NATO', 'Mr', 'Zycie', 'Warszawy', 'Emperor', 'Jr', 'Interfax', 'Korea',
            'Israeli','American','German','France','Croat','Serb','Russian','Yemen', 'Ruch', 'Poland',
            'Bros'
        ]
        return word in words

    def upperCaseInside(self, word):
        return bool(filter((lambda c: c.isupper()), word[1:]))

    def uppers(self, word):
        return re.sub(r'[^A-Z]', '', word)

    def nonLetters(self, word):
        return re.sub(r'[A-Za-z]', '', word)

    def shape(self, word):
        s = re.sub(r'[a-z]', 'x', word)
        s = re.sub(r'[A-Z]', 'X', s)
        return s

    def simplifyShape(self, shape):
        result = []
        for char in shape:
            if len(result) > 0 and result[-1] == char:
                next
            else:
                result.append(char)
        return ''.join(result)


    def isInitial(self, word):
        return re.match('[A-Z]\.$', word)

    def vowelClusters(self, word, size):
        return re.findall(r'[euioay]{%d,}'%size, word.lower())

    def consonantClusters(self, word, size):
        return re.findall(r'[bcdfghjklmnpqrstvxz]{%d,}'%size, word.lower())

    def ngrams(self, word, size):
        return [word.lower()[i:i+size] for i in range(0, len(word)-(size-1))]

    def halves(self, word):
        half = len(word)/2
        return[word[:half], word[half:]]

    def letterStats(self, word):
        stats = {}
        for ch in word.lower():
            if stats.get(ch):
                stats[ch] += 1
            else:
                stats[ch] = 1

        return stats

    def soundShape(self, word):
        s = word.lower()
        s = re.sub(r'[euioay]', 'a', s)
        s = re.sub(r'[bcdfghjklmnpqrstvxz]', 'b', s)
        return s

    def vowelCount(self, word):
        return len(self.vowelClusters(word, 1))

    def vowelRatio(self, word):
        return float(len(re.findall(r'[euioay]', word.lower())))/len(word)

    def clusteredVowelRatio(self, word):
        ratio = self.vowelRatio(word)
        if ratio < 0.5:
            return '0.5'
        else:
            return '1.00'


    def isNoble(self, word):
        return re.match(r'v[ao]n$', word.lower()) or re.match(r'der?$', word.lower())

    def isRomanNumber(self, word):
        #return re.match(r'[IVX]+$', word)
        numerals = ['III', 'VIII', 'IX']
        if word in numerals:
            return True
        else:
            return False

    def strangeClusters(self, word):
        strange = [
             #'rz', 'ao', 'ziz', 'uu', 'tin', 'shin', 'yukh', 'enk', 'yev', 'kac', 'uig'
             'rz', 'xi', 'ao', 'cz', 'dz', 'ziz', 'uu', 'yi', 'hai', 'ss', 'tin', 'shin', 'ily', 'yukh', 'enk', 'zvi', 'yevr', 'kac',
             'uig', 'kyi', 'marek'
#            'ida', 'olli', 'uin', 'rda', 'mao', 'ung'
#            'ango', 'ios', 'gham', 'ilv', 'eir', 'ily'
#            'zvi', 'nye', 'xia'
        ]
        for cluster in strange:
            if cluster in word.lower():
                return True
        return False

    def numberedList(self, words, position):
        if position - 2 > 0:
            context = "".join(words[position-2:position-1])
            return re.match(r'\d+-$', context)

    def pointsNext(self, words, position):
        if position + 3 < len(words):
            context = "".join(words[position+1:position+3])
            return re.match(r'\(\d+-\d+\)$', context)

    def window(self, words, position, r):
        return map(lambda w: w.lower(), words[max(position-r, 0):position+r])

    def anyPersonWordsInWindow(self, window):
        personWords = [
            'minister', 'president', 'friend', 'rival', 'soldier', 'statesman', 'husband', 'wife', 'footballer', 'captain',
            'chairman', 'king', 'queen', 'businessman', 'coach', 'prince'
        ]
        return bool(set(window) & set(personWords))

    def notAlpha(self, word):
        return not bool(re.findall(r'[a-z]', word.lower()))

    """ Do not modify this method """
    def readData(self, filename):
        data = []

        for line in open(filename, 'r'):
            line_split = line.split()
            # remove emtpy lines
            if len(line_split) < 2:
                continue
            word = line_split[0]
            label = line_split[1]

            datum = Datum(word, label)
            data.append(datum)

        return data

    """ Do not modify this method """
    def readTestData(self, ch_aux):
        data = []

        for line in ch_aux.splitlines():
            line_split = line.split()
            # remove emtpy lines
            if len(line_split) < 2:
                continue
            word = line_split[0]
            label = line_split[1]

            datum = Datum(word, label)
            data.append(datum)

        return data


    """ Do not modify this method """
    def setFeaturesTrain(self, data):
        newData = []
        words = []

        for datum in data:
            words.append(datum.word)

        ## This is so that the feature factory code doesn't
        ## accidentally use the true label info
        previousLabel = "O"
        for i in range(0, len(data)):
            datum = data[i]

            newDatum = Datum(datum.word, datum.label)
            newDatum.features = self.computeFeatures(words, previousLabel, i)
            newDatum.previousLabel = previousLabel
            newData.append(newDatum)

            previousLabel = datum.label

        return newData

    """
    Compute the features for all possible previous labels
    for Viterbi algorithm. Do not modify this method
    """
    def setFeaturesTest(self, data):
        newData = []
        words = []
        labels = []
        labelIndex = {}

        for datum in data:
            words.append(datum.word)
            if not labelIndex.has_key(datum.label):
                labelIndex[datum.label] = len(labels)
                labels.append(datum.label)

        ## This is so that the feature factory code doesn't
        ## accidentally use the true label info
        for i in range(0, len(data)):
            datum = data[i]

            if i == 0:
                previousLabel = "O"
                datum.features = self.computeFeatures(words, previousLabel, i)

                newDatum = Datum(datum.word, datum.label)
                newDatum.features = self.computeFeatures(words, previousLabel, i)
                newDatum.previousLabel = previousLabel
                newData.append(newDatum)
            else:
                for previousLabel in labels:
                    datum.features = self.computeFeatures(words, previousLabel, i)

                    newDatum = Datum(datum.word, datum.label)
                    newDatum.features = self.computeFeatures(words, previousLabel, i)
                    newDatum.previousLabel = previousLabel
                    newData.append(newDatum)

        return newData

    """
    write words, labels, and features into a json file
    Do not modify this method
    """
    def writeData(self, data, filename):
        outFile = open(filename + '.json', 'w')
        for i in range(0, len(data)):
            datum = data[i]
            jsonObj = {}
            jsonObj['_label'] = datum.label
            jsonObj['_word']= base64.b64encode(datum.word)
            jsonObj['_prevLabel'] = datum.previousLabel

            featureObj = {}
            features = datum.features
            for j in range(0, len(features)):
                feature = features[j]
                featureObj['_'+feature] = feature
            jsonObj['_features'] = featureObj

            outFile.write(json.dumps(jsonObj) + '\n')

        outFile.close()
