import tensorflow as tf
import math

def stdd(num):
    return math.sqrt(2.0 / float(num))

weights = {
    'wc1': tf.Variable(tf.random_normal([7, 7, 3, 64], stddev=stdd(3))),
    'wc2a_2a': tf.Variable(tf.random_normal([1, 1, 64, 64], stddev=stdd(64))),
    'wc2a_2b': tf.Variable(tf.random_normal([3, 3, 64, 64], stddev=stdd(64))),
    'wc2a_2c': tf.Variable(tf.random_normal([1, 1, 64, 256], stddev=stdd(64))),
    'wc2a_1': tf.Variable(tf.random_normal([1, 1, 64, 256], stddev=stdd(64))),
    'wc2b_2a': tf.Variable(tf.random_normal([1, 1, 256, 64], stddev=stdd(256))),
    'wc2b_2b': tf.Variable(tf.random_normal([3, 3, 64, 64], stddev=stdd(64))),
    'wc2b_2c': tf.Variable(tf.random_normal([1, 1, 64, 256], stddev=stdd(64))),
    'wc2c_2a': tf.Variable(tf.random_normal([1, 1, 256, 64], stddev=stdd(256))),
    'wc2c_2b': tf.Variable(tf.random_normal([3, 3, 64, 64], stddev=stdd(64))),
    'wc2c_2c': tf.Variable(tf.random_normal([1, 1, 64, 256], stddev=stdd(64))),
    'wc3a_2a': tf.Variable(tf.random_normal([1, 1, 256, 128], stddev=stdd(256))),
    'wc3a_2b': tf.Variable(tf.random_normal([3, 3, 128, 128], stddev=stdd(128))),
    'wc3a_2c': tf.Variable(tf.random_normal([1, 1, 128, 512], stddev=stdd(128))),
    'wc3a_1': tf.Variable(tf.random_normal([1, 1, 256, 512], stddev=stdd(256))),
    'wc3b_2a': tf.Variable(tf.random_normal([1, 1, 512, 128], stddev=stdd(512))),
    'wc3b_2b': tf.Variable(tf.random_normal([3, 3, 128, 128], stddev=stdd(128))),
    'wc3b_2c': tf.Variable(tf.random_normal([1, 1, 128, 512], stddev=stdd(128))),
    'wc3c_2a': tf.Variable(tf.random_normal([1, 1, 512, 128], stddev=stdd(512))),
    'wc3c_2b': tf.Variable(tf.random_normal([3, 3, 128, 128], stddev=stdd(128))),
    'wc3c_2c': tf.Variable(tf.random_normal([1, 1, 128, 512], stddev=stdd(128))),
    'wc3d_2a': tf.Variable(tf.random_normal([1, 1, 512, 128], stddev=stdd(512))),
    'wc3d_2b': tf.Variable(tf.random_normal([3, 3, 128, 128], stddev=stdd(128))),
    'wc3d_2c': tf.Variable(tf.random_normal([1, 1, 128, 512], stddev=stdd(128))),
    'wc4a_2a': tf.Variable(tf.random_normal([1, 1, 512, 256], stddev=stdd(512))),
    'wc4a_2b': tf.Variable(tf.random_normal([3, 3, 256, 256], stddev=stdd(256))),
    'wc4a_2c': tf.Variable(tf.random_normal([1, 1, 256, 1024], stddev=stdd(256))),
    'wc4a_1': tf.Variable(tf.random_normal([1, 1, 512, 1024], stddev=stdd(512))),
    'wc4b_2a': tf.Variable(tf.random_normal([1, 1, 1024, 256], stddev=stdd(1024))),
    'wc4b_2b': tf.Variable(tf.random_normal([3, 3, 256, 256], stddev=stdd(256))),
    'wc4b_2c': tf.Variable(tf.random_normal([1, 1, 256, 1024], stddev=stdd(256))),
    'wc4c_2a': tf.Variable(tf.random_normal([1, 1, 1024, 256], stddev=stdd(1024))),
    'wc4c_2b': tf.Variable(tf.random_normal([3, 3, 256, 256], stddev=stdd(256))),
    'wc4c_2c': tf.Variable(tf.random_normal([1, 1, 256, 1024], stddev=stdd(256))),
    'wc4d_2a': tf.Variable(tf.random_normal([1, 1, 1024, 256], stddev=stdd(1024))),
    'wc4d_2b': tf.Variable(tf.random_normal([3, 3, 256, 256], stddev=stdd(256))),
    'wc4d_2c': tf.Variable(tf.random_normal([1, 1, 256, 1024], stddev=stdd(256))),
    'wc4e_2a': tf.Variable(tf.random_normal([1, 1, 1024, 256], stddev=stdd(1024))),
    'wc4e_2b': tf.Variable(tf.random_normal([3, 3, 256, 256], stddev=stdd(256))),
    'wc4e_2c': tf.Variable(tf.random_normal([1, 1, 256, 1024], stddev=stdd(256))),
    'wc4f_2a': tf.Variable(tf.random_normal([1, 1, 1024, 256], stddev=stdd(1024))),
    'wc4f_2b': tf.Variable(tf.random_normal([3, 3, 256, 256], stddev=stdd(256))),
    'wc4f_2c': tf.Variable(tf.random_normal([1, 1, 256, 1024], stddev=stdd(256))),
    'wc5a_2a': tf.Variable(tf.random_normal([1, 1, 1024, 512], stddev=stdd(1024))),
    'wc5a_2b': tf.Variable(tf.random_normal([3, 3, 512, 512], stddev=stdd(512))),
    'wc5a_2c': tf.Variable(tf.random_normal([1, 1, 512, 2048], stddev=stdd(512))),
    'wc5a_1': tf.Variable(tf.random_normal([1, 1, 1024, 2048], stddev=stdd(1024))),
    'wc5b_2a': tf.Variable(tf.random_normal([1, 1, 2048, 512], stddev=stdd(2048))),
    'wc5b_2b': tf.Variable(tf.random_normal([3, 3, 512, 512], stddev=stdd(512))),
    'wc5b_2c': tf.Variable(tf.random_normal([1, 1, 512, 2048], stddev=stdd(512))),
    'wc5c_2a': tf.Variable(tf.random_normal([1, 1, 2048, 512], stddev=stdd(2048))),
    'wc5c_2b': tf.Variable(tf.random_normal([3, 3, 512, 512], stddev=stdd(512))),
    'wc5c_2c': tf.Variable(tf.random_normal([1, 1, 512, 2048], stddev=stdd(512))),

    'out': tf.Variable(tf.random_normal([8*8*2048, 100], stddev=stdd(8*8*2048))),

}
biases = {
    'bc1': tf.Variable(tf.random_normal([64], stddev=0)),
    'bc2a_2a': tf.Variable(tf.random_normal([64], stddev=0)),
    'bc2a_2b': tf.Variable(tf.random_normal([64], stddev=0)),
    'bc2a_2c': tf.Variable(tf.random_normal([256], stddev=0)),
    'bc2a_1': tf.Variable(tf.random_normal([256], stddev=0)),
    'bc2b_2a': tf.Variable(tf.random_normal([64], stddev=0)),
    'bc2b_2b': tf.Variable(tf.random_normal([64], stddev=0)),
    'bc2b_2c': tf.Variable(tf.random_normal([256], stddev=0)),
    'bc2c_2a': tf.Variable(tf.random_normal([64], stddev=0)),
    'bc2c_2b': tf.Variable(tf.random_normal([64], stddev=0)),
    'bc2c_2c': tf.Variable(tf.random_normal([256], stddev=0)),
    'bc3a_2a': tf.Variable(tf.random_normal([128], stddev=0)),
    'bc3a_2b': tf.Variable(tf.random_normal([128], stddev=0)),
    'bc3a_2c': tf.Variable(tf.random_normal([512], stddev=0)),
    'bc3a_1': tf.Variable(tf.random_normal([512], stddev=0)),
    'bc3b_2a': tf.Variable(tf.random_normal([128], stddev=0)),
    'bc3b_2b': tf.Variable(tf.random_normal([128], stddev=0)),
    'bc3b_2c': tf.Variable(tf.random_normal([512], stddev=0)),
    'bc3c_2a': tf.Variable(tf.random_normal([128], stddev=0)),
    'bc3c_2b': tf.Variable(tf.random_normal([128], stddev=0)),
    'bc3c_2c': tf.Variable(tf.random_normal([512], stddev=0)),
    'bc3d_2a': tf.Variable(tf.random_normal([128], stddev=0)),
    'bc3d_2b': tf.Variable(tf.random_normal([128], stddev=0)),
    'bc3d_2c': tf.Variable(tf.random_normal([512], stddev=0)),
    'bc4a_2a': tf.Variable(tf.random_normal([256], stddev=0)),
    'bc4a_2b': tf.Variable(tf.random_normal([256], stddev=0)),
    'bc4a_2c': tf.Variable(tf.random_normal([1024], stddev=0)),
    'bc4a_1': tf.Variable(tf.random_normal([1024], stddev=0)),
    'bc4b_2a': tf.Variable(tf.random_normal([256], stddev=0)),
    'bc4b_2b': tf.Variable(tf.random_normal([256], stddev=0)),
    'bc4b_2c': tf.Variable(tf.random_normal([1024], stddev=0)),
    'bc4c_2a': tf.Variable(tf.random_normal([256], stddev=0)),
    'bc4c_2b': tf.Variable(tf.random_normal([256], stddev=0)),
    'bc4c_2c': tf.Variable(tf.random_normal([1024], stddev=0)),
    'bc4d_2a': tf.Variable(tf.random_normal([256], stddev=0)),
    'bc4d_2b': tf.Variable(tf.random_normal([256], stddev=0)),
    'bc4d_2c': tf.Variable(tf.random_normal([1024], stddev=0)),
    'bc4e_2a': tf.Variable(tf.random_normal([256], stddev=0)),
    'bc4e_2b': tf.Variable(tf.random_normal([256], stddev=0)),
    'bc4e_2c': tf.Variable(tf.random_normal([1024], stddev=0)),
    'bc4f_2a': tf.Variable(tf.random_normal([256], stddev=0)),
    'bc4f_2b': tf.Variable(tf.random_normal([256], stddev=0)),
    'bc4f_2c': tf.Variable(tf.random_normal([1024], stddev=0)),
    'bc5a_2a': tf.Variable(tf.random_normal([512], stddev=0)),
    'bc5a_2b': tf.Variable(tf.random_normal([512], stddev=0)),
    'bc5a_2c': tf.Variable(tf.random_normal([2048], stddev=0)),
    'bc5a_1': tf.Variable(tf.random_normal([2048], stddev=0)),
    'bc5b_2a': tf.Variable(tf.random_normal([512], stddev=0)),
    'bc5b_2b': tf.Variable(tf.random_normal([512], stddev=0)),
    'bc5b_2c': tf.Variable(tf.random_normal([2048], stddev=0)),
    'bc5c_2a': tf.Variable(tf.random_normal([512], stddev=0)),
    'bc5c_2b': tf.Variable(tf.random_normal([512], stddev=0)),
    'bc5c_2c': tf.Variable(tf.random_normal([2048], stddev=0)),

}

bnorm = {
    #Not trainable variables
    'bn1': 64,
    'bn2a_2a': 64,
    'bn2a_2b': 64,
    'bn2a_2c': 256,
    'bn2a_1': 256,
    'bn2b_2a': 64,
    'bn2b_2b': 64,
    'bn2b_2c': 256,
    'bn2c_2a': 64,
    'bn2c_2b': 64,
    'bn2c_2c': 256,
    'bn3a_2a': 128,
    'bn3a_2b': 128,
    'bn3a_2c': 512,
    'bn3a_1': 512,
    'bn3b_2a': 128,
    'bn3b_2b': 128,
    'bn3b_2c': 512,
    'bn3c_2a': 128,
    'bn3c_2b': 128,
    'bn3c_2c': 512,
    'bn3d_2a': 128,
    'bn3d_2b': 128,
    'bn3d_2c': 512,
    'bn4a_2a': 256,
    'bn4a_2b': 256,
    'bn4a_2c': 1024,
    'bn4a_1': 1024,
    'bn4b_2a': 256,
    'bn4b_2b': 256,
    'bn4b_2c': 1024,
    'bn4c_2a': 256,
    'bn4c_2b': 256,
    'bn4c_2c': 1024,
    'bn4d_2a': 256,
    'bn4d_2b': 256,
    'bn4d_2c': 1024,
    'bn4e_2a': 256,
    'bn4e_2b': 256,
    'bn4e_2c': 1024,
    'bn4f_2a': 256,
    'bn4f_2b': 256,
    'bn4f_2c': 1024,
    'bn5a_2a': 512,
    'bn5a_2b': 512,
    'bn5a_2c': 2048,
    'bn5a_1': 2048,
    'bn5b_2a': 512,
    'bn5b_2b': 512,
    'bn5b_2c': 2048,
    'bn5c_2a': 512,
    'bn5c_2b': 512,
    'bn5c_2c': 2048,

    'bout': 100,
}
