<h1 align="center">☁️ Side Meters Suite</h1>

<p align="center">
Coleção de widgets e automações desenvolvidas para o Rainmeter, focadas em monitoramento e utilidades para desktop.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Em%20Expansão-brightgreen">
  <img src="https://img.shields.io/badge/Linguagem-Python-blue">
  <img src="https://img.shields.io/badge/Integração-Rainmeter-lightgrey">
  <img src="https://img.shields.io/badge/Language-PT--BR%20-orange">
</p>

---

<h2>📌 Sobre</h2>

<p>
O <b>Side Meters Suite</b> é uma suíte de widgets e automações criada para expandir as funcionalidades do Rainmeter através de monitoramento contínuo, integração com scripts externos e módulos independentes.
</p>

<p>
Cada componente possui backend próprio e integração automática com o Rainmeter, permitindo adicionar funcionalidades avançadas além dos widgets tradicionais.
</p>

<h2>🧩 Módulos atuais</h2>

<ul>
  <li>🌐 RedeMonitor</li>
  <li>🌐 Link Speed (Network.ini)</li>
  <li>🌐 System RAM Usage (System.ini)</li>
</ul>

---

<h2>🚀 Como utilizar</h2>

<ol>
  <li>Instale o Rainmeter pelo site oficial <a href="https://www.rainmeter.net/" target="_blank">clicando aqui</a></li> 
  <li>Execute <b>RedeMonitorUI.exe</b></li>
  <li>Cadastre os dispositivos</li>
  <li>Clique em <b>Atualizar</b></li>
  <li>O Rainmeter será configurado automaticamente</li>
</ol>

---

<h2>🌐 RedeMonitor</h2>

<p>
O primeiro módulo da suíte é o <b>RedeMonitor</b>, responsável pelo monitoramento contínuo de dispositivos locais e remotos diretamente no desktop via Rainmeter.
</p>

<p>
O sistema verifica automaticamente a conectividade dos equipamentos e atualiza o widget em tempo real.
</p>

<ul>
  <li>Status ONLINE / OFFLINE</li>
  <li>Atualização automática</li>
  <li>Indicadores visuais</li>
  <li>Monitor persistente</li>
  <li>Integração automática com Rainmeter</li>
</ul>

---

<h2>🖥️ Interface visual</h2>

<p>
A partir da versão atual o projeto passou a utilizar uma interface dedicada chamada <b>RedeMonitorUI</b>.
</p>

<p>
Agora não é mais necessário editar arquivos manualmente.
</p>

<p>
A interface permite:
</p>

<ul>
  <li>Adicionar dispositivos</li>
  <li>Editar dispositivos</li>
  <li>Remover dispositivos</li>
  <li>Salvar configurações</li>
  <li>Atualizar automaticamente o Rainmeter</li>
</ul>

---

<h2>🧩 Arquitetura</h2>

<pre>
RedeMonitorUI.exe
        ↓
    devices.ini
        ↓
 RedeMonitor.exe
        ↓
    Rainmeter
</pre>

<p>
O sistema foi dividido entre:
</p>

<ul>
  <li><b>RedeMonitorUI:</b> interface de gerenciamento</li>
  <li><b>RedeMonitor:</b> backend responsável pela geração automática dos arquivos</li>
</ul>

---

<h2>🔧 Configuração</h2>

<p>
Os dispositivos monitorados ficam armazenados automaticamente em:
</p>

<pre>
Documents\Rainmeter\Scripts\devices.ini
</pre>

<p>
Exemplo:
</p>

<pre>
[Notebook]
ip=192.168.0.10

[Servidor]
ip=10.0.0.5

[Câmera]
ip=192.168.0.50

[DDNS]
ip=meuservidor.ddns.net
</pre>

<p>
Suporte para:
</p>

<ul>
  <li>IP local</li>
  <li>IP externo</li>
  <li>Hostname</li>
  <li>DDNS</li>
</ul>

---

<h2>⚙️ Funcionamento automático</h2>

<p>
O backend gera automaticamente toda a estrutura necessária do Rainmeter:
</p>

<ul>
  <li>PowerShell persistente</li>
  <li>Integração LUA</li>
  <li>Execução oculta via VBS</li>
  <li>Controle via BAT</li>
  <li>Skin dinâmica</li>
</ul>

<p>
Durante a atualização o sistema:
</p>

<ul>
  <li>Fecha Rainmeter</li>
  <li>Remove arquivos antigos</li>
  <li>Reconstrói a skin</li>
  <li>Reabre o Rainmeter</li>
  <li>Ativa automaticamente o widget</li>
</ul>

---

<h2>🔄 Monitoramento persistente</h2>

<p>
O monitor utiliza PowerShell em execução contínua.
</p>

<p>
A cada ciclo:
</p>

<ul>
  <li>Os dispositivos são testados</li>
  <li>O status é salvo</li>
  <li>O LUA lê os dados</li>
  <li>O Rainmeter atualiza a interface</li>
</ul>

<p>
Atualização padrão:
</p>

<pre>
5 segundos
</pre>

---

<h2>🎨 Interface do widget</h2>

<p>
O layout é integrado ao tema Illustro do Rainmeter.
</p>

<p>
Exibe:
</p>

<ul>
  <li>Dispositivos monitorados</li>
  <li>Status em tempo real</li>
  <li>Cores dinâmicas</li>
  <li>Atualização automática</li>
</ul>

---

<h2>🛠 Tecnologias</h2>

<ul>
  <li>Python</li>
  <li>Rainmeter</li>
  <li>PowerShell</li>
  <li>LUA</li>
  <li>VBScript</li>
  <li>Batch Script</li>
  <li>Tkinter</li>
</ul>

---

<h2>📦 Estrutura</h2>

<pre>
SideMetersSuite/
│
├── RedeMonitorUI.exe
├── RedeMonitor.exe
│
└── Rainmeter/
    │
    ├── Scripts/
    │   ├── devices.ini
    │   ├── check_network.ps1
    │   ├── check_network.bat
    │   ├── start_hidden.vbs
    │   ├── network.lua
    │   └── network_status.txt
    │
    └── Skins/
        └── illustro/
            └── NetworkDevices/
                └── RedeMonitor.ini
</pre>

---

## 📸 Preview

<p align="center">
  <img width="400" alt="image" src="https://github.com/user-attachments/assets/3d83c3a5-eb35-4886-bb24-43ad6ed19d80" />
</p>

---

<p align="center">
Suite de widgets para Rainmeter focada em monitoramento, automação e integração desktop. ⚙️
</p>
