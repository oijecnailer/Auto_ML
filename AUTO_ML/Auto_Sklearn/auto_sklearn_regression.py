# -*- coding: utf-8 -*-
"""Auto_Sklearn_regression.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QNSGoSa-P6y7qtIVvZDSx2YaXZxu9Eaw
"""

!sudo apt-get install build-essential swig

!curl https://raw.githubusercontent.com/automl/auto-sklearn/master/requirements.txt | xargs -n 1 -L 1 pip install

!pip install auto-sklearn

import sklearn.model_selection
import sklearn.datasets
import sklearn.metrics

import autosklearn.regression

X, y = sklearn.datasets.load_boston(return_X_y=True)
feature_types = (['numerical'] * 3) + ['categorical'] + (['numerical'] * 9)
X_train, X_test, y_train, y_test = \
    sklearn.model_selection.train_test_split(X, y, random_state=1)

automl = autosklearn.regression.AutoSklearnRegressor(
    time_left_for_this_task=120,
    per_run_time_limit=30,
    tmp_folder='/tmp/autosklearn_regression_example_tmp',
    output_folder='/tmp/autosklearn_regression_example_out',
)
automl.fit(X_train, y_train, dataset_name='boston',
           feat_type=feature_types)

"""Print the final ensemble constructed by auto-sklearn"""

print(automl.show_models())

"""Get the Score of the final ensemble"""

predictions = automl.predict(X_test)
print("R2 score:", sklearn.metrics.r2_score(y_test, predictions))