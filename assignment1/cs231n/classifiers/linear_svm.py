import numpy as np
from random import shuffle
from past.builtins import xrange
import copy

def svm_loss_naive(W, X, y, reg):
  """
  Structured SVM loss function, naive implementation (with loops).

  Inputs have dimension D, there are C classes, and we operate on minibatches
  of N examples.

  Inputs:
  - W: A numpy array of shape (D, C) containing weights.
  - X: A numpy array of shape (N, D) containing a minibatch of data.
  - y: A numpy array of shape (N,) containing training labels; y[i] = c means
    that X[i] has label c, where 0 <= c < C.
  - reg: (float) regularization strength

  Returns a tuple of:
  - loss as single float
  - gradient with respect to weights W; an array of same shape as W
  """
  dW = np.zeros(W.shape) # initialize the gradient as zero

  # compute the loss and the gradient
  num_classes = W.shape[1]
  num_train = X.shape[0]
  loss = 0.0
  delta = 1.0
  for i in xrange(num_train):
    scores = X[i].dot(W)
    correct_class_score = scores[y[i]]
    for j in xrange(num_classes):
      grad = 0.0
      # if j == y[i]:
      #   for k in range(num_classes):
      #     if k != j:
      #       grad += max(0, scores[k] - correct_class_score + delta)
      #   grad = -1 * grad * X[i]
      #   print(grad.shape)
      #   dW[:,j] += grad
      # else:
      margin = scores[j] - correct_class_score + delta # note delta = 1
      if j == y[i]:
        total = 0
        for c in range(num_classes):
          if c != y[i]:
            if scores[c] - correct_class_score + delta > 0:
              total += 1.0
        #print(total, "total")
        grad = -1 * total
      else:
        if margin > 0:
          loss += margin
          grad = 1.0
      dW[:,j] += grad * X[i]

  # Right now the loss is a sum over all training examples, but we want it
  # to be an average instead so we divide by num_train.
  loss /= num_train
  dW /= num_train

  # Add regularization to the loss.
  loss += reg * np.sum(W * W)
  dW += reg * np.sum(W * W)
  #############################################################################
  # TODO:                                                                     #
  # Compute the gradient of the loss function and store it dW.                #
  # Rather that first computing the loss and then computing the derivative,   #
  # it may be simpler to compute the derivative at the same time that the     #
  # loss is being computed. As a result you may need to modify some of the    #
  # code above to compute the gradient.                                       #
  #############################################################################

  return loss, dW


def svm_loss_vectorized(W, X, y, reg):
  """
  Structured SVM loss function, vectorized implementation.

  Inputs and outputs are the same as svm_loss_naive.
  """
  loss = 0.0
  dW = np.zeros(W.shape) # initialize the gradient as zero

  #############################################################################
  # TODO:                                                                     #
  # Implement a vectorized version of the structured SVM loss, storing the    #
  # result in loss.                                                           #
  #############################################################################
  delta = 1.0
  num_train = X.shape[0]
  
  scores = X.dot(W) #(N,C)
  
  y_scores = scores[np.arange(scores.shape[0]), y]
  margins = (scores.T - y_scores).T + delta
  margins = np.maximum(margins, 0)
  margins[np.arange(margins.shape[0]), y] = 0.0
  gradient = copy.deepcopy(margins)
  gradient[gradient>0] = 1
  sum_vec = np.sum(gradient, axis=1)
  gradient[np.arange(margins.shape[0]),y] = -sum_vec
  dW = X.T.dot(gradient) #(D, N) dot (N, C) = (D,C)
  loss = np.sum(margins)
  loss /= num_train
  dW /= num_train
  loss += reg * np.sum(W * W)
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  

  #############################################################################
  # TODO:                                                                     #
  # Implement a vectorized version of the gradient for the structured SVM     #
  # loss, storing the result in dW.                                           #
  #                                                                           #
  # Hint: Instead of computing the gradient from scratch, it may be easier    #
  # to reuse some of the intermediate values that you used to compute the     #
  # loss.                                                                     #
  #############################################################################
  pass
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################

  return loss, dW
