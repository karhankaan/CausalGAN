#-*- coding: utf-8 -*-
import argparse

def str2bool(v):
    #return (v is True) or (v.lower() in ('true', '1'))
    return v is True or v.lower() in ('true', '1')

arg_lists = []
parser = argparse.ArgumentParser()

def add_argument_group(name):
    arg = parser.add_argument_group(name)
    arg_lists.append(arg)
    return arg


#Network
net_arg = add_argument_group('Network')
net_arg.add_argument('--input_scale_size', type=int, default=64,
                     help='input image will be resized with the given value as width and height')
#net_arg.add_argument('--graph',type=str,default='big_causal_graph')
net_arg.add_argument('--conv_hidden_num', type=int, default=128,
                     choices=[64, 128],help='n in the paper')
net_arg.add_argument('--separate_labeler', type=str2bool, default=True)
net_arg.add_argument('--z_dim', type=int, default=64, choices=[64, 128])


# Data
data_arg = add_argument_group('Data')
data_arg.add_argument('--dataset', type=str, default='celebA')
data_arg.add_argument('--split', type=str, default='train')
data_arg.add_argument('--batch_size', type=int, default=16)
data_arg.add_argument('--grayscale', type=str2bool, default=False)
#data_arg.add_argument('--num_worker', type=int, default=4)
data_arg.add_argument('--num_worker', type=int, default=24,
                     help='number of threads to use for loading and preprocessing data')

# Training / test parameters
train_arg = add_argument_group('Training')
train_arg.add_argument('--beta1', type=float, default=0.5)
train_arg.add_argument('--beta2', type=float, default=0.999)
train_arg.add_argument('--d_lr', type=float, default=0.00008)
train_arg.add_argument('--g_lr', type=float, default=0.00008)
train_arg.add_argument('--indep_causal', type=str2bool, default=False)
#train_arg.add_argument('--is_train', type=str2bool, default=True)
train_arg.add_argument('--label_loss',type=str,default='squarediff',choices=['xe','absdiff','squarediff'])
train_arg.add_argument('--lr_update_step', type=int, default=100000, choices=[100000, 75000])
train_arg.add_argument('--max_step', type=int, default=50000)
train_arg.add_argument('--noisy_labels', type=str2bool, default=False)
train_arg.add_argument('--num_iter',type=int,default=100000,
                       help='the number of training iterations to run the model for')
train_arg.add_argument('--optimizer', type=str, default='adam')
train_arg.add_argument('--round_fake_labels',type=str2bool,default=True,
                       help='''Whether the label outputs of the causal
                       controller should be rounded first before calculating
                       the loss of generator or d-labeler''')
train_arg.add_argument('--use_gpu', type=str2bool, default=True)
train_arg.add_argument('--num_gpu', type=int, default=1,
                      help='specify 0 for cpu. If k specified, will default to\
                      first k of n detected. If use_gpu=True but num_gpu not\
                      specified will default to 1')


margin_arg = add_argument_group('Margin')
margin_arg.add_argument('--gamma', type=float, default=0.5)
margin_arg.add_argument('--gamma_label', type=float, default=0.5)
margin_arg.add_argument('--lambda_k', type=float, default=0.001)
margin_arg.add_argument('--lambda_l', type=float, default=0.00008)
margin_arg.add_argument('--lambda_z', type=float, default=0.01)
margin_arg.add_argument('--no_third_margin', type=str2bool, default=False)
margin_arg.add_argument('--zeta', type=float, default=0.5)

# Misc
misc_arg = add_argument_group('Misc')
misc_arg.add_argument('--build_all', type=str2bool, default=False,
                     help='''normally specifying is_pretrain=False will cause
                     the pretraining components not to be built and likewise
                      with is_train=False only the pretrain compoenent will
                      (possibly) be built. This is here as a debug helper to
                      enable building out the whole model without doing any
                      training''')
misc_arg.add_argument('--data_dir', type=str, default='data')
misc_arg.add_argument('--dry_run', action='store_true')
#misc_arg.add_argument('--dry_run', type=str2bool, default='False')
misc_arg.add_argument('--is_crop', type=str2bool, default='True')
misc_arg.add_argument('--resize_method',type=str,default='AREA',choices=['AREA','BILINEAR','BICUBIC','NEAREST_NEIGHBOR'],
                     help='''methods to resize image to 64x64. AREA seems to work
                     best, possibly some scipy methods could work better''')
misc_arg.add_argument('--cc_load_path', type=str, default='')
misc_arg.add_argument('--log_step', type=int, default=100)
misc_arg.add_argument('--save_step', type=int, default=5000)
misc_arg.add_argument('--num_log_samples', type=int, default=3)
misc_arg.add_argument('--log_level', type=str, default='INFO', choices=['INFO', 'DEBUG', 'WARN'])
misc_arg.add_argument('--log_dir', type=str, default='logs')
misc_arg.add_argument('--test_data_path', type=str, default=None,
                      help='directory with images which will be used in test sample generation')
#misc_arg.add_argument('--sample_per_image', type=int, default=64,
#                      help='# of sample per image during test sample generation')
misc_arg.add_argument('--random_seed', type=int, default=123)

#Doesn't do anything atm
#misc_arg.add_argument('--visualize', action='store_true')


def gpu_logic(config):

    #consistency between use_gpu and num_gpu
    if config.num_gpu>0:
        config.use_gpu=True
    else:
        config.use_gpu=False
#        if config.use_gpu and config.num_gpu==0:
#            config.num_gpu=1
    return config


def get_config():
    config, unparsed = parser.parse_known_args()
    config=gpu_logic(config)

    #this has to respect gpu/cpu
    #data_format = 'NCHW'
    if config.use_gpu:
        data_format = 'NCHW'
    else:
        data_format = 'NHWC'
    setattr(config, 'data_format', data_format)


    print('Loaded ./causal_began/config.py')

    return config, unparsed

if __name__=='__main__':
    #for debug of config
    config, unparsed = get_config()

