## Spellchecker / Language models (Ex. 2)

* In Kneser-Ney crucial was to [use](https://github.com/mrzasa/classic-nlp-course/blob/master/HW02-spellchecker/python/CustomLanguageModel.py#L98) `discount/V * discount/V` probablility for unknown words
* In general: the most important and difficult part seems to be what to do with unknown or underrepresented words/n-grams. There are multiple methods to deal with it, from simple ones (Laplace, add-k) to very sophisticated (interpolation, Kneser-Ney). 

### References:
* [Jurafsky&Martin chapter](https://web.stanford.edu/~jurafsky/slp3/3.pdf)
* Kneser-Ney smoothing
  * https://github.com/smilli/kneser-ney
  * http://idiom.ucsd.edu/~rlevy/lign256/winter2008/kneser_ney_mini_example.pdf
  * https://stats.stackexchange.com/questions/114863/in-kneser-ney-smoothing-how-are-unseen-words-handled/291504
  * https://stats.stackexchange.com/questions/297115/zero-counts-in-kneser-ney-smoothing
  * http://smithamilli.com/blog/kneser-ney/


## Named Entity Recognition (ex. 4)

* Assignment seemed to be easy (just preparing features, ML method provided by the profs), but it was really difficult and time consuming. Two reasons - test run takes about 5 mins and features need to be added a bit blindly.
* Would be nice to see how feature scores impact the final result. I tried to dig into java ML code, but failed.
* Plan for next assignment with feature preparations, a script that:
  * takes descripton of changes
  * runs test
  * records metrics result to a log file along with the description
  * commits code
* Notable features used:
  * trigrams (character-based) - bigrams were used but rejected in last steps
  * prefixes and suffixes of word
  * checking if word includes strange clusters of characters (suggesting that it's not an English word)
  * dictionary featues:
    * is previous/current word a preposition related to persons?
    * is previous/current word a stop word
    * is current word on a list of popular names
    * is previous/next word one of specific verbs (mostly related to speaking)
  * in all cases listed above, lists were quite arbitrary - if some words increased the score, they were kept, if not - they were removed
