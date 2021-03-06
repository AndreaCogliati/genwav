###############################################################################
# Language Modeling on Penn Tree Bank
#
# This file generates new sentences sampled from the language model
#
###############################################################################

import argparse
import time
import math
import numpy as np
import scipy.io.wavfile as wavfile

import torch
import torch.nn as nn
from torch.autograd import Variable

parser = argparse.ArgumentParser(description='PyTorch PTB Language Model')

# Model parameters.
parser.add_argument('--checkpoint', type=str, default='./model.pt',
                    help='model checkpoint to use')
parser.add_argument('--outf', type=str, default='generated.wav',
                    help='output file for generated wav')
parser.add_argument('--samples', type=int, default='1000',
                    help='number of samples to generate')
parser.add_argument('--seed', type=int, default=1111,
                    help='random seed')
parser.add_argument('--cuda', action='store_true',
                    help='use CUDA')
parser.add_argument('--temperature', type=float, default=1.0,
                    help='temperature - higher will increase diversity')
parser.add_argument('--log-interval', type=int, default=100,
                    help='reporting interval')
args = parser.parse_args()

# Set the random seed manually for reproducibility.
torch.manual_seed(args.seed)
if torch.cuda.is_available():
    if not args.cuda:
        print("WARNING: You have a CUDA device, so you should probably run with --cuda")
    else:
        torch.cuda.manual_seed(args.seed)

if args.temperature < 1e-3:
    parser.error("--temperature has to be greater or equal 1e-3")

with open(args.checkpoint, 'rb') as f:
    model = torch.load(f)

if args.cuda:
    model.cuda()
else:
    model.cpu()

ntokens = 65536
hidden = model.init_hidden(1)
input = Variable(torch.rand(1, 1).mul(ntokens).long(), volatile=True)
if args.cuda:
    input.data = input.data.cuda()

data = []
for i in range(args.samples):
    output, hidden = model(input, hidden)
    sample_weights = output.squeeze().data.div(args.temperature).exp().cpu()
    next_sample = torch.multinomial(sample_weights, 1)[0]
    input.data.fill_(next_sample)
    data.append(int(next_sample - 32768))

wavfile.write(args.outf, 11025, np.array(data))

if i % args.log_interval == 0:
    print('| Generated {}/{} samples'.format(i, args.samples))
