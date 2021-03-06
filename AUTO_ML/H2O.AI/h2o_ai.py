# -*- coding: utf-8 -*-
"""H2O.ai.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nr0jcVkEZrwalV0tCWpuYW-1xcRM_dcc

Install Library
"""

!pip install h2o

"""Import Libraries & Initialize the library"""

import h2o

h2o.init()

from h2o.automl import H2OAutoML

data = h2o.import_file('column_2C_weka.csv')

"""Load data"""

data.head()

data.types

data.describe()

"""Train,Test and Validation Split:-

Train:- 70%

Test:- 15%

Validation :- 15%
"""

data_train,data_test,data_valid = data.split_frame(ratios=[.7, .15])

data_train #check train data

data_test  #check test data

data_valid    #check validation data

"""Predictors and outcome split"""

y = "class"
x = data.columns
x.remove(y)

"""Create model object:-

maximum model= 10

nfold=0 means no cross validation (default=5)

exclude_algorithms = stacking and dL both allowed

for entire seen output use verbosity ='debug'
"""

aml = H2OAutoML(max_models = 10, seed = 10, exclude_algos = ["StackedEnsemble", "DeepLearning"], verbosity="info", nfolds=0)

!nvidia-smi                  #Check GPU

"""Train the model"""

aml.train(x = x, y = y, training_frame = data_train, validation_frame=data_valid)

!nvidia-smi

leaderboard = aml.leaderboard

leaderboard.head()

"""From above leaderboard we found that GBM is working fine
​

# Prediction on test data
"""

data_pred=aml.leader.predict(data_test)

data_pred.head()
## Probabilty of abnormal and normal for head(10) records

"""Check performance metrics"""

aml.leader.model_performance(data_test)

"""Try with all the model rather than leader model only i.e GBM"""

model_ids = list(aml.leaderboard['model_id'].as_data_frame().iloc[:,0])

model_ids

h2o.get_model([i for i in model_ids if "DRF" in i][0])

h2o.get_model([i for i in model_ids if "XGBoost" in i][0])

"""Check Parameters use for xgboost model"""

final = h2o.get_model([i for i in model_ids if "XGBoost" in i][0])

final.params

"""Check best parameters after converting H2O parameter into xgboost parameter"""

final.convert_H2OXGBoostParams_2_XGBoostParams()

final

final_gbm = h2o.get_model([x for x in model_ids if "GBM" in x][0])

"""Confusion matrix"""

final.confusion_matrix()

final.varimp_plot()    #Importance of feature plot

"""Download the final model in mojo"""

aml.leader.download_mojo(path = "./")