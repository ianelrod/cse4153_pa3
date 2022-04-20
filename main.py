# Name: Ian Goforth
# Email: img56@msstate.edu
# Student ID: 902-268-372

import math
import random
import threading
from time import sleep
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import datetime
import queue

def main():
    q = queue.Queue()
    
    x = []
    y = []

    for i in range(3):
        x.append(Thread(i, q))
        x[i].daemon = True
        x[i].start()

    x[0].join()

    print('Collecting data')
    while not q.empty():
        y.append(q.get())
    
    print(y)
    
    with PdfPages('cse4153_pa3.pdf') as pdf:
        fig = plt.figure()
        ax = fig.add_subplot(111)

        ind = np.arange(len(y[0]))
        width = 0.35

        rects1 = ax.bar(ind, y[0], width, color='red')
        rects2 = ax.bar(ind+width, y[1], width, color='green')
        rects3 = ax.bar(ind+width+width, y[2], width, color='blue')

        ax.set_xlim(-width, len(ind) + width)
        ax.set_ylim(0, 1000000)
        ax.set_ylabel('Average Latency')
        ax.set_xlabel('Number of Nodes N')
        ax.set_title('Average latency for nodes n')
        xTickMarks = [str(i) for i in range(100, 6100, 100)]
        ax.set_xticks(ind + width)
        xtickNames = ax.set_xticklabels(xTickMarks)
        plt.setp(xtickNames, rotation=45, fontsize=10)
        ax.legend((rects1[0], rects2[0], rects3[0]), ('Binary Exponential Backoff', 'Linear Backoff', 'LogLog Backoff'))
        pdf.savefig()
        plt.close()

        firstPage = plt.figure(figsize=(11.69,8.27))
        firstPage.clf()
        txt = '1. Which backoff protocol appears to give the best (lowest) average latency value as the number of devices tends to infinity?\nThe exponential protocol gives the lowest average latency because the windows get large the quickest to compensate for a lot of data.\n2. Which backoff protocol appears to give the worst (highest) average latency value as the number of devices tends to infinity?\nThe linear protocol gives the highest average latency because every iteration only increases the window length by 1. When working with a lot of data, this is just too slow of a compensation.\n3. Why do you think the worst (in terms of latency) protocol is behaving so poorly compared to the other two?\nI believe the worst protocol behaves poorly because it does not compensate the necessary amount quickly enough for the amount of data required to be sent.'
        firstPage.text(0.5,0.5,txt, transform=firstPage.transFigure, size=8, ha="center")
        pdf.savefig()
        plt.close()

        d = pdf.infodict()
        d['Title'] = 'CSE4153_PA3 Report'
        d['Author'] = 'Ian Goforth\xe4nen'
        d['Subject'] = 'A Report on Linear Backoff, Binary Exponential Backoff, and LogLog Backoff'
        d['CreationDate'] = datetime.datetime(2022, 4, 19)
        d['ModDate'] = datetime.datetime.today()

class Thread(threading.Thread):
    
    def __init__(self, num, queue):
        threading.Thread.__init__(self)
        self.num = num
        self.queue = queue
    
    def run(self):
        return_value = thread(self.num)
        self.queue.put(return_value)
        self.queue.task_done()

def thread(mode):
    x = []
    for i in range(100, 6100, 100):
        x.append(findAverage(mode, i))
    return x

def findAverage(mode, devices):
    r = []
    while len(r) <= 10:
        if mode == 2:
            length = 4
        else:
            length = 2
        x = [None] * length
        y = 0
        z = length - 1
        j = devices
        exit = False
        while exit is not True:
            for l in range(j):
                rand = random.randint(y, z)
                if x[rand] is None:
                    x[rand] = True
                elif x[rand] is True:
                    x[rand] = False
            for m in range(y, z):
                if x[m] is True:
                    j = j - 1
                    if j == 0:
                        r.append(len(x) - (z - y - m))
                        exit = True
                        break
            length = nextLength(mode, length)
            y = len(x)
            z = len(x) + length - 1
            add = [None] * length
            x.extend(add)

    print('mode {} with i {} and average {}'.format(mode, devices, sum(r) / len(r)))
    return sum(r) / len(r)

def nextLength(mode, prev):
    if mode == 0:
        return prev + 1
    if mode == 1:
        return prev * 2
    if mode == 2:
        return math.floor((1 + (1 / math.log(math.log(prev, 2), 2))) * prev)

main()