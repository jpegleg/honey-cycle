import threading
import subprocess
import time
import sys
import os

from datetime import datetime

def timeslice():
    '''Make a global TIMESTAMP with datetime module.'''
    global TIMESTAMP
    TIMESTAMP = datetime.now()
    return(TIMESTAMP)

class honeyCycle():
    '''kill and start tcpdump and remove old files in a loop forever'''
    def __init__(self, name, interval):
        '''honeyCycle class has two properties, name and interval.'''
        self.name = name # cycler
        self.interval = interval # 1

    def tcpd(self):
        '''Kill and then start tcpdump'''
        timeslice()
        print (TIMESTAMP, "honeyCycle >>> killing tcpdump", self.name)
        process = subprocess.Popen(('pkill', 'tcpdump'), stdout=subprocess.PIPE)
        output = process.communicate()
        process.wait()
        timeslice()
        print (TIMESTAMP, "honeyCycle >>> starting tcpdump", self.name)
        starttcpdump = '/usr/sbin/tcpdump -nnvvXSs 9999 -i any -w /opt/net-gargoyle/$(hostname)_$(date +%Y%m%d%H%M%S)_hc.pcap &'
        os.system(starttcpdump)
        time.sleep(CYCLER.interval)

    def cleaner(self):
        '''Remove old files'''
        timeslice()
        print (TIMESTAMP, "honeyCycle >>> compress fresh backup db files", self.name)
        gzipdbs = 'find /opt/net-gargoyle/*.db -mtime +1 -exec gzip -9 {} \;'
        os.system(gzipdbs)
        timeslice()
        print (TIMESTAMP, "honeyCycle >>> removing old db files", self.name)
        olddbs = 'find /opt/net-gargoyle/*.db.gz -mtime +17 -exec rm -f {} \;'
        os.system(olddbs)
        timeslice()
        print (TIMESTAMP, "honeyCycle >>> cleaning up old pcap files", self.name)
        cleanpcap = 'find /opt/net-gargoyle/*.pcap -mtime +2 -exec rm -f {} \;'
        os.system(cleanpcap)

    def diskcheck(self):
        '''Check disk usage'''
        timeslice()
        print (TIMESTAMP, "honeyCycle >>> check disk usage", self.name)
        sized = 'df /opt | tail -n1 | awk \'{print $5}\' | grep "^9\|^100"'
        alertsize = os.system(sized)
        timeslice()
        print (TIMESTAMP, "honeyCycle <<< value of alertsize is", alertsize)
        if alertsize == 0:
            timeslice()
            print(TIMESTAMP, "honeyCycle <<< Disk size problem potential, clearing pcaps.")
            clearpcaps = 'rm -rf /opt/net-gargoyle/*.pcap'
            os.system(clearpcaps)
        else:
            timeslice()
            print(TIMESTAMP, "honeyCycle <<< Disk usage is not concerning yet, continue on.")
        timeslice()
        print (TIMESTAMP, "honeyCycle >>> check disk usage", self.name)
        sized2 = 'df /opt | tail -n1 | awk \'{print $5}\' | grep "^9\|^100"'
        alertsize2 = os.system(sized2)
        timeslice()
        print (TIMESTAMP, "honeyCycle <<< value of alertsize is", alertsize)
        if alertsize2 == 0:
            timeslice()
            print(TIMESTAMP, "honeyCycle <<< Disk size problem potential, clearing pcaps.")
            clearpcaps = 'rm -rf /opt/net-gargoyle/*.pcap'
            os.system(clearpcaps)
        else:
            timeslice()
            print(TIMESTAMP, "honeyCycle <<< Disk usage is not concerning yet, continue on.")
        timeslice()
        print (TIMESTAMP, "honeyCycle >>> check disk usage", self.name)
        sized3 = 'df /opt | tail -n1 | awk \'{print $5}\' | grep "^9\|^100"'
        alertsize3 = os.system(sized3)
        timeslice()
        print (TIMESTAMP, "honeyCycle <<< value of alertsize is", alertsize3)
        if alertsize3 == 0:
            timeslice()
            print(TIMESTAMP, "honeyCycle <<< Disk size problem potential, already have cleaned up our files.")
            print(TIMESTAMP, "honeyCycle >>> EXIT now, manual attention to /opt needed.")
            sys.exit(1)
        else:
            timeslice()
            print(TIMESTAMP, "honeyCycle <<< Disk usage is not concerning yet, continue on.")

if __name__ == '__main__':
    INTV = int(sys.argv[2])
    NAMED = str(sys.argv[1])
    CYCLER = honeyCycle(NAMED, INTV)
    while True:
        DISKCHECKER = threading.Thread(target=CYCLER.diskcheck(), name='Checker')
        DISKCHECKER.start()
        HONEYCYCLER = threading.Thread(target=CYCLER.tcpd(), name='Cycler')
        HONEYCYCLER.start()
        NETCYCLER = threading.Thread(target=CYCLER.cleaner(), name='Cleaner')
        NETCYCLER.start()
        DISKCHECKER.join()
        HONEYCYCLER.join()
        NETCYCLER.join()
