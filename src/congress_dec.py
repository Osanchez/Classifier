import math


class Tree:
    def __init__(self):
        self.bill = None
        self.left = None
        self.right = None
        self.result = ''

    def decision_result(self):
        return self.result


class DecisionTree:
    def __init__(self):
        self.tree = None

        self.republican_voters = 0
        self.democrat_voters = 0

        self.votes = {}
        self.combined_votes = {}

        self.class_entropy = 0
        self.entropy = {}
        self.gain = {}

    def train_model(self, train_model_directory):
        # Keep the total number of yes and no votes for each bill (initialization)
        for i in range(42):
            self.combined_votes[i] = {'Yea': 0, 'Nay': 0}

        # Keep the number of yes and no votes for each class for each bill (initialization)
        for i in range(42):
            self.votes[i] = {'Republican': {'Yea': 0, 'Nay': 0}, 'Democrat': {'Yea': 0, 'Nay': 0}}

        # Begin reading training set
        with open(train_model_directory, 'r') as f:
            for line in f:
                line = line.strip('\n').split(',')
                classification = line[len(line) - 1]
                votes = line[0:len(line) - 1]

                if classification == "Republican":
                    self.republican_voters += 1
                elif classification == "Democrat":
                    self.democrat_voters += 1

                for i in range(len(votes)):
                    vote = votes[i]
                    if vote != "Yea":
                        vote = "Nay"
                        self.combined_votes[i][vote] += 1
                        self.votes[i][classification][vote] += 1
                    else:
                        self.combined_votes[i][vote] += 1
                        self.votes[i][classification][vote] += 1

        # --------------- calculate entropy of attribute ---------------
        print("# republicans:", self.republican_voters)
        print("# democrats:", self.democrat_voters)
        print("Votes", self.votes)
        print("Combined Votes", self.combined_votes)

        for i in range(len(self.combined_votes)):
            # calculate entropy of class
            q = sum(self.votes.get(i).get("Republican").values()) / sum(self.combined_votes.get(i).values())  # P
            self.class_entropy = (-q * math.log(q, 2)) - ((1 - q) * math.log((1 - q), 2))

            # 1. information gain
            self.entropy[i] = 0

            p_i = self.votes.get(i).get("Republican").get("Yea")  # yes votes from republicans for bill
            n_i = self.votes.get(i).get("Democrat").get("Yea")  # yes votes from democrats for bill
            q = p_i / (p_i + n_i)

            if p_i == n_i:
                information_gain_yea = 1
            elif p_i == 0 or n_i == 0:
                information_gain_yea = 0
            else:
                information_gain_yea = (-q * math.log(q, 2)) - ((1 - q) * math.log((1 - q), 2))

            self.entropy[i] += (((p_i + n_i) / (self.republican_voters + self.democrat_voters))
                                * information_gain_yea)

            p_i = self.votes.get(i).get("Republican").get("Nay")  # nay votes from republicans for bill
            n_i = self.votes.get(i).get("Democrat").get("Nay")  # nay votes from democrats for bill
            q = p_i / (p_i + n_i)

            if p_i == n_i:
                information_gain_nay = 1
            elif p_i == 0 or n_i == 0:
                information_gain_nay = 0
            else:
                information_gain_nay = (-q * math.log(q, 2)) - ((1 - q) * math.log((1 - q), 2))

            # 2. entropy
            self.entropy[i] += (((p_i + n_i) / (self.republican_voters + self.democrat_voters))
                                * information_gain_nay)  # information_gain_nay

            # 3. gain
            self.gain[i] = self.class_entropy - self.entropy[i]

        print("Entropy:", self.entropy)
        print("Gain:", self.gain)

        print("Root:", max(self.gain.keys(), key=(lambda k: self.gain[k])))  # max gain


    def build_tree_classifier(self, examples, attributes, parent_examples):
        if len(examples) == 0:
            return self.plurality_value(parent_examples)
        elif 1:
            pass
        elif len(attributes) == 0:
            return self.plurality_value(examples)

    def plurality_value(self, parent_example):



    def test_model(self, test_model_directory):
        pass


def main():
    tree = DecisionTree()
    tree.train_model('../data/congress_train.csv')


if __name__ == "__main__":
    main()
