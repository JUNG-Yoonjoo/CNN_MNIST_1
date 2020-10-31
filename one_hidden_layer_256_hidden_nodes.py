# -*- coding: utf-8 -*-
"""One hidden layer_256 hidden nodes.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GateBLu1tUP-1eylKdMUg9W-ioHa68Nb
"""

import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import datetime
import numpy as np
import cv2

# Number of hidden neurons
n_hidden1 = 256

learning_rate = 0.01
training_epochs = 12
batch_size = 128

mnist = input_data.read_data_sets("./MNIST_DATA", one_hot=True)

X_train = tf.placeholder('float', [None, 784]) 
Y_train = tf.placeholder('float', [None, 10]) 

batch = mnist.train.next_batch(100)
x_batch = batch[0]
batch_tensor = tf.reshape(x_batch, [100, 28, 28, 1])
resized_images = tf.image.resize_images(batch_tensor, [7,7])

# Initialize Weights
W1 = tf.Variable(tf.random_normal([784, n_hidden1]))
W_output = tf.Variable(tf.random_normal([n_hidden1, 10]))

B1 = tf.Variable(tf.random_normal([n_hidden1]))
B_output = tf.Variable(tf.random_normal([10]))

# Construct model
L1 = tf.nn.relu(tf.add(tf.matmul(X_train,W1),B1))

# Output layer
L_output = tf.add(tf.matmul(L1,W_output),B_output) 

# Cross_entropy and Accuracy
cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=Y_train, logits=L_output))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cross_entropy)

correct_pred = tf.equal(tf.argmax(L_output, 1), tf.argmax(Y_train, 1))
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

init = tf.initialize_all_variables()

with tf.Session() as sess:
    sess.run(init)
    
    start_time = datetime.datetime.now()
    print('\n Start Reading! \n')

    # Training loop
    for epoch in range(training_epochs):
        total_batch = int(mnist.train.num_examples/batch_size)

        for step in range(total_batch):
            batch_xs, batch_ys = mnist.train.next_batch(batch_size)
            
            # Fit training
            sess.run(optimizer, feed_dict={X_train: batch_xs, Y_train: batch_ys})

        if epoch % 1 == 0:
          batch_accuracy = sess.run(
            accuracy,
            feed_dict={X_train: batch_xs, Y_train: batch_ys}
            )
        print(
            "Accuracy =",
            str(batch_accuracy)
            )
            
    finish_time = datetime.datetime.now()
    print ('\n Finish Reading! \n')


    # Test
    correct_prediction = tf.equal(tf.argmax(L_output, 1), tf.argmax(Y_train, 1))
    
    # Calculate accuracy
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
    print ("Accuracy:", accuracy.eval({X_train: mnist.test.images, Y_train: mnist.test.labels}))
    print('\n The duration is: %s \n'%(str(finish_time-start_time)))