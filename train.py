#!/usr/bin/env python


"""Train the model ... """
__author__      = "Eduard Barbu"



import sys
from GetFeatures import *
import Parameters




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


def generateTrainingFile (pTrainingFile) :
    """Generate the training file"""
    
    gf=GetFeatures(pTrainingFile)
    gf.generateTrainingFeatures()



def main():
    pTrainingFile="Parameters/p-Training.txt"
    loggingFile="train.log"
    initLogger(loggingFile)
    generateTrainingFile (pTrainingFile)
   
    

if __name__ == '__main__':
  main()
  