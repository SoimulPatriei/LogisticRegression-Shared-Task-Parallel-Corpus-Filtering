#!/usr/bin/env python

"""Compare the automatic with the manualy made training set"""
__author__      = "Eduard Barbu"


import sys
import re
import codecs
import math
from sklearn import metrics

def roundA(mArray):
    """Round the results of an array"""
    
    rArray=[]
    for item in mArray:
        rItem=round (item,2)
        rArray.append(rItem)
    return rArray


def mpBinary(y_true,y_pred,fStat):
        
    """Measure Performance for the Binary Task ... """
    
    
    fo = codecs.open(fStat, "w", "utf-8")
    fo.write ("Confusion matrix\n")
    cm=metrics.confusion_matrix(y_true,y_pred,[1,0])
    fo.write ( str(cm)+"\n")
    fo.write("--------------------------------------------------\n")
    
    
    arrayP=roundA(metrics.precision_score(y_true, y_pred,[1,0], average=None))
    arrayR=roundA(metrics.recall_score(y_true,y_pred,[1,0], average=None))
    arrayF1=roundA(metrics.f1_score(y_true,y_pred,[1,0], average=None))
    
    fo.write("Per class measures\n")
    fo.write("Precision :"+str(arrayP)+"\n")
    fo.write("Recall :"+str(arrayR)+"\n")
    fo.write("F1 Score :"+str(arrayF1)+"\n")
    fo.write("------------------------------------------------\n")
    
    ba=(arrayR[0]+arrayR[1])/2
    fo.write("Balanced Accuracy:"+str(ba)+"\n")
    fo.close()
    
    
    

    
def readScores (fInput) :
    """Read the scores from the true file or from the predicted file"""

    fi = codecs.open(fInput, "r", "utf-8")
    
    y=[]
    for line in fi :
        line=line.rstrip()
        components=line.split("\t")
        y.append(int(components[-1]))
    fi.close()
    return y
    
    
    

def main():
    
    
    fAutomatic="automaticTrainingSet.txt"
    fManual="manualTrainingSet.txt"
    
    y_true=readScores (fManual)
    y_pred=readScores (fAutomatic)
    
    fStat="stat-AutomaticManual.txt"
    mpBinary(y_true,y_pred,fStat)
    
    print ("Results in =>" +fStat)
    
    
    
    
   
   
    

if __name__ == '__main__':
  main()    