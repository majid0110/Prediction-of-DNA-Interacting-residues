
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

train_data = 'Input file/Training_dataset.csv'
test_data = 'Input file/New_Validation_Dataset.csv'

#Taking the path of traning and testing data

# train_data = input('Enter the path of traning dataset  :  ')
# test_data = input('Enter the path of testing dataset  :  ')

## This function takes the path and segregates both the labels and the string

def getData(path):
  sequence = []
  lable = []

  with open(train_data) as f:
    for line in f:
      text_file = line.split(",")
      if text_file[0] == 'Label':
        continue
      lable.append(text_file[0])
      sequence.append(text_file[1][:-1])

  return sequence, lable

## Segregates both the labels and the string

x_train, y_train = getData(train_data)

print('There are',len(y_train),'number of DNA Patterns available.')

## Dipeptide Feature extraction, in this it has 780 features. Two character combination with amino acid sequence

aminoacid_sequence = ['A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','W','Y']

dipeptide_seq = []

for charone in aminoacid_sequence:
    for chartwo in aminoacid_sequence:
        char_to_add = charone+chartwo
        char_to_addback = chartwo + charone    
        dipeptide_seq.append(char_to_add)
        if char_to_add == char_to_addback:
            continue
        dipeptide_seq.append(char_to_addback)

## Here for each sequence, an 780 featured dipeptide feature is extracted using the dipeptide calculations
def get_dipeptite_dictionary(str):
    
    size = len(str)
    
    i = 0
    eachseq_list = []
    while( i < size - 1 ):
        add_seq = str[i] + str[i+1]
        eachseq_list.append(add_seq)
        i += 1
    
    i = 0
    while( i < size - 2 ):
        add_seq = str[i] + str[i+2]
        eachseq_list.append(add_seq)
        i += 1 
        
    getdict = {}
    
    for item in eachseq_list:
        if getdict.get(item) == None:
            getdict[item] = 1
        else:
            temp = getdict[item]
            temp += 1
            getdict[item] = temp
    
    new_dict = {}
    for item in getdict:
        value = getdict[item]
        value = value/(len(str))
        new_dict[item] = value
    
    return new_dict

## These two fucntions helps us to create an vector for each sequence

def getlist_of_dictionary(x_train):
    list_dictionary = []
    
    for each in x_train:
        dic = get_dipeptite_dictionary(each)
        list_dictionary.append(dic)
        
    return list_dictionary

def getvector(vector_dictionary):
    final_vector = []
    
    for dic in vector_dictionary:
        vec = [0.0] * 780
        for item in dic:
            for seq in dipeptide_seq:
                if seq == item:
                    index = dipeptide_seq.index(seq)
                    vec[index] = dic[item]
                    
        final_vector.append(vec)            
    
    return final_vector

#Hepls to extract vectors for traning the model
training_vector_dict = getlist_of_dictionary(x_train)

X_Train = getvector(training_vector_dict)

## The data is converted into numpy array.

x = np.array(X_Train)
y = np.array(y_train)



## Split the data into train and validation @ 70% and 30% respectivly

x_train, x_val, y_train, y_val = train_test_split(x,y, test_size=0.3, random_state=42)

print('Splited the data into train and validation @ 70% and 30% respectivly')

print('Shape of Train data : ',x_train.shape)
print('Shape of Validation data : ',x_val.shape)

"""Test data"""

## Same extracting dipeptide vector from test data

ID = []
test_sequence = []

with open(test_data) as f:
    for line in f:
        after_split = line.split(",")
        if after_split[0] == 'ID':
            continue;
        ID.append(after_split[0])
        test_sequence.append(after_split[1][:-1])

## Same extracting dipeptide vector from test data

testing_vector_dict = getlist_of_dictionary(test_sequence)
x_test = getvector(testing_vector_dict)
x_test = np.array(x_test)

print('Shape of test data : ',x_test.shape)

"""Normalization"""

#scaling of the data using min-max scaler
# from sklearn.preprocessing import MinMaxScaler

# sc = MinMaxScaler()
# X_train = sc.fit_transform(X_train)
# X_test = sc.transform(X_test)

"""Feature Reduction"""

# # Features are reduced from 318 to lesser features using Principal Component Analysis (PCA)
# from sklearn.decomposition import PCA

# # Reducing the features to 125
# pca = PCA(n_components=125)

# x_train_pca = pca.fit_transform(x_train)
# x_test_pca = pca.transform(X_test)

"""Applying Models"""

## Import libraries of all the model libraries

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier
import xgboost as xgb
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.neighbors import KNeighborsClassifier
import numpy as np

# Applying RepeatedStratifiedKFold
cv_method = RepeatedStratifiedKFold(n_splits=5, 
                                    n_repeats=3, 
                                    random_state=999)

# It takes filename and predicted model

def writeintopredfile(filename, model_pre):
  
  f = open(filename,'w')
  s = "ID,Label\n"
  c = 0
  for i in model_pre:
    s = s+ID[c]+","+i.__str__()+"\n"
    c += 1

  f.write(s)
  f.close()

print('')

print('Choose the model : ')
print('1. Random Forest')
print('2. Multi Layer Perceptron')
print('3. Naive Bayes')
print('4. XGBoost')
print('5. KNN')

print('')

k = int(input('Enter a number to choose the model : '))

if k == 1 :

  #Parameter tuning with gridsearchcv
  param_grid = {
      'bootstrap': [True],
      'max_depth': [80, 90, 100],
      'max_features': [2, 3],
      'n_estimators': [300,400]
  }

  rf = RandomForestClassifier()
  grid_search = GridSearchCV(estimator = rf, param_grid = param_grid, 
                            cv = 3, n_jobs = -1, verbose = 100)
  # Model is being trained with splitted data
  grid_search.fit(x_train, y_train)
   # Out of the given parameters the best parameters are printed.
  print('Best parameters are : ',grid_search.best_params_)
  print('Validation accuracy : ',accuracy_score(y_val,grid_search.predict(x_val)))
  ans_RF = grid_search.predict(x_test)
  print('The prediction on test data is ',ans_RF)
  writeintopredfile('RF_86.csv',ans_RF)

elif k == 2 :

  # Number of iterations has been set as 100. This I have tried with different max iteration values.
  mlp_gs = MLPClassifier(max_iter=100)
  #Parameter tuning with gridsearchcv
  parameter_space = {
      'hidden_layer_sizes': [(10,30,10)],
      'activation': ['tanh'],
      'solver': ['adam'],
      'alpha': [0.05],
      'learning_rate': ['constant'],
  }
  # Cross Validation is set as 10.
  clf = GridSearchCV(mlp_gs, parameter_space, n_jobs=-1, verbose = 50 ,cv=10)
  # Model is being trained with splitted data
  clf.fit(x_train, y_train)
  # Out of the given parameters the best parameters are printed.
  print('Best parameters found:\n', clf.best_params_)
  print(' Validation score is : ',accuracy_score(y_val,clf.predict(x_val)))
  # Prediction is done on test data 
  y_pred = clf.predict(x_test)
  print('The prediction on test data is ',y_pred)
  writeintopredfile('MLP_67.csv',y_pred)

elif k == 3 :

  from sklearn.naive_bayes import GaussianNB

  np.random.seed(999)

  nb_classifier = GaussianNB()

  params_NB = {'var_smoothing': np.logspace(0,-9, num=100)}

  gs_NB = GridSearchCV(estimator=nb_classifier, 
                      param_grid=params_NB, 
                      cv=cv_method,
                      verbose=100, 
                      scoring='accuracy')
  
  gs_NB.fit(x_train, y_train);
  print('Best parameters are : ',gs_NB.best_params_)
  print('Best score are : ',gs_NB.best_score_)

  ans_NB= gs_NB.predict(x_test)
  print('The prediction on test data is ',ans_NB)
  writeintopredfile('NB_65.csv',ans_NB)

elif k == 4:

  validationPredictions=[]
  trainingPredictions=[]
  xgbClassifiersUsed=[]

  xgboostClassifier= xgb.XGBClassifier(booster='gbtree',n_estimators=100,max_depth=6)
  xgboostClassifier.fit(x_train,y_train)

  xgbClassifiersUsed.append(xgboostClassifier)

  YBoostTrain = xgboostClassifier.predict(x_train)
  YBoostValidate = xgboostClassifier.predict(x_val)

  print("\nXGBoost Forest :-")
  print("Training Set - AUCCURACY : ",accuracy_score(y_train,YBoostTrain))
  print("Validation Set - AUCCURACY : ",accuracy_score(y_val,YBoostValidate))

  ans_XGB = xgboostClassifier.predict(x_test)

  print('The prediction on test data is ',ans_XGB)

  writeintopredfile('XGB_71.csv',ans_XGB)

elif k == 5 :


  params_KNN = {'n_neighbors': [4], 
                'p': [1]}


  gs_KNN = GridSearchCV(estimator=KNeighborsClassifier(), 
                        param_grid=params_KNN, 
                        cv=cv_method,
                        verbose=100,  # verbose: the higher, the more messages
                        scoring='accuracy', 
                        return_train_score=True)

  gs_KNN.fit(x_train, y_train);

  gs_KNN.best_params_

  accuracy_score(y_val,gs_KNN.predict(x_val))

  ans_KNN = gs_KNN.predict(x_test)

  writeintopredfile('KNN_65.csv',ans_NB)

else:
  print('You have entered wrong details')

















