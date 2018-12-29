import sys
import os
import datetime

import keras
import numpy
from keras.layers import Dense
from keras import Sequential
import surf_image


def create_model(input_dimension):
    model = Sequential()
    # use dropout to prevent overfitting
    model.add(Dense(units=32, activation=keras.activations.relu, input_dim=input_dimension))  # input dim = input_dimension
                    # kernel_initializer=keras.initializers.RandomNormal))
    model.add(Dense(units=256, activation=keras.activations.sigmoid))
    model.add(Dense(units=256, activation=keras.activations.sigmoid))
    model.add(Dense(units=1, activation=keras.activations.sigmoid))

    # For a binary classification problem
    model.compile(optimizer='rmsprop',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

    # sgd = keras.optimizers.SGD(lr=0.01, momentum=0.0, decay=0.0, nesterov=False)
    # model.compile(loss='mean_squared_error',
    #               optimizer=sgd,
    #               metrics=[accuracy, keras.metrics.binary_accuracy, keras.metrics.categorical_accuracy])

    return model


def get_file_data(file_config):
    # keras.utils.normalize(x_array)
    x_lst = []
    y_lst = []
    source_folder = os.path.dirname(file_config)
    with open(file_config) as fin:
        for line in fin:
            image, class_name = line.strip().split()
            if class_name == "Cocacola":
                y_lst.append(numpy.array([0]))
            elif class_name == "Pepsi":
                y_lst.append(numpy.array([1]))
            image_path = os.path.join(source_folder, image)
            x_lst.append(list(surf_image.surf_extract_features(image_path)))

            # x_nd = surf_image.surf_extract_features(image_path)
            # x_lst.append(x_nd.reshape(x_nd.shape[0], 1))

    x_np_array = numpy.array(x_lst)
    y_np_array = numpy.array(y_lst)
    print("File data: \nx: shape: {}, y: shape: {}".format(x_np_array.shape, y_np_array.shape))

    return x_np_array, y_np_array


def load_sequential_model_from_file(model_file_path):
    return Sequential.from_config(model_file_path)


def save_model(model, model_config_file):
    print("Saving model to file {}".format(model_config_file))
    model.save(model_config_file)


def load_model(model_config_file):
    return keras.models.load_model(model_config_file)


def train_model(model, x_train_data, y_train_data):
    start_time = datetime.datetime.today()
    print("Training model. x: {}, y: {}\n Start time: {}".format(x_train_data.shape, y_train_data.shape, start_time))

    # shuffle data before epochs
    print("x_train_data shape: {}. y_train_data shape: {}".format(x_train_data.shape, y_train_data.shape))
    model_history = model.fit(x_train_data, y_train_data, shuffle=True, epochs=100)

    end_time = datetime.datetime.today()
    print("End of training.\n End time: {}\n Duration: {}\nModel history:{}"
          .format(end_time, end_time-start_time, model_history))


def test_model(model, x_test_data, y_test_data):
    print("Evaluating model with {} input data".format(len(x_test_data)))
    evaluate_status = model.evaluate(x_test_data, y_test_data, verbose=1)
    print("Metrics names: {}".format(model.metrics_names))
    print("Done evaluating. Status: {}".format(evaluate_status))


def main(train_file_config, test_file_config):
    dump_model_file = "model.cfg"

    x_train_data, y_train_data = get_file_data(train_file_config)
    model = create_model(input_dimension=x_train_data.shape[1])
    train_model(model, x_train_data, y_train_data)

    keras.utils.print_summary(model)
    keras.utils.plot_model(model, to_file='model.png')

    save_model(model, dump_model_file)

    x_test_data, y_test_data = get_file_data(test_file_config)
    test_model(model, x_test_data, y_test_data)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: train_model.py TRAIN_FILE_PATH TEST_FILE_PATH")
        sys.exit(-1)
    sys.exit(main(sys.argv[1], sys.argv[2]))
