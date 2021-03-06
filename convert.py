#!/usr/bin/env python

import os
import sys
import numpy as np
import argparse
from kaffe import KaffeError, print_stderr
from kaffe.tensorflow import TensorFlowTransformer


def fatal_error(msg):
    print_stderr(msg)
    exit(-1)


def validate_arguments(args):
    if (args.data_output_path is not None) and (args.caffemodel is None):
        fatal_error('No input data path provided.')
    if (args.caffemodel is not None) and (args.data_output_path is None):
        fatal_error('No output data path provided.')
    if (args.code_output_path is None) and (args.data_output_path is None):
        fatal_error('No output path specified.')


def convert(def_path, caffemodel_path, data_output_path, code_output_path, phase):
    try:
        transformer = TensorFlowTransformer(def_path, caffemodel_path, phase=phase)
        print_stderr('Converting data...')
        if caffemodel_path is not None:
            data = transformer.transform_data()
            print_stderr('Saving data...')
            with open(data_output_path, 'wb') as data_out:
                np.save(data_out, data)
        if code_output_path:
            print_stderr('Saving source...')
            with open(code_output_path, 'wb') as src_out:
                src_out.write(transformer.transform_source())
        print_stderr('Done.')
    except KaffeError as err:
        fatal_error('Error encountered: {}'.format(err))


def main():
    # parser = argparse.ArgumentParser()
    # parser.add_argument('def_path', help='Model definition (.prototxt) path')
    # parser.add_argument('--caffemodel', help='Model data (.caffemodel) path')
    # parser.add_argument('--data-output-path', help='Converted data output path')
    # parser.add_argument('--code-output-path', help='Save generated source to this path')
    # parser.add_argument('-p',
    #                     '--phase',
    #                     default='test',
    #                     help='The phase to convert: test (default) or train')
    # args = parser.parse_args()
    # validate_arguments(args)

    class Arg(object):
       def __init__(self):
           pass

    args = Arg()
    args.def_path = '../resnet_sal/model/res50-sorm-baseline/test.prototxt'
    args.caffemodel = '../resnet_sal/model/res50-sorm-baseline/sorm_iter_40000.caffemodel'
    args.data_output_path = '../resnet_sal/model/tfmodel/resnet50_tfmodel.npy-ignore'
    args.code_output_path = '../resnet_sal/model/tfmodel/resnet50_tfmodel.py-ignore'
    args.phase = 'test'
    convert(args.def_path, args.caffemodel, args.data_output_path, args.code_output_path,
            args.phase)


if __name__ == '__main__':
    main()
