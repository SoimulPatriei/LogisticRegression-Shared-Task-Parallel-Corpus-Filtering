#!/usr/bin/env python

"""Generate the test features, load the model and classify ... """
__author__      = "Eduard Barbu"



import sys
from GetFeatures import *
import Parameters
from Classification import *


def initLogger(loggingFile):
    """Init the logger for the console and logging file"""
    
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename=loggingFile,
                        filemode='w')
    
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    # tell the handler to use this format
    
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)    


def generateTestFeatures (pTestFile) :
    """Generate the training file"""
    
    gf=GetFeatures(pTestFile)
    gf.generateTestFeatures(pTestFile)



def classify(pTestFile) :
    """Perform the classification"""
    
    cl=Classification(pTestFile)
    cl.classify()


def main():
    pTestFile="Parameters/p-Test.txt"
    loggingFile="classification.log"
    initLogger(loggingFile)
    #generateTestFeatures (pTestFile)
    
    classify(pTestFile)
    
   
   
    

if __name__ == '__main__':
  main()