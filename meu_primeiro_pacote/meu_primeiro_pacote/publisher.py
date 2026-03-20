# Publisher básico - envia mensagens de texto no tópico /meu_topico a cada 1s

# =====================================================
# IMPORTS - Bibliotecas necessárias
# =====================================================

# rclpy = ROS Client Library for Python
# É a biblioteca principal que conecta seu código Python ao ROS2
import rclpy

# Node é a classe base - todo node ROS2 herda dela
# Um Node é como um "programa independente" dentro do ROS2
from rclpy.node import Node

# String é o tipo de mensagem que vamos publicar
# ROS2 tem vários tipos prontos: String, Int32, Float64, Bool, etc.
# Todos ficam em std_msgs.msg (mensagens padrão)
from std_msgs.msg import String


# =====================================================
# CLASSE DO NODE
# =====================================================

class MeuPublisher(Node):
    """Publisher que envia mensagens no tópico /meu_topico a cada 1 segundo."""

    def __init__(self):
        # super().__init__('nome_do_node') registra este node no ROS2
        # O nome 'meu_publisher' é como outros nodes vão identificar este
        # IMPORTANTE: o nome deve ser único na rede ROS2
        super().__init__('meu_publisher')

        # ---- Criando o Publisher ----
        # create_publisher(TipoMsg, 'nome_do_topico', tamanho_da_fila)
        #   - String: tipo da mensagem (importado acima)
        #   - 'meu_topico': nome do tópico onde as mensagens serão publicadas
        #   - 10: tamanho da fila (quantas mensagens guardar se o subscriber estiver lento)
        self.publisher_ = self.create_publisher(String, 'meu_topico', 10)

        # ---- Criando o Timer ----
        # create_timer(periodo_segundos, funcao_callback)
        #   - 1.0: executa a cada 1 segundo
        #   - self.timer_callback: função que será chamada a cada intervalo
        self.timer = self.create_timer(1.0, self.timer_callback)

        # Variável para contar quantas mensagens já enviamos
        self.contador = 0

        # Mostra no terminal que o node iniciou
        # get_logger().info() é como um print(), mas formatado para ROS2
        self.get_logger().info('Publisher iniciado! Publicando em /meu_topico')

    def timer_callback(self):
        """Função chamada automaticamente pelo timer a cada 1 segundo."""

        # 1. Cria uma mensagem vazia do tipo String
        msg = String()

        # 2. Preenche o campo 'data' da mensagem com o texto
        #    Cada tipo de mensagem tem seus campos específicos
        #    String tem apenas o campo 'data' (texto)
        msg.data = f'Ola ROS2! Mensagem #{self.contador}'

        # 3. Publica a mensagem no tópico
        #    Todos os subscribers inscritos em '/meu_topico' vão receber
        self.publisher_.publish(msg)

        # 4. Mostra no terminal o que foi publicado (para debug)
        self.get_logger().info(f'Publicando: {msg.data}')

        # 5. Incrementa o contador para a próxima mensagem
        self.contador += 1


# =====================================================
# FUNÇÃO MAIN - Ponto de entrada do programa
# =====================================================

def main(args=None):
    # 1. Inicializa o sistema ROS2
    #    Deve ser chamado ANTES de criar qualquer node
    rclpy.init(args=args)

    # 2. Cria uma instância do nosso node
    node = MeuPublisher()

    try:
        # 3. spin() mantém o node vivo e processando
        #    Sem isso, o programa terminaria imediatamente
        #    O spin fica em loop esperando eventos (timers, mensagens, etc.)
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass  # Ctrl+C para parar - comportamento normal
    finally:
        # 4. Limpeza: destrói o node e encerra o ROS2
        #    Sempre faça isso para liberar recursos
        node.destroy_node()
        rclpy.shutdown()


# Permite rodar o arquivo diretamente com: python3 publisher.py
if __name__ == '__main__':
    main()
