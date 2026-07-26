<h1 align="center">☁️ Side Meters Suite</h1>

<p align="center">
Coleção de widgets, skins e automações desenvolvidas para o Rainmeter, focadas em monitoramento de dispositivos, servidores e integração com sistemas externos.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Em%20Expansão-brightgreen">
  <img src="https://img.shields.io/badge/Linguagem-Python-blue">
  <img src="https://img.shields.io/badge/Integração-Rainmeter-lightgrey">
  <img src="https://img.shields.io/badge/Language-PT--BR-orange">
</p>

---

<h2>📌 Sobre</h2>

<p>
O <b>Side Meters Suite</b> é uma suíte de widgets, skins e ferramentas para o <b>Rainmeter</b>, criada para automatizar monitoramentos e fornecer painéis inspirados em interfaces clássicas de ficção científica.
</p>

<p>
Cada módulo possui backend próprio, integração automática com o Rainmeter e pode ser configurado através de uma interface gráfica, eliminando praticamente toda necessidade de edição manual de arquivos.
</p>

---

<h2>🧩 Módulos atuais</h2>

<ul>
  <li>🌐 <b>RedeMonitor</b> — Monitoramento ONLINE / OFFLINE de dispositivos em rede</li>
  <li>🖥 <b>SEVASTOLINK</b> — Dashboard inspirado nos computadores da Sevastopol (Alien: Isolation)</li>
  <li>🌐 Link Speed (Network.ini Update)</li>
  <li>💾 New System RAM Usage (System.ini Update)</li>
</ul>

---

<h2>🚀 Como utilizar</h2>

<ol>
  <li>Instale o Rainmeter pelo site oficial <a href="https://www.rainmeter.net/" target="_blank">clicando aqui</a></li>
  <li>Execute <b>RedeMonitorUI.exe</b></li>
  <li>Escolha o módulo desejado</li>
  <li>Configure os parâmetros</li>
  <li>Clique em <b>Atualizar</b></li>
  <li>O Rainmeter será configurado automaticamente</li>
</ol>

---

<h2>🌐 RedeMonitor</h2>

<p>
O <b>RedeMonitor</b> é responsável pelo monitoramento contínuo de equipamentos locais ou remotos, exibindo seu status diretamente no desktop através do Rainmeter.
</p>

<p>
Cada dispositivo pode ser monitorado utilizando Ping tradicional ou conexão TCP, permitindo verificar tanto máquinas quanto serviços específicos.
</p>

<ul>
  <li>✅ Status ONLINE / OFFLINE</li>
  <li>🌐 Suporte a IP, Hostname e DDNS</li>
  <li>🔌 Suporte a monitoramento por porta TCP</li>
  <li>⚡ Atualização automática</li>
  <li>🟢 Indicadores visuais</li>
  <li>🔄 Monitor persistente em background</li>
</ul>

---

<h2>🖥 SEVASTOLINK</h2>

<p>
O <b>SEVASTOLINK</b> é uma skin inspirada nos computadores da estação espacial <b>Sevastopol</b>, do universo de <b>Alien: Isolation</b>.
</p>

<p>
Ela transforma o Rainmeter em um painel de monitoramento do servidor, utilizando uma API HTTP para exibir informações em tempo real.
</p>

<p>
A configuração é totalmente automatizada pela interface do Side Meters Suite.
</p>

<ul>
  <li>🖥 Utilização do layout inspirado na Sevastopol</li>
  <li>📡 Integração com API HTTP</li>
  <li>🌡 Monitoramento de CPU</li>
  <li>💾 Monitoramento de Memória</li>
  <li>💿 Utilização de Disco</li>
  <li>🌐 Rede</li>
  <li>⚡ Atualização automática</li>
  <li>🔄 Recarregamento automático da skin</li>
</ul>

---

<h2>🖥 Interface de Configuração</h2>

<p>
O <b>RedeMonitorUI</b> centraliza toda a configuração da suíte.
</p>

<p>
A interface agora possui duas abas independentes:
</p>

<ul>
  <li>🌐 Status de Dispositivos (RedeMonitor)</li>
  <li>🖥 Status do Servidor (SEVASTOLINK)</li>
</ul>

<p>
Cada módulo pode ser configurado individualmente através da interface gráfica.
</p>

---

<h2>⚙️ Automação</h2>

<p>
O Side Meters Suite gera automaticamente todos os arquivos necessários para funcionamento das skins.
</p>

<ul>
  <li>PowerShell</li>
  <li>VBScript</li>
  <li>Batch Script</li>
  <li>LUA</li>
  <li>Arquivos INI</li>
  <li>Pastas do Rainmeter</li>
</ul>

<p>
Durante a atualização o sistema pode:
</p>

<ul>
  <li>Validar configurações</li>
  <li>Gerar arquivos automaticamente</li>
  <li>Inicializar scripts em segundo plano</li>
  <li>Abrir o Rainmeter automaticamente</li>
  <li>Recarregar as skins</li>
</ul>

---

<h2>🧩 Arquitetura</h2>

<pre>
                  RedeMonitorUI.exe
                          │
        ┌─────────────────┴──────────────────┐
        │                                    │
        ▼                                    ▼
  RedeMonitor                      SEVASTOLINK
        │                                    │
 devices.ini                    update_api.ps1
        │                                    │
check_network.ps1                    api.txt
        │                                    │
network_status.txt             ServerMonitor.ini
        │                                    │
        └──────────────► Rainmeter ◄─────────┘
</pre>

---

<h2>📂 Estrutura</h2>

<pre>
Documentos/
│
└── Rainmeter/
    │
    ├── network_status.txt
    │
    ├── Scripts/
    │   ├── devices.ini
    │   ├── check_network.ps1
    │   ├── check_network.bat
    │   ├── start_hidden.vbs
    │   └── network.lua
    │
    └── Skins/
        │
        ├── illustro/
        │   └── NetworkDevices/
        │       └── RedeMonitor.ini
        │
        ├── ServerMonitor/
        │   ├── ServerMonitor.ini
        │   ├── Scripts/
        │   │   ├── start_api.bat
        │   │   ├── run_hidden.vbs
        │   │   └── update_api.ps1
        │   │
        │   └── @Resources/
        │       └── api.txt
        │
        ├── Network/
        │   ├── Network.ini
        │   ├── LinkSpeed.ps1
        │   ├── RunLinkSpeed.vbs
        │   └── linkspeed.txt
        │
        └── System/
            └── System.ini
</pre>

---

<h2>🛠 Tecnologias</h2>

<ul>
  <li>Python</li>
  <li>Tkinter</li>
  <li>Rainmeter</li>
  <li>PowerShell</li>
  <li>LUA</li>
  <li>VBScript</li>
  <li>Batch Script</li>
  <li>HTTP API</li>
  <li>TCP Monitoring</li>
  <li>WebParser</li>
</ul>

---

## 📸 Preview

<p align="center">
<i><img width="400" alt="image" src="https://github.com/user-attachments/assets/ae26c7b3-8a3a-4f66-94d9-d70cba3b5cb9" />
  <img width="400" alt="image" src="https://github.com/user-attachments/assets/6eb485e3-20c4-41db-bacb-fcaa17002e08" /><br>
  <img width="400" alt="image" src="https://github.com/user-attachments/assets/c27fc82a-d13a-42b3-b4ca-3c64ceddcff3" />
</i>
</p>

---

<p align="center">
<b>Side Meters Suite</b> reúne diferentes módulos para o Rainmeter, oferecendo monitoramento de dispositivos, servidores e automações em uma única interface de configuração.
</p>
