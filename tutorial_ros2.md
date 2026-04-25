# Guia Iniciante de ROS2 (Robot Operating System 2)


## O que é o ROS2?

ROS2 é um **framework open-source para desenvolvimento de robôs**. Ele fornece ferramentas, bibliotecas e convenções para facilitar a criação de software robótico complexo. Pense nele como um "sistema operacional" que permite diferentes partes do seu robô se comunicarem entre si.

---

## Onde dá para rodar?

> **No ARARABOTS usamos exclusivamente ROS2 Humble + Ubuntu 22.04 LTS.** Não use outras distros (Foxy, Iron, Jazzy) — nossos pacotes não foram testados nelas e quebram em coisas sutis.

| Ambiente | Status no time | Observação |
|----------|----------------|------------|
| **Ubuntu 22.04 LTS (nativo)** | ✅ Recomendado | Melhor experiência, sem camadas de compatibilidade |
| **WSL2 com Ubuntu 22.04 (Windows 10/11)** | ✅ Funciona bem | Use o filesystem Linux (`~/`), **não** `/mnt/c/` — compilar lá é muito mais lento. Para GUI precisa de WSLg (vem por padrão no Win 11) |
| **Windows nativo** | ❌ Não use | Instalação difícil e sem suporte do time |
| **macOS** | ❌ Não use | ROS2 no Mac é experimental, builds da comunidade |
| **Outras versões de Ubuntu (20.04, 24.04)** | ❌ Não use | Forçariam outra distro do ROS2 (Foxy / Jazzy), incompatível com nossos pacotes |

**Quem está no Windows:** instale o WSL2 com Ubuntu 22.04. No PowerShell como administrador:

```powershell
wsl --install -d Ubuntu-22.04
```

Confirme sua versão antes de prosseguir:

```bash
lsb_release -a              # deve mostrar Ubuntu 22.04
echo $ROS_DISTRO            # depois de instalar, deve mostrar "humble"
```

---

## Conceitos Fundamentais

### 1. Nodes (Nós)

- São **processos individuais** que executam uma tarefa específica
- Exemplo: um nó para a câmera, outro para os motores, outro para navegação
- Cada nó é independente e se comunica com outros nós

### 2. Topics (Tópicos)

- São **canais de comunicação** entre nós (modelo publish/subscribe)
- Um nó **publica** dados em um tópico
- Outro nó **se inscreve** nesse tópico para receber os dados
- Comunicação **assíncrona** e unidirecional

```
[Nó Câmera] --publica--> /camera/image --inscreve--> [Nó Processamento]
```

### 3. Services (Serviços)

- Comunicação **request/response** (requisição e resposta)
- Um nó faz um **pedido**, outro nó **responde**
- Útil para ações pontuais (ex: ligar/desligar um sensor)

### 4. Actions (Ações)

- Como serviços, mas para **tarefas longas** com feedback
- Exemplo: "vá até o ponto X" — o robô envia progresso enquanto se move

### 5. Messages (Mensagens)

- São as **estruturas de dados** enviadas pelos tópicos/serviços
- Tipos comuns: `String`, `Int32`, `Twist` (velocidade), `Image`, etc.

---

## Passo a Passo para Começar

### Passo 1 — Instalar o ROS2

A distribuição recomendada atual é o **ROS2 Humble** ou **Iron** (no Ubuntu 22.04):

```bash
# No Ubuntu 22.04 (recomendado para iniciantes)
sudo apt update && sudo apt install -y curl gnupg2 lsb-release
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/ros2.list
sudo apt update
sudo apt install ros-humble-desktop
```

> **No Windows:** Você pode usar WSL2 (Ubuntu) ou instalar nativamente, mas WSL2 é mais fácil.

### Passo 2 — Configurar o ambiente

```bash
# Adicione isso ao final do seu ~/.bashrc
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

### Passo 3 — Testar a instalação

```bash
# Verificar se o ROS2 está funcionando
ros2 --help

# Testar comunicação entre terminais usando CLI (sem simulador)
# Terminal 1: publicar mensagens manualmente
ros2 topic pub /teste std_msgs/msg/String "{data: 'Ola ROS2'}" --rate 1

# Terminal 2: escutar o tópico
ros2 topic echo /teste
```

Se no Terminal 2 você vir as mensagens aparecendo, a instalação está funcionando corretamente.

### Passo 4 — Explorar comandos básicos

```bash
# Listar todos os nós ativos
ros2 node list

# Listar todos os tópicos
ros2 topic list

# Ver dados sendo publicados em um tópico
ros2 topic echo /teste

# Ver informações de um tópico (tipo de mensagem, publishers, subscribers)
ros2 topic info /teste

# Ver a frequência de publicação
ros2 topic hz /teste

# Listar serviços disponíveis
ros2 service list

# Ver detalhes de um nó
ros2 node info /nome_do_no
```

### Passo 5 — Criar seu primeiro pacote

Se ainda **não tem um workspace**, crie um primeiro:

```bash
mkdir -p ~/ros2_ws/src
```

> **No WSL2?** Use o filesystem do Linux (`~/`), não o `/mnt/c/` — compilar lá é muito mais lento.

Agora crie o pacote:

```bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_python meu_primeiro_pacote
```

### Passo 6 — Estrutura do pacote

Após criar o pacote, a estrutura gerada é:

```
~/ros2_ws/src/meu_primeiro_pacote/
├── meu_primeiro_pacote/
│   └── __init__.py          ← já existe (criado automaticamente)
├── package.xml
├── setup.py                 ← registrar os nós aqui
├── setup.cfg
├── resource/
│   └── meu_primeiro_pacote
└── test/
```

Os arquivos `publisher.py` e `subscriber.py` vão **na mesma pasta** do `__init__.py`:

```
~/ros2_ws/src/meu_primeiro_pacote/
├── meu_primeiro_pacote/
│   ├── __init__.py
│   ├── publisher.py         ← você cria
│   └── subscriber.py        ← você cria
├── setup.py
└── ...
```

### Passo 7 — Seu primeiro Publisher (Python)

Crie o arquivo `~/ros2_ws/src/meu_primeiro_pacote/meu_primeiro_pacote/publisher.py`:

```bash
cd ~/ros2_ws/src/meu_primeiro_pacote/meu_primeiro_pacote/
nano publisher.py
```

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MeuPublisher(Node):
    def __init__(self):
        super().__init__('meu_publisher')
        self.publisher_ = self.create_publisher(String, 'meu_topico', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)  # a cada 1 segundo
        self.contador = 0

    def timer_callback(self):
        msg = String()
        msg.data = f'Olá ROS2! Mensagem #{self.contador}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publicando: {msg.data}')
        self.contador += 1

def main(args=None):
    rclpy.init(args=args)
    node = MeuPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
```

### Passo 8 — Seu primeiro Subscriber (Python)

Crie na **mesma pasta** do publisher:

```bash
nano subscriber.py
```

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MeuSubscriber(Node):
    def __init__(self):
        super().__init__('meu_subscriber')
        self.subscription = self.create_subscription(
            String, 'meu_topico', self.listener_callback, 10)

    def listener_callback(self, msg):
        self.get_logger().info(f'Recebi: {msg.data}')

def main(args=None):
    rclpy.init(args=args)
    node = MeuSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
```

### Passo 9 — Registrar os nós no setup.py

**Este passo é obrigatório!** Sem ele, o `ros2 run` não encontra os nós.

Edite o arquivo `~/ros2_ws/src/meu_primeiro_pacote/setup.py`:

```bash
nano ~/ros2_ws/src/meu_primeiro_pacote/setup.py
```

Encontre a seção `entry_points` e adicione os dois nós:

```python
entry_points={
    'console_scripts': [
        'publisher = meu_primeiro_pacote.publisher:main',
        'subscriber = meu_primeiro_pacote.subscriber:main',
    ],
},
```

### Passo 10 — Compilar e rodar

```bash
# Volte para a raiz do workspace (onde ficam as pastas src/, build/, install/)
cd ~/ros2_ws

# Compila todos os pacotes dentro de src/
# Gera as pastas build/ e install/ automaticamente
colcon build

# Carrega os pacotes compilados no terminal atual
# IMPORTANTE: precisa rodar isso em CADA terminal novo que abrir
source install/setup.bash
```

Agora abra **dois terminais** e rode:

```bash
# Terminal 1 — inicia o publisher (envia mensagens)
ros2 run meu_primeiro_pacote publisher

# Terminal 2 — inicia o subscriber (recebe mensagens)
# Lembre de rodar "source install/setup.bash" neste terminal também!
ros2 run meu_primeiro_pacote subscriber
```

> Se alterar o código, precisa compilar de novo (`colcon build`) e dar `source install/setup.bash` antes de rodar.

---

## Como tudo se conecta no ROS2

No ROS2, os **Nós** são programas independentes que se comunicam por **Tópicos**.
Pense assim: um nó **publica** uma mensagem em um tópico, e qualquer outro nó que esteja **inscrito** nesse tópico recebe a mensagem.

### Exemplo 1: O que você acabou de criar

```
 SEU PUBLISHER                    TÓPICO                     SEU SUBSCRIBER
┌─────────────────┐          ┌──────────────┐          ┌─────────────────────┐
│                  │  envia   │              │  recebe  │                     │
│  publisher.py    │ ───────> │ /meu_topico  │ ───────> │  subscriber.py      │
│                  │          │              │          │                     │
│  Gera mensagens  │          │  (canal de   │          │  Imprime mensagens  │
│  "Olá ROS2 #1"  │          │  comunicação)│          │  no terminal        │
│  "Olá ROS2 #2"  │          │              │          │                     │
└─────────────────┘          └──────────────┘          └─────────────────────┘
```

> O tópico `/meu_topico` é como um **canal de TV**:
> - O publisher é a **emissora** (transmite)
> - O subscriber é o **telespectador** (assiste)
> - Vários subscribers podem escutar o mesmo tópico ao mesmo tempo

### Exemplo 2: Robô real com vários nós

Em um robô de verdade, você teria vários nós se comunicando por diferentes tópicos:

```
┌─────────────┐     /camera/image      ┌──────────────────┐
│  Nó Câmera  │ ─────────────────────> │  Nó Detecção     │
│  (captura   │    (imagem do frame)   │  (identifica     │
│   imagens)  │                        │   objetos)       │
└─────────────┘                        └────────┬─────────┘
                                                │
                                                │ /objetos_detectados
                                                │ (lista de objetos)
                                                ▼
┌─────────────┐     /cmd_vel           ┌──────────────────┐
│  Nó Motor   │ <───────────────────── │  Nó Navegação    │
│  (gira as   │   (velocidade linear   │  (decide para    │
│   rodas)    │    e angular)          │   onde ir)       │
└─────────────┘                        └──────────────────┘
                                                ▲
                                                │ /scan
                                                │ (distância dos obstáculos)
                                                │
                                       ┌──────────────────┐
                                       │  Nó Lidar        │
                                       │  (mede distância │
                                       │   ao redor)      │
                                       └──────────────────┘
```

**Leitura do diagrama acima:**
1. O **Nó Câmera** captura imagens e publica no tópico `/camera/image`
2. O **Nó Detecção** recebe essas imagens, identifica objetos e publica no tópico `/objetos_detectados`
3. O **Nó Lidar** mede distâncias ao redor do robô e publica no tópico `/scan`
4. O **Nó Navegação** recebe dados de detecção e lidar, decide para onde ir e publica velocidade no tópico `/cmd_vel`
5. O **Nó Motor** recebe a velocidade e gira as rodas

> Cada nó é um **arquivo .py independente**, assim como o publisher.py e subscriber.py que você criou. A diferença é que em vez de `String`, eles usam tipos de mensagem específicos como `Image`, `LaserScan` e `Twist`.

---

## Próximo passo

Leia o [conceitos_avancados.md](conceitos_avancados.md) para aprender:
- Interfaces (formatos de mensagem)
- Launch Files (iniciar vários nós de uma vez)
- Parâmetros (configurar nós sem alterar código)
- Services (comunicação request/response)
- QoS (controle de confiabilidade)
- TF2 (transformações de coordenadas)
