class NaiveBayes:

    def __init__(self):
        self.bill_votes = {}

        self.republic = {}
        self.republic_prob = 0

        self.democrat = {}
        self.democrat_prob = 0

        self.train_expected = []
        self.test_actual = []

    """
    calculates the probability of the data given each class and returns the highest probability class
    input: a line from the test data
    output: the highest probability class as well as its probability
    """

    def naive_bayes_classifier(self, data):
        republican_prob = 1
        democratic_prob = 1

        # log probabilities for numerator
        for i in range(len(data) - 1):
            vote = data[i]
            # Π((vote_i | party)P(party))

            if vote == "Yea":
                add_republican = self.republic.get(i).get('Yea') * self.republic_prob
                republican_prob *= add_republican

                add_democratic = self.democrat.get(i).get('Yea') * self.democrat_prob
                democratic_prob *= add_democratic
                # print("P(bill_" + str(i) + " | party = republican):", add_republican)
                # print("P(bill_" + str(i) + " | party = democratic):", add_democratic)

            elif vote == "Nay":
                add_republican = self.republic.get(i).get('Nay') * self.republic_prob
                republican_prob *= add_republican

                add_democratic = self.democrat.get(i).get('Nay') * self.democrat_prob
                democratic_prob *= add_democratic
                # print("P(bill_" + str(i) + " | party = republican):", add_republican)
                # print("P(bill_" + str(i) + " | party = democratic):", add_democratic)

            else:
                add_republican = self.republic.get(i).get('Other') * self.republic_prob
                republican_prob *= add_republican

                add_democratic = self.democrat.get(i).get('Other') * self.democrat_prob
                democratic_prob *= add_democratic
                # print("P(bill_" + str(i) + " | party = republican):", add_republican)
                # print("P(bill_" + str(i) + " | party = democratic):", add_democratic)

        # normalize probabilities
        results = [republican_prob, democratic_prob]
        normalized = [float(i)/sum(results) for i in results]
        # republican_prob = republican_prob / (self.republic_prob * self.democrat_prob)
        # democratic_prob = democratic_prob / (self.republic_prob * self.democrat_prob)

        # print("Republican," + str(republican_prob))
        # print("Democratic," + str(democratic_prob))

        if republican_prob > democratic_prob:
            print("Republican," + str(normalized[0]))
            self.test_actual.append("Republican")
        elif republican_prob < democratic_prob:
            print("Democratic," + str(normalized[1]))
            self.test_actual.append("Democrat")

    """
    Reads the training data
    input: training data csv file
    output: frequency tables and probabilities used for naive bayes classifier
    """

    def train_model(self, train_data_directory):

        number_of_republican_voters = 0
        number_of_democratic_voters = 0

        # Read the training data and store raw data into lists bases on classification
        with open(train_data_directory, 'r') as f:
            for line in f:
                line = line.strip('\n').split(',')  # removes new line characters and empty elements
                classification = line[len(line) - 1]  # file formatted to have classification as last element in line
                training_data = line[0:len(line) - 1]  # training data with the classification label stripped

                # gets the number of republican and democratic voters
                if classification == "Republican":
                    number_of_republican_voters += 1
                    self.train_expected.append(classification)
                if classification == "Democrat":
                    number_of_democratic_voters += 1
                    self.train_expected.append(classification)

                # gets the number of yea and no votes for each bill from each party
                for i in range(len(training_data)):
                    if self.bill_votes.get(i) is None:
                        self.bill_votes[i] = {'Republican': {'Yea': 0, 'Nay': 0, 'Other': 0},
                                              'Democrat': {'Yea': 0, 'Nay': 0, 'Other': 0}}

                        if classification == "Republican":
                            if training_data[i] == "Yea":
                                self.bill_votes[i]["Republican"]['Yea'] = 1
                            elif training_data[i] == "Nay":
                                self.bill_votes[i]["Republican"]['Nay'] = 1
                            else:
                                self.bill_votes[i]["Republican"]['Other'] = 1

                        if classification == "Democrat":
                            if training_data[i] == "Yea":
                                self.bill_votes[i]["Democrat"]['Yea'] = 1
                            elif training_data[i] == "Nay":
                                self.bill_votes[i]["Democrat"]['Nay'] = 1
                            else:
                                self.bill_votes[i]["Democrat"]['Other'] = 1
                    else:
                        if classification == "Republican":
                            if training_data[i] == "Yea":
                                self.bill_votes[i]["Republican"]['Yea'] += 1
                            elif training_data[i] == "Nay":
                                self.bill_votes[i]["Republican"]['Nay'] += 1
                            else:
                                self.bill_votes[i]["Republican"]['Other'] += 1

                        if classification == "Democrat":
                            if training_data[i] == "Yea":
                                self.bill_votes[i]["Democrat"]['Yea'] += 1
                            elif training_data[i] == "Nay":
                                self.bill_votes[i]["Democrat"]['Nay'] += 1
                            else:
                                self.bill_votes[i]["Democrat"]['Other'] += 1

        # Probability of each party
        voters_for_both_parties = number_of_republican_voters + number_of_democratic_voters
        self.republic_prob = (number_of_republican_voters + 1) / voters_for_both_parties + 2
        self.democrat_prob = (number_of_democratic_voters + 1) / voters_for_both_parties + 2

        # Get probabilities of each vote for both parties
        for bill in self.bill_votes:
            # initialize value of each bill in dictionary
            self.republic[bill] = {"Yea": 0, "Nay": 0, "Other": 0}
            self.democrat[bill] = {"Yea": 0, "Nay": 0, "Other": 0}

            # Calculate P(vote_i | party) with laplace smoothing
            # Republican
            self.republic[bill]['Yea'] = (self.bill_votes[bill]['Republican']["Yea"] + 1) / (number_of_republican_voters + 1)
            self.republic[bill]['Nay'] = (self.bill_votes[bill]['Republican']["Nay"] + 1) / (number_of_republican_voters + 1)
            self.republic[bill]['Other'] = (self.bill_votes[bill]['Republican']["Other"] + 1) / (number_of_republican_voters + 1)
            # Democratic
            self.democrat[bill]['Yea'] = (self.bill_votes[bill]['Democrat']["Yea"] + 1) / (number_of_democratic_voters + 1)
            self.democrat[bill]['Nay'] = (self.bill_votes[bill]['Democrat']["Nay"] + 1) / (number_of_democratic_voters + 1)
            self.democrat[bill]['Other'] = (self.bill_votes[bill]['Democrat']["Other"] + 1) / (number_of_democratic_voters + 1)


    """
    reads each line from the test data and outputs classification
    input: the test data
    output: a line for each set in the test data that gives the chosen classification and its probability
    """

    def test_model(self, test_data_directory):
        with open(test_data_directory, 'r') as f:
            for line in f:
                voting_data = line.strip('\n').split(',')
                self.naive_bayes_classifier(voting_data)

    """
    The classification of each voter in the training data is removed and the modified data is added to the test file. 
    This method simply gets the classification for each line and compares it to the actual test data. 
    Output: The number of classifications from the test data that matched the training data
    """

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


def main():
    classifier = NaiveBayes()

    # classifier.train_model(args[0])  # arg 0
    # classifier.test_model(args[1])  # arg 1

    classifier.train_model('../data/my_train.csv')  # arg 0
    classifier.test_model('../data/my_test.csv')  # arg 1

    classifier.model_results()


if __name__ == '__main__':
    main()
