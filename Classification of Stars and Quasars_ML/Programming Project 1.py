import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.mlab as mlab 
from sklearn.utils import shuffle

from sklearn import metrics 
from sklearn.naive_bayes import GaussianNB
from sklearn.mixture import GaussianMixture

import math


# Load Data
data = np.load('sdss_data.npy').item()
X_train = data['X_train']
X_test = data['X_test']
y_train = data['y_train']
y_test = data['y_test']
feature_names = data['feature_names']
class_labels = data['class_labels'] 

# PART 1

# Feature plot
idx_1 = 0 # select first feature
idx_2 = 1 # select second feature
plt.scatter(X_train[y_train==0, idx_1], X_train[y_train==0, idx_2], s=1,
            color='blue', label=class_labels[0])
plt.scatter(X_train[y_train==1, idx_1], X_train[y_train==1, idx_2], s=1, 
            color='red', label=class_labels[1])

plt.legend(scatterpoints=1)
plt.ylim([-0.5,1.5])
plt.xlim([-0.5,2.5])
plt.xlabel(feature_names[idx_1], fontsize=14)
plt.ylabel(feature_names[idx_2], fontsize=14)

# Correlation matrices to judge dependance of features
print np.corrcoef(X_train[:,0], X_train[:,1])
print np.corrcoef(X_train[:,0], X_train[:,2])
print np.corrcoef(X_train[:,0], X_train[:,3])
print np.corrcoef(X_train[:,1], X_train[:,2])
print np.corrcoef(X_train[:,1], X_train[:,3])
print np.corrcoef(X_train[:,2], X_train[:,3])


# Feature bin plot
idx = 3 # select feature
c = 1 # select class
n, bins, patches = plt.hist(X_train[:,idx][y_train==c], 50, normed=1, color='blue',label=class_labels[0])
mu = np.mean(X_train[:,idx][y_train==c])
sigma = np.std(X_train[:,idx][y_train==c])

# overlay a Gaussian
plt.plot(bins, mlab.normpdf(bins, mu, sigma), color = 'red')


# PART 2

# Fit GaussianNB
gnb = GaussianNB()
gnb.fit(X_train, y_train)
print "Means: "
print gnb.theta_
print "Std devs: "
print gnb.sigma_
print "Class Priors: "
print gnb.class_prior_

# Predict labels

y_pred = gnb.predict(X_test)
print "Accuracy"
print float(np.sum(y_test==y_pred))/len(y_test)
print 'or'
print metrics.classification.accuracy_score(y_test, y_pred)
print "Confusion Matrix" #rows are actual, columns are predicted
print metrics.confusion_matrix(y_test, y_pred)
print "Classification Report"
print metrics.classification_report(y_test, y_pred)

# PART 3

# Gaussian Mixture (Log-Likelihoods)
c_0 = GaussianMixture(n_components=1, covariance_type='diag')
c_0.fit(X_train[y_train == 0])
print "Means: "
print c_0.means_
print "Std devs: "
print c_0.covariances_
print "log likelihoods" # this is P(x|C_0)
print c_0.score_samples(X_test)

c_1 = GaussianMixture(n_components=1, covariance_type='diag')
c_1.fit(X_train[y_train == 1])
print "Means: "
print c_1.means_
print "Std devs: "
print c_1.covariances_
print "log likelihoods" # this is P(x|C_1)
print c_1.score_samples(X_test)

log_likec0 = c_0.score_samples(X_test)
log_likec1 = c_1.score_samples(X_test)

p0 = ((y_train == 0).sum()*1.0)/len(y_train)
log_p0 = math.log(p0)
p1 = (1-p0)
log_p1 = math.log(p1)

y_pred1 = []
for i in range(len(X_test)):
    g0 = log_likec0[i] + log_p0
    g1 = log_likec1[i] + log_p1
    
    if (g0>g1):
        y_pred1.append(0)
        
    else:
        y_pred1.append(1)

print metrics.classification.accuracy_score(y_test, y_pred1)
print "Confusion Matrix" #rows are actual, columns are predicted
print metrics.confusion_matrix(y_test, y_pred1)
print "Classification Report"
print metrics.classification_report(y_test, y_pred1)


# Modifications in complexity of Model

# Split training dataset
X_train, y_train = shuffle(X_train, y_train)
X_train_new = X_train[0:350000, :]
X_validate = X_train[350000:505290, :]
y_train_new = y_train[0:350000]
y_validate = y_train[350000:505290]

c_0 = GaussianMixture(n_components=5, covariance_type='diag')
c_0.fit(X_train_new[y_train_new == 0])
print "Means: "
print c_0.means_
print "Std devs: "
print c_0.covariances_
print "log likelihoods" # this is P(x|C_0)
print c_0.score_samples(X_validate)

c_1 = GaussianMixture(n_components=5, covariance_type='diag')
c_1.fit(X_train_new[y_train_new == 1])
print "Means: "
print c_1.means_
print "Std devs: "
print c_1.covariances_
print "log likelihoods" # this is P(x|C_1)
print c_1.score_samples(X_validate)

log_likec0 = c_0.score_samples(X_validate)
log_likec1 = c_1.score_samples(X_validate)

p0 = ((y_train_new == 0).sum()*1.0)/len(y_train_new)
log_p0 = math.log(p0)
p1 = (1-p0)
log_p1 = math.log(p1)

y_pred1 = []
for i in range(len(X_validate)):
    g0 = log_likec0[i] + log_p0
    g1 = log_likec1[i] + log_p1
    
    if (g0>g1):
        y_pred1.append(0)
        
    else:
        y_pred1.append(1)

print metrics.classification.accuracy_score(y_validate, y_pred1)
print "Confusion Matrix" #rows are actual, columns are predicted
print metrics.confusion_matrix(y_validate, y_pred1)
print "Classification Report"
print metrics.classification_report(y_validate, y_pred1)


# Final Selected model classification

c_0 = GaussianMixture(n_components=5, covariance_type='diag')
c_0.fit(X_train[y_train == 0])
print "Means: "
print c_0.means_
print "Std devs: "
print c_0.covariances_
print "log likelihoods" # this is P(x|C_0)
print c_0.score_samples(X_test)

c_1 = GaussianMixture(n_components=5, covariance_type='diag')
c_1.fit(X_train[y_train == 1])
print "Means: "
print c_1.means_
print "Std devs: "
print c_1.covariances_
print "log likelihoods" # this is P(x|C_1)
print c_1.score_samples(X_test)

log_likec0 = c_0.score_samples(X_test)
log_likec1 = c_1.score_samples(X_test)

p0 = ((y_train == 0).sum()*1.0)/len(y_train)
log_p0 = math.log(p0)
p1 = (1-p0)
log_p1 = math.log(p1)

y_pred1 = []
for i in range(len(X_test)):
    g0 = log_likec0[i] + log_p0
    g1 = log_likec1[i] + log_p1
    
    if (g0>g1):
        y_pred1.append(0)
        
    else:
        y_pred1.append(1)

print metrics.classification.accuracy_score(y_test, y_pred1)
print "Confusion Matrix" #rows are actual, columns are predicted
print metrics.confusion_matrix(y_test, y_pred1)
print "Classification Report"
print metrics.classification_report(y_test, y_pred1)
