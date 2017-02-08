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
apt autoclean
```

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

Then rename the file:

`mv /etc/sudoers.d/010_pi-nopasswd /etc/sudoers.d/010_pi`

## Set Up OpenVPN to connect at boot time
- Copy over the client.ovpn file that you created from your OpenVPN server or recieved from your OpenVPN service.
- Place the client.ovpn file in the `/root/` directory.
- Secure the client.ovpn file. (This prevents anyone other than root from reading or editing the file.)

`sudo chmod 700 /root/client.ovpn`

- 

