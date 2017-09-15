# Add Encrypted Storage for your Kali-Pi!
These instructions will walk you through creating an encrypted partition on your Kali-Pi's SD card.

You can use this parition to store data such as private keys or Open VPN connection files that you don't want others to access if they find this device.

**WARNING #1** The normal filesystem on the SD Cards for Raspberry Pi's are not encrypted! Anyone can plug the card into a Linux machine and read your files.

## Intial Preperation
- Start by backing up any data or setting you have on your device. Since we are going to be messing with the partition tables this is always a good idea.

- Power off your Kali-Pi if it is running.

- Remove the SD card from the Pi device.

- Mount the SD card in Kali on a PC or VM (Ubuntu or Debian will work too as long as it has gparted and cryptsetup)

## Creating a partition to be encrypted
- Open gparted and select the SD card device.

- **Important!** Make note of the device label as you will need it later. For this example my SD card label is `/dev/sdb`

- Right click on `/dev/sdb2` and select `unmount` so that you can make changes to the card.

- If you used the instructions from the intial setup instructions you should have no free space and almost all of your SD card used by partition `/dev/sdb2`.

- Right click on `/dev/sdb2` and select `Resize`. Change the size of this partition so that you have free space at the end of the disk. I use 64 GB cards, so I usually leave about 16 GB of free space at the end of the disk. It's probably overkill, but hey, space is space!

- Right click on the new empty space and select `New`.

- In the `Create New Partition` window, change the File System Type to `unformatted` and click `Add` at the bottom. (We will format it here in a bit.)

- On the main gparted window, click `Edit` and select `Apply All Operations`.

- Once completed, close gparted

## Setup and Format Encrypted Partition

