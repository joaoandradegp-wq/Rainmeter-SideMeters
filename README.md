<h1 align="center">
 <img width="400" src="https://github.com/user-attachments/assets/87e1d3ab-e046-48de-bf6b-3c54d198f4d4" />
</h1>

<p align="center">
Coleção de widgets e automações para Rainmeter, com foco em monitoramento de dispositivos, servidores, rede e hardware.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Em%20Expansão-brightgreen">
  <img src="https://img.shields.io/badge/Versão-1.5-blue">
  <img src="https://img.shields.io/badge/Linguagem-Python-blue">
  <img src="https://img.shields.io/badge/Integração-Rainmeter-lightgrey">
  <img src="https://img.shields.io/badge/Language-PT--BR-orange">
</p>

---

## 📌 Sobre

O **Side Meters Suite** é uma aplicação criada para centralizar a configuração e automação de widgets do Rainmeter.

A aplicação permite configurar dispositivos, monitorar servidores e rede, atualizar skins e integrar o **LibreHardwareMonitor** para exibição das temperaturas de CPU e GPU.

---

## 🧩 Módulos atuais

* **SideMeterDevices** - Gerenciamento de dispositivos monitorados;
* **CRT Terminal** - Monitoramento de servidores através de API;
* **Link Speed** - Monitoramento da velocidade do link;
* **System CPU/RAM** - Monitoramento de CPU e memória;
* **LibreHardwareMonitor** - Instalação, ativação e monitoramento de temperaturas de CPU e GPU.

---

## ⚙️ Principais funcionalidades

### SideMeterDevices

* Cadastro, edição e remoção de dispositivos
* Suporte a IP, Hostname e DDNS
* Geração automática do `devices.ini`

### CRT Terminal

* Configuração de servidor através de API HTTP
* Teste de conexão
* Validação dos campos esperados
* Atualização automática dos dados utilizados pelo Rainmeter

### Link Speed

* Identificação automática da interface de rede
* Prioridade para Ethernet
* Fallback para Wi-Fi
* Monitoramento de velocidade, download e upload

### System

* CPU e RAM
* Memória disponível
* Temperatura da CPU
* Temperatura da GPU
* Identificação do processador e GPU
* Indicadores de temperatura

### LibreHardwareMonitor

* Instalação automática através do WinGet
* Instalação das dependências necessárias
* Configuração do Web Server na porta `8085`
* Inicialização automática com privilégios administrativos
* Verificação do status do servidor
* Integração com a skin `System`

---

## 🌡️ LibreHardwareMonitor

O LibreHardwareMonitor faz parte do fluxo de configuração do módulo **System**.

Caso não esteja instalado, o Side Meters Suite permite realizar a instalação diretamente pela interface.

Após a instalação, o programa pode configurar e iniciar o LibreHardwareMonitor com o Web Server disponível em:

```text
http://localhost:8085/data.json
```

A skin System utiliza os sensores:

```text
CPU Package
GPU Core
```

para apresentar as temperaturas no Rainmeter.

Caso o LibreHardwareMonitor já esteja aberto, mas o Web Server esteja desativado, a interface informa que ele deve ser habilitado em:

```text
Options > Remote Web Server > Run
```

---

## 🚀 Como utilizar

1. Instale o **Rainmeter**.
2. Execute o **Side Meters Suite**.
3. Selecione o módulo desejado.
4. Configure os parâmetros.
5. Clique em **Adicionar**, **Atualizar** ou **Testar Conexão**, conforme o módulo.
6. O programa gera ou atualiza os arquivos necessários e ativa a skin correspondente.

Para o monitoramento de temperatura:

```text
Rainmeter
   └── System
       └── LibreHardwareMonitor
           ├── Instalar
           ├── Ativar
           └── Verificar
```

---

## 📂 Estrutura

```text
Documents/
└── Rainmeter/
    ├── Scripts/
    │   └── devices.ini
    │
    └── Skins/
        ├── illustro/
        │   ├── Network/
        │   │   ├── Network.ini
        │   │   ├── LinkSpeed.ps1
        │   │   └── RunLinkSpeed.vbs
        │   │
        │   └── System/
        │       └── System.ini
        │
        └── ServerMonitor/
            ├── ServerMonitor.ini
            ├── Scripts/
            │   ├── start_api.bat
            │   ├── run_hidden.vbs
            │   └── update_api.ps1
            └── @Resources/
                └── api.txt
```

---

## 🛠 Tecnologias

* Python
* Tkinter
* Rainmeter
* PowerShell
* VBScript
* WinGet
* LibreHardwareMonitor
* PawnIO
* HTTP API
* WebParser

---

## 📸 Preview

<p align="center">
  <img width="300" src="https://github.com/user-attachments/assets/7a463a2c-68ad-4772-9e84-c19a04d90dee" />
  <img width="300" src="https://github.com/user-attachments/assets/3f7d841e-ad60-4180-b1c8-f861f7bb9b60" />
  <br>
  <img width="300" src="https://github.com/user-attachments/assets/1b6fc158-895e-4a2d-9d1d-b1d27209d19e" />
  <img width="300" src="https://github.com/user-attachments/assets/e14134ad-d11d-4988-900f-ddc2906459eb" />
</p>

---

<p align="center">
<b>Side Meters Suite</b> centraliza a configuração e automação dos seus widgets Rainmeter em uma única aplicação. 🤖
</p>
