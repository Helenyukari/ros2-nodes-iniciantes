"""
=== TUTORIAL: Subscriber Básico em ROS2 ===

O que este node faz:
  - Cria um "subscriber" (assinante) que RECEBE mensagens de texto
  - Escuta o tópico '/meu_topico' e mostra no terminal o que recebeu

Conceitos que você vai aprender:
  1. Como criar um Subscriber para receber dados
  2. Como funciona o callback (função chamada quando chega uma mensagem)
  3. Como Publisher e Subscriber se comunicam pelo tópico

Como rodar:
  Terminal 1: ros2 run meu_primeiro_pacote publisher    (envia as mensagens)
  Terminal 2: ros2 run meu_primeiro_pacote subscriber   (recebe as mensagens)

  IMPORTANTE: Rode o subscriber PRIMEIRO ou ao mesmo tempo que o publisher!

Diagrama:
  [publisher] ---String---> /meu_topico ---String---> [subscriber] <-- VOCÊ ESTÁ AQUI
"""

# =====================================================
# IMPORTS
# =====================================================

import rclpy
from rclpy.node import Node
from std_msgs.msg import String  # Mesmo tipo que o publisher usa!


# =====================================================
# CLASSE DO NODE
# =====================================================

class MeuSubscriber(Node):
    """Subscriber que escuta mensagens do tópico /meu_topico."""

    def __init__(self):
        # Registra o node com nome 'meu_subscriber'
        super().__init__('meu_subscriber')

        # ---- Criando o Subscriber ----
        # create_subscription(TipoMsg, 'nome_do_topico', callback, tamanho_fila)
        #   - String: tipo da mensagem esperada (deve ser IGUAL ao do publisher!)
        #   - 'meu_topico': nome do tópico para escutar (deve ser IGUAL ao do publisher!)
        #   - self.listener_callback: função chamada quando chega uma mensagem
        #   - 10: tamanho da fila de mensagens pendentes
        #
        # NOTA: o tópico conecta publisher e subscriber pelo NOME
        #       Se o nome for diferente, eles não se comunicam!
        self.subscription = self.create_subscription(
            String,
            'meu_topico',
            self.listener_callback,
            10
        )

        self.get_logger().info('Subscriber iniciado! Escutando /meu_topico')

    def listener_callback(self, msg):
        """
        Callback = função chamada AUTOMATICAMENTE quando uma mensagem chega.

        Parâmetros:
          - self: referência ao próprio objeto (padrão Python)
          - msg: a mensagem recebida (tipo String neste caso)

        O ROS2 chama esta função para cada mensagem que chega no tópico.
        Você NÃO precisa chamar esta função manualmente!
        """
        # msg.data contém o texto que o publisher enviou
        self.get_logger().info(f'Recebi: {msg.data}')


# =====================================================
# FUNÇÃO MAIN
# =====================================================

def main(args=None):
    # Mesma estrutura do publisher:
    # 1. Inicializa o ROS2
    rclpy.init(args=args)

    # 2. Cria o node
    node = MeuSubscriber()

    try:
        # 3. spin() fica esperando mensagens chegarem
        #    Quando uma mensagem chega, o spin chama o listener_callback
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        # 4. Limpeza
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
