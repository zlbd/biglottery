# !/usr/bin/env python3
# -*- codingg:utf-8 -*-
# author:zlbd


import pandas as pd
import numpy as np
from matplotlib.pylab import *
from bl import Lottery


class Panel:
    def __init__(self, data):
        self.data = data
        self.showEnable = True 
        #self.showEnable = False 

    def x(self, n):
        ks = []
        for k in range(0, n):
            ks.append(k)
        return np.array(ks)

    def y(self, lyst):
        return np.array(lyst)

    def show(self):
        if self.showEnable:
            bar(self.x(13), self.y(self.data.blues))
            bar(self.x(36), self.y(self.data.reds))
            show()


def main():
    lottery = Lottery('web.shtml')
    lottery.fixture()
    lottery.generate()
    panel = Panel(lottery)
    panel.show()


if __name__ == '__main__':
    main()

