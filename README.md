![honey-cycle](https://carefuldata.com/images/cdlogo.png)

# honey-cycle
pcap collection and disk cleaning daemon for net-gargoyle2 honeypot

See https://github.com/jpegleg/net-gargoyle2 for the net-gargoyle2 honeypot base.

The honey-cycle system adds pcap collection and rotation with tcpdump,
and cleans up after the net-gargoyle2 sqlite db backups that net-gargoyle2
makes in /opt/net-gargoyle/ when the db reaches the configured sizes, defaulting
at 500MB.

honey-cycle creates a self-maintaining honeypot appliance out of net-gargoyle2
that upgrades itself and manages its disk space.

# Using the install script
The 'install' file will also install net-gargoyle2 if not already installed.
Usage example:

```
chmod +x install
./install
honey-cycle
```

Using systemd (unit file installed by script)

```
systemctl start honey
```

The file cycler.py is placed in /opt/net-gargoyle/workspace/cycler.py and contains the age
in addition to the sleep set in /usr/sbin/honey-cycle

Use the sleep to extend the amount of time each tcpdump is cut off.

If the partion that /opt is in gets 90% or more full, honey-cycle will start deleting .db.gz and .pcap files
out of /opt/net-gargoyle/ regardless of their age. If removing those files doesn't get it below 90% it will exit
instead of running as to not compound the problem with more pcaps.
