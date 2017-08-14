#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 00:07:15 2017

@author: kazuyuki
"""

import lstm_func as lf
import glob
import pandas as pd
import matplotlib.pyplot as plt

def test1(model, test_iter, total='Total'):
    
    model.reset_state()
    res1 = pd.DataFrame(index=range(test_iter.seq_length), columns=range(test_iter.columns), data=pd.np.NaN)
    res2 = pd.DataFrame(index=range(test_iter.seq_length), columns=[total], data=pd.np.NaN)
    
    for i in range(test_iter.seq_length):
        
        test_iter.loop = i
        x, t = test_iter.next()
        y = model(x)
        
        res1.iloc[i, :] = ((y - t)**2).data.mean(axis=0)**0.5
        res2.iloc[i, 0] = ((y - t)**2).data.mean()**0.5
        
    res = pd.concat([res1, res2], axis=1)
    
    res.index += 1
    
    return res

def test2(model, test_iter, s=0):
    
    model.reset_state()
    res1 = pd.DataFrame(index=range(test_iter.seq_length), columns=range(test_iter.columns), data=pd.np.NaN)
    res2 = pd.DataFrame(index=range(test_iter.seq_length), columns=['Total'], data=pd.np.NaN)
    
    for i in range(test_iter.seq_length):
        
        test_iter.loop = i
        x, t = test_iter.next()
        
        if i <= s:
            y = model(x)
        else:
            y = model(y)
        
        res1.iloc[i, :] = ((y - t)**2).data.mean(axis=0)**0.5
        res2.iloc[i, 0] = ((y - t)**2).data.mean()**0.5
        
    res = pd.concat([res1, res2], axis=1)
    
    res.index += 1
    
    return res        
        

if __name__ == "__main__":
    
    lf.chainer.config.train = False
    sine = True
    gpu = -1
    out = 'result_1'
    
    if sine == True:
        
        n_units = 100
        train, test = lf.getSineData()
        
        
        
    trainer = lf.getTrainer(train, n_units, gpu=-1, batch_size=10, seq_len=10, support_len=10, pred=1, 
                            out=out, snap=10, epoch=100)
    
    test_iter = lf.LSTM_Iterator(test, repeat=False, seq_len=20)
    
    trainers = glob.glob(out+"/trainer*")
    trainers.sort()

    lf.serializers.load_npz(trainers[-1], trainer)
    trainer.updater.get_iterator('main').iteration = trainer.updater.iteration
    
    model = trainer.updater.get_optimizer('main').target.predictor
    
    test1res = test1(model, test_iter)
    test2res = test2(model, test_iter, 0)

    for t in trainers:
        lf.serializers.load_npz(t, trainer)
        trainer.updater.get_iterator('main').iteration = trainer.updater.iteration
        
        model = trainer.updater.get_optimizer('main').target.predictor
        
        test1res = test1(model, test_iter, t[-5:])
        test1res.iloc[:, -1].plot(logy=True)   
        plt.legend()