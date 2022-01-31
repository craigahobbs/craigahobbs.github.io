## Git configuration

To generate a git key, execute the following:

```
ssh-keygen -t ed25519 -C <key-name>
```

To set the git global configuration, execute the following:

```
git config --global init.defaultBranch main
git config --global pull.rebase false
git config --global core.editor emacs
git config --global user.email "Craig A. Hobbs"
git config --global user.name "craigahobbs@gmail.com"
```

To add a git bash command line prompt, add the following to the end of your .bashrc:

``` sh
# git-prompt.sh
if [ ! -f ~/.git-prompt.sh ]; then
    echo Downloading git-prompt.sh ...
    wget -O ~/.git-prompt.sh https://raw.githubusercontent.com/git/git/master/contrib/completion/git-prompt.sh
fi
source ~/.git-prompt.sh
PS1=$(expr substr "$PS1" 1 $(expr length "$PS1" - 3))'$(__git_ps1 " (%s)")'${PS1: -3}
```


## Debian: Dell XPS 13 7390 Laptop Wifi Drivers

Following Debian 11 install on wired connection:

1. Add "non-free" in "Software & Updates" application

2. Execute the following commands in a terminal
```
sudo apt update && sudo apt install firmware-iwlwifi
sudo modprobe -r iwlwifi ; sudo modprobe iwlwifi
```