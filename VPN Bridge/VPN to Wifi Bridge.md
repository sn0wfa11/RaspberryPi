# Raspberry Pi VPN Bridge
This folder provides instructions and code to set up your Raspberry Pi serve as a Wifi bridge to an OpenVPN connection. Meaning that you will have a Wifi access point that routes all of your traffic through an OpenVPN service.

This requires that you either have your own OpenVPN server or have service through an online subscription.

If you would like to set up your own, I have a script and instructions at: https://github.com/sn0wfa11/OpenVPN-Setup-Script

I started this project mainly to be able to stream movies from my home Plex Server to a Google Chromecast while on vacation in Colorado, and not have to pay Plex a montly fee for remote service. (Why pay when you can learn how to get it for free!?)

One final note, I have training and experience in penetration testing. As such, this and other projects have a level of security that other sites may not include in similar instructions. This comes from experience knowing what can be used for Linux privilege escalation. Better to be safe than sorry, especially in this project as it may have access to your internal home network if you are using your own OpenVPN server.

## Requirements
- A Raspberry Pi 3
- An 8 or 16 GB high speed SD card with Raspbian flashed to it.
- A USB Wifi card. (Yes the R-Pi 3 has Wifi built in, you need two Wifi cards for this project.)
- A client.ovpn file for accessing the OpenVPN service of your choice. (It's easy to set up a server, do it yourself!)

## Initial Setup
- Start up the R-Pi and get it updated.
```
sudo su
apt-get update
apt-get upgrade -y
apt-get dist-upgrade -y
rpi-update
apt-get autoremove -y
apt-get autoclean
```

- Install the Openvpn application

`apt-get install openvpn -y`

### Get things a bit more secure
Standard R-Pi settings are a bit too insecure for me.

- Change the `pi` user's password. **Make it good**

`pi@vpnbridge:~$ passwd` Follow the instructions

- Change root's password. **Make this good and long!**

```
sudo su
root@vpnbridge:~# passwd
```

- Require a password for sudo. (This drives me nuts that it defauts to no password!!! Easy privilege escalation for an attacker!)
```
sudo su
cd /etc/sudoers.d/
ls
```

You should see a file like: `010_pi-nopasswd`. Use what is shown for you as this file name.

`visudo -f /etc/sudoers.d/010_pi-nopasswd`

Change the following line:

`pi ALL=(ALL) NOPASSWD: ALL`

To:

`pi ALL=(ALL) PASSWD: ALL`

Save and exit.

Then rename the file:

`mv /etc/sudoers.d/010_pi-nopasswd /etc/sudoers.d/010_pi`

---

## Set Up OpenVPN to connect at boot time
- Copy over the client.ovpn file that you created from your OpenVPN server or recieved from your OpenVPN service.
- Place the client.ovpn file in the `/root/` directory.
- Secure the client.ovpn file. (This prevents anyone other than root from reading or editing the file.)

`sudo chmod 700 /root/client.ovpn`

- Setup the script to connect to OpenVPN at boot and disconnect at shutdown
```
sudo su
cd /etc/init.d
nano vpnconnect
```

Cut and paste the script from vpnconnect in this directory into nano.

**Note: In you need to make any changes to this file, be sure that it includes the full path to openvpn such as `/usr/sbin/openvpn`. Leaving it up to your $PATH can lead to another easy privilege escalation!**

Save and exit

- Adjust permissions for the file

`chmod 755 vpnconnect`

- Ensure that the file is owned by root and permissions are correct.

`ls -al | grep vpnconnect`

You should see something like:

`-rwxr-xr-x   1 root root  857 Feb  7 21:49 vpnconnect`

If not, do the following

```
chown root:root vpnconnect
ls -al | grep vpnconnect
```

Ensure it matches the permissions and owner like the above line.

- Set it to start at boot

`update-rc.d vpnconnect defaults`

- Test it out

`reboot`

Check your OpenVPN server to make sure it is connected once the R-Pi boots up.

Also check that the R-Pi knows it is connected:

`ifconfig`

You should see an entry called `tun0` with an IPv4 address. (You will be using the tun0 interface in a bit for the second part.)

---

## Set up the bridge
This is a modified version of the instructions linked below.

https://frillip.com/using-your-raspberry-pi-3-as-a-wifi-access-point-with-hostapd/

http://alphaloop.blogspot.com/2014/01/raspberry-pi-as-vpn-wireless-access.html

https://makezine.com/projects/browse-anonymously-with-a-diy-raspberry-pi-vpntor-router/

- Make sure that your USB Wifi card is attached to the R-Pi

`ifconfig`

You should see `wlan0` and `wlan1`.

- Elevate to root. (Makes things easier now that we set a sudo password requirement.)

`sudo su`

### Install First Set of Needed Packages

`apt-get install -y dnsmasq hostapd`

### Configure Interfaces
In this section, we will be configuring the `wlan1` interface to be our Wifi access point. The nice part about connecting a second Wifi card to the R-Pi is that we can use either `wlan0` or `eth0` to connect to the internet.

- Start by editing the `/etc/dhcpd.conf` file

`nano /etc/dhcpcd.conf`

Add the line following line at the bottom of the file: (If you have added any interfaces to this configuration file, the below line must occur before thoes interfaces.)

`denyinterfaces wlan1`

- Next we need to configure the `wlan1` interface with a static IP and a network subnet. (You can use the any of the private IPv4 subnets. A list of these network ranges can be found here: https://en.wikipedia.org/wiki/Private_network, I prefer the 10.x.x.x range, just make sure it is different than the subnet that your OpenVPN server is using.)

`nano /etc/network/interfaces`

Edit the `wlan1` section as follows: (Change the IPv4 subnet as needed to match your network enviornment.)

```
allow-hotplug wlan1
iface wlan1 inet static
    address 10.9.0.1
    netmask 255.255.255.0
    network 10.9.0.0
    broadcast 10.9.0.255
# wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf
```

- Restart dhcpcd

`service dhcpcd restart`

- Reload Config for `wlan1`

`ifdown wlan1; ifup wlan1`

### Configure HostAPD
Now you need to configure the Wifi access point that will be operating on `wlan1`. You can change any settings that you would like. Be sure to set a good WPA passphrase!

`nano /etc/hostapd/hostapd.conf`

Add the following config settings. **You need to set a passphrase!**

```
# wlan1 will be the access point for this setup
interface=wlan1

# Use the nl80211 driver with the brcmfmac driver
driver=nl80211

# This is the name of the network. Set it to what you like.
ssid=GetOffMyLAN

# Use the 2.4GHz band
hw_mode=g

# Use channel 6
channel=6

# Enable 802.11n
ieee80211n=1

# Enable WMM
wmm_enabled=1

# Enable 40MHz channels with 20ns guard interval
ht_capab=[HT40][SHORT-GI-20][DSSS_CCK-40]

# Accept all MAC addresses
macaddr_acl=0

# Use WPA authentication
auth_algs=1

# Require clients to know the network name
ignore_broadcast_ssid=0

# Use WPA2
wpa=2

# Use a pre-shared key
wpa_key_mgmt=WPA-PSK

# The network passphrase. CHANGE ME! Make it a good one!
wpa_passphrase=<passphrase>

# Use AES, instead of TKIP
rsn_pairwise=CCMP
```

- Configure HostAPD to know where to get the settings.

`nano /etc/default/hostapd`

Change the following line:

`#DAEMON_CONF=""`

To:

`DAEMON_CONF="/etc/hostapd/hostapd.conf"`

### Configure DNSMASQ
This will set up your DNS requests and IP assignments for the Wifi Access point.

- Start my renaming the old config file and making a new one

```
mv /etc/dnsmasq.conf /etc/dnsmasq.conf.old
nano /etc/dnsmasq.conf
```

Put the folliwng in the config file. Make sure you use the same subnet that you used above for the configuration of `wlan1`.

```
interface=wlan1      # Use interface eth0  
listen-address=10.9.0.1 # Explicitly specify the address to listen on  
bind-interfaces      # Bind to the interface to make sure we aren't sending things elsewhere  
server=8.8.8.8       # Forward DNS requests to Google DNS  
domain-needed        # Don't forward short names  
bogus-priv           # Never forward addresses in the non-routed address spaces.  
dhcp-range=10.9.0.50,10.9.0.150,12h # Assign IP addresses between 10.9.0.50 and 10.9.0.150 with a 12 hour lease time.
```

### Set up IPv4 Forwarding and IPTables
- Ip forwarding - One nice easy line

`echo 1 > /proc/sys/net/ipv4/ip_forward`

- IPtables setup
This creates the routing between `wlan1` and `tun0`. Run the following lines individually.

```
iptables -t nat -A POSTROUTING -o tun0 -j MASQUERADE
iptables -A FORWARD -i tun0 -o wlan1 -m state --state RELATED,ESTABLISHED -j ACCEPT
iptables -A FORWARD -i wlan1 -o tun0 -j ACCEPT
```

- Set up iptables-persistant.
I prefer this method over the manual "iptables-restore" method.

**Be sure to select `yes` when the setup script asks you to save the IPv4 tables**

`apt-get install -y iptables-persistent`

Set the service to start at boot.

`update-rc.d netfilter-persistent enable`

### Start Services and Set Start at Boot
```
service hostapd start
service dnsmasq start
update-rc.d hostapd enable
update-rc.d dnsmasq enable
```

### Reboot
That's it. Test stuff out to make sure it all works correctly.
