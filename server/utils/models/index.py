import torch.nn.functional as F 
import torch
import math
import torch.nn as nn
from torch.nn.grad import conv2d_input, conv2d_weight

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class LinearFunction(torch.autograd.Function) :

  @staticmethod
  def forward(ctx, input, weight, bias=None) :
    ctx.save_for_backward(input, weight, bias)

    output = F.linear(input, weight, bias)
    return output

  @staticmethod
  def backward(ctx, grad_output):  # type: ignore[override]
    input, weight, bias = ctx.saved_tensors

    grad_input = grad_output @ weight
    grad_weight = grad_output.T @ input
    grad_bias = torch.sum(grad_output, dim=0)


    return grad_input, grad_weight, grad_bias

class ConvolutionFunction(torch.autograd.Function) :

  @staticmethod
  def forward(ctx, input, weight, bias=None, stride = 1, padding = 0) :
    ctx.save_for_backward(input, weight, bias)
    ctx.stride = stride
    ctx.padding = padding

    output = F.conv2d(input, weight, bias, stride, padding)
    return output

  @staticmethod
  def backward(ctx, grad_output) :  # type: ignore[override]
    input, weight, bias = ctx.saved_tensors
    stride = ctx.stride
    padding = ctx.padding

    grad_input = conv2d_input(input.shape, weight, grad_output, stride, padding)
    grad_weight = conv2d_weight(input, weight.shape, grad_output, stride, padding)
    grad_bias = torch.sum(grad_output, dim=(0,2,3))

    return grad_input, grad_weight, grad_bias, None, None

class Dense(nn.Module):

  def __init__(self, input_size, output_size):
    super(Dense, self).__init__()
    self.weights = nn.Parameter(torch.empty(output_size, input_size, device=device))
    self.bias = nn.Parameter(torch.zeros(output_size, device=device))
    nn.init.kaiming_uniform_(self.weights, a=math.sqrt(5))

  def forward(self, input) :
    return LinearFunction.apply(input, self.weights, self.bias)

class Convolution(nn.Module) :

  def __init__(self, in_channel, out_channel, kernel_size) :
    super(Convolution, self).__init__()
    self.kernels = nn.Parameter(torch.empty(out_channel, in_channel, kernel_size, kernel_size, device=device))
    self.bias = nn.Parameter(torch.zeros(out_channel, device=device))
    nn.init.kaiming_uniform_(self.kernels, a=math.sqrt(5))

  def forward(self, input) :
    return ConvolutionFunction.apply(input, self.kernels, self.bias)

class MaxPool(nn.Module) :
  def __init__(self, kernel_size) :
    super(MaxPool, self).__init__()
    self.kernel_size = kernel_size

  def forward(self, input) :
    output = F.max_pool2d(input, self.kernel_size)
    return output

class NeuralNet(nn.Module) :

  def __init__(self):
    super(NeuralNet, self).__init__()

    self.conv1 = Convolution(3, 32, 3)
    self.conv2 = Convolution(32, 64, 3)
    self.conv3 = Convolution(64, 128, 3)
    self.conv4 = Convolution(128, 256, 3)
    self.conv5 = Convolution(256, 512, 3)
    self.pool = MaxPool(2)

    self.fc1 = Dense(6*6*512,1024)
    self.fc2 = Dense(1024, 64)
    self.fc3 = Dense(64, 10)
    self.flatten = nn.Flatten(start_dim=1)

  def forward(self, x) :
    x = self.pool(F.relu(self.conv1(x)))
    x = self.pool(F.relu(self.conv2(x)))
    x = self.pool(F.relu(self.conv3(x)))
    x = self.pool(F.relu(self.conv4(x)))
    x = self.pool(F.relu(self.conv5(x)))

    x = self.flatten(x)
    x = F.relu(self.fc1(x))
    x = F.relu(self.fc2(x))
    x = self.fc3(x)
    return x
