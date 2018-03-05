from color_net import neural_net
import json
import numpy
import time


def train(net, epochs, file_location):
    train_file = open(file_location)
    file_list = train_file.readlines()
    train_file.close()

    counter = 0

    for e in range(epochs):
        for record in file_list:
            # split the record by the ',' commas
            all_values = record.split(',')
            # scale and shift the inputs
            inputs = numpy.asfarray(all_values[1:-1]) / 255.0 * 0.99 + 0.01
            # create the target output values (all 0.01, except the desired label which is 0.99)
            targets = numpy.zeros(net.o_nodes) + 0.01
            # all_values[0] is the target label for this record
            # targets[int(all_values[0])] = 0.99
            targets[0] = 0.99
            net.train(inputs, targets)
            # commit progress
            print(compute_progress(counter, file_list.__len__(), epochs))
            counter += 1
            pass
        pass


def load_json_file(file_location):
    config_file = open(file_location)
    file_list = config_file.readlines()
    config_file.close()
    return json.loads(''.join(file_list))


def write_output_file(net, file_location):
    timestamp = time.strftime("%d_%m_%Y_%H_%M_%S", time.gmtime())
    path = file_location + '\\' + str(timestamp) + '.json'
    file = open(path, 'w')
    data = {
        'input_nodes': net.i_nodes,
        'hidden_nodes': net.h_nodes,
        'output_nodes': net.o_nodes,
        'weight_i_h': array2string(net.wih),
        'weight_h_o': array2string(net.who),
        'learning_rate': net.lr
    }
    file.write(json.dumps(data))
    pass


def array2string(a):
    return '|'.join('='.join('%0.3f' % x for x in y) for y in a)


def compute_progress(index, lines, epochs):
    progress = (index / lines) / epochs * 100
    return round(progress)


def main():
    # load configs
    config = load_json_file('./config.json')
    net_data = config['neural_network']
    print(net_data)
    # init net
    net = neural_net.NeuralNetwork(
        net_data['input_nodes'],
        net_data['hidden_nodes'],
        net_data['output_nodes'],
        net_data['learning_rate']
    )

    # set data locations
    training_file_location = './data/training/02_03_2018_02_37_01.csv'
    training_output_location = './data/training'

    # run training
    train(net, net_data['epochs'], training_file_location)

    # write output
    write_output_file(net, training_output_location)
    pass


main()
