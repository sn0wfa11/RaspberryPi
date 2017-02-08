# Install Full Kali Linux on a Raspberry Pi

## Download the Image
https://www.offensive-security.com/kali-linux-arm-images/

## Setup onto SD Card Using Win32DiskImager

## Exapand the root FS
- Boot up the fist time to get things setup.
- Shut it down and pull out the memory card.
- Mount it in Kali normal
- Open gparted
- Expand partition to use the full card.
- Put back into pi and boot up.

## Install Kali Full
```
apt-get update
apt-get upgrade -y
apt-get dist-upgrade -y
reboot
apt-get install kali-linux-full
```

## Generate New SSH Keys
```
rm /etc/ssh/ssh_host_*
dpkg-reconfigure openssh-server
service ssh restart
```

