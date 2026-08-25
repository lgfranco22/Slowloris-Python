# Slowloris Python

Implementação simples de um ataque **Slowloris** escrita em Python, desenvolvida para fins educacionais e de estudo sobre conexões HTTP persistentes, gerenciamento de sockets e mecanismos de proteção contra ataques de negação de serviço.

> ⚠️ **DISCLAIMER — LEIA ANTES DE USAR**
>
> Este projeto foi desenvolvido **exclusivamente para fins educacionais, testes em laboratório e pesquisa de segurança autorizada**.
>
> **NÃO utilize este código contra servidores, sistemas, redes ou serviços que não sejam de sua propriedade ou para os quais você não possua autorização explícita para realizar testes.**
>
> O uso deste programa contra terceiros sem autorização pode causar indisponibilidade de serviços e pode ser ilegal.
>
> O autor deste projeto **não se responsabiliza por quaisquer danos, indisponibilidade, perda de dados, prejuízos ou consequências legais** decorrentes do uso deste software.
>
> Ao utilizar este projeto, você assume integralmente a responsabilidade pelo ambiente e pelo alvo contra o qual o teste é realizado.

## Sobre o projeto

O **Slowloris** é uma técnica de negação de serviço que procura manter diversas conexões HTTP abertas por um longo período, enviando dados de forma lenta e incompleta.

A ideia básica é:

1. Abrir várias conexões TCP com o servidor.
2. Enviar o início de uma requisição HTTP.
3. Manter as conexões abertas.
4. Enviar pequenos dados periodicamente para evitar que as conexões sejam encerradas por timeout.
5. Reestabelecer conexões que forem encerradas.

O objetivo deste projeto é permitir estudar esse comportamento em um **ambiente controlado**, como uma máquina virtual, servidor local ou laboratório de testes.

## Requisitos

* Python 3.x
* Conectividade TCP com o ambiente de teste
* Um servidor HTTP autorizado para testes

O projeto utiliza somente módulos da biblioteca padrão do Python:

```text
socket
time
sys
```

Não é necessário instalar dependências externas.

## Instalação

Clone o repositório:

```bash
git clone https://github.com/lgfranco22/slowloris-python.git
cd slowloris-python
```

Execute diretamente com Python:

```bash
python3 slowloris.py
```

## Uso

Sintaxe:

```text
python3 slowloris.py <IP> [porta] [sockets] [intervalo]
```

Parâmetros:

| Parâmetro   | Obrigatório | Padrão | Descrição                               |
| ----------- | ----------: | -----: | --------------------------------------- |
| `IP`        |         Sim |      — | Endereço do servidor de teste           |
| `porta`     |         Não |   `80` | Porta TCP do servidor HTTP              |
| `sockets`   |         Não |  `500` | Quantidade de conexões a tentar manter  |
| `intervalo` |         Não |   `10` | Intervalo, em segundos, entre os envios |

### Exemplo

Em um ambiente de laboratório autorizado:

```bash
python3 slowloris.py 192.168.1.100 80 100 10
```

Nesse exemplo:

* alvo: `192.168.1.100`
* porta: `80`
* conexões: `100`
* intervalo: `10 segundos`

**Use valores baixos inicialmente em ambientes de teste**, especialmente quando o servidor estiver sendo executado na mesma máquina ou em uma rede compartilhada.

## Como funciona

A função principal cria sockets TCP e estabelece conexões com o servidor:

```python
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(4)
s.connect((target, port))
```

Depois, uma requisição HTTP incompleta é enviada:

```text
GET / HTTP/1.1
Host: 192.168.1.100
```

A requisição não é finalizada imediatamente. O programa mantém a conexão aberta e envia pequenos headers periodicamente.

Quando uma conexão é encerrada pelo servidor, ela é removida da lista e o programa tenta estabelecer uma nova conexão para manter a quantidade configurada de sockets.

## Estrutura

```text
slowloris-python/
├── slowloris.py
└── README.md
```

## Ambiente recomendado para testes

Para estudar o comportamento com segurança, recomenda-se utilizar um laboratório isolado, por exemplo:

```text
┌─────────────────────┐
│ Máquina de testes   │
│ Python / Slowloris  │
└──────────┬──────────┘
           │
           │ Rede isolada
           │
┌──────────▼──────────┐
│ Servidor HTTP       │
│ Apache / Nginx      │
│ Ambiente de teste   │
└─────────────────────┘
```

Uma máquina virtual também pode ser utilizada para evitar impacto sobre sistemas reais.

## O que estudar com este projeto

Este projeto pode ser utilizado para estudar:

* TCP sockets em Python
* HTTP/1.1
* Conexões persistentes
* HTTP request timeout
* Limites de conexões de servidores
* Gerenciamento de recursos
* Ataques de negação de serviço
* Mitigação de Slowloris
* Configuração de Apache e Nginx
* Monitoramento de conexões TCP

## Mitigação

Administradores podem estudar diferentes mecanismos de proteção contra esse tipo de comportamento, incluindo:

* Timeouts adequados para requisições HTTP
* Limitação do número de conexões
* Reverse proxies
* Rate limiting
* Web Application Firewalls (WAF)
* Monitoramento de conexões abertas
* Configuração adequada de workers/processos
* Ferramentas de detecção de tráfego anômalo

O objetivo deste projeto não é apenas reproduzir o comportamento, mas também facilitar o estudo de **como identificar e mitigar esse tipo de ataque**.

## Limitações

Esta é uma implementação simples para fins didáticos. Ela não pretende ser uma implementação completa ou otimizada de uma ferramenta de teste de carga.

O comportamento também depende de diversos fatores, como:

* servidor HTTP utilizado;
* configuração de timeout;
* sistema operacional;
* firewall;
* limites de sockets;
* recursos disponíveis;
* versão e configuração do servidor web.

## Licença

Distribuído sob a licença definida no arquivo `LICENSE`.

Consulte o arquivo de licença antes de utilizar, modificar ou redistribuir este projeto.

---

## ⚠️ Uso responsável

Este software deve ser utilizado **somente em sistemas próprios ou em ambientes nos quais você tenha autorização explícita para realizar testes de segurança**.

Nunca utilize este projeto para interromper, degradar ou prejudicar serviços de terceiros.

**Você é o único responsável pelo uso que fizer deste código.**
