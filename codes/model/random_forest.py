import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, KFold, cross_val_predict
from sklearn.metrics import confusion_matrix, cohen_kappa_score, classification_report

from model import selected_attributes as sa
from model import conf_mat_plot
from model import learning_curve_plot

import warnings

warnings.filterwarnings('ignore')

match_format = 'combined'
match_data = sa.get_selected_attributes(match_format)

wc_value = []
match_data.apply(lambda x: wc_value.append('yes') if x['wc_match'] == True else wc_value.append('no'), axis=1)
match_data.loc[:, 'wc_match'] = wc_value

day_night_value = []
match_data.apply(lambda x: day_night_value.append('yes') if x['day_and_night'] == True else day_night_value.append('no'), axis=1)
match_data.loc[:, 'day_and_night'] = wc_value


columns_to_encode = ['win_team', 'location', 'day_and_night', 'wc_match', 'rained',
                     'team_bat_first', 'team_bat_second', 'format']
dynamic_attributes = [x for x in match_data.columns if x not in columns_to_encode]

df_index = [x for x in range(match_data.shape[0])]
match_data.loc[:, 'row_no'] = df_index
match_data.set_index(keys='row_no', inplace=True)

label = ['win_team']

label_encoder = LabelEncoder()
label_frame = match_data.loc[:, label]
label_frame.loc[:, 'row_no'] = df_index
label_frame.set_index(keys='row_no', inplace=True)

label_frame = label_frame.apply(label_encoder.fit_transform)

dummy_encode = match_data.loc[:, [column for column in columns_to_encode if column not in label]]
dummy_encode.loc[:, 'row_no'] = df_index
dummy_encode.set_index(keys='row_no', inplace=True)
dummy_encode = pd.get_dummies(dummy_encode, drop_first=True)

predictor_frame = pd.concat([dummy_encode, match_data[dynamic_attributes]], axis=1)

######################## Random forest - classifier ############################

# create k-folds
k_fold = KFold(n_splits=10, shuffle=False, random_state=0)

# # get the null accuracy - using 90:10 split since 10 folds are used
pred_train, pred_test, label_train, label_test = train_test_split(predictor_frame.values, label_frame.values,
                                                                  test_size=0.10, random_state=0)
null_accuracy = max(label_test.mean(), 1 - label_test.mean()) * 100
print('Null accuracy: ', null_accuracy)

# create the classifier
# default - n_estimators = 10, n_jobs = 1, criterion='gini', max_features='auto', min_samples_leaf=1
clf = RandomForestClassifier(n_estimators=85, n_jobs=1, criterion='gini', max_features=0.50, min_samples_leaf=10)

###### Performance Metrics ###########

accuracy_list = []
variance_list = []
for x in range(0, 10):
    # get model accuracy and 95% confidence interval(+/-)
    scores = cross_val_score(clf, np.array(predictor_frame.values), np.array(label_frame.values), cv=k_fold,
                             scoring='accuracy')
    score_mean = scores.mean()
    accuracy_list.append(score_mean)
    variance_list.append(scores.std() * 2)

# print model accuracy and 95% confidence interval(+/-)
print("Accuracy: %0.4f (+/- %0.2f)" % (max(accuracy_list) * 100, np.array(variance_list).std() * 2))


# get predicted labels
label_predicted = cross_val_predict(clf, predictor_frame.values, label_frame.values, cv=k_fold)

# get the confusion matrix
conf_mat = confusion_matrix(label_frame.values,label_predicted)
print(conf_mat)

# precision, recall, f-score, support(frequency for each class)
report = classification_report(label_frame.values, label_predicted, target_names=match_data[label].values)
print(report)

# ROC - AUC
auc = cross_val_score(clf, predictor_frame.values, label_frame.values, cv=k_fold, scoring='roc_auc')
print("AUC: %0.4f (+/- %0.2f)" % (auc.mean(), auc.std() * 2))

# get Cohen's Kappa k
kappa = cohen_kappa_score(label_frame.values, label_predicted)
print('kappa: ', kappa)