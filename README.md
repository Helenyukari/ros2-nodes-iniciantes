# ROS2 Nodes — Tutoriais ARARABOTS

Repositório de **estudo e onboarding** para quem está entrando no time ARARABOTS e nunca mexeu com ROS2.
Aqui você aprende os conceitos básicos antes de encarar o código do `ssl-VICE` (sistema do robô de futebol).

---

## Por onde começar

Leia os tutoriais nessa ordem:

1. **[tutorial_ros2.md](tutorial_ros2.md)** — o que é ROS2, conceitos (nodes, topics, messages), como instalar e criar seu primeiro pacote.
2. **[conceitos_avancados.md](conceitos_avancados.md)** — interfaces, launch files, parâmetros, services, QoS e TF2.
3. **[meu_primeiro_pacote/](meu_primeiro_pacote/)** — pacote ROS2 com exemplos prontos (publisher, subscriber, classificador). Veja o [README do pacote](meu_primeiro_pacote/README.md) para rodar.

---

## Estrutura do repositório

```
ROS2_nodes/
├── tutorial_ros2.md            ← tutorial inicial (comece aqui)
├── conceitos_avancados.md      ← conceitos além do básico
├── meu_primeiro_pacote/        ← pacote ROS2 de exemplo (Python)
│   ├── meu_primeiro_pacote/    ← código dos nodes
│   ├── setup.py                ← registra os nodes (entry_points)
│   └── package.xml             ← metadados e dependências ROS2
└── build/, install/, log/      ← gerados pelo colcon (não versionar)
```

> As pastas `build/`, `install/` e `log/` aparecem depois do primeiro `colcon build` e estão no `.gitignore`. Não tente versioná-las.

---

## Pré-requisitos

- **Linux Ubuntu 22.04** (recomendado) ou WSL2 no Windows
- **ROS2 Humble** instalado (passo a passo no [tutorial_ros2.md](tutorial_ros2.md))
- **Python 3.10+** (vem com o Ubuntu 22.04)

---

## Quer explorar mais?

Documentação oficial do ROS2 Humble: **[docs.ros.org/en/humble](https://docs.ros.org/en/humble/index.html)**

Lá você encontra tutoriais avançados, referência de API (`rclpy`, `rclcpp`), guia de pacotes oficiais (`nav2`, `moveit`, etc.) e troubleshooting. Sempre confira que está navegando na seção da distro **Humble** — a doc tem versões para outras distros e os comandos podem diferir.
