# Debian Linux Setup


## Create a Debian Linux USB Drive

1. Download the [Debian Stable ISO](https://www.debian.org/distrib/netinst).
   Alternatively, you can use a [Debian Testing ISO](https://www.debian.org/devel/debian-installer/).

2. Insert the USB drive and determine its device name:

   **Linux**

   ~~~sh
   sudo fdisk -l
   ~~~

   **macOS**

   ~~~sh
   diskutil list
   ~~~

3. Write it to the USB drive:

   **Linux**

   ~~~sh
   sudo umount /dev/sdX
   sudo dd bs=4M status=progress oflag=sync if=/path/to/iso of=/dev/sdX
   ~~~

   **macOS**

   ~~~sh
   diskutil unmountDisk /dev/diskN
   sudo dd bs=4m status=progress oflag=sync if=/path/to/iso of=/dev/rdiskN
   ~~~


## Initial Setup

First, add yourself to the sudoers:

~~~sh
su -l -c "usermod -aG sudo $USER && reboot"
~~~

Next, install applications, remove the grub delay, and reboot:

~~~sh
sudo apt install emacs git git-gui make nodejs npm podman python3-venv rsync screen tree xsel
sudo apt purge evolution evolution-data-server evolution-ews-core exim4-base exim4-config exim4-daemon-light gnome-bluetooth-sendto gnome-calculator gnome-calendar gnome-characters gnome-clocks gnome-contacts gnome-games gnome-maps gnome-music gnome-sound-recorder gnome-text-editor gnome-tour gnome-user-share gnome-weather libreoffice* mailutils mailutils-common rhythmbox rygel rygel-playbin rygel-tracker shotwell simple-scan totem yelp
sudo apt autoremove
sudo apt purge $(dpkg -l | grep '^rc' | awk '{print $2}')
sudo sed -i 's/^GRUB_TIMEOUT=.*/GRUB_TIMEOUT=0/' /etc/default/grub
sudo update-grub
sudo reboot
~~~


## .bashrc

Add the following to the end of your .bashrc:

~~~sh
# git-prompt.sh
if [ ! -f ~/.git-prompt.sh ]; then
    echo Downloading git-prompt.sh ...
    wget -O ~/.git-prompt.sh https://raw.githubusercontent.com/git/git/master/contrib/completion/git-prompt.sh
fi
source ~/.git-prompt.sh
PS1=$(expr substr "$PS1" 1 $(expr length "$PS1" - 3))'$(__git_ps1 " (%s)")'${PS1: -3}

# Use podman for development
export USE_PODMAN=1

# Add venv/bin to path
export PATH=$HOME/venv/bin:$PATH
~~~


## Trim Log Files

To reduce disk log file disk usage, periodically execute the following command:

~~~sh
sudo journalctl --vacuum-time=2d
~~~


# macOS Setup


## Install Homebrew

~~~sh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install aspell cloc git git-gui grep node python screen tree
brew install --cask emacs-app
~~~


## Uninstall Homebrew

If you ever need to unistall Homebrew for any reason:

~~~sh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/uninstall.sh)"
~~~


# Windows Setup

Install the following:

- [Python for Windows](https://www.python.org/downloads/windows/)
- [Node for Windows](https://nodejs.org/en/download/)
- [MSYS2](https://www.msys2.org/)

Install MSYS packages using the MSYS shell:

~~~sh
pacman -Suy
pacman -S diffutils git make mingw-w64-x86_64-emacs rsync
~~~

Add the following to the end of your MSYS .bashrc file:

~~~ sh
# Windows Node
export PATH=$PATH:/c/'Program Files'/nodejs

# Windows Python
export PATH=$PATH:/c/Users/craig/AppData/Local/Microsoft/WindowsApps
~~~


# Git Setup

To generate a git key, execute the following:

~~~sh
ssh-keygen -t ed25519 -C "debian-laptop"
~~~

To set the git global configuration, execute the following:

~~~sh
git config --global init.defaultBranch main
git config --global fetch.prune true
git config --global pull.rebase false
git config --global core.editor emacs
git config --global user.email "craigahobbs@gmail.com"
git config --global user.name "Craig A. Hobbs"
~~~

Finally, add the key to your [GitHub SSH Keys](https://github.com/settings/keys). The following
command copies your public SSH key to the clipboard.

~~~sh
cat ~/.ssh/id_ed25519.pub | xsel -ib
~~~


# Clone Source Code

~~~sh
mkdir ~/src
cd ~/src
git clone git@github.com:craigahobbs/craigahobbs.github.io.git
make -C ~/src/craigahobbs.github.io/projects/ pull -j; echo $?
~~~
