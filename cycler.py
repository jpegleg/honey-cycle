import threading
import subprocess
import time
import sys
import os

class honeyCycle():
    '''kill and start tcpdump and remove old files in a loop forever'''
    def __init__(self, name, interval):
        '''honeyCycle class has two properties, name and interval.'''
        self.name = name # cycler
        self.interval = interval # 1

    def tcpd(self):
        '''Kill and then start tcpdump'''
        print ("honeyCycle >>> killing tcpdump", self.name)
        process = subprocess.Popen(('pkill', 'tcpdump'), stdout=subprocess.PIPE)
        output = process.communicate()
        process.wait()
        print ("honeyCycle >>> starting tcpdump", self.name)
        starttcpdump = '/usr/sbin/tcpdump -nnvvXSs 9999 -i any -w /opt/net-gargoyle/$(hostname)_$(date +%Y%m%d%H%M%S)_hc.pcap &'
        os.system(starttcpdump)
        time.sleep(CYCLER.interval)

    def cleaner(self):
        '''Remove old files'''
        print ("honeyCycle >>> compress fresh backup db files", self.name)
        gzipdbs = 'find /opt/net-gargoyle/*.db -mtime +1 -exec gzip -9 {} \;'
        os.system(gzipdbs)
        print ("honeyCycle >>> removing old db files", self.name)
        olddbs = 'find /opt/net-gargoyle/*.db.gz -mtime +17 -exec rm -f {} \;'
        os.system(olddbs)
        print ("honeyCycle >>> cleaning up old pcap files", self.name)
        cleanpcap = 'find /opt/net-gargoyle/*.pcap -mtime +2 -exec rm -f {} \;'
        os.system(cleanpcap)

    def diskcheck(self):
        '''Check disk usage'''
        print ("honeyCycle >>> check disk usage", self.name)
        sized = 'df /opt | tail -n1 | awk \'{print $5}\' | grep "^9\|^100"'
        alertsize = os.system(sized)
        print ("honeyCycle <<< value of alertsize is", alertsize)
        if alertsize == 0:
            print("honeyCycle <<< Disk size problem potential, clearing pcaps.")
            clearpcaps = 'rm -rf /opt/net-gargoyle/*.pcap'
            os.system(clearpcaps)
        else:
            print("honeyCycle <<< Disk usage is not concerning yet, continue on.")
        print ("honeyCycle >>> check disk usage", self.name)
        sized = 'df /opt | tail -n1 | awk \'{print $5}\' | grep "^9\|^100"'
        alertsize = os.system(sized)
        print ("honeyCycle <<< value of alertsize is", alertsize)
        if alertsize == 0:
            print("honeyCycle <<< Disk size problem potential, clearing pcaps.")
            clearpcaps = 'rm -rf /opt/net-gargoyle/*.pcap'
            os.system(clearpcaps)
        else:
            print("honeyCycle <<< Disk usage is not concerning yet, continue on.")
        print ("honeyCycle >>> check disk usage", self.name)
        sized = 'df /opt | tail -n1 | awk \'{print $5}\' | grep "^9\|^100"'
        alertsize3 = os.system(sized)
        print ("honeyCycle <<< value of alertsize is", alertsize3)
        if alertsize == 0:
            print("honeyCycle <<< Disk size problem potential, already have cleaned up our files.")
            print("honeyCycle >>> EXIT now, manual attention to /opt needed.")
            sys.exit(1)
        else:
            print("honeyCycle <<< Disk usage is not concerning yet, continue on.")          
            
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
