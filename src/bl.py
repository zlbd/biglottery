#!/usr/bin/env python3
#-*- codingg:utf-8 -*-
#author:zlbd


from random import randint
from time import sleep


def myhash(nlist, n):
    sig = 0
    for i in range(1, n+1):
        if i in nlist:
            sig += (1<<i)
    return sig


class Signal:
    sigdic = {}
    def __init__(self, ticket, lyst, n):
        self.ticket = ticket
        self.val = myhash(lyst, n)
        self.resizeDic()

    def resizeDic(self):
        if self.val in self.sigdic:
            self.sigdic[self.val].append(self.ticket)
        else:
            tickets = [self.ticket]
            self.sigdic[self.val] = tickets

    def __str__(self):
        return str(self.val)

    def __eq__(self, sig):
        return (self.ticket.t == sig.ticket.t)

    def __ne__(self, sig):
        return (self.ticket.t != sig.ticket.t)

    def __le__(self, sig):
        return (self.ticket.t  <= sig.ticket.t)

    def __lt__(self, sig):
        return (self.ticket.t < sig.ticket.t)

    def __ge__(self, sig):
        return (self.ticket.t >= sig.ticket.t)

    def __gt__(self, sig):
        return (self.ticket.t > sig.ticket.t)


class RedSignal(Signal):
    redsigdic = {}

    def resizeDic(self):
        if self.val in self.redsigdic:
            self.redsigdic[self.val].append(self.ticket)
        else:
            tickets = [self.ticket]
            self.redsigdic[self.val] = tickets


class BlueSignal(Signal):
    bluesigdic = {}

    def resizeDic(self):
        if self.val in self.bluesigdic:
            self.bluesigdic[self.val].append(self.ticket)
        else:
            tickets = [self.ticket]
            self.bluesigdic[self.val] = tickets


class TicketBase:
    def __init__(self, nums):
        self.nums = nums
        self.t    = nums[0]     # t:    2007001
        self.red  = nums[1:6]   # blue: [22, 24, 29, 31, 35]
        self.blue = nums[6:]    # red:  [4, 11]
        self.val  = nums[1:]    # val:  [22, 24, 29, 31, 35, 4, 11]

    def __str__(self):
        return str(self.nums)


class Ticket(TicketBase):
    def __init__(self, nlist):
        super(Ticket, self).__init__(nlist)
        self.redsig  = RedSignal(self, self.red, 35)
        self.bluesig = BlueSignal(self, self.blue, 12)

        valtmp = self.red + list(map(lambda n:n+35, self.blue))
        self.valsig = Signal(self, valtmp, 35+12)


class TicketGroup:
    def __init__(self, tickets = None):
        if tickets is not None:
            self.tickets = tickets
        else:
            self.tickets = []

    def __contains__(self, ticket):
        for t in self.tickets:
            if t.valsig.val == ticket.valsig.val:
                return True
        return False

    def append(self, ticket):
        self.tickets.append(ticket)

    def findsame(self, ticket):
        for t in self.tickets:
            if t.valsig.val == ticket.valsig.val:
                return t
        return None


class Lottery:
    def __init__(self, fname):
        self.fname = fname
        self.slist = []
        self.tupletable = []
        self.numtbl = []
        self.reds = []
        self.redtotal = 0
        self.blues = []
        self.bluetotal = 0
        self.logEnable = False
        self.tickets = []
        self.newticket = None
        self.testEnable = False
        self.testticket = None

    def file2list(self):
        with open(self.fname) as f:
            self.slist = f.readlines()

    def take(self, line, head, tail):
        """take the data and rest between head and tail from line."""
        data = None
        rest = line
        begin = line.find(head)
        if begin != -1:
            line = line[begin + len(head):]
            end = line.find(tail)
            if end != -1:
                data = line[:end]
                rest = line[end + len(tail):]
        return (data, rest)

    def filter(self, tds, tags, reverse = False):
        """if tds[0] is in tags, append item to new list to return."""
        lyst = []
        for td in tds:
            if reverse:
                if td[0] not in tags:
                    lyst.append(td)
            else:
                if td[0] in tags:
                    lyst.append(td)

        return lyst

    def line2tds(self, line):
        rest = line
        tds = []
        while True:
            cls, rest = self.take(rest, '<td class="', '"')
            if cls is None:
                break
            dat, rest = self.take(rest, '>', '</td>')
            if dat is None:
                break
            tds.append((cls, dat))
        return tds

    def tuple2num(self, tpltbl):
        numtbl = []
        for tpls in tpltbl:
            numline = []
            for tpl in tpls:
                numline.append(int(tpl[1]))
            numtbl.append(numline)
        return numtbl

    def extractall(self):
        self.tupletable = []
        for i,line in enumerate(self.slist):
            tds = self.line2tds(line)
            if tds:
                tags = ('Issue', 'B_1', 'B_1 fgx', 'B_5', 'B_5 fgx')
                lyst = self.filter(tds, tags)
                self.tupletable.append(lyst)
        self.numtbl = self.tuple2num(self.tupletable)

    def calctickets(self):
        self.tickets = []
        for line in self.numtbl:
            self.tickets.append(Ticket(line))

        if self.testEnable:
            self.testticket = self.tickets.pop()
            print(self.testticket)

    def calc_num_frequency(self):
        # 1.count numbers
        reddic = {}
        bluedic = {}
 
        for ticket in self.tickets:
            for k in ticket.red:
                if k in reddic:
                    reddic[k] += 1
                else:
                    reddic[k] = 0
            for k in ticket.blue:
                if k in bluedic:
                    bluedic[k] += 1
                else:
                    bluedic[k] = 0
        # 2. calc reds,redcount, blues, bluecount
        self.reds = []
        self.redcount = 0
        self.reds.append(0)
        for key in sorted(reddic):
            self.reds.append(reddic[key])
            self.redcount += reddic[key]

        self.blues = []
        self.bluecount = 0
        self.blues.append(0)
        for key in sorted(bluedic):
            self.blues.append(bluedic[key])
            self.bluecount += bluedic[key]

        # 3. print log
        if self.logEnable:
            print("----------------- frequency")
            print(self.reds)
            print(self.blues)

    def calc_ticket_repeat(self):
        if self.logEnable:
            print("----------------- repeat")
            for k in sorted(Signal.sigdic.keys()):
                if len(Signal.sigdic[k]) >= 2:
                    for ticket in Signal.sigdic[k]:
                        print(ticket)
                    print('------------')
                
    def analysis(self):
        self.calc_num_frequency()
        self.calc_ticket_repeat()

    def fixture(self):
        self.file2list()
        self.extractall()
        self.calctickets()
        self.analysis()

    def selectoneold(self, freqs):
        freqcount = sum(freqs)
        one = randint(1, freqcount)
        for i in range(1, len(freqs)):
            if freqs[i-1] < one < freqs[i]:
                break
        return i

    def selectone(self, fs):
        freqcount = 0
        for item in fs:
            freqcount += item[1]
        one = randint(1, freqcount)
        k = 0
        for i in range(1, len(fs)):
            k += fs[i-1][1]
            if k < one < k + fs[i][1]:
                break
        return i  #fs[i][0]

    def selectalot(self, freqs, ncount):
        alot = []
        fs = [(n, freq) for n, freq in enumerate(freqs)]
        for n in range(ncount):
            i = self.selectone(fs)
            alot.append(fs.pop(i))
        alot = [item[0] for item in alot]
        alot = sorted(alot)
        return alot


    def generate(self):
        """
        1. Random selection of numbers according to established probabilities
        2. Count the number of duplicate rows
        """
        ticketGroup = TicketGroup(self.tickets)

        cnt = 0
        while True:
            # step 0. print current time
            cnt += 1

            # step 1. select red
            reds = self.selectalot(self.reds, 5)

            # step 2. select blue
            blues = self.selectalot(self.blues, 2)

            # step 3. combine red and blue
            vals = [2020001] + reds + blues
            self.newticket = Ticket(vals)

            # step test
            if self.testEnable:
                if cnt < 10:
                    print("try times:{}".format(cnt))
                elif (cnt < 100) and (cnt % 10 == 0):
                    print("try times:{}".format(cnt))
                    sleep(0.05)
                elif (cnt < 1000) and (cnt % 100 == 0):
                    print("try times:{}".format(cnt))
                    sleep(0.05)
                else:
                    if (cnt % 5000 == 0):
                        print("try times:{}".format(cnt))
                        sleep(0.05)

                if self.newticket.valsig != self.testticket.valsig:
                    continue
                else:
                    break

            # step 4. if red+blue is in vals, goto step 1.
            if self.newticket in ticketGroup:
                print(self.newticket, ticketGroup.findsame(self.newticket))
            else:
                break
            
        # step 5. return result
        print("-----------------------------------")
        print("try total times:{}".format(cnt))
        print(self.newticket)


def main():
    lottery = Lottery('web.shtml')
    lottery.fixture()
    lottery.generate()


if __name__ == '__main__':
    main()

