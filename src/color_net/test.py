from color_net import neural_net
import json
import numpy

def load_json_file(file_location):
    config_file = open(file_location)
    file_list = config_file.readlines()
    config_file.close()
    return json.loads(''.join(file_list))


def test(net, file_location):
    test_file = open(file_location)
    file_list = test_file.readlines()
    test_file.close()

    counter = 0
    scorecard = []

    # go through all the records in the test data set
    for record in file_list:
        # split the record by the ',' commas
        all_values = record.split(',')
        # correct answer is first value
        correct_label = int(all_values[0])
        # scale and shift the inputs
        inputs = (numpy.asfarray(all_values[1:-1]) / 255.0 * 0.99) + 0.01
        # query the network
        outputs = net.query(inputs)
        # the index of the highest value corresponds to the label
        label = numpy.argmax(outputs)
        # append correct or incorrect to list
        if label == correct_label:
            # network's answer matches correct answer, add 1 to scorecard
            scorecard.append(1)
        else:
            # network's answer doesn't match correct answer, add 0 to scorecard
            scorecard.append(0)
            pass
        # commit progress
        print(compute_progress(counter, file_list.__len__()))
        counter += 1
        pass
    scorecard_array = numpy.asarray(scorecard)
    return {'percentage': scorecard_array.sum() / scorecard_array.size * 100}


def compute_progress(index, lines):
    progress = (index / lines) * 100
    return round(progress)


def string_to_matrix(data):
    nd_array = []
    rows = data.split('|')
    for row in rows:
        m = row.split('=')
        for i in range(m.__len__()):
            m[i] = float(m[i])
            pass
        nd_array.append(m)
        pass
    mat = numpy.asmatrix(nd_array)
    return mat


def main():
    # set data locations
    net_data_location = './data/training/02_03_2018_02_37_20.json'
    testing_file_location = './data/training/02_03_2018_02_37_01.csv'

    # load net weights
    net_data = load_json_file(net_data_location)

    # init net
    net = neural_net.NeuralNetwork(
        net_data['input_nodes'],
        net_data['hidden_nodes'],
        net_data['output_nodes'],
        net_data['learning_rate']
    )
    net.set_weights(
        string_to_matrix(net_data['weight_i_h']),
        string_to_matrix(net_data['weight_h_o'])
    )

    # run test
    performance = test(net, testing_file_location)
    print('performance: ', str(performance['percentage']) + '%')


main()
