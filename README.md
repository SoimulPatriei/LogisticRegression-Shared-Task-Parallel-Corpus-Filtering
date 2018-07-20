# LogisticRegression-Shared-Task-Parallel-Corpus-Filtering

This is the core system (based on "sklearn") that participated in the "Parallel Corpus Filtering Task" http://statmt.org/wmt18/parallel-corpus-filtering.html.<br/>
The whole pipeline is presented in the paper "A hybrid system of rule and machine learning to filter web-crawled parallel corpora". 
The paper is also included here in the file "HybridSystem.pdf"  <br/>
In the folder **Training** there is a manually annotated file with positive and negative examples.<br/>
In the folder **Test** there is a test file that you can classify using the trained model.<br/>
In the folder **Evaluation** there is a the automatic annotated file that we use to build the model run on the 
test corpus provided by the organizers . If you want to use this file instead the manually annotated one, copy the automatic annoated file 
 in the **Training** directory and modify the corresponding
parameters values (Parameters/p-Training.txt for training) and (Parameters/p-Test.txt for test)<br/>

1. Train (The parameters are configured in Parameters/p-Training.txt). *Generates the features for the training file.*
>> python train.py

1. Test (The parameters are configured in Parameters/p-Test.txt). *Fits a Logistic Regression model on the training file, 
generates the features for the test file and classifies the test file*
>> python test.py

1. Evaluation (Go to folder **Evaluation** and evaluate the automatic annotated file we talk about in the paper 
against the mannualy annotated file)
>> python compareTrainingSets.py

