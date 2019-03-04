"""
Gabriella Uwadiegwu
NLP Project 1
Prof. Rozovskaya
03/03/2019
"""

import math

class Modelling():

    unigram = {}
    bigram = {}

    def __init__(self, *args):
        """

        :param args: list of files
        """
        for i in args:
            self.pad(i, "new-"+i)

    def pad(self, old, new):

        """

        :param old: old file
        :param new: new file
        :return: None
        :description: pad data set lines with <s> and </s>
        """
        with open(old, 'r') as f:
            with open(new, 'w') as w:
                for line in f.readlines():
                    temp = "<s> " + line.replace('\n', ' </s>\n')
                    w.write(temp.lower())

    def pre_process(self):
        """

        :return: None
        :description: pre-process data sets
        """
        # A dictionary mapping words to their number of occurrences in brown train
        brown_train = open('new-brown-train.txt', 'r')
        count = {}
        for line in brown_train:
            for word in line.split():
                if word in count:
                    count[word] += 1
                else:
                    count[word] = 1
        brown_train.close()

        # pre-process <unk> token
        old = open('new-brown-train.txt', 'r')
        new = open('unknown-brown-train.txt', 'w')
        for line in old:
            for word in line.split():
                if count[word] == 1:
                    new.write("<unk>" + " ")
                elif word == '</s>':
                    new.write(word)
                else:
                    new.write(word + " ")
            new.write("\n")
        old.close()
        new.close()

        # get unigram and bigram in dictionary
        unk_file = open('unknown-brown-train.txt', 'r')
        previous = ""
        for line in unk_file:
            for word in line.split():

                if word in self.unigram:
                    self.unigram[word] += 1
                else:
                    self.unigram[word] = 1

                if word == '<s>':
                    previous = word
                elif previous + " " + word not in self.bigram:
                    self.bigram[previous + " " + word] = 1
                    previous = word
                else:
                    self.bigram[previous + " " + word] += 1
                    previous = word
        unk_file.close()

        # store tokens in corpus
        self.tokens = sum(model.unigram.values())

    def untrained_unigram_without_unk(self, fileName, unigram):
        """

        :param fileName: Name of test corpora file
        :param unigram: unigram dictionary before unk
        :return: None
        :description: percentage of word tokens and word types in each of the test corpora did not occur in training
        """
        file = open(fileName, 'r')
        tokens = 0
        token_not_in_training = 0
        for line in file:
            for word in line.split():
                tokens += 1
                if word not in unigram:
                    token_not_in_training += 1
        print("\t\t" + file.name)
        print("\t\tPercentage =", (token_not_in_training / tokens))
        print()
        file.close()

    def untrained_bigram_with_unk(self, fileName, unigram, bigram):
        """

        :param fileName: Name of test corpora file
        :param unigram: unigram dictionary
        :param bigram:  bigram dictionary
        :return: None
        :description: percentage of bigrams in each test corpora that did not occur in training
        """

        file = open(fileName, 'r')
        bigrams = 0
        bigrams_not_in_training = 0

        for line in file:
            previous = ""
            for word in line.split():
                if word not in unigram:
                    word = "<unk>"

                if word == '<s>':
                    previous = word
                elif previous + " " + word not in bigram:
                    bigrams_not_in_training += 1
                    bigrams += 1
                    previous = word
                else:
                    bigrams += 1
                    previous = word

        print("\t\t" + file.name)
        print("\t\tPercentage =", (bigrams_not_in_training / bigrams))
        print()
        file.close()

    def unigram_probability(self, sentence, unigram, tokens):
        """

        :param sentence: self explanatory
        :param unigram: unigram dictionary
        :param tokens: token count
        :return: None
        :description: Computes unigram probability and call unigram_perplexity function to compute perplexity
        """

        print(sentence)
        print()
        words = len(sentence.split()) # sentence word count
        log_probability = 0
        for word in sentence.lower().split():
            if word not in unigram:
                word = "<unk>"
            if word == '<s>':
                pass
            else:
                log_probability += math.log2(unigram[word] / tokens)  # sum all tokens and computes its log

        print("\t\tUnigram log probability =", log_probability)

        # call to compute perplexity
        self.unigram_perplexity(words, log_probability)

    def unigram_perplexity(self, words, unigram_probability):
        """

        :param words: sentence word count
        :param unigram_probability: self explanatory
        :return: None
        """

        temp = (1 / words) * unigram_probability
        print("\t\tUnigram perplexity =", 2 ** -temp)  # perplexity formula

    def bigram_probability(self, sentence, unigram, bigram):
        """

        :param sentence: self explanatory
        :param unigram: unigram dictionary
        :param bigram: bigram dictionary
        :return: None
        :description: Computes bigram probability and call bigram_perplexity function to compute perplexity
        """
        probability = 1
        previous = ""
        words = len(sentence.split())  # sentence word count
        for word in sentence.lower().split():
            if word not in unigram:
                word = "<unk>"

            if word == '<s>':
                previous = word
            elif previous + " " + word not in bigram:
                probability *= (0 / unigram[previous])
                previous = word
            else:
                probability *= (bigram[previous + " " + word] / unigram[previous])
                previous = word
        print()

        # bigram log probability [(p(A) * p(B))/p(B)]
        if probability == 0:
            print("\t\tBigram log probability =", str(probability))
        else:
            print("\t\tBigram log probability =", math.log2(probability))

        # call to compute perplexity
        self.bigram_perplexity(words, probability)

    def bigram_perplexity(self, words, bigram_probability, toogle=False, total=False):
        """

        :param words: sentence word count
        :param bigram_probability: self explanatory
        :param toogle: indicator for bigram smooth or bigram
        :param total: indicator for total bigram in Question 7
        :return: None
        :description: it used as utility for both bigram and bigram smoothed perplexity computation
        """

        if bigram_probability != 0 and not toogle:
            temp = (1 / words) * math.log2(bigram_probability)
            print("\t\tBigram perplexity =", 2 ** -temp)
        elif toogle or total:
            temp = (1 / words) * bigram_probability
            if total:
                print("\t\tBigram perplexity =", 2 ** -temp)
            else:
                print("\t\tBigram smoothing perplexity =", 2 ** -temp)
        else:
            print("\t\tBigram perplexity = cannot compute as probability is 0")

    def bigram_probability_and_smoothing(self, sentence, unigram, bigram):
        """

        :param sentence:
        :param unigram:
        :param bigram:
        :return:
        :description: Computes bigram smoothing probability and call bigram_perplexity function to compute perplexity
        """
        words = len(sentence.split())
        previous = ""
        probability = 0
        for word in sentence.lower().split():
            if word not in unigram:
                word = "<unk>"
            if word == '<s>':
                previous = word
            elif previous + " " + word not in bigram:
                probability += math.log2(1 / (unigram[previous] + len(unigram)))
                previous = word
            else:
                probability += math.log2((bigram[previous + " " + word] + 1) / (unigram[previous] + len(unigram)))
                previous = word
        print()
        print("\t\tBigram smoothing log probability =", probability)

        self.bigram_perplexity(words, probability, True)

    def total_unigram_corpora_perplexity(self, fileName, unigram, tokens):
        """

        :param fileName: self explanatory
        :param unigram: unigram dictionay
        :param tokens: token count
        :return:
        :description:
        """

        words = 0
        file = open(fileName, 'r')

        for line in file:
            words += len(line.split())
        file.close()

        file = open(fileName, 'r')
        total_unigram_log_probability = 0
        for line in file:
            log_probability = 0
            for word in line.split():
                if word not in unigram:
                    word = "<unk>"
                if word == '<s>':
                    pass
                else:
                    log_probability += math.log2(unigram[word] / tokens)

            total_unigram_log_probability += log_probability

        m = (1 / words) * total_unigram_log_probability
        print(file.name)
        print("\t\tUnigram perplexity =", pow(2, -m))

        file.close()

    def total_bigram_corpora_perplexity(self, fileName, unigram, bigram):
        """

        :param fileName: self explanatory
        :param unigram: unigram dictionary
        :param bigram: bigram dictionary
        :return:
        :description: perplexity of total text corpora for bigram and bigram smoothed
        """

        file = open(fileName, 'r')
        words = 0
        for line in file:
            words += len(line.split())
        file.close()

        total_bigram_log_probability = 0
        total_smoothed_bigram_log_probability = 0

        file = open(fileName, 'r')
        for line in file:
            sentence_probability = 1
            previous = ""
            for word in line.split():
                if word not in unigram:
                    word = "<unk>"
                if word == '<s>':
                    previous = word
                elif previous + " " + word not in bigram:
                    sentence_probability *= (0 / unigram[previous])
                    previous = word
                else:
                    sentence_probability *= (bigram[previous + " " + word] / unigram[previous])
                    previous = word

            if sentence_probability == 0:
                words -= len(line.split())
            else:
                total_bigram_log_probability += math.log2(sentence_probability)

            log_probability = 0
            for word in line.split():
                if word not in unigram:
                    word = "<unk>"
                if word == '<s>':
                    previous = word
                elif previous + " " + word not in bigram:
                    log_probability += math.log2(1 / (unigram[previous] + len(unigram)))
                    previous = word
                else:
                    log_probability += math.log2((bigram[previous + " " + word] + 1) / (unigram[previous] + len(unigram)))
                    previous = word
            total_smoothed_bigram_log_probability += log_probability

        # call for total bigram perplexity
        self.bigram_perplexity(words, total_bigram_log_probability, toogle=True, total=True)

        # call for total bigram smoothed perplexity
        self.bigram_perplexity(words, total_smoothed_bigram_log_probability, toogle=True, total=True)

        file.close()

if __name__ == "__main__":

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    PRE-PROCESSING
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    # Initialize by padding data sets
    model = Modelling('brown-train.txt', 'brown-test.txt', 'learner-test.txt')
    model.pre_process()
    unigram_count = len(model.unigram)

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    SOLUTIONS
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    # Question 1
    print()
    print("Question 1:")
    print("\t\tUnique words in training corpus = ", unigram_count)

    print()
    print()

    # Question 2
    print("Question 2:")
    print("\t\tTotal token in training corpus = ", model.tokens)

    print()
    print()

    # Question 3
    print("Question 3:")
    model.untrained_unigram_without_unk('new-brown-test.txt', model.unigram)
    model.untrained_unigram_without_unk('new-learner-test.txt', model.unigram)

    # Question 4
    print("Question 4:")
    model.untrained_bigram_with_unk('new-brown-test.txt', model.unigram, model.bigram)
    model.untrained_bigram_with_unk('new-learner-test.txt', model.unigram, model.bigram)

    # Question 5 & 6
    print("Question 5 & 6:")
    one = "<s> He was laughed off the screen . </s>"
    two = "<s> There was no compulsion behind them . </s>"
    three = "<s> I look forward to hearing your reply . </s>"

    print()
    model.unigram_probability(one, model.unigram, model.tokens)
    model.bigram_probability(one, model.unigram, model.bigram)
    model.bigram_probability_and_smoothing(one, model.unigram, model.bigram)

    print()
    model.unigram_probability(two, model.unigram, model.tokens)
    model.bigram_probability(two, model.unigram, model.bigram)
    model.bigram_probability_and_smoothing(two, model.unigram, model.bigram)

    print()
    model.unigram_probability(three, model.unigram, model.tokens)
    model.bigram_probability(three, model.unigram, model.bigram)
    model.bigram_probability_and_smoothing(three, model.unigram, model.bigram)
    print()

    # Question 7
    print("Question 7:")

    print()
    model.total_unigram_corpora_perplexity('new-brown-test.txt', model.unigram, model.tokens)
    model.total_bigram_corpora_perplexity('new-brown-test.txt', model.unigram, model.bigram)

    print()
    model.total_unigram_corpora_perplexity('new-learner-test.txt', model.unigram, model.tokens)
    model.total_bigram_corpora_perplexity('new-learner-test.txt', model.unigram, model.bigram)
    print()