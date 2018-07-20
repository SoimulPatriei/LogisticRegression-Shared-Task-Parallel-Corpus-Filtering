#!/usr/bin/env python


"""Compute the Features for Training or Test set."""
__author__      = "Eduard Barbu"

import sys
import codecs
import collections
import re
from Features import *
import logging
import Parameters


class GetFeatures:
   """Compute the Features for Training or Test set."""
   

   def getOrder(self,category=0) :
      """Read the order of the features"""
      
      fi = codecs.open(self.pDict["fOrder"], "r", "utf-8")
      featureOrderList=[]
      for line in fi :
         line=line.rstrip()
         if line :
            featureOrderList.append(line)
      fi.close()
      
      if category :
         featureOrderList.append("category")
      
      return featureOrderList
   
   
   
   def writeFeatureNames (self,fOutput,featureOrderList) :
      
      fs = codecs.open(fOutput, "a", "utf-8")
         
      #------Write the first row containing feature names--------
      featureString=""
      for feature in featureOrderList :
        featureString+=feature+","
      featureString=featureString.rstrip(',')+"\n"
      
      fs.write(featureString)   
      fs.close()
      
   def writeFeatureFile (self,fOutput,featuresDict,featureOrderList) :
    """Print the file in the CSV format to be handeled by scikit-learn"""

    fs = codecs.open(fOutput, "a", "utf-8")
    #write the rest of the values
   
    featureValueString=""
    for featureName in featureOrderList :
      featureValueString+=str(featuresDict[featureName])+","
    featureValueString=featureValueString.rstrip(',')+"\n"
    fs.write(featureValueString)
    fs.close()  
   
   def cleanSegment (self,segment) :
    """It cleans the segment from trailing spaces and the sign %@% that means "EOL"."""
    
    segment=re.sub("^\s+","",segment)
    segment=re.sub("\s+$","",segment)
    
    return segment
    
   def printFeatures (self,featuresDict) :
      """Print Features to see if they were computed well"""
      
      for key in featuresDict :
            print key+"=>"+str(featuresDict[key])
   
   def generateFeatures (self,line) :
    """It generates the features for a bisegment"""
    
    featuresDict={}
    components=line.split("\t")
    sourceSegment=components[0]
    targetSegment=components[1]
    saScore=components[2]
    perplexitySource=components[3]
    perplexityTarget=components[4]
    
    category=""
    if len(components) ==6 :
      category=components[5]
      featuresDict["category"]=category
      
    sourceSegment=self.cleanSegment (sourceSegment)
    targetSegment=self.cleanSegment(targetSegment)
    features=Features(sourceSegment,targetSegment,self.pDict["fileRe"])      
    nWordsSource,nWordsTarget=features.getNWords()
        
  
   
    #--------Features used in ML------------------
   
    #Sentence alignment score is already provided in the file
    featuresDict["saScore"]=saScore
   
    #The Ken-LM language model score (perplexity) for source and target segment
    featuresDict["perplexitySource"]=perplexitySource
    featuresDict["perplexityTarget"]=perplexityTarget
   
    #Gale-Church score
    featuresDict["cgscore"]=features.getCGSore()
    featuresDict["same"]=features.isEqual ()
   
    #Capital Letters
    featuresDict["hassourcecl"],featuresDict["hastargetcl"]=features.haveCL()
    featuresDict["caplettersworddif"]=features.difWordsCapitalLetters ()
    featuresDict["onlycaplettersdif"]=features.difWholeWordsCapitalLetters ()
   
    #URL and Similarity
    featuresDict["hassourceurl"],featuresDict["hastargeturl"]=features.haveItem("urlRe")
    featuresDict["urlsim"]=features.getItemSimilarity("urlRe")
   
    #TAG and Similarity
    featuresDict["hassourcetag"],featuresDict["hastargettag"]=features.haveItem("tagRe")
    featuresDict["tagsim"]=features.getItemSimilarity("tagRe")
   
    #EMAIL and Similarity
    featuresDict["hassourceemail"],featuresDict["hastargetemail"]=features.haveItem("emailRe")
    featuresDict["emailsim"]=features.getItemSimilarity("emailRe")
   
    #NUMBER and Similarity
    featuresDict["hassourcenumber"],featuresDict["hastargetnumber"]=features.haveItem("numberRe")
    featuresDict["numbersim"]=features.getNumberSimilarity("numberRe")
   
    #PUNCTUATION and Similarity
    featuresDict["hassourcepunctuation"],featuresDict["hastargetpunctuation"]=features.havePunctuation()
    featuresDict["punctsim"]=features.getPunctuationSimilarity()
   
    #Name Entity Detection and Similarity
    featuresDict["hassourcenameentity"],featuresDict["hastargetnameentity"]=features.haveNameEntity()
    featuresDict["nersimilarity"]=features.getNameEntitiesSimilarity()
   
    return featuresDict
   
   def generateTestFeatures(self,pTest):
    """Generate Test Features"""
    

    #clean the test feature file and write the features
    fo = codecs.open(self.pDict["testFeatureFile"], "w", "utf-8")
    fo.close()
    featureOrderList=self.getOrder()
    self.writeFeatureNames(self.pDict["testFeatureFile"],featureOrderList)
    
    
    logger = logging.getLogger('GetFeatures::generateTestFeatures')
    logger.info ("Generate Test Features ")
    fs = codecs.open(self.pDict["fileTest"], "r", "utf-8")
    for line in fs:
        line=line.rstrip()
        featuresDict=self.generateFeatures(line)
        self.writeFeatureFile (self.pDict["testFeatureFile"],featuresDict,featureOrderList)
    
    logger.info ("Test Features File in => "+self.pDict["testFeatureFile"])
    
    
    
   def generateTrainingFeatures(self):
    """Generate Training Features"""
    
    fo = codecs.open(self.pDict["trainingFeatureFile"], "w", "utf-8")
    fo.close()
    
    #----Generate the features adding the category------
    featureOrderList=self.getOrder(1)
    self.writeFeatureNames(self.pDict["trainingFeatureFile"],featureOrderList)
    
    logger = logging.getLogger('GetFeatures::generateTrainingFeatures')
    logger.info( "Generate The Features ")
    fs = codecs.open(self.pDict["fCategory"], "r", "utf-8")
    for line in fs:
        line=line.rstrip()
        featuresDict=self.generateFeatures(line)
        self.writeFeatureFile (self.pDict["trainingFeatureFile"],featuresDict,featureOrderList)
    
    logger.info ("Training Features File in => "+self.pDict["trainingFeatureFile"])
    
   def __init__(self,pFile):
    self.pDict=Parameters.readParameters(pFile)
     
   
   