# Debian Linux Setup


## Create a Debian Linux USB Drive

1. [Download Debian Stable ISO](https://www.debian.org/distrib/netinst)

2. Write the ISO to the USB drive:

   **Linux**

   ~~~
   sudo fdisk -l
   sudo umount /dev/sdX
   sudo dd bs=4M status=progress oflag=sync if=/path/to/iso of=/dev/sdX
   ~~~

   **MacOS**

   ~~~
   diskutil list
   diskutil unmountDisk /dev/diskN
   sudo dd bs=4m status=progress oflag=sync if=/path/to/iso of=/dev/rdiskN
   ~~~


## Initial Setup

First, add yourself to the sudoers:

~~~
su -l -c "usermod -aG sudo $USER && reboot"
~~~

Install applications, configure docker, and reboot:

~~~
sudo apt install docker.io emacs git git-gui make python3-venv rsync xsel
sudo usermod -aG docker $USER
sudo reboot
~~~


## Git Setup

To generate a git key, execute the following:

~~~
ssh-keygen -t ed25519 -C "debian-laptop"
~~~

To set the git global configuration, execute the following:

~~~
git config --global init.defaultBranch main
git config --global pull.rebase false
git config --global core.editor emacs
git config --global user.email "Craig A. Hobbs"
git config --global user.name "craigahobbs@gmail.com"
~~~

Finally, add the key to your [GitHub SSH Keys](https://github.com/settings/keys). The following
command copies your public SSH key to the clipboard.

~~~
cat ~/.ssh/id_ed25519.pub | xsel -ib
~~~


### Git Bash Prompt

Add the following to the end of your .bashrc:

~~~
# git-prompt.sh
if [ ! -f ~/.git-prompt.sh ]; then
    echo Downloading git-prompt.sh ...
    wget -O ~/.git-prompt.sh https://raw.githubusercontent.com/git/git/master/contrib/completion/git-prompt.sh
fi
source ~/.git-prompt.sh
PS1=$(expr substr "$PS1" 1 $(expr length "$PS1" - 3))'$(__git_ps1 " (%s)")'${PS1: -3}
~~~


## Clone Source Code

~~~
mkdir ~/src
cd ~/src
git clone git@github.com:craigahobbs/craigahobbs.github.io.git
make -C ~/src/craigahobbs.github.io/projects/ pull -j; echo $?
~~~


## Trim Log Files

To reduce disk log file disk usage, periodically execute the following command:

~~~
sudo journalctl --vacuum-time=2d
~~~
