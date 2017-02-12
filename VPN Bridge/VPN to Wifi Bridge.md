# Raspberry Pi VPN Bridge
This folder provides instructions and code to set up your Raspberry Pi serve as a Wifi bridge to an OpenVPN connection. Meaning that you will have a Wifi access point that routes all of your traffic through an OpenVPN service.

This requires that you either have your own OpenVPN server or have service through an online subscription.

If you would like to set up your own, I have a script and instructions at: https://github.com/sn0wfa11/OpenVPN-Setup-Script

I started this project mainly to be able to stream movies from my home Plex Server to a Google Chromecast while on vacation in Colorado, and not have to pay Plex a montly fee for remote service. (Why pay when you can learn how to get it for free!?)

One final note, I have training and experience in penetration testing. As such, this and other projects have a level of security that other sites may not include in similar instructions. This comes from experience knowing what can be used for Linux privilege escalation. Better to be safe than sorry, especially in this project as it may have access to your internal home network if you are using your own OpenVPN server.

## Requirements
- A Raspberry Pi 3
- An 8 or 16 GB high speed SD card with Raspbian flashed to it.
- A client.ovpn file for accessing the OpenVPN service of your choice. (It's easy to set up a server, do it yourself!)
- Ethernet or USB internet access. For this project I used the USB mode from a cellular air card.

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

You should see `wlan0`.

- Elevate to root. (Makes things easier now that we set a sudo password requirement.)

`sudo su`

### Install First Set of Needed Packages

`apt-get install hostapd udhcpd bind9`

### Configure Interfaces
In this section, we will be configuring the `wlan0` interface to be our Wifi access point. 

- Start by editing the `/etc/udhcpd.conf` file

`nano /etc/udhcpd.conf`

Add the following - Substitute the IP range of your choosing. You can use any of the privte IP range that does not conflict with your VPN or LAN range. https://en.wikipedia.org/wiki/Private_network

```
start 10.9.0.2
end 10.9.0.254
interface wlan0
remaining yes
opt dns 10.9.0.1
option subnet 255.255.255.0
opt router 10.9.0.1
option lease 864000 # 10 days
```

- Now edit the `/etc/default/udhcpd` file

`nano /etc/default/udhcpd`

Change the following line:

`#DHCPD_ENABLED="yes"`

To:

`DHCPD_ENABLED="yes"`

- Next, set and configure the IP address for `wlan0`

`ifconfig wlan0 10.9.0.1`

- And to make it stay that way edit `/etc/network/interfaces`

`nano /etc/network/interfaces`

Remove the following line:

`iface wlan0 inet dhcp`

Add the following: (Note the tabs on the second and third line)

```
iface wlan0 inet static
    address 10.9.0.1
    netmask 255.255.255.0
```

Comment out the lines to match what is shown below:
```
#allow-hotplug wlan0
#wpa-roam /etc/wpa_supplicant/wpa_supplicant.conf
#iface default inet manual
```

### Configure HostAPD
Now you need to configure the Wifi access point that will be operating on `wlan0`. You can change any settings that you would like. Be sure to set a good WPA passphrase!

`nano /etc/hostapd/hostapd.conf`

Add the following config settings. **You need to set a passphrase!**

```
# wlan1 will be the access point for this setup
interface=wlan0
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
# Set WPA
wpa_pairwise=TKIP
# Use AES
rsn_pairwise=CCMP
```

Try this:

```
interface=wlan0
driver=nl80211
ssid=GetOffMyLAN
hw_mode=g
channel=6
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=<YOUR_PASSWORD>
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
```

- Configure HostAPD to know where to get the settings.

`nano /etc/default/hostapd`

Change the following line:

`#DAEMON_CONF=""`

To:

`DAEMON_CONF="/etc/hostapd/hostapd.conf"`

- Start services and enable at boot

```
service hostapd start
service udhcpd start
update-rc.d hostapd enable
update-rc.d udhcpd enable
```

### Configure DNS
This will set up your DNS requests and IP assignments for the Wifi Access point.

- Edit `/etc/bind/named.conf.options`

`nano /etc/bind/named.conf.options`

Add the following forwarders:

```
forwarders {
8.8.8.8;
8.8.4.4;
};
```

Restart and enable the DNS Server
```
service bind9 restart
update-rc.d bind9 enable
```
### Set up IPv4 Forwarding and NAT for IPTables
- Ip forwarding - One nice easy line

`echo 1 > /proc/sys/net/ipv4/ip_forward`

- IPtables setup
This creates the routing between `wlan0` and `tun0`. Run the following lines individually.

`iptables -t nat -A POSTROUTING -o tun0 -j MASQUERADE`

You may also need to add the following lines if things are not working

```
iptables -A FORWARD -i tun0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
iptables -A FORWARD -i wlan0 -o tun0 -j ACCEPT
```

- Save the IP tables so they reload at boot

`iptables-save > /etc/iptables.nat.vpn.secure`

### Reboot
That's it. Test stuff out to make sure it all works correctly.
