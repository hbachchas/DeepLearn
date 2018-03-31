"""
** deeplean-ai.com **
** dl-lab **
created by :: GauravBh1010tt
"""

import model_Siam_LSTM as model
from dl_text.metrics import eval_sick
from dl_text import dl
import sick_utils as sick
import numpy as np

lrmodel = model.S_LSTM
model_name = lrmodel.func_name

embedding_dim = 300
LSTM_neurons = 50
dimx = 30
dimy = 30
lamda = 0.01
vocab_size = 8000
batch_size = 32
epochs = 4

try:
    word = wordVec_model['word']
    print 'using loaded model.....'
    sent1, sent2, train_len, test_len, train_score, test_score, pred_fname = sick.load_sick(model_name)
    
except:
    wordVec = 'D:/workspace/NLP/data/GoogleNews-vectors-negative300.bin.gz'
    #wordVec_model = gen.models.KeyedVectors.load_word2vec_format("GoogleNews-vectors-negative300.bin.gz",binary=True)
    sent1, sent2, train_len, test_len, train_score, test_score, wordVec_model, pred_fname = sick.load_sick(model_name, wordVec)


if True:
    data_l, data_r, embedding_matrix = dl.process_data(sent1, sent2,
                                                 wordVec_model,dimx=dimx,
                                                 dimy=dimy,vocab_size=vocab_size,
                                                 embedding_dim=embedding_dim)  
   
    X_train_l,X_test_l,X_dev_l,X_train_r,X_test_r,X_dev_r = dl.prepare_train_test(data_l,data_r,
                                                                           train_len,test_len)
    #train_score = np.array(train_score)*4 + 1
    #train_score = dl.encode_labels(train_score)
        
   
print 'built model....'

#def trainModel(m):
if True:
    
    lrmodel = lrmodel(dimx = dimx, dimy = dimy, embedding_matrix=embedding_matrix, 
                      LSTM_neurons = LSTM_neurons, dense_neurons = dense_neurons)
    st,end = 0,train_len
    lrmodel.fit([X_train_l[st:end],X_train_r[st:end]], 
              #[np.array(train_score[st:end]),np.zeros_like(train_score[st:end])],
                train_score[st:end],                 
                 nb_epoch=epochs,
                 batch_size=batch_size,verbose=1)

print '\n evaluating performance \n'
sp_coef, per_coef, mse = eval_sick(lrmodel, X_test_l, X_test_r, test_score)
print 'spearman coef :',sp_coef
print 'pearson coef :',per_coef
print 'mse :',mse