#!/usr/bin/env python

"""Compute the number of times the rules fire
   and extract a number of examples for each rule"""
__author__      = "Eduard Barbu"

import sys
import codecs

def count (fRules,fOutput,number) :
    """ """
    
    countDict={}
    examplesDict={}
    fi= codecs.open(fRules, "r", "utf-8")
    fo= codecs.open(fOutput, "w", "utf-8")
    for line in fi :
        line=line.rstrip()
        components=line.split("\t")
        rule=components[0]
        
        
        #add the count rules
        countDict.setdefault(rule, 0)
        countDict[rule]+=1
        
        #add the example
        examplesDict.setdefault(rule, {})
        if (len(examplesDict[rule].keys()) <=number) :
            del components[0]
            rest="\t".join(components)
            examplesDict[rule][rest]=0
        
    fi.close()
    
    for rule in countDict :
        fo.write(rule+"\t"+str(countDict[rule])+"\n")
    
    for rule in examplesDict :
        fo.write("========="+rule+"================"+"\n")
        for example in examplesDict[rule] :
            fo.write(example+"\n")
        
    
    fo.close()
    


def main():
    
    fRules="outputRules.txt"
    fOutput="rules.example.txt"
    number=200
    
    count (fRules,fOutput,number)
    print ("Results in =>",fOutput)
    
    
    
    
    
    
    
   
   
    

if __name__ == '__main__':
  main()