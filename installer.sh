set -e
pkg install -y python
pkg install -y wget
pkg install -y iconv
pkg install -y unrar
echo "clear" >> ../usr/etc/bash.bashrc
echo "alias sub='python /data/data/com.termux/files/usr/share/sub4time/sub4time/sub.py'" >> ../usr/etc/bash.bashrc
clear
termux-setup-storage
echo "Instalación completa. Reinicia Termux."
kill -9 $PPID
