# ROS2 — Conceitos Importantes

> Pré-requisito: leia o [readme.md](readme.md) primeiro (tutorial inicial)

---

## 1. Interfaces — os "contratos" de comunicação

No ROS2, quando um nó envia dados para outro, ambos precisam concordar sobre o **formato** dos dados. Esse formato é definido pelas **interfaces**.

Existem 3 tipos:

### 1.1 Messages (.msg) — usadas em Tópicos

Define a estrutura dos dados que trafegam em um tópico.

```
# Exemplo: std_msgs/msg/String (o que você usou no tutorial)
string data          ← apenas um campo de texto

# Exemplo: geometry_msgs/msg/Twist (usado para mover robôs)
Vector3 linear       ← velocidade em x, y, z
Vector3 angular      ← rotação em x, y, z
```

**Analogia:** é como um **formulário**. O publisher preenche os campos e envia. O subscriber recebe e sabe exatamente quais campos esperar. Se os dois lados não usarem o mesmo formulário, a comunicação não funciona.

### 1.2 Services (.srv) — usadas em Serviços

Define o **pedido** e a **resposta**, separados por `---`

```
# Exemplo: std_srvs/srv/SetBool
bool data              ← PEDIDO (true ou false)
---
bool success           ← RESPOSTA (deu certo?)
string message         ← RESPOSTA (mensagem de retorno)
```

**Analogia:** é como pedir comida em um restaurante. Você faz o **pedido** (acima do `---`) e recebe a **resposta** (abaixo do `---`).

### 1.3 Actions (.action) — usadas em Ações

Define **objetivo**, **resultado** e **feedback**, separados por `---`

```
# Exemplo: navegar até um ponto
float64 x              ← OBJETIVO (coordenada x)
float64 y              ← OBJETIVO (coordenada y)
---
bool sucesso           ← RESULTADO FINAL (chegou?)
---
float64 distancia      ← FEEDBACK (distância restante, atualizado em tempo real)
```

**Analogia:** é como pedir uma entrega. Você diz o **destino** (objetivo), recebe **atualizações de rastreio** (feedback) e no final sabe se a **entrega foi feita** (resultado).

### Comandos úteis para explorar interfaces

```bash
# Listar todas as interfaces disponíveis
ros2 interface list

# Ver os campos de uma interface
ros2 interface show std_msgs/msg/String
ros2 interface show geometry_msgs/msg/Twist
ros2 interface show std_srvs/srv/SetBool

# Listar apenas mensagens
ros2 interface list -m

# Listar apenas serviços
ros2 interface list -s
```

### Criar sua própria interface (custom message)

Para o ARARABOT, você pode criar mensagens personalizadas.

**1. Crie um pacote só para interfaces:**

```bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_cmake arara_interfaces
mkdir arara_interfaces/msg
mkdir arara_interfaces/srv
```

**2. Crie o arquivo de mensagem** `arara_interfaces/msg/AraraStatus.msg`:

```
string nome_robo
float64 bateria
bool motor_ligado
float64 velocidade
```

**3. Crie o arquivo de serviço** `arara_interfaces/srv/Comando.srv`:

```
string comando
float64 valor
---
bool sucesso
string resposta
```

**4. Configure o `CMakeLists.txt`** para gerar as interfaces:

```cmake
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/AraraStatus.msg"
  "srv/Comando.srv"
)
```

**5. Configure o `package.xml`** — adicione estas dependências:

```xml
<buildtool_depend>rosidl_default_generators</buildtool_depend>
<exec_depend>rosidl_default_runtime</exec_depend>
<member_of_group>rosidl_interface_packages</member_of_group>
```

**6. Compile e use:**

```bash
cd ~/ros2_ws
colcon build --packages-select arara_interfaces
source install/setup.bash

# Verificar se foi criada
ros2 interface show arara_interfaces/msg/AraraStatus
```

**7. Usar no seu código Python:**

```python
from arara_interfaces.msg import AraraStatus

msg = AraraStatus()
msg.nome_robo = "ARARABOT-01"
msg.bateria = 87.5
msg.motor_ligado = True
msg.velocidade = 1.2
self.publisher_.publish(msg)
```

---

## 2. Launch Files — iniciar múltiplos nós de uma vez

Em vez de abrir vários terminais, você usa um **launch file** para iniciar tudo com um único comando.

### Launch file básico

Crie a pasta e o arquivo `~/ros2_ws/src/meu_primeiro_pacote/launch/sistema.launch.py`:

```bash
mkdir -p ~/ros2_ws/src/meu_primeiro_pacote/launch
nano ~/ros2_ws/src/meu_primeiro_pacote/launch/sistema.launch.py
```

```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='meu_primeiro_pacote',
            executable='publisher',
            name='meu_publisher',
            output='screen'
        ),
        Node(
            package='meu_primeiro_pacote',
            executable='subscriber',
            name='meu_subscriber',
            output='screen'
        ),
    ])
```

### Registrar no setup.py

Adicione no `setup.py` do pacote para que o `ros2 launch` encontre o arquivo:

```python
import os
from glob import glob

# Dentro de data_files, adicione:
data_files=[
    ('share/ament_index/resource_index/packages', ['resource/meu_primeiro_pacote']),
    ('share/' + package_name, ['package.xml']),
    (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),  # ← adicione esta linha
],
```

### Rodar

```bash
cd ~/ros2_ws
colcon build
source install/setup.bash
ros2 launch meu_primeiro_pacote sistema.launch.py
```

> Isso inicia o publisher e o subscriber juntos. Pressione `Ctrl+C` para parar todos de uma vez.

### Launch file com parâmetros

```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='meu_primeiro_pacote',
            executable='publisher',
            name='publisher_rapido',
            output='screen',
            parameters=[{
                'mensagem': 'Sensor ativo',
                'frequencia': 5.0
            }]
        ),
        Node(
            package='meu_primeiro_pacote',
            executable='publisher',
            name='publisher_lento',
            output='screen',
            parameters=[{
                'mensagem': 'Bateria OK',
                'frequencia': 0.5
            }],
            remappings=[
                ('meu_topico', 'status_bateria')  # publica em outro tópico
            ]
        ),
    ])
```

> Note que você pode rodar **o mesmo executável várias vezes** com nomes e parâmetros diferentes.

---

## 3. Parâmetros — configurar nós sem alterar o código

Parâmetros são **variáveis configuráveis** que você define no código mas pode mudar pelo terminal ou launch file.

### Nó com parâmetros

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class PublisherComParametros(Node):
    def __init__(self):
        super().__init__('publisher_parametros')

        # Declara parâmetros com valores padrão
        self.declare_parameter('mensagem', 'Olá ROS2')
        self.declare_parameter('frequencia', 1.0)

        frequencia = self.get_parameter('frequencia').value
        self.publisher_ = self.create_publisher(String, 'meu_topico', 10)
        self.timer = self.create_timer(1.0 / frequencia, self.timer_callback)

    def timer_callback(self):
        mensagem = self.get_parameter('mensagem').value
        msg = String()
        msg.data = mensagem
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publicando: {msg.data}')

def main(args=None):
    rclpy.init(args=args)
    node = PublisherComParametros()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
```

### Comandos de parâmetros

```bash
# Rodar com parâmetros personalizados
ros2 run meu_primeiro_pacote publisher --ros-args -p mensagem:="Sensor ativo" -p frequencia:=5.0

# Listar parâmetros de um nó em execução
ros2 param list /publisher_parametros

# Ver valor atual de um parâmetro
ros2 param get /publisher_parametros mensagem

# Alterar parâmetro em tempo real (sem reiniciar o nó)
ros2 param set /publisher_parametros mensagem "Nova mensagem"
```

### Arquivo YAML de configuração

Para muitos parâmetros, use um arquivo YAML em vez de passar tudo pela linha de comando:

```yaml
# config/parametros.yaml
publisher_parametros:
  ros__parameters:
    mensagem: "ARARABOT operando"
    frequencia: 2.0
```

```bash
# Rodar com arquivo de configuração
ros2 run meu_primeiro_pacote publisher --ros-args --params-file config/parametros.yaml
```

---

## 4. Services — comunicação request/response

Diferente dos tópicos (fluxo contínuo), serviços são para **pedidos pontuais**: você pede, recebe a resposta, e acabou.

```
TÓPICO:   Publisher ──────────> Subscriber     (fluxo contínuo, sem resposta)
SERVIÇO:  Cliente ── pedido ──> Servidor       (pedido único, com resposta)
                  <── resposta ─┘
```

### Servidor (quem responde)

```python
import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool

class MeuServico(Node):
    def __init__(self):
        super().__init__('meu_servico')
        self.srv = self.create_service(SetBool, 'ligar_motor', self.callback)
        self.motor_ligado = False

    def callback(self, request, response):
        self.motor_ligado = request.data
        estado = "LIGADO" if self.motor_ligado else "DESLIGADO"
        response.success = True
        response.message = f'Motor {estado}'
        self.get_logger().info(f'Motor {estado}')
        return response

def main(args=None):
    rclpy.init(args=args)
    node = MeuServico()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
```

### Cliente (quem pede)

```python
import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool

class MeuCliente(Node):
    def __init__(self):
        super().__init__('meu_cliente')
        self.client = self.create_client(SetBool, 'ligar_motor')
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Aguardando serviço...')

    def enviar_pedido(self, ligar):
        request = SetBool.Request()
        request.data = ligar
        future = self.client.call_async(request)
        return future

def main(args=None):
    rclpy.init(args=args)
    node = MeuCliente()
    future = node.enviar_pedido(True)  # Liga o motor
    rclpy.spin_until_future_complete(node, future)
    resultado = future.result()
    node.get_logger().info(f'Resposta: {resultado.message}')
    node.destroy_node()
    rclpy.shutdown()
```

### Testar via CLI

```bash
# Terminal 1: rodar o servidor
ros2 run meu_primeiro_pacote servico

# Terminal 2: chamar o serviço sem precisar do cliente
ros2 service call /ligar_motor std_srvs/srv/SetBool "{data: true}"
ros2 service call /ligar_motor std_srvs/srv/SetBool "{data: false}"
```

---

## 5. QoS (Quality of Service) — controle de confiabilidade

QoS define **como** as mensagens são entregues. Importante quando você tem sensores rápidos ou rede instável.

### Dois perfis principais

| Perfil | Quando usar | Comportamento |
|--------|-------------|---------------|
| `RELIABLE` | Comandos, configurações | **Garante** que a mensagem chegou. Se perder, reenvia |
| `BEST_EFFORT` | Sensores, câmera, lidar | **Prioriza velocidade**. Se perder uma mensagem, ignora e segue |

### Exemplo no código

```python
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

# Para sensores (aceita perder mensagens antigas, prioriza as novas)
sensor_qos = QoSProfile(
    reliability=ReliabilityPolicy.BEST_EFFORT,
    history=HistoryPolicy.KEEP_LAST,
    depth=5
)

# Para comandos críticos (garante entrega)
comando_qos = QoSProfile(
    reliability=ReliabilityPolicy.RELIABLE,
    history=HistoryPolicy.KEEP_LAST,
    depth=10
)

# Usar no publisher
self.publisher_ = self.create_publisher(String, 'sensor_data', sensor_qos)

# Usar no subscriber (deve ser compatível com o publisher)
self.subscription = self.create_subscription(String, 'sensor_data', self.callback, sensor_qos)
```

> **Regra importante:** o QoS do subscriber deve ser **compatível** com o do publisher. Um subscriber `RELIABLE` **não** consegue receber de um publisher `BEST_EFFORT`.

### Verificar QoS de um tópico ativo

```bash
ros2 topic info /sensor_data --verbose
```

---

## 6. TF2 — Transformações de Coordenadas

TF2 responde a pergunta: **"onde está cada parte do robô em relação às outras?"**

### Por que é importante?

Imagine que o lidar detecta um obstáculo a 2 metros de distância. Mas o lidar está montado na **frente** do robô. O centro do robô está 30cm **atrás** do lidar. Para o nó de navegação calcular corretamente, ele precisa saber a posição do obstáculo em relação ao **centro** do robô, não ao lidar.

TF2 faz essa conversão automaticamente.

### Conceito: árvore de frames

```
          base_link (centro do robô)
          ├── lidar_link (30cm à frente)
          ├── camera_link (20cm acima)
          └── roda_esquerda_link
              roda_direita_link
```

Cada "link" é um ponto de referência. O TF2 sabe a relação entre todos eles.

### Publicar uma transformação estática

Para relações fixas (o lidar está sempre no mesmo lugar do robô):

```bash
# Lidar está 30cm à frente e 10cm acima do centro do robô
ros2 run tf2_ros static_transform_publisher 0.3 0 0.1 0 0 0 base_link lidar_link
```

### Ver a árvore de transformações

```bash
# Instalar ferramentas de visualização
sudo apt install -y ros-jazzy-tf2-tools

# Gerar diagrama da árvore
ros2 run tf2_tools view_frames

# Ver transformação entre dois frames
ros2 run tf2_ros tf2_echo base_link lidar_link
```

---

## Resumo: quando usar cada coisa

```
┌────────────────────┬────────────────────────────────────────┐
│  Conceito          │  Quando usar                           │
├────────────────────┼────────────────────────────────────────┤
│  Tópico            │  Dados contínuos (sensor, câmera)      │
│  Serviço           │  Pedido pontual (ligar/desligar algo)  │
│  Action            │  Tarefa longa com feedback (navegar)   │
│  Interface         │  Definir formato dos dados              │
│  Parâmetro         │  Configurar nó sem recompilar          │
│  Launch File       │  Iniciar vários nós de uma vez         │
│  QoS               │  Controlar confiabilidade da entrega   │
│  TF2               │  Saber posição das partes do robô      │
└────────────────────┴────────────────────────────────────────┘
```

---

## Roadmap de Aprendizado

```
[Básico]  Nodes, Topics, Publisher/Subscriber ✅  ← readme.md
      │
      ▼
[Intermediário]  Interfaces, Launch Files, Parâmetros,  ← você está aqui
                 Services, QoS, TF2
      │
      ▼
[Avançado]  Escolha conforme seu projeto:
      │
      ├── Nav2 ─────────── navegação autônoma
      ├── MoveIt2 ──────── controle de braços robóticos
      ├── Gazebo ────────── simulação 3D de robôs
      └── micro-ROS ────── ROS2 em microcontroladores (ESP32, STM32)
```
