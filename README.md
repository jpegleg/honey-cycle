# honey-cycle
pcap collection and disk cleaning daemon for net-gargoyle2 honeypot

See https://github.com/jpegleg/net-gargoyle2 for the net-gargoyle2 honeypot base.

The honey-cycle system adds pcap collection and rotation with tcpdump,
and cleans up after the net-gargoyle2 sqlite db backups that net-gargoyle2
makes in /opt/net-gargoyle/ when the db reaches the configured sizes, defaulting
at 500MB.

honey-cycle creates a self-maintaining honeypot appliance out of net-gargoyle2
that upgrades itself and manages its disk space.
