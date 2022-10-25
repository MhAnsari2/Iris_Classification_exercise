# -*- coding: utf-8 -*-
"""MohammadHosseinAnsari_RL.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1F0k6eQMZWe96bjiAIRsCXVNzADchXeGZ
"""

#for this part to run you need to install the scikit learn library so that you are able to import sklearn
#try the following code:
#pip install -U scikit-learn scipy matplotlib

import pandas as pnds
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import torch
import torch.nn as tnn
import torch.nn.functional as tFunc

iris = pnds.read_csv('https://gist.githubusercontent.com/netj/8836201/raw/6f9306ad21398ea43cba4f7d537619d0e07d5ae3/iris.csv')

mappings = {
   'Setosa': 0,
   'Versicolor': 1,
   'Virginica': 2}

iris['variety'] = iris['variety'].apply(lambda x: mappings[x])

X = iris.drop('variety', axis=1).values
y = iris['variety'].values
trdata_X, tstdata_X, trdata_y,tstdata_y = train_test_split(X, y, test_size=0.2, random_state=20)
trdata_X = torch.FloatTensor(trdata_X)
tstdata_X = torch.FloatTensor(tstdata_X)
trdata_y = torch.LongTensor(trdata_y)
y_test = torch.LongTensor(tstdata_y)

class ANN(tnn.Module):
   def __init__(self):
       super().__init__()
       self.fllyconnctd1 = tnn.Linear(in_features=4, out_features=25)
       self.fllyconnctd2 = tnn.Linear(in_features=25, out_features=15)
       self.output = tnn.Linear(in_features=15, out_features=3)
 
   def forward(self, x):
       x = tFunc.relu(self.fllyconnctd1(x))
       x = tFunc.relu(self.fllyconnctd2(x))
       x = self.output(x)
       return x

model = ANN()
lossfunc = tnn.CrossEntropyLoss()
updater = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.9)

# Commented out IPython magic to ensure Python compatibility.
# %%time
# 
# 
# epoch = 200
# lossarray = []
# for i in range(epoch):
#    target = model.forward(trdata_X)
#    loss = lossfunc(target, trdata_y)
#    lossarray.append(loss)
#  
#    if i % 10 == 0:
#        print(f'Epoch: {i} Loss: {loss}')
#  
#    updater.zero_grad()
#    loss.backward()
#    updater.step()
#   
# plt.plot(range(epoch), lossarray)
# plt.xlabel('number of epoch iterations')
# plt.ylabel('Accuracy Score')
# plt.title('Accuracy of model through runtime')
# plt.show()

prediction = []
with torch.no_grad():
   for val in tstdata_X:
       target = model.forward(val)
       prediction.append(target.argmax().item())

df = pnds.DataFrame({'target':tstdata_y, 'predicted': prediction})
df['right'] = [1 if corr == pred else 0 for corr, pred in zip(df['target'], df['predicted'])]
df['right'].sum() / len(df)