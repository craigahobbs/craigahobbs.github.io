# Debian Linux Setup


## Initial Setup

Install applications, configure docker, and reboot:

~~~
su -c "apt install docker.io emacs git git-gui make python3-venv rsync xsel"
su -c "usermod -aG docker $USER && reboot"
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

Finally, add the key to your [GitHub SSH Keys](https://github.com/settings/keys).


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


## Trim Log Files

To reduce disk log file disk usage, periodically execute the following command:

~~~
sudo journalctl --vacuum-time=2d
~~~
