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
