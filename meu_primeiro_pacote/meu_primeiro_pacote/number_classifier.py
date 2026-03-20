# Subscriber de estudo - recebe números do /random_number e classifica como par/ímpar
# Funciona em dupla com o random_publisher.py

import rclpy
from rclpy.node import Node

# Int32 - deve ser o MESMO tipo que o random_publisher publica
# Se os tipos forem diferentes, a comunicação não funciona!
from std_msgs.msg import Int32


class NumberClassifier(Node):
    """Subscriber que recebe números e classifica como par ou ímpar."""

    def __init__(self):
        super().__init__('number_classifier')

        # Cria subscriber no tópico 'random_number'
        # Parâmetros: (tipo_msg, nome_topico, callback, tamanho_fila)
        # O callback é chamado automaticamente quando chega um número
        self.subscription = self.create_subscription(
            Int32,
            'random_number',
            self.listener_callback,
            10
        )

        self.get_logger().info('Number Classifier iniciado! Escutando /random_number')

    def listener_callback(self, msg):
        """
        Callback que processa cada número recebido.

        Aqui está a diferença do subscriber básico:
        em vez de só imprimir, fazemos LÓGICA com o dado.
        """
        number = msg.data

        # Operador módulo (%) retorna o resto da divisão
        # Se o resto da divisão por 2 for 0, o número é par
        if number % 2 == 0:
            self.get_logger().info(f'O numero {number} e PAR')
        else:
            self.get_logger().info(f'O numero {number} e IMPAR')


def main(args=None):
    # Inicializa o ROS2
    rclpy.init(args=args)

    # Cria o node classificador
    node = NumberClassifier()

    try:
        # spin() mantém o node vivo, esperando mensagens
        # Quando chega uma mensagem, chama o listener_callback
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
