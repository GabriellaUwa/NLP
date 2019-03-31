"""
Naive Bayes classifier class
"""
from preprocess import PreProcess
import os

"""Part A"""
class NB():
    
    
    classification = {}
    number_of_docs = None
    vocab_unique = None
    classes = None

    number_of_docs = None
    inputData = None
    vocab_unique = None
    classes = None

    words = {}
    process = PreProcess()
    testing = {}

    train_file = None
    test_file = None


    def __init__(self, train=None, test=None, train_dir=None, test_dir=None):
        """

        :aim: Classify for either a file or given directory
        :param train: Train file if a file is given
        :param test: Test file is a file is given
        :param train_dir: Train directory if directory is given
        :param test_dir: Test directory if directory is given
        """

        if train is not None or test is not None:
            self.train_file = train
            self.test_file = test

            self.number_of_docs = self.process.getNumberOfDocs(train)
            self.inputData = self.process.processFile(train)
            self.vocab_unique = self.process.createVocab(self.inputData)
            self.classes = self.process.getClasses(self.inputData)

        else:

            for i in os.listdir(train_dir + "neg"):

                self.number_of_docs += self.process.getNumberOfDocs(train)
                self.inputData += self.process.processFile(train)
                self.vocab_unique += self.process.createVocab(self.inputData)
                self.classes += self.process.getClasses(self.inputData)

            for i in os.listdir(train_dir + "pos"):

                self.number_of_docs += self.process.getNumberOfDocs(train)
                self.inputData += self.process.processFile(train)
                self.vocab_unique += self.process.createVocab(self.inputData)
                self.classes += self.process.getClasses(self.inputData)

            """
            for i in os.listdir(test_dir + "neg"):
                
            for i in os.listdir(test_dir + "pos"):
                
            """

    def classify(self):
        """

        :aim: Classify training
        :return: None
        """
        for c in self.classes:
            temp_dict = {}
            for word in self.vocab_unique:
                temp_dict[word] = 0
            self.classification[c] = temp_dict

        # keys = classes, values = count of words in document given class
        for key in self.classification:
            for line in self.inputData:
                if line[len(line) - 1] != key:
                    continue
                else:
                    for word in line:
                        if word not in self.classification[key]:
                            continue
                        (self.classification[key])[word] += 1

    def count_words(self):
        """

        :aim: Count words per class
        :return: None
        """

        for cl in self.classes:
            count = 0
            for k in self.classification[cl]:
                count += self.classification[cl][k]
            self.words[cl] = count

    def classify_smoothed(self):
        """

        :aim: Add one smoothing to probability
        :return: None
        """
        self.dict_likelihood = self.classification.copy()

        for cl in self.classes:
            for k in self.dict_likelihood[cl]:
                self.dict_likelihood[cl][k] = (self.dict_likelihood[cl][k] + 1) / float(self.words[cl] +
                                                                                        len(self.vocab_unique))


    def test_probability(self):
        """

        :aim: Test data on training
        :return: None
        """

        # Number of documents, given a class
        for cl in self.classes:
            d = self.process.numberOfDocsGivenClass(cl, self.inputData)
            self.process.docs[cl] = d

        # prior probabilities
        self.priors = {}
        for cl in self.classes:
            if cl not in self.priors:
                self.priors[cl] = self.process.docs[cl] / float(self.number_of_docs)

        with open(self.test_file) as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        test_data = content

        # add classes as keys to testing dict, values = prior probabilities
        for cl in self.classes:
            if cl not in self.testing:
                self.testing[cl] = self.priors[cl]

        for cl in self.classes:
            for w in test_data:
                for key in self.dict_likelihood[cl]:
                    if key != w:
                        continue
                    elif key == w:
                        self.testing[cl] *= self.dict_likelihood[cl][w]

        # Compute the most likely class
        self.result = max(self.testing, key=self.testing.get)

    def output(self):
        """

        :aim: Write final classification output to file
        :return: None
        """
        string = \
        "Total number of documents/lines in input" + str(self.number_of_docs) + "\n" + \
        "Vocabulary of unique words: " + str(self.vocab_unique) + "\n"+ \
        "Classes:" + str(self.classes) + "\n"+ \
        "Count of words, given class: " + str(self.words) + "\n"+ \
        "Word likelihoods with add - 1 smoothing with respect to class: " + str(self.dict_likelihood) + "\n"+ \
        "Prior probabilities: ",  str(self.priors) + "\n" + \
        "Probabilities of test data: " + str(self.testing) + "\n" + \
        "The most likely class for the test document: " + self.result

        if self.train_file is not None:
            f = open("movies-small.txt", "w")
            f.write("\n".join(string))
            f.close()
        else:
            #for multiple directory implementation
            pass


"""Part B & C"""
def movie_small():
    """

    :aim: Small training set of movie review
    :return: None
    """

    nb = NB(train="movie-review-small.NB", test="document.NB")
    nb.classify()
    nb.count_words()
    nb.classify_smoothed()
    nb.test_probability()
    nb.output()

"""Part D"""
def movie_big():
    """

    :aim: Much latger training set of movie review
    :return: None
    """

    nb = NB(os.path.dirname(os.path.abspath(__file__)) + "/movie-review-HW2/aclImdb/train/",
            os.path.dirname(os.path.abspath(__file__)) + "/movie-review-HW2/aclImdb/test/")


if __name__ == "__main__":
    movie_small()
    #movie_big()

