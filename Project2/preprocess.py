"""
Gabriella Uwadiegwu
CS 381 NLP
Prof. Rozovskaya
"""

class PreProcess:

    inputData = []
    classes = []
    dict_likelihood = {}
    docs = {}

    def getNumberOfDocs (self, textFile):
        """

        :aim: count how many documents - lines in text file
        :param textFile:
        :return:
        """
        count = 0
        with open(textFile, 'r') as read_input:
            for line in read_input:
                count += 1
        read_input.close()
        return count

    def processFile (self, inputText):
        """

        :aim: list of lists that are lines from file
        :param inputText: test file
        :return: List of Lists i.e [[]]
        """
        out_list = []
        read_input = open(inputText, 'r')
        for line in read_input:
            temp = line.strip().split()
            out_list.append(temp)
        read_input.close()
        return out_list


    def createVocab (self, inList):
        """

        :aim: prepare vocabulary - list of unique words
        :param inList: []
        :return: None
        """
        vocab = []
        new_list = []
        for line in inList:
            for words in line:
                if words != line[len(line)-1]:
                    new_list.append(words)
        for w in new_list:
            if w in vocab:
                continue
            else:
                vocab.append(w)
        return vocab

    def getClasses (self, inList):
        """

        :aim: Get list of classes
        :param inList: []
        :return: List of classes
        """
        # list of classes
        out_list = []
        for line in inList:
            if line[len(line)-1] in out_list:
                continue
            else:
                out_list.append(line[len(line)-1])
        return out_list

    def numberOfDocsGivenClass(self, cl, inList):
        """

        :aim: get number of documents associated with a given class
        :param cl: class name
        :param inList: []
        :return: Count (int)
        """
        count = 0
        for line in inList:
            if line[len(line)-1] != cl:
                continue
            else:
                count += 1
        return count


