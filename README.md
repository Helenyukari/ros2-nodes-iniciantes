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

## Fluxo geral de quem está chegando

1. Lê o `tutorial_ros2.md` e instala o ROS2.
2. Clona este repo dentro de `~/ros2_ws/src/` (o workspace ROS2 padrão).
3. Compila com `colcon build` na raiz do workspace.
4. Roda os exemplos do `meu_primeiro_pacote` para ver publishers e subscribers em ação.
5. Lê o `conceitos_avancados.md` quando quiser entender interfaces customizadas, services e launch files.

---

## Convenções do repositório

- **Idioma:** português nos comentários e docs (é o idioma do time).
- **Nomes de nodes:** `snake_case` (ex.: `random_publisher`, `web_bridge`).
- **Nomes de tópicos:** `snake_case` sem barra inicial no código (`random_number`), o ROS2 adiciona o `/` automaticamente.
- **Tipos de mensagem:** sempre que possível use os de `std_msgs` ou `geometry_msgs` antes de criar uma interface custom.
