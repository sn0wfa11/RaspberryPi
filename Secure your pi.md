# Better Securing your pi

Standard R-Pi settings are a bit too insecure for me.

## Change the `pi` user's password

**Make it good**

`pi@vpnbridge:~$ passwd` Follow the instructions

## Change root's password

**Make this good and long!**

```
sudo su
root@vpnbridge:~# passwd
```

## Require a password for sudo. 
(This drives me nuts that it defauts to no password!!! Easy privilege escalation for an attacker!)

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
