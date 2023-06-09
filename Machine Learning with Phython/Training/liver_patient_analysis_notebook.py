# -*- coding: utf-8 -*-
"""Liver Patient Analysis Notebook.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nZ84cEvenyXKQqucwjZ97dCl81ggFN9X

# 👉🏻 👉🏻 👉🏻 👉🏻 LIVER PATIENT ANALYSIS & PREDICTION 👈🏻 👈🏻 👈🏻 👈🏻

1) Data Analysis: 
 This is in general looking at the data to figure out whats going on. Inspect the data: Check whether there is any missing data, irrelevant data and do a cleanup.

2) Data Visualization:

3) Feature selection.

4) Search for any trends, relations & correlations.

5) Draw an inference and predict whether the patient can be identified to be having liver disease or not
"""

# Commented out IPython magic to ensure Python compatibility.
#Import all required libraries for reading data, analysing and visualizing data

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline
from sklearn.preprocessing import LabelEncoder

"""# Data Analysis"""

#Read the training & test data
# liver_df = pd.read_csv('liver_patient.csv')
import types
import pandas as pd
from botocore.client import Config
import ibm_boto3

def __iter__(self): return 0

# @hidden_cell
# The following code accesses a file in your IBM Cloud Object Storage. It includes your credentials.
# You might want to remove those credentials before you share your notebook.
client_4d3b180310594496b884c11ba3138863 = ibm_boto3.client(service_name='s3',
    ibm_api_key_id='dukeFNtwWPtt4DcrXh6HLxDSUIEYxGUMG-xsnXmY5EDW',
    ibm_auth_endpoint="https://iam.eu-gb.bluemix.net/oidc/token",
    config=Config(signature_version='oauth'),
    endpoint_url='https://s3.eu-geo.objectstorage.service.networklayer.com')

body = client_4d3b180310594496b884c11ba3138863.get_object(Bucket='socialnetworkads-donotdelete-pr-hqu2bvcls9ycig',Key='liver_patient.csv')['Body']
# add missing __iter__ method, so pandas accepts body as file-like object
if not hasattr(body, "__iter__"): body.__iter__ = types.MethodType( __iter__, body )

liver_df= pd.read_csv(body)
liver_df.head()

#Top 5 rows of the dataset

liver_df.head()

# To get a concise summary of the dataframe

liver_df.info()

"""Here are the observations from the dataset:

- Only gender is non-numeric veriable. All others are numeric.

- There are 10 features and 1 output - dataset. Value 1 indicates that the patient has liver disease and 0 indicates the patient does not have liver disease.
"""

# Statistical information about NUMERICAL columns in the dataset

liver_df.describe(include='all')

"""- We can see that there are missing values for Albumin_and_Globulin_Ratio as only 579 entries have valid values indicating 4 missing values.
- Gender has only 2 values - Male/Female
"""

# Features of the dataset (Labels)

liver_df.columns

# Check for any null values

liver_df.isnull().sum()

"""- The only data that is null is the Albumin_and_Globulin_Ratio - Only 4 rows are null. Lets see whether this is an important feature

# Data Visualization
"""

# Frequency of patients diagnosed and not diagnoised with liver disease

sns.countplot(data=liver_df, x = 'Dataset', label='Count')

LD, NLD = liver_df['Dataset'].value_counts()
print('Number of patients diagnosed with liver disease: ',LD)
print('Number of patients not diagnosed with liver disease: ',NLD)

# Frequency of patients based on their gender

sns.countplot(data=liver_df, x = 'Gender', label='Count')

M, F = liver_df['Gender'].value_counts()
print('Number of patients that are male: ',M)
print('Number of patients that are female: ',F)

sns.factorplot(x="Age", y="Gender", hue="Dataset", data=liver_df);

"""- Age seems to be a factor for liver disease for both male and female genders"""

liver_df[['Gender', 'Dataset','Age']].groupby(['Dataset','Gender'], as_index=False).count().sort_values(by='Dataset', ascending=False)

liver_df[['Gender', 'Dataset','Age']].groupby(['Dataset','Gender'], as_index=False).mean().sort_values(by='Dataset', ascending=False)

g = sns.FacetGrid(liver_df, col="Dataset", row="Gender", margin_titles=True)
g.map(plt.hist, "Age", color="red")
plt.subplots_adjust(top=0.9)
g.fig.suptitle('Disease by Gender and Age');

g = sns.FacetGrid(liver_df, col="Gender", row="Dataset", margin_titles=True)
g.map(plt.scatter,"Direct_Bilirubin", "Total_Bilirubin", edgecolor="w")
plt.subplots_adjust(top=0.9)

"""- There seems to be direct relationship between Total_Bilirubin and Direct_Bilirubin. We have the possibility of removing one of this feature."""

sns.jointplot("Total_Bilirubin", "Direct_Bilirubin", data=liver_df, kind="reg")

g = sns.FacetGrid(liver_df, col="Gender", row="Dataset", margin_titles=True)
g.map(plt.scatter,"Aspartate_Aminotransferase", "Alamine_Aminotransferase",  edgecolor="w")
plt.subplots_adjust(top=0.9)

"""- There is linear relationship between Aspartate_Aminotransferase and Alamine_Aminotransferase and the gender. We have the possibility of removing one of this feature."""

sns.jointplot("Aspartate_Aminotransferase", "Alamine_Aminotransferase", data=liver_df, kind="reg")

g = sns.FacetGrid(liver_df, col="Gender", row="Dataset", margin_titles=True)
g.map(plt.scatter,"Alkaline_Phosphotase", "Alamine_Aminotransferase",  edgecolor="w")
plt.subplots_adjust(top=0.9)

sns.jointplot("Alkaline_Phosphotase", "Alamine_Aminotransferase", data=liver_df, kind="reg")

"""- No linear correlation between Alkaline_Phosphotase and Alamine_Aminotransferase"""

g = sns.FacetGrid(liver_df, col="Gender", row="Dataset", margin_titles=True)
g.map(plt.scatter,"Total_Protiens", "Albumin",  edgecolor="w")
plt.subplots_adjust(top=0.9)

"""- There is linear relationship between Total_Protiens and Albumin and the gender. We have the possibility of removing one of this feature."""

sns.jointplot("Total_Protiens", "Albumin", data=liver_df, kind="reg")

g = sns.FacetGrid(liver_df, col="Gender", row="Dataset", margin_titles=True)
g.map(plt.scatter,"Albumin", "Albumin_and_Globulin_Ratio",  edgecolor="w")
plt.subplots_adjust(top=0.9)

"""- There is linear relationship between Albumin_and_Globulin_Ratio and Albumin. We have the possibility of removing one of this feature."""

sns.jointplot("Albumin_and_Globulin_Ratio", "Albumin", data=liver_df, kind="reg")

g = sns.FacetGrid(liver_df, col="Gender", row="Dataset", margin_titles=True)
g.map(plt.scatter,"Albumin_and_Globulin_Ratio", "Total_Protiens",  edgecolor="w")
plt.subplots_adjust(top=0.9)

"""### Observation:

From the above jointplots and scatterplots, we find direct relationship between the following features:
* Direct_Bilirubin & Total_Bilirubin
* Aspartate_Aminotransferase & Alamine_Aminotransferase
* Total_Protiens & Albumin
* Albumin_and_Globulin_Ratio & Albumin

Hence, we can very well find that we can omit one of the features. I'm going to keep the follwing features:
* Total_Bilirubin
* Alamine_Aminotransferase
* Total_Protiens
* Albumin_and_Globulin_Ratio
* Albumin
"""

liver_df.head(3)

"""- Convert categorical variable "Gender" to indicator variables"""

pd.get_dummies(liver_df['Gender'], prefix = 'Gender').head()

liver_df = pd.concat([liver_df,pd.get_dummies(liver_df['Gender'], prefix = 'Gender')], axis=1)

liver_df.head()

liver_df.describe()

"""- Finding the null values in 'Albumin_and_Globulin_Ratio'"""

liver_df[liver_df['Albumin_and_Globulin_Ratio'].isnull()]

liver_df["Albumin_and_Globulin_Ratio"] = liver_df.Albumin_and_Globulin_Ratio.fillna(liver_df['Albumin_and_Globulin_Ratio'].mean())

#liver_df[liver_df['Albumin_and_Globulin_Ratio'] == 0.9470639032815201]

# The input variables/features are all the inputs except Dataset.
# The prediction or label is 'Dataset' that determines whether the patient has liver disease or not. 
# Dropping Gender and Dataset

X = liver_df.drop(['Gender','Dataset'], axis=1)
X.head(3)

y = liver_df['Dataset'] 

# 1 for liver disease; 2 for no liver disease

# Correlation

liver_corr = X.corr()
liver_corr

plt.figure(figsize=(30, 30))
sns.heatmap(liver_corr, cbar = True,  square = True, annot=True, fmt= '.2f',annot_kws={'size': 15},cmap= 'coolwarm')
plt.title('Correlation between features');

"""The above correlation also indicates the following correlation
- Total_Protiens & Albumin
- Alamine_Aminotransferase & Aspartate_Aminotransferase
- Direct_Bilirubin & Total_Bilirubin
- There is some correlation between Albumin_and_Globulin_Ratio and Albumin. But its not as high as Total_Protiens & Albumin

# Machine Learning
"""

# Importing modules
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report,confusion_matrix
from sklearn import linear_model
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, BaggingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import Perceptron
from sklearn.linear_model import SGDClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=101)
print (X_train.shape)
print (y_train.shape)
print (X_test.shape)
print (y_test.shape)

"""# Logistic Regression"""

# Create logistic regression object

logreg = LogisticRegression()

# Train the model using the training sets and check score

logreg.fit(X_train, y_train)

#Predict Output

log_predicted= logreg.predict(X_test)
logreg_score = round(logreg.score(X_train, y_train) * 100, 2)
logreg_score_test = round(logreg.score(X_test, y_test) * 100, 2)

#Equation coefficient and Intercept

print('Logistic Regression Training Score: \n', logreg_score)
print('Logistic Regression Test Score: \n', logreg_score_test)
print('Coefficient: \n', logreg.coef_)
print('Intercept: \n', logreg.intercept_)
print('Accuracy: \n', accuracy_score(y_test,log_predicted))
print('Confusion Matrix: \n', confusion_matrix(y_test,log_predicted))
print('Classification Report: \n', classification_report(y_test,log_predicted))

sns.heatmap(confusion_matrix(y_test,log_predicted),annot=True,fmt="d")

coeff_df = pd.DataFrame(X.columns)
coeff_df.columns = ['Feature']
coeff_df["Correlation"] = pd.Series(logreg.coef_[0])
pd.Series(logreg.coef_[0])

coeff_df.sort_values(by='Correlation', ascending=False)

"""# Gaussian Naive Bayes"""

# Create gaussian object

gaussian = GaussianNB()
gaussian.fit(X_train, y_train)

#Predict Output
gauss_predicted = gaussian.predict(X_test)

gauss_score = round(gaussian.score(X_train, y_train) * 100, 2)
gauss_score_test = round(gaussian.score(X_test, y_test) * 100, 2)
print('Gaussian Score: \n', gauss_score)
print('Gaussian Test Score: \n', gauss_score_test)
print('Accuracy: \n', accuracy_score(y_test, gauss_predicted))
print(confusion_matrix(y_test,gauss_predicted))
print(classification_report(y_test,gauss_predicted))

sns.heatmap(confusion_matrix(y_test,gauss_predicted),annot=True,fmt="d")

"""# Random Forest"""

# create random_forest object

random_forest = RandomForestClassifier(max_depth=3,n_estimators=56,criterion='entropy')
random_forest.fit(X_train, y_train)

#Predict Output

rf_predicted = random_forest.predict(X_test)

random_forest_score = round(random_forest.score(X_train, y_train) * 100, 2)
random_forest_score_test = round(random_forest.score(X_test, y_test) * 100, 2)
print('Random Forest Score: \n', random_forest_score)
print('Random Forest Test Score: \n', random_forest_score_test)
print('Accuracy: \n', accuracy_score(y_test,rf_predicted))
print(confusion_matrix(y_test,rf_predicted))
print(classification_report(y_test,rf_predicted))

finX = liver_df[['Total_Protiens','Albumin', 'Gender_Male']]
finX.head(4)

"""# Logistic Regression"""

X_train, X_test, y_train, y_test = train_test_split(finX, y, test_size=0.30, random_state=101)

# Create logistic regression object

logreg = LogisticRegression()

# Train the model using the training sets and check score

logreg.fit(X_train, y_train)

# Predict Output

log_predicted= logreg.predict(X_test)

logreg_score = round(logreg.score(X_train, y_train) * 100, 2)
logreg_score_test = round(logreg.score(X_test, y_test) * 100, 2)

# Equation coefficient and Intercept

print('Logistic Regression Training Score: \n', logreg_score)
print('Logistic Regression Test Score: \n', logreg_score_test)
print('Coefficient: \n', logreg.coef_)
print('Intercept: \n', logreg.intercept_)
print('Accuracy: \n', accuracy_score(y_test,log_predicted))
print('Confusion Matrix: \n', confusion_matrix(y_test,log_predicted))
print('Classification Report: \n', classification_report(y_test,log_predicted))

sns.heatmap(confusion_matrix(y_test,log_predicted),annot=True,fmt="d")

"""# Decision Tree Classifier"""

# Create decision tree object

dt=DecisionTreeClassifier()

# Train the model using the training sets and check score

dt.fit(X_train,y_train)

# Predict Output

y_pred=dt.predict(X_test)

dt_score = round(dt.score(X_train, y_train) * 100, 2)
dt_test = round(dt.score(X_test, y_test) * 100, 2)

from sklearn.metrics import accuracy_score
accuracy_score(y_test,y_pred)

from sklearn.metrics import confusion_matrix
confusion_matrix(y_test,y_pred)

"""# Model evaluation"""

# We can now rank our evaluation of all the models to choose the best one for our problem.

models = pd.DataFrame({
    'Model': [ 'Logistic Regression', 'Gaussian Naive Bayes','Random Forest','Decision Tree'],
    'Score': [ logreg_score, gauss_score, random_forest_score,dt_score],
    'Test Score': [ logreg_score_test, gauss_score_test, random_forest_score_test,dt_test]})
models.sort_values(by='Test Score', ascending=False)

from watson_machine_learning_client import WatsonMachineLearningAPIClient

wml_credentials = {
   "instance_id": "1c8b2a30-08fb-4355-a71b-ea152c85f5b7",
  "password": "c88f97ec-f410-425e-bd14-114b067ffec2",
  "url": "https://eu-gb.ml.cloud.ibm.com",
  "username": "4478a4bf-e7d3-4311-8e99-b93fc1ace7a0"
}

client = WatsonMachineLearningAPIClient(wml_credentials)
model_props = {client.repository.ModelMetaNames.AUTHOR_NAME: "Abhishek", 
               client.repository.ModelMetaNames.AUTHOR_EMAIL: "abhishekrockstar545@gmail.com", 
               client.repository.ModelMetaNames.NAME: "LiverPatient Model"
              }
	

model=client.repository.store_model(logreg, meta_props=model_props)

published_model_uid = client.repository.get_model_uid(model)
published_model_uid

deployment = client.deployments.create(published_model_uid, name="Patient")

scoring_endpoint = client.deployments.get_scoring_url(deployment)
scoring_endpoint

client.deployments.list()

client.deployments.delete("e3ab3d2f-a3c1-4193-8f84-b637ada2b92a")