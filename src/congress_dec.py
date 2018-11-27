import math

class Node:

    def __init__(self, vote_answer):
        self.vote = vote_answer
        self.republican_voters = 0
        self.democratic_voters = 0
        self.result = ''

    def update_voters(self, classification):
        if classification == "Republican":
            self.republican_voters += 1
        elif classification == "Democrat":
            self.democratic_voters += 1

    def get_republican_votes(self):
        return self.republican_voters

    def get_democratic_votes(self):
        return self.democratic_voters

    def is_pure(self):
        is_pure = False
        if self.republican_voters > 0 and self.democratic_voters == 0:
            self.result = "Republican"
            is_pure = True
        if self.republican_voters == 0 and self.democratic_voters > 0:
            is_pure = True
            self.result = "Democrat"
        return is_pure

    def get_stats(self):
        stats = {"Republicans": self.republican_voters, "Democrats": self.democratic_voters}
        return stats

    def decision_result(self):
        return self.result


class DecisionTree:
    def __init__(self):
        self.votes = {}
        self.entropy = {}

    def train_model(self, train_model_directory):
        # Keep the number of yes and no votes for each bill
        for i in range(42):
            self.votes[i] = {'Yea': 0, 'Other': 0}

        with open(train_model_directory, 'r') as f:
            for line in f:
                line = line.strip('\n').split(',')
                classification = line[len(line) - 1]
                votes = line[0:len(line) - 1]

                for i in range(len(votes)):
                    vote = votes[i]
                    if vote != "Yea":
                        vote = "Other"
                    self.votes[i][vote] += 1

        print(self.votes)
        for i in range(42):
            q = self.votes.get(i).get("Yea") / sum(self.votes.get(i).values())
            entropy = -(q * math.log(q, 2) + (1 - q) * math.log(1-q, 2))
            print(i, entropy)



    def test_model(self, test_model_directory):
        pass


def main():
    tree = DecisionTree()
    tree.train_model('../data/congress_train.csv')


if __name__ == "__main__":
    main()
