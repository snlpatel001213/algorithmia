
# coding: utf-8

from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
import numpy as np
import random

# read file content
filename = "lyricsText.txt"
raw_text = open(filename).read()
raw_text = raw_text.lower()

# All unique characters in text
chars = set(raw_text)

# mapping character to integer
char_indices = dict((c, i) for i, c in enumerate(chars))
# mapping integer to character back
indices_char = dict((i, c) for i, c in enumerate(chars))

# number of previous characters require to predict next character
maxlen = 100


def get_text_chunks(raw_text_part):
    sentences = []
    next_chars = []
    for i in range(0, len(raw_text_part) - maxlen, 1):
        sentences.append(raw_text_part[i: i + maxlen])
        next_chars.append(raw_text_part[i + maxlen])
    print('nb sequences:', len(sentences))
    X = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool)
    y = np.zeros((len(sentences), len(chars)), dtype=np.bool)
    for i, sentence in enumerate(sentences):
        for t, char in enumerate(sentence):
            X[i, t, char_indices[char]] = 1
        y[i, char_indices[next_chars[i]]] = 1
    return X,y


# defining a model
model = Sequential()
model.add(LSTM(512,  input_shape=(maxlen,len(chars)), return_sequences=False))
model.add(Dropout(0.5))

# you may use this unused layers for bigger dataset, I'm not using it
# model.add(LSTM(512, return_sequences=True))
# model.add(Dropout(0.5))

# model.add(LSTM(512, return_sequences=True))
# model.add(Dropout(0.20))

# model.add(LSTM(256, return_sequences=False))
# model.add(Dropout(0.5))

model.add(Dense(len(chars)))
model.add(Activation('tanh'))

# compile or load weights then compile depending

def sample(preds, temperature=1.0):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
#     print np.argmax(preds),
    exp_preds = np.exp(preds)
#     print np.argmax(preds),
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
#     print np.argmax(probas),
    return np.argmax(probas)

def generatetext(text_partition,i,model):
    """
    To generate text from trained modle
    i = can be any integer, while training you may pass epoch iterator as i to keep watch on quality of model.
    modle =  a trained model
    """
    # seed text  provides previous n( here 100) characters on basis of which n+ characters will be predicted.
    # randomly take seed text from text
    start_index = random.randint(0, len(raw_text) - maxlen - 1)
    seed_text  =  raw_text[start_index : start_index + maxlen]
#     seed_text = "When Mexico sends its people, they’re not sending the best. They’re not sending you, they’re sending people that have lots of problems and they’re bringing those problems with us."
    generated = '' + seed_text[-100:]
    print("EPOCH : ", i," | TEXT PARTITION : ",text_partition,"| SEED TEXT : ",generated)
    # will print next 300 characters
    for iteration in range(500):
            # create x vector from seed to predict on
            #generating numpy array as generated above
            x = np.zeros((1, maxlen, len(chars)))
            for t, char in enumerate(seed_text[-100:]):
                x[0, t, char_indices[char]] = 1.
            #predict next character
            preds = model.predict(x, verbose=0)[0]
            next_index = sample(preds)
            next_char = indices_char[next_index]
            #append next character to seed text, on the basis on new 100 character generate next to next character and so on. 
            generated += next_char
            seed_text = seed_text[1:] + next_char
#             print seed_text,next_char
    print('follow up with: ' + generated)


model.compile(loss='categorical_crossentropy', optimizer='rmsprop',metrics=['accuracy'])

# training for number of epochs
number_of_partition = 1
epochs = 10
chunkSize = len(raw_text)/number_of_partition
for i in range(0,epochs):
    for text_partition in range(number_of_partition):
        X,y = get_text_chunks(raw_text[text_partition*chunkSize: (text_partition+1)*chunkSize])
        model.fit(X,y, batch_size=1000,nb_epoch=1,verbose=0)  
        generatetext(text_partition,i,model)
    # saving model at every epoch
    model.save_weights('small/trump_'+str(text_partition)+"_"+str(i)+'.h5')


generatetext("test1","test1",model)




