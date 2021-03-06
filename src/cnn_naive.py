from __future__ import division, print_function, absolute_import

import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected, flatten
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.normalization import local_response_normalization
from tflearn.layers.estimator import regression
import tensorflow as tf
import numpy as np


def get_network(do_dropout=True):
        # input images
        network = input_data(shape=[None,33,33,4], name='input')

	# conv + pool + norm + conv + pool + norm
	network = conv_2d(network, 32, 3, activation='relu', regularizer="L2")
	network = max_pool_2d(network, 2)
	network = local_response_normalization(network)
	network = conv_2d(network, 64, 3, activation='relu', regularizer="L2")
	network = max_pool_2d(network, 2)
	network = local_response_normalization(network)

	# fully connected layers
	network = fully_connected(network, 128, activation='relu')
	if do_dropout:
		network = dropout(network, 0.8)
	network = fully_connected(network, 256, activation='relu')
	if do_dropout:
		network = dropout(network, 0.8)

	# softmax + output layers
	network = fully_connected(network, 5, activation='softmax', name='soft')
	network = regression(network, optimizer='adam', learning_rate=0.00001, # 0.001
			     loss='categorical_crossentropy', name='target', batch_size=1000)
	return network
