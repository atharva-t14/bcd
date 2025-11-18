#!/bin/bash
sudo iptables -L
sudo iptables -P INPUT DROP
sudo iptables -P FORWARD DROP
sudo iptables -P OUTPUT ACCEPT
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -s 192.168.1.100 -j DROP
sudo iptables-save > /etc/iptables/rules.v4
