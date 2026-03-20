# Publisher de estudo - publica números aleatórios (Int32) no tópico /random_number
# Funciona em dupla com o number_classifier.py

import rclpy
from rclpy.node import Node

# Int32 = número inteiro de 32 bits (range: -2.147.483.648 a 2.147.483.647)
# Diferente do tutorial básico que usa String, aqui usamos um tipo numérico
# Outros tipos disponíveis: Int64, Float32, Float64, Bool, etc.
from std_msgs.msg import Int32

# Biblioteca padrão do Python para gerar números aleatórios
import random


class RandomPublisher(Node):
    """Publica números inteiros aleatórios no tópico /random_number."""

    def __init__(self):
        super().__init__('random_publisher')

        # Publisher de Int32 (número inteiro) no tópico 'random_number'
        # Parâmetros: (tipo_mensagem, nome_topico, tamanho_fila)
        self.publisher_ = self.create_publisher(Int32, 'random_number', 10)

        # Timer que dispara a cada 1 segundo
        # A cada disparo, chama self.timer_callback
        self.timer = self.create_timer(1.0, self.timer_callback)

        self.get_logger().info('Random Publisher iniciado! Publicando em /random_number')

    def timer_callback(self):
        """Gera e publica um número aleatório entre 0 e 100."""
        msg = Int32()

        # random.randint(a, b) retorna um inteiro N tal que a <= N <= b
        msg.data = random.randint(0, 100)

        # Publica no tópico - o number_classifier vai receber
        self.publisher_.publish(msg)

        # Log para acompanhar no terminal
        self.get_logger().info(f'Publicando numero aleatorio: {msg.data}')


def main(args=None):
    rclpy.init(args=args)
    node = RandomPublisher()

    try:
        rclpy.spin(node)  # Mantém o node rodando e publicando
    except KeyboardInterrupt:
        pass  # Ctrl+C para parar
    finally:
        # Limpeza: destrói o node e encerra o rclpy
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
