import random
import time


class CSVWriter:
    def __init__(self, directory):
        self.directory = './color_net/data/' + directory
        print(self.directory)
        pass

    def write(self, data):
        timestamp = time.strftime("%d_%m_%Y_%H_%M_%S", time.gmtime())
        filename = timestamp + '.csv'
        file = open(self.directory + '/' + filename, 'w')
        with file:
            for line in data:
                file.write(line)
                file.write('\n')
        print("Writing complete")
        pass

#
# def write_dummy_data():
#     data = []
#     append_line(data)
#     append_line(data)
#     append_line(data)
#     append_line(data)
#
#     w = CSVWriter('./training')
#     w.write(data)
#     pass
#
#
# def append_line(data):
#     line = '0,'
#     for n in range(256):
#         if n is not 256:
#             line += str(round(random.random() * 256)) + ','
#         else:
#             line += str(round(random.random() * 256))
#     data.append(line)
#     pass
#
