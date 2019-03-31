def classify():

    """
    :Question: No. 1

    Assume that you have trained a Naïve Bayes classifier for the task of sentiment classification
    (please refer to Chapter 6, pp. 1-9 in the J&M book). The classifier uses only
    bag-of-word features. Assume the following parameters for each word being part of a
    positive or negative movie review, and the prior probabilities are 0.4 for the positive
    class and 0.6 for the negative class.

    :return: None
    """
    print()
    pos_list = dict()
    pos_list["I"] = 0.09
    pos_list["always"] = 0.07
    pos_list["like"] = 0.29
    pos_list["foreign"] = 0.04
    pos_list["films"] = 0.08

    neg_list = dict()
    neg_list["I"] = 0.16
    neg_list["always"] = 0.06
    neg_list["like"] = 0.06
    neg_list["foreign"] = 0.15
    neg_list["films"] = 0.11

    pos_class_prob = pos_list["I"] * pos_list["always"] * pos_list["like"] * pos_list["foreign"] * pos_list["films"]
    print("P(pos) * P(S|pos) = P(I|pos) * P(always|pos) * P(like|pos) * P(foreign|pos) * P(films|pos)")
    print("= " + str(pos_list["I"]) + " * " + str(pos_list["always"]) + " * " + str(pos_list["like"]) + " * " +
          str(pos_list["foreign"]) + " * " + str(pos_list["films"]))
    print("= " + str(pos_class_prob)+'\n')

    neg_class_prob = neg_list["I"] * neg_list["always"] * neg_list["like"] * neg_list["foreign"] * neg_list["films"]
    print("P(neg) * P(S|neg) = P(I|neg) * P(always|neg) * P(like|neg) * P(foreign|neg) * P(films|neg)")
    print("= " + str(neg_list["I"]) + " * " + str(neg_list["always"]) + " * " + str(neg_list["like"]) +
          " * " + str(neg_list["foreign"]) + " * " + str(neg_list["films"]))

    print("= " + str(neg_class_prob) + '\n')

    if neg_class_prob > pos_class_prob:
        print("Naive Bayes Classifier: Negative Class")
    else:
        print("Naive Bayes Classifier: Positive Class")

classify()