import nltk

class Analyzer():
    """Implements sentiment analysis."""

    def __init__(self, positives="positive-words.txt", negatives="negative-words.txt"):
        """Initialize Analyzer."""
        # create empty lists to be loaded
        self.poslist = []
        self.neglist = []

        # open positive and negative words files
        posfile = open(positives)
        negfile = open(negatives)

        # fill poslist with positive words from posfile
        for line in posfile:
            if not line.startswith(";"):
                self.poslist.append(line.strip())

        # fill neglist with negative words from negfile
        for line in negfile:
            if not line.startswith(";"):
                self.neglist.append(line.strip())

        # close the opened files
        posfile.close()
        negfile.close()

    def analyze(self, text):
        """Analyze text for sentiment, returning its score."""
        score = 0

        # tokenize the text into a list of lowercase words
        tokenizer = nltk.tokenize.TweetTokenizer()
        tokens = tokenizer.tokenize(str.lower(text))

        # check if each word is in one the list and iterate score accordingly
        for token in tokens:
            if token in self.poslist:
                score += 1
            elif token in self.neglist:
                score -= 1
        return score
