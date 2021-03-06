
import bn_read as rb
import tensorflow as tf
from bn_para_2 import *
import numpy as np

learning_rate = 0.001
training_iters = 40000
batch_size = 100
display_step = 20
save_step = 10000
val_step = 20

n_input = 126*126*3
n_classes = 100

x = tf.placeholder(tf.float32, [batch_size,126,126,3])
y = tf.placeholder(tf.int32, [batch_size])
train_phase = tf.placeholder(tf.bool, name='train_phase')
#To tell batch_norm whether to update global mean and var

def generate_name(num):
    name = str(num)
    for i in range(len(num),8):
        name = "0" + name
    return name

def read_tests():
    x=np.zeros([10000,128,128,3])
    n = []
    for i in range(1, 10001):
        name = "data/images/test/" + generate_name(i)
        n.append(generate_name(i))
        x[i-1] = sm.imread(name)*np.float32(1/255)
    return (n, x)

def max5(pr):
    pr = np.array(pr)
    ls = []
    for i in range(5):
        ag = np.argmax(pr)
        ls.append(ag)
        pr[ag] = 0
    return pr

def top_k_error(predictions, labels, k):
    in_top1 = tf.to_float(tf.nn.in_top_k(predictions, labels, k))
    num_correct = tf.reduce_sum(in_top1)
    return (float(batch_size) - num_correct) / float(batch_size)

def conv2d(name, l_input, w):
    #tf.nn.conv2d([patch,hight,width,channel], [filter_height, filter_width, in_channels, out_channels], strides=[patch,hight,width,channel])
    return tf.nn.conv2d(l_input, w, strides=[1, 1, 1, 1], padding='SAME', name=name)
def conv2dp(name, l_input, w):
    #tf.nn.conv2d([patch,hight,width,channel], [filter_height, filter_width, in_channels, out_channels], strides=[patch,hight,width,channel])
    return tf.nn.conv2d(l_input, w, strides=[1, 2, 2, 1], padding='SAME', name=name)
# def bias(name, l_input,b):
#     return tf.nn.bias_add(l_input,b,name=name)
def relu(name, l_input):
    return tf.nn.relu(l_input,name=name)
def max_pool(name, l_input, k,s=2):
    # ksize[patch,height,width,channel], strides[patch,height,width,channel]
    return tf.nn.max_pool(l_input, ksize=[1, k, k, 1], strides=[1, s, s, 1], padding='SAME', name=name)
def avg_pool(name, l_input, k,s=1):
    # ksize[patch,height,width,channel], strides[patch,height,width,channel]
    return tf.nn.avg_pool(l_input, ksize=[1, k, k, 1], strides=[1, s, s, 1], padding='SAME', name=name)
def cbbr(name, l_input, w, bn):
    return relu(name,batch_norm(conv2d(name, l_input,w), bn, train_phase, scope='bn'))
def cpbbr(name, l_input, w, bn):
    return relu(name,batch_norm(conv2dp(name, l_input,w), bn, train_phase, scope='bn'))
def batch_norm(x, bn, train_phase, scope='bn'):
    """
    Batch normalization on convolutional maps.
    Args:
        x:           Tensor, 4D BHWD input maps
        bn:       integer, depth of input maps
        train_phase: boolean tf.Varialbe, true indicates training phase
        scope:       string, variable scope
    Return:
        normed:      batch-normalized maps
    """
    with tf.variable_scope(scope):
        beta = tf.Variable(tf.constant(0.0, shape=[bn]),name='beta', trainable=True)
        gamma = tf.Variable(tf.constant(1.0, shape=[bn]),name='gamma', trainable=True)
        batch_mean, batch_var = tf.nn.moments(x, [0,1,2], name='moments')
        ema = tf.train.ExponentialMovingAverage(decay=0.5)
        def mean_var_with_update():
            ema_apply_op = ema.apply([batch_mean, batch_var])
            with tf.control_dependencies([ema_apply_op]):
                return tf.identity(batch_mean), tf.identity(batch_var)

        mean, var = tf.cond(train_phase,
                            mean_var_with_update,
                            lambda: (ema.average(batch_mean), ema.average(batch_var)))
        normed = tf.nn.batch_normalization(x, mean, var, beta, gamma, 1e-3)
    return normed

def res_new(_X, _weights, _bnorm):

    conv1 = cpbbr('conv1', _X, _weights['wc1'], _bnorm['bn1'])
    #[patch,63,63,64]
    conv1 = avg_pool('pool1',conv1,k=3,s=2)
    #[patch,32,32,64]
    conv2a_2a = cbbr('conv2a_2a', conv1, _weights['wc2a_2a'], _bnorm['bn2a_2a'])
    conv2a_2b = cbbr('conv2a_2b', conv2a_2a, _weights['wc2a_2b'], _bnorm['bn2a_2b'])
    conv2a_2c = cbbr('conv2a_2c', conv2a_2b, _weights['wc2a_2c'], _bnorm['bn2a_2c'])
    # [patch,32,32,256]

    conv2a_1 = cbbr('conv2a_1', conv1, _weights['wc2a_1'], _bnorm['bn2a_1'])
    # [patch,32,32,256]

    conv2a = tf.add(conv2a_1, conv2a_2c)
    conv2a = relu('conv2a', conv2a)
    # [patch,32,32,256]

    conv2b_2a = cbbr('conv2b_2a', conv2a, _weights['wc2b_2a'], _bnorm['bn2b_2a'])
    conv2b_2b = cbbr('conv2b_2b', conv2b_2a, _weights['wc2b_2b'], _bnorm['bn2b_2b'])
    conv2b_2c = cbbr('conv2b_2c', conv2b_2b, _weights['wc2b_2c'], _bnorm['bn2b_2c'])
    # [patch,32,32,256]

    conv2b = tf.add(conv2a, conv2b_2c)
    conv2b = relu('conv2b', conv2b)
    #[path,32,32,256]


    conv2c_2a = cbbr('conv2c_2a', conv2b, _weights['wc2c_2a'], _bnorm['bn2c_2a'])
    conv2c_2b = cbbr('conv2c_2b', conv2c_2a, _weights['wc2c_2b'], _bnorm['bn2c_2b'])
    conv2c_2c = cbbr('conv2c_2c', conv2c_2b, _weights['wc2c_2c'], _bnorm['bn2c_2c'])
    # [path,32,32,256]

    conv2c = tf.add(conv2b, conv2c_2c)
    conv2c = relu('conv2c', conv2c)
    #[path,32,32,256]

    conv3a_2a = cpbbr('conv3a_2a', conv2c, _weights['wc3a_2a'], _bnorm['bn3a_2a'])
    # [path,16,16,128]
    conv3a_2b = cbbr('conv3a_2b', conv3a_2a, _weights['wc3a_2b'], _bnorm['bn3a_2b'])
    conv3a_2c = cbbr('conv3a_2c', conv3a_2b, _weights['wc3a_2c'], _bnorm['bn3a_2c'])
    # [path,16,16,512]

    conv3a_1 = cpbbr('conv3a_1', conv2c, _weights['wc3a_1'], _bnorm['bn3a_1'])
    # [path,16,16,512]

    conv3a = tf.add(conv3a_1, conv3a_2c)
    conv3a = relu('conv3a', conv3a)
    #[path,16,16,512]

    conv3b_2a = cbbr('conv3b_2a', conv3a, _weights['wc3b_2a'], _bnorm['bn3b_2a'])
    conv3b_2b = cbbr('conv3b_2b', conv3b_2a, _weights['wc3b_2b'], _bnorm['bn3b_2b'])
    conv3b_2c = cbbr('conv3b_2c', conv3b_2b, _weights['wc3b_2c'], _bnorm['bn3b_2c'])
    # [path,16,16,512]

    conv3b = tf.add(conv3a, conv3b_2c)
    conv3b = relu('conv3b', conv3b)
    # [path,16,16,512]

    conv3c_2a = cbbr('conv3c_2a', conv3b, _weights['wc3c_2a'], _bnorm['bn3c_2a'])
    conv3c_2b = cbbr('conv3c_2b', conv3c_2a, _weights['wc3c_2b'], _bnorm['bn3c_2b'])
    conv3c_2c = cbbr('conv3c_2c', conv3c_2b, _weights['wc3c_2c'], _bnorm['bn3c_2c'])
    # [path,16,16,512]

    conv3c = tf.add(conv3b, conv3c_2c)
    conv3c = relu('conv3c', conv3c)
    # [path,16,16,512]

    conv3d_2a = cbbr('conv3d_2a', conv3c, _weights['wc3d_2a'], _bnorm['bn3d_2a'])
    conv3d_2b = cbbr('conv3d_2b', conv3d_2a, _weights['wc3d_2b'], _bnorm['bn3d_2b'])
    conv3d_2c = cbbr('conv3d_2c', conv3d_2b, _weights['wc3d_2c'], _bnorm['bn3d_2c'])
    # conv3d_2c = bias('conv3d_2c', conv3d_2c, __bnorm['bn3d_2c'])

    conv3d = tf.add(conv3c, conv3d_2c)
    conv3d = relu('conv3c', conv3d)
    #[path,16,16,512]

    # conv4a_2a = cpbbr('conv4a_2a', conv3d, _weights['wc4a_2a'], _bnorm['bn4a_2a'])
    # #[path,8,8,256]
    # conv4a_2b = cbbr('conv4a_2b', conv4a_2a, _weights['wc4a_2b'], _bnorm['bn4a_2b'])
    # conv4a_2c = cbbr('conv4a_2c', conv4a_2b, _weights['wc4a_2c'], _bnorm['bn4a_2c'])
    # #[path,8,8,1024]
    #
    # conv4a_1 = cpbbr('conv4a_1', conv3d, _weights['wc4a_1'], _bnorm['bn4a_1'])
    # #[path,8,8,1024]
    #
    # conv4a = relu('conv4a', tf.add( conv4a_1 , conv4a_2c ))
    # #[path,8,8,1024]
    #
    # conv4b_2a = cbbr('conv4b_2a', conv4a, _weights['wc4b_2a'], _bnorm['bn4b_2a'])
    # conv4b_2b = cbbr('conv4b_2b', conv4b_2a, _weights['wc4b_2b'], _bnorm['bn4b_2b'])
    # conv4b_2c = cbbr('conv4b_2c', conv4b_2b, _weights['wc4b_2c'], _bnorm['bn4b_2c'])
    #
    # conv4b = relu('conv4b', tf.add( conv4a , conv4b_2c ))
    # #[path,8,8,1024]
    #
    # conv4c_2a = cbbr('conv4c_2a', conv4b, _weights['wc4c_2a'], _bnorm['bn4c_2a'])
    # conv4c_2b = cbbr('conv4c_2b', conv4c_2a, _weights['wc4c_2b'], _bnorm['bn4c_2b'])
    # conv4c_2c = cbbr('conv4c_2c', conv4c_2b, _weights['wc4c_2c'], _bnorm['bn4c_2c'])
    #
    # conv4c = relu('conv4c', tf.add( conv4b , conv4c_2c ))
    #[path,8,8,1024]

    pool4 = avg_pool('pool4', conv3d, k=5, s=1)
    #[path,8,8,1024]

    dense1 = tf.reshape(pool4, [-1, _weights['out'].get_shape().as_list()[0]])
    #[patch,hight*width*channel]
    #out = tf.add(tf.matmul(dense1, _weights['out']), __bnorm['bout'])
    out = tf.matmul(dense1, _weights['out'])
    return out

pred = res_new(x, weights, bnorm)


cost = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(pred, y))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

top1=top_k_error(pred,y,1)
top5=top_k_error(pred,y,5)

saver = tf.train.Saver(tf.all_variables())
init = tf.initialize_all_variables()

with tf.Session() as sess:
    sess.run(init)
    saver.restore(sess,"resnew-6000")
    test = read_tests()
    f = ""
    for t in test:
        pred1 = res_net(t[1], weights, biases)
        top5 = max5(pred1.eval())
        f += "val/" + t[0]
        for i in top5:
            f += " " + str(i)
        f += "\n"
    print(f)

