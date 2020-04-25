import random as r
import math as m


class Neuron:
    weights = []
    dat = []
    back_neurs = []
    my_err = 0

    def __init__(self, input_dat):
        if type(len(input_dat) > 0 and input_dat[0]).__name__ == 'Neuron':
            self.back_neurs = input_dat
        self.weights = [None for _ in range(len(input_dat))]
        self.dat = [None for _ in range(len(input_dat))]
        for i in range(len(input_dat)):
            if type(input_dat[i]).__name__ == 'Neuron':
                self.dat[i] = input_dat[i].output()
            else:
                self.dat[i] = input_dat[i]
            self.weights[i] = r.randint(0, 10)/10-0.5

    def set_dat(self, input_dat):
        for i in range(len(input_dat)):
            if type(input_dat[i]).__name__ == 'Neuron':
                self.dat[i] = input_dat[i].output()
            else:
                self.dat[i] = input_dat[i]

    def sygm(self, x):
        res = 1/(1+m.exp(-x))
        return res

    def dsygm(self):
        return self.sygm(self.summ())*(1-self.sygm(self.summ()))

    def summ(self):
        res = 0
        for i in range(len(self.weights)):
            res += self.weights[i]*self.dat[i]
        return res

    def output(self):
        sm = self.summ()
        res = self.sygm(sm)
        return res
