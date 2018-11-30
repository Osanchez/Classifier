import math
import operator
import random
from collections import Counter


class DecisionTree:
    def __init__(self):
        self.tree = None
        self.data = []
        self.test = []
        self.attributes = [i for i in range(43)]

        self.train_expected = []
        self.test_actual = []

    def read_data(self, train_model_directory):
        # Begin reading training set
        with open(train_model_directory, 'r') as f:
            for line in f:
                line = line.strip('\n').split(',')
                self.train_expected.append(line[len(line) - 1])
                self.data.append(line)

    def getExamples(self, data, best_attribute, val):
        examples = [[]]
        index = best_attribute
        for entry in data:
            if entry[index] == val:
                new_entry = []
                # add value if it is not in best column
                for i in range(len(entry)):
                    if i != index:
                        new_entry.append(entry[i])
                examples.append(new_entry)
        examples.remove([])
        return examples

    def getValues(self, examples, best_attribute):
        values = []

        for example in examples:
            if example[best_attribute] not in values:
                values.append(example[best_attribute])
        return values

    def importance(self, examples, attributes):
        gain = []

        number_republicans = 0
        number_democrats = 0

        # gets the number of republicans and democratic voters in examples
        for example in examples:
            classification = example[len(example) - 1]
            if classification == "Republican":
                number_republicans += 1
            elif classification == "Democrat":
                number_democrats += 1

        # print(number_republicans)
        # print(number_democrats)

        # calculate entropy of class attribute
        P = number_republicans
        N = number_democrats
        entropy_class = ((-P) / (P + N)) * math.log((P / (P + N)), 2) - (N / (P + N)) * math.log((N / (P + N)), 2)

        # information gain
        for attribute_index in attributes:
            # yes vote
            p_i = 0
            n_i = 0

            # no vote
            p_i_2 = 0
            n_i_2 = 0

            for voter in examples:

                classification = voter[len(voter) - 1]
                vote = voter[attribute_index]

                if vote == "Yea" and classification == "Republican":
                    p_i += 1
                elif vote == "Yea" and classification == "Democrat":
                    n_i += 1
                elif vote != "Yea" and classification == "Republican":
                    p_i_2 += 1
                elif vote != "Yea" and classification == "Democrat":
                    n_i_2 += 1

        # entropy of attribute
            entropy_attribute = (((p_i + n_i)/(P + N)) * self.information_gain(p_i, n_i)) + \
                                (((p_i_2 + n_i_2)/(P + N)) * self.information_gain(p_i_2, n_i_2))
            # print(entropy_attribute)

        # gain
            attribute_gain = entropy_class - entropy_attribute
            gain.append(attribute_gain)

        # print(max(enumerate(gain), key=operator.itemgetter(1))[0])  # return the attribute with greatest gain

        return max(enumerate(gain), key=operator.itemgetter(1))[0]

    def information_gain(self, p_i, n_i):
        if p_i == n_i:
            return 1
        elif p_i == 0 or n_i == 0:
            return 0
        else:
            return ((-p_i) / (p_i + n_i)) * math.log((p_i / (p_i + n_i)), 2)\
                   - (n_i / (p_i + n_i)) * math.log((n_i / (p_i + n_i)), 2)

    def plurality_value(self, examples):
        tie_breaker = ["Republican", "Democrat"]
        republicans = 0
        democrats = 0

        for example in examples:
            classification = example[len(example) - 1]
            if classification == "Republican":
                republicans += 1
            elif classification == "Democrat":
                democrats += 1

        if republicans > democrats:
            return "Republican"
        elif democrats > republicans:
            return "Democrat"
        else:
            return random.choice(tie_breaker)

    def build_tree_classifier(self, examples, attributes, parent_examples):
        # print("examples", examples)
        # print("attributes", attributes)
        # print("parent example", parent_examples)
        # print()

        republicans = None
        democrats = None

        if len(examples[0]) > 1:
            republicans = 0
            democrats = 0
            for i in range(len(examples)):
                classification = examples[i][len(examples[i]) - 1]
                if classification == "Republican":
                    republicans += 1
                elif classification == "Democrat":
                    democrats += 1

        if len(examples[0]) == 0:
            return self.plurality_value(parent_examples)
        elif republicans == 0:
            return "Democrat"
        elif democrats == 0:
            return "Republican"
        elif len(attributes) == 0:
            return self.plurality_value(examples)
        else:
            # calculate the attribute with highest importance given a list of examples
            A = self.importance(examples, attributes)
            tree = {A: {}}

            # Create a new decision tree/sub-node for each of the values in the best attribute field
            for val in self.getValues(examples, A):  # v_k
                # Create a subtree for the current value under the "best" field
                exs = self.getExamples(examples, A, val)
                attributes_copy = [i for i in range(len(exs[0]))]
                # print(len(exs[0]))
                subtree = self.build_tree_classifier(exs, attributes_copy, examples)
                # Add the new subtree to the empty dictionary object in our new
                # tree/node we just created.
                tree[A][val] = subtree
            self.tree = tree
            return tree

    def test_model(self, test_model_directory):
        # Begin reading training set
        with open(test_model_directory, 'r') as f:
            for line in f:
                line = line.strip('\n').split(',')
                self.test.append(line)

        examples = self.test
        tree = self.tree

        for example in examples:
            tree = self.tree
            while tree != "Republican" and tree != "Democrat":
                # enter tree at key while recording key
                key = list(tree.keys())[0]
                tree = tree.get(key)

                # grab vote from example using recorded key
                vote = example[key]
                # if vote != "Yea":
                #     vote = "Nay"

                # navigate tree using recorded vote
                tree = tree.get(vote)

            self.test_actual.append(tree)
            print(tree)

    def model_results(self):
        matched = 0
        values = len(self.test_actual)
        incorrect_lines = []

        for i in range(len(self.test_actual)):
            if self.train_expected[i] == self.test_actual[i]:
                matched += 1
            else:
                incorrect_lines.append(i + 1)
        print()
        print("Correct/Total: ", str(matched) + "/" + str(values))
        print("Incorrect Lines:", incorrect_lines)

    def result_information(self):
        print(Counter(self.test_actual))


def main():
    d_tree = DecisionTree()
    d_tree.read_data('../data/congress_train.csv')
    d_tree.build_tree_classifier(d_tree.data, d_tree.attributes, [])
    d_tree.test_model('../data/congress_test.csv')
    # d_tree.model_results()
    d_tree.result_information()


if __name__ == "__main__":
    main()
