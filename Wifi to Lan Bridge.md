# R-Pi Wifi to Lan Bridge
This mini project is a modified version of the following post: https://www.raspberrypi.org/forums/viewtopic.php?t=132674

I set up one of these to connect to a cellular aircard in the event that the cable internet goes down at my house.

## Requirements
You only need a Raspberry Pi 3 and an SD card!

## Start
Download and install Raspbian on SD Card and fire it up.

## Update
```
sudo su
apt-get update && apt-get upgrade -y && apt-get install rpi-update dnsmasq -y
rpi-update
```

## Connect to Wifi
`nano  /etc/wpa_supplicant/wpa_supplicant.conf`

Add:

```
network={
        ssid="mynetwork"
        psk="secret"
        key_mgmt=WPA-PSK
}
```

## Ethernet Static IP
Setup a static ip for the dhcp server. If you are using Raspbian Stretch see below.

`nano /etc/network/interfaces`

Comment out the existhing eth0 line and add the below configuration to the file:

(You can use any of the private IP ranges described here: https://en.wikipedia.org/wiki/Private_network

```
#iface eth0 inet manual
allow-hotplug eth0  
iface eth0 inet static  
    address 10.5.5.1
    netmask 255.255.255.0
    network 10.5.5.0
    broadcast 10.5.5.255
```

### Raspbian Stretch
 `nano /etc/dhcpcd.conf`
 
 ```
interface eth0
static ip_address=10.5.5.1/24
static routers=10.5.5.1
static domain_name_servers=8.8.8.8
```
 

## DNSmasq Setup
Save old config and make a new one. If you are using Raspbian Stretch see below.

```
mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig  
nano /etc/dnsmasq.conf
```

Add:
```
interface=eth0      # Use interface eth0  
listen-address=10.5.5.1 # Explicitly specify the address to listen on  
bind-interfaces      # Bind to the interface to make sure we aren't sending things elsewhere  
server=8.8.8.8       # Forward DNS requests to Google DNS  
domain-needed        # Don't forward short names  
bogus-priv           # Never forward addresses in the non-routed address spaces.  
dhcp-range=10.5.5.50,10.5.5.150,12h # Assign IP addresses between 10.5.5.50 and 10.5.5.150 with a 12 hour lease time 
```

### Raspbian Stretch
```
interface=eth0      # Use interface eth0  
listen-address=10.5.5.1 # Explicitly specify the address to listen on  
bind-interfaces      # Bind to the interface to make sure we aren't sending things elsewhere  
domain-needed        # Don't forward short names  
bogus-priv           # Never forward addresses in the non-routed address spaces.  
dhcp-range=10.5.5.50,10.5.5.150,12h # Assign IP addresses between 10.5.5.50 and 10.5.5.150 with a 12 hour lease time 
```

## Enable IPv4 forwarding.
`nano /etc/sysctl.conf`

Uncomment the following line:

`net.ipv4.ip_forward=1`

## IP Tables
`iptables -t nat -A POSTROUTING -o wlan0 -j MASQUERADE`

### IP Tables Persistent
Install this application to load the IPtables configuration at boot. This works better than the manual way on other sites.

`apt-get install -y iptables-persistent`

Be sure to select `yes` when the setup script asks you to save the IPv4 and IPv6 tables.

- Start the service at boot

`update-rc.d netfilter-persistent enable`

## Reboot
