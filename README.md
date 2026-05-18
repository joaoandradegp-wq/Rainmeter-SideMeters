<h1 align="center">☁️ Side Meters Suite</h1>

<p align="center">
Coleção de widgets e automações desenvolvidas para o Rainmeter, focadas em monitoramento, produtividade, integração de rede e utilidades para desktop.
</p>

<p align="center">🌐
  <a href="https://www.rainmeter.net/" target="_blank">
     Site Oficial do Rainmeter
  </a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Em%20Expansão-brightgreen">
  <img src="https://img.shields.io/badge/Linguagem-Python-blue">
  <img src="https://img.shields.io/badge/Integração-Rainmeter-lightgrey">
</p>

---

<h2>📌 Sobre</h2>

<p>
O <b>Side Meters Suite</b> é/será um conjunto de widgets personalizados criados para expandir as capacidades do Rainmeter através de automações externas, monitoramento contínuo e integração com scripts auxiliares.
</p>

<p>
A ideia do projeto é centralizar diversos módulos independentes em uma única suíte visual e funcional para desktop Windows.
</p>

<p>
Cada widget possui sua própria automação, lógica de atualização e integração com o Rainmeter, permitindo adicionar funcionalidades avançadas além dos medidores tradicionais da plataforma.
</p>

<h2>🧩 Widgets da suíte</h2>

<ul>
  <li>🌐 RedeMonitor (monitoramento de dispositivos)</li>
  <li>📊 Widgets futuros em desenvolvimento</li>
  <li>⚙️ Integrações automatizadas</li>
  <li>🖥️ Utilitários desktop</li>
  <li>📡 Ferramentas de rede</li>
  <li>🔄 Monitores persistentes</li>
</ul>

<h2>🌐 RedeMonitor</h2>

<p>
O primeiro módulo da suíte é o <b>RedeMonitor</b>, responsável por monitorar dispositivos da rede local e conexões externas em tempo real.
</p>

<p>
O widget verifica continuamente o status de dispositivos previamente cadastrados utilizando testes automáticos de conectividade.
</p>

<p>
Cada equipamento é exibido diretamente no desktop através do Rainmeter, indicando:
</p>

<ul>
  <li>Status ONLINE</li>
  <li>Status OFFLINE</li>
  <li>Atualização automática</li>
  <li>Indicadores visuais por cor</li>
  <li>Monitoramento persistente em background</li>
</ul>

<h2>🔧 Configuração dos dispositivos</h2>

<p>
Os dispositivos monitorados não ficam diretamente no código Python.
</p>

<p>
O sistema utiliza um arquivo externo chamado <b>devices.ini</b>, permitindo configurar os equipamentos sem alterar o script principal.
</p>

<p>
Isso facilita:
</p>

<ul>
  <li>Distribuição pública no GitHub sem expor IPs pessoais</li>
  <li>Personalização rápida dos dispositivos monitorados</li>
  <li>Facilidade de manutenção</li>
  <li>Maior organização do projeto</li>
</ul>

<p>
O arquivo deve ser criado em:
</p>

<pre>
Documents\Rainmeter\Scripts\devices.ini
</pre>

<p>
Exemplo de configuração:
</p>

<pre>
[PC CASA]
ip=192.168.0.10

[NOTEBOOK]
ip=192.168.0.20

[SERVIDOR]
ip=10.0.0.5

[CAMERA]
ip=192.168.0.50

[DDNS REMOTO]
ip=meuservidor.ddns.net
</pre>

<p>
Cada seção representa um dispositivo exibido no widget.
</p>

<p>
O sistema possui suporte tanto para:
</p>

<ul>
  <li>IPs locais</li>
  <li>IPs externos</li>
  <li>DDNS</li>
  <li>Hosts personalizados</li>
</ul>

<h2>⚙️ Funcionamento automático</h2>

<p>
O sistema gera automaticamente toda a estrutura necessária para funcionamento do widget.
</p>

<p>
Durante a execução, o instalador/configurador:
</p>

<ul>
  <li>Fecha o Rainmeter automaticamente</li>
  <li>Remove arquivos antigos</li>
  <li>Cria diretórios necessários</li>
  <li>Gera scripts PowerShell</li>
  <li>Cria automações BAT e VBS</li>
  <li>Gera integração LUA</li>
  <li>Cria o arquivo INI do Rainmeter</li>
  <li>Reabre o Rainmeter automaticamente</li>
  <li>Ativa o widget já configurado</li>
</ul>

<p>
Todo o processo é realizado automaticamente via Python.
</p>

<h2>🔄 Monitoramento persistente</h2>

<p>
O monitor opera continuamente em background utilizando PowerShell em loop persistente.
</p>

<p>
A cada ciclo de atualização:
</p>

<ul>
  <li>Os dispositivos são testados automaticamente</li>
  <li>Os resultados são gravados em arquivo temporário</li>
  <li>O script LUA lê os dados atualizados</li>
  <li>O Rainmeter atualiza os medidores em tempo real</li>
</ul>

<p>
Isso permite monitoramento constante sem necessidade de interação manual.
</p>

<h2>🧠 Integração entre tecnologias</h2>

<p>
O projeto combina múltiplas tecnologias trabalhando juntas:
</p>

<ul>
  <li><b>Python:</b> geração automática dos arquivos e gerenciamento</li>
  <li><b>PowerShell:</b> monitoramento dos dispositivos</li>
  <li><b>LUA:</b> comunicação com o Rainmeter</li>
  <li><b>VBS:</b> execução oculta dos processos</li>
  <li><b>BAT:</b> controle de inicialização e reinício</li>
  <li><b>Rainmeter:</b> interface visual desktop</li>
</ul>

<h2>🎨 Interface visual</h2>

<p>
O widget utiliza layout minimalista integrado ao tema Illustro do Rainmeter.
</p>

<p>
A interface exibe:
</p>

<ul>
  <li>Lista de dispositivos monitorados</li>
  <li>Status em tempo real</li>
  <li>Cores dinâmicas de disponibilidade</li>
  <li>Atualização automática sem refresh manual</li>
  <li>Integração visual transparente com desktop</li>
</ul>

<h2>📡 Recursos do RedeMonitor</h2>

<ul>
  <li>Monitoramento contínuo de rede</li>
  <li>Suporte a IP local</li>
  <li>Suporte a DDNS</li>
  <li>Execução invisível em background</li>
  <li>Atualização automática a cada 5 segundos</li>
  <li>Inicialização automática junto ao Rainmeter</li>
  <li>Reconstrução automática dos arquivos da skin</li>
  <li>Gerenciamento automático de processos</li>
</ul>

<h2>🛠️ Tecnologias utilizadas</h2>

<ul>
  <li>Python 3</li>
  <li>Rainmeter</li>
  <li>PowerShell</li>
  <li>LUA</li>
  <li>VBScript</li>
  <li>Batch Script</li>
  <li>Windows Desktop APIs</li>
</ul>

<h2>📁 Arquivos ignorados no GitHub</h2>

<p>
Por questões de privacidade e segurança, o arquivo <b>devices.ini</b> não deve ser enviado ao GitHub.
</p>

<p>
O repositório utiliza um arquivo de exemplo para configuração inicial:
</p>

<pre>
devices.example.ini
</pre>

<p>
Basta renomear o arquivo para:
</p>

<pre>
devices.ini
</pre>

<p>
Após isso, configure seus dispositivos normalmente.
</p>

<h2>🚀 Estrutura modular</h2>

<p>
O <b>Phobos Rainmeter Suite</b> foi projetado para crescer com múltiplos widgets independentes.
</p>

<p>
A arquitetura permite adicionar facilmente novos módulos futuramente, mantendo:
</p>

<ul>
  <li>Automação independente</li>
  <li>Widgets separados</li>
  <li>Atualizações isoladas</li>
  <li>Integração centralizada</li>
  <li>Padronização visual</li>
</ul>

<p>
O objetivo é transformar a suíte em um conjunto completo de ferramentas desktop personalizadas para monitoramento, produtividade e automação.
</p>

---

<h2>📦 Estrutura dos arquivos</h2>

<pre>
Rainmeter/
│
├── Scripts/
│   ├── check_network.ps1
│   ├── check_network.bat
│   ├── start_hidden.vbs
│   ├── network.lua
│   ├── devices.ini
│   └── network_status.txt
│
└── Skins/
    └── illustro/
        └── NetworkDevices/
            └── RedeMonitor.ini
</pre>

<h2>🚀 Como utilizar</h2>

<ol>
  <li>Instale o Rainmeter</li>
  <li>Execute o script Python</li>
  <li>Edite o arquivo <b>devices.ini</b></li>
  <li>Reexecute o script para atualizar os dispositivos</li>
  <li>O widget será carregado automaticamente no desktop</li>
</ol>

---

<p align="center">
Suíte de widgets Rainmeter desenvolvida para automação, monitoramento e integração desktop.
</p>
