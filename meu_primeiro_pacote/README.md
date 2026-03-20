# meu_primeiro_pacote

Pacote ROS2 de estudo com exemplos básicos de comunicação por tópicos.

## Nodes

| Node | Tipo | Tópico | Descrição |
|------|------|--------|-----------|
| `publisher` | Publisher (String) | `/meu_topico` | Envia mensagens de texto a cada 1s |
| `subscriber` | Subscriber (String) | `/meu_topico` | Recebe e exibe as mensagens de texto |
| `random_publisher` | Publisher (Int32) | `/random_number` | Publica números aleatórios de 0 a 100 |
| `number_classifier` | Subscriber (Int32) | `/random_number` | Classifica os números como par ou ímpar |

## Como rodar

```bash
# Compilar (na raiz do workspace)
cd ~/ros2_ws
colcon build
source install/setup.bash

# Exemplo 1: Publisher + Subscriber de texto
ros2 run meu_primeiro_pacote publisher       # Terminal 1
ros2 run meu_primeiro_pacote subscriber      # Terminal 2

# Exemplo 2: Números aleatórios + Classificador
ros2 run meu_primeiro_pacote random_publisher    # Terminal 1
ros2 run meu_primeiro_pacote number_classifier   # Terminal 2
```

> Lembre de rodar `source install/setup.bash` em cada terminal novo.
