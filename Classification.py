#!/usr/bin/env python

"""This Class contains the methods for classifing """
__author__      = "Eduard Barbu"





import sys
import re
import logging
import sklearn as sk
import numpy as np
import csv
import codecs
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler
import Parameters
from sklearn.linear_model import LogisticRegression





class Classification:
   """Classification of the test set"""
   
   
   def __init__(self,pFile):
      self.pDict=Parameters.readParameters(pFile)
      
   
   def decideClass(self,listPred):
      """Decide the class based on probability scores """
      
      threshold=float(self.pDict["threshold"])
      classRes=int(self.pDict["defaultClass"])
      if listPred[1-classRes]>threshold :
         classRes=1-classRes
      return classRes
     
   
   def loadTrainingDataSet (self) :
        """It reads the training dataSet from the CSV file."""
        
        fs = codecs.open(self.pDict["trainingFeatureFile"], "r", "utf-8")
        reader = csv.reader(fs, delimiter=',')
        
        #Load feature names and remove the ones you do not want
        row = reader.next()
        self.feature_training_names = list(row)
        
        #Load dataset, and target classes
        X, y = [], []
        for row in reader:  
            y.append(row.pop())
            floatRowList=[float(i) for i in row]
            X.append(floatRowList)
        
        
        X = np.array(X)    
        y = np.array(y)
        
        
        
        
        return X,y
   
   
   def scale(self,X):
        """Scale the values using apropriate scaling"""
        
        scaler = preprocessing.StandardScaler().fit(X)
        X_scaled=scaler.transform(X)
        return X_scaled
        
   
   def getToClassify (self,nToClassify) :
    """A generator that returns k items to classify """
    
    fs = codecs.open(self.pDict["testFeatureFile"], "r", "utf-8")
    reader = csv.reader(fs, delimiter=',')
    row = reader.next()
    X_test= []
    indexRow=0
    for row in reader:
        indexRow+=1
        floatRowList=[float(i) for i in row]
        X_test.append(floatRowList)
        if indexRow==nToClassify :
            X_test = np.array(X_test)
            yield X_test
            indexRow=0
            X_test=[]
    fs.close()
    if X_test :
        yield X_test
   
   
   def writeResults (self,predicted,predictedProbabilities) :
    """Write the classification results """
    
    fo = codecs.open(self.pDict["fResults"], "a", "utf-8")
    for i in range (0, len(predicted)) :
        sir="\t".join([str(predicted[i]),str(round(predictedProbabilities[i][0],3)),
                       str(round(predictedProbabilities[i][1],3))])
        fo.write(sir+"\n")
   
   
    fo.close()
   
   
   def classify(self) :
    """Perform the classification"""
    
    nToClassify=100000
    X_train,y_train=self.loadTrainingDataSet()
    clf=LogisticRegression()
   
    
    logger = logging.getLogger('Classification::classify')
    logger.info ("Empty file =>"+self.pDict["fResults"])
    fo = codecs.open(self.pDict["fResults"], "w", "utf-8")
    fo.close()
    
    logger.info ("Classify in loop "+str(nToClassify)+" Items")
    index=0
    for X_test in self.getToClassify(nToClassify) :
        index+=1
        logger.info ("Index_"+str(index))
        
        #concatanate "train set" and "test set" and scale them
        Z=np.concatenate((X_train, X_test), axis=0)
        Z=self.scale(Z)
        X_train_scaled=Z[0:len(X_train)]
        X_test_scaled= Z[len(X_train):len(Z)]
        
        #Predict
        clf.fit(X_train_scaled,y_train)
        predicted = clf.predict(X_test_scaled)
        predictedProbabilities=clf.predict_proba(X_test_scaled)
        
        logger.info ("Write Results")
        self.writeResults (predicted,predictedProbabilities) 
    logger.info ("I am done")    
   
   
    
   
   
        
     
def main():
    pass
    
   
    
if __name__ == '__main__':
  main()
