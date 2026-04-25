# meu_primeiro_pacote

Pacote ROS2 de **estudo** com exemplos básicos de comunicação por tópicos.
Usado para o onboarding de novos membros do ARARABOTS.

> Pré-requisito: ter feito a instalação do ROS2 conforme o [tutorial_ros2.md](../tutorial_ros2.md).

---

## Nodes disponíveis

| Node | Tipo | Tópico | O que faz |
|------|------|--------|-----------|
| `publisher` | Publisher (`String`) | `/meu_topico` | Envia uma mensagem de texto a cada 1s |
| `subscriber` | Subscriber (`String`) | `/meu_topico` | Recebe e imprime as mensagens de texto |
| `random_publisher` | Publisher (`Int32`) | `/random_number` | Publica números aleatórios entre 0 e 100 |
| `number_classifier` | Subscriber (`Int32`) | `/random_number` | Classifica os números como **par** ou **ímpar** |

Cada node está em [meu_primeiro_pacote/](meu_primeiro_pacote/) e é registrado em [setup.py](setup.py) na seção `entry_points`.

---

## Como rodar

### 1. Compilar o pacote

Os comandos abaixo são rodados **na raiz do workspace ROS2** (geralmente `~/ros2_ws/`), não dentro do pacote.

```bash
cd ~/ros2_ws
colcon build
source install/setup.bash
```

### 2. Rodar os exemplos

Cada node é iniciado em um terminal separado. **Em cada terminal novo, rode `source install/setup.bash` antes do `ros2 run`.**

```bash
# Exemplo 1: Publisher + Subscriber de texto
ros2 run meu_primeiro_pacote publisher       # Terminal 1
ros2 run meu_primeiro_pacote subscriber      # Terminal 2

# Exemplo 2: Números aleatórios + Classificador
ros2 run meu_primeiro_pacote random_publisher    # Terminal 1
ros2 run meu_primeiro_pacote number_classifier   # Terminal 2
```

---

## Por que esses comandos?

Quem nunca mexeu com ROS2 fica perdido com tanto comando. Aqui vai o **porquê de cada um**:

### `colcon build`
Compila **todos os pacotes** dentro de `~/ros2_ws/src/`. É o "build system" oficial do ROS2.
- Lê o `package.xml` e `setup.py` de cada pacote.
- Gera as pastas `build/` (artefatos intermediários) e `install/` (versão "instalada" pronta para usar).
- Você precisa rodar de novo **toda vez que alterar o código** ou adicionar/renomear um node em `setup.py`.

> Dica: rodar `colcon build --packages-select meu_primeiro_pacote` compila só esse pacote, mais rápido em workspaces grandes.

### `source install/setup.bash`
"Carrega" o pacote compilado no terminal atual. Sem isso, o `ros2 run` não acha seus nodes.
- Adiciona os executáveis do `install/` ao `PATH`.
- Adiciona os módulos Python do pacote ao `PYTHONPATH`.
- **É por sessão de terminal:** cada terminal novo precisa do seu próprio `source`. Se abriu 3 terminais, são 3 `source install/setup.bash`.
- Para automatizar, você pode adicionar a linha no `~/.bashrc`, mas no início é melhor rodar manual para entender o que está acontecendo.

### `ros2 run <pacote> <node>`
Executa um node registrado no `entry_points` do `setup.py`.
- `<pacote>` é o nome em `setup.py` (`meu_primeiro_pacote`).
- `<node>` é a chave do `entry_points` (ex.: `publisher`, `random_publisher`).
- Se errar o nome, dá erro `No executable found`. Confira em [setup.py](setup.py#L21-L29).

### `ros2 topic list` / `ros2 topic echo /meu_topico`
Comandos de **debug**, úteis quando algo não funciona.
- `ros2 topic list` mostra todos os tópicos ativos no momento.
- `ros2 topic echo /meu_topico` imprime as mensagens publicadas em `/meu_topico` em tempo real (faz o papel de um "subscriber genérico" no terminal).
- Se o publisher está rodando mas o tópico não aparece em `ros2 topic list`, provavelmente esqueceu o `source install/setup.bash`.

---

## Fluxo de desenvolvimento (loop típico)

Quando você está mexendo no código e quer testar:

```bash
# 1. Edita o arquivo .py em meu_primeiro_pacote/meu_primeiro_pacote/

# 2. Recompila (na raiz do workspace)
cd ~/ros2_ws
colcon build --packages-select meu_primeiro_pacote

# 3. Re-source (ou abra terminal novo)
source install/setup.bash

# 4. Roda de novo
ros2 run meu_primeiro_pacote publisher
```

> Esqueceu o `colcon build` depois de editar? O `ros2 run` vai rodar a **versão antiga**. É a pegadinha mais comum de quem está começando.

---

## Adicionando um novo node

1. Crie o arquivo em `meu_primeiro_pacote/meu_primeiro_pacote/meu_node.py` com uma função `main()`.
2. Registre em [setup.py](setup.py#L21-L29):
   ```python
   entry_points={
       'console_scripts': [
           # ... os existentes ...
           'meu_node = meu_primeiro_pacote.meu_node:main',
       ],
   },
   ```
3. Recompile:
   ```bash
   cd ~/ros2_ws && colcon build --packages-select meu_primeiro_pacote && source install/setup.bash
   ```
4. Rode: `ros2 run meu_primeiro_pacote meu_node`.
