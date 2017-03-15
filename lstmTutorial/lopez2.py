
# coding: utf-8

# In[84]:


import keras.preprocessing.text
import numpy as np

np.random.seed(1337)  # for reproducibility

from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM


# In[85]:

print('Loading data...')
import pandas

thedata = pandas.read_csv("labeledTrainData.tsv", sep=', ', delimiter='\t', header='infer', names=None)


# In[86]:

x = thedata['review']
y = thedata['sentiment']


# In[87]:

x = x.loc[:].values
X_train = x[:15000]
X_test = x[15001:]
y = y.loc[:].values
Y_train = y[:15000]
Y_test = y[15001:]


# In[88]:

X_test


# In[89]:

tk = keras.preprocessing.text.Tokenizer(nb_words=2000, filters=keras.preprocessing.text.base_filter(), lower=True, split=" ")


# In[97]:

tk.fit_on_texts(X_train)
tk.fit_on_texts(X_test)


# In[99]:

X_train = tk.texts_to_sequences(X_train)
X_test = tk.texts_to_sequences(X_test)


# In[100]:

max_len = 80


# In[101]:

X_train = sequence.pad_sequences(X_train, maxlen=max_len)
X_test = sequence.pad_sequences(X_test, maxlen=max_len)


# In[102]:

max_features = 20000
model = Sequential()
print('Build model...')


# In[103]:

model.add(Embedding(max_features, 128, input_length=max_len, dropout=0.2))
model.add(LSTM(128, dropout_W=0.2, dropout_U=0.2))
model.add(Dense(1))
model.add(Activation('sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='rmsprop')
model.fit(X_train, y=Y_train, batch_size=200, nb_epoch=1, verbose=1, validation_split=0.2, show_accuracy=True, shuffle=True)


# In[104]:

# Final evaluation of the model
scores = model.evaluate(X_test, Y_test, verbose=0)
print scores


# In[ ]:


