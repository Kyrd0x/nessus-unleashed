# nessus-unleashed
Nessus Expert Re Installator

# Functionnalities : 

Init : Initial install (no save/delete needed)

Uninstall : cqfd

ReInstall : below 

ReInstall + Scan : Reinstall and launch web scan(s?)

# Installation

It's a simple Python tool, so

```bash
git clone https://github.com/Couscouz/nessus-unleashed
cd nessus-unleashed
python tool.py init
```
Make sure you have ```requests``` library, otherwise :
```bash
pip install requests
```

# RE INSTALL PROCESS

## Step 1 : SAVE

Download all *.nessus reports

## Step 2 : STOP

stop daemon and rm -rf /opt/nessus

## Step 3 : INSTALL

e install from .deb (download if wrong checksum) and start daemon

## Step 4 : SET

generate trial code, activate and set eveyrthing

## Step 5 : RESTORE

restore all *.nessus reports