# Strategy — Árvore de Decisão do ssl-VICE

Este documento explica como funciona o sistema de estratégia do ssl-VICE, desde a inicialização até os comandos enviados aos robôs.

---

## Visão Geral

O sistema de estratégia usa uma **Behaviour Tree** (árvore de comportamento) que roda a **10Hz** (a cada 0.1 segundo). A cada ciclo, a árvore percorre seus nós de cima para baixo e decide o que cada robô deve fazer.

```
┌─────────────────────────────────────────────────────────────┐
│                      strategy_node                          │
│                                                             │
│   A cada 0.1s executa root.run()                            │
│   Recebe (status, lista de Skills)                          │
│   Envia Skills para os robôs via ROS2 Services              │
│                                                             │
│   Services usados:                                          │
│   ├── strategy_command  → posição e velocidade              │
│   ├── set_orientation   → ângulo do robô                    │
│   ├── update_obstacles  → obstáculos a desviar              │
│   └── update_kick       → ativar/desativar chute            │
└─────────────────────────────────────────────────────────────┘
```

---

## Arquitetura em Camadas

O sistema é dividido em 3 camadas. Cada uma tem uma responsabilidade:

```
┌──────────────────────────────────────────────────────┐
│  PLAYS (plays/)                                      │
│  "QUANDO fazer?"                                     │
│                                                      │
│  Monta a árvore de decisão. Verifica o estado do     │
│  jogo (referee) e decide qual jogada executar.        │
│                                                      │
│  Arquivos: halt.py, stop.py, running.py,             │
│            kickoff.py, freekick.py                    │
└──────────────────────┬───────────────────────────────┘
                       │ chama
                       ▼
┌──────────────────────────────────────────────────────┐
│  TACTICS (tatics/)                                   │
│  "O QUE fazer?"                                      │
│                                                      │
│  Lógica de equipe. Define como os robôs se           │
│  posicionam e coordenam (ataque, defesa, goleiro).   │
│                                                      │
│  Arquivos: running.py (Atack, Defense),              │
│            goalkeeper.py, halt.py, stop.py,           │
│            kickoff.py, freekick.py                    │
└──────────────────────┬───────────────────────────────┘
                       │ gera
                       ▼
┌──────────────────────────────────────────────────────┐
│  SKILLS (skills/)                                    │
│  "COMO fazer?"                                       │
│                                                      │
│  Comandos individuais para cada robô.                │
│  Cada Skill contém: posição alvo, velocidade,        │
│  ângulo, obstáculos e estado do chute.               │
│                                                      │
│  Arquivo: skills.py (Skill, Skills)                  │
└──────────────────────────────────────────────────────┘
```

---

## Árvore de Decisão Completa

### Como ler a árvore

- **Selector** (tenta cada filho até um dar SUCCESS — como um "OU")
- **Sequence** (executa cada filho em ordem, para se um der FAILURE — como um "E")
- **LeafNode** (nó folha — executa uma verificação ou ação)
- Retornos possíveis: `SUCCESS`, `FAILURE`, `RUNNING`

### Árvore raiz

```
RootTree (Selector) ─── tenta cada play na ordem, executa o primeiro que funcionar
│
├── 1. Stop
├── 2. Halt
├── 3. Kickoff
├── 4. Freekick
└── 5. NormalStart
```

> A **ordem importa**: Stop e Halt têm prioridade sobre tudo. Se o referee mandar parar, o jogo para independente do que estava acontecendo.

---

### 1. Stop — Referee mandou parar

```
Stop (Sequence)
│
├── CheckState ─── referee mandou "STOP"?
│   │               ├── SIM → SUCCESS (continua)
│   │               └── NÃO → FAILURE (pula para próximo play)
│   │
└── Selector ─── decide o que fazer
    │
    ├── Sequence
    │   ├── CheckDistance ─── robô está longe da bola (>500mm)?
    │   │                     ├── SIM → SUCCESS
    │   │                     └── NÃO → FAILURE
    │   └── KeepPosition ─── fica parado onde está
    │
    └── GetoffBall ─── afasta da bola (está perto demais)
```

**Lógica:** Se o referee mandou STOP → verifica se está longe da bola. Se sim, fica parado. Se não, se afasta.

---

### 2. Halt — Parada total

```
Halt (Sequence)
│
├── checkState ─── referee mandou "HALT"?
│                   ├── SIM → SUCCESS
│                   └── NÃO → FAILURE
│
└── HaltAction ─── para todos os robôs imediatamente (velocidade 0)
```

**Lógica:** Halt = emergência. Para tudo.

---

### 3. Kickoff — Saída de bola

```
Kickoff (Sequence)
│
├── CheckState ─── é situação de kickoff?
│                   (PREPARE_KICKOFF_OURS ou PREPARE_KICKOFF_THEIRS)
│
└── Selector
    │
    ├── Sequence
    │   ├── CheckIfOurKickoff ─── é NOSSO kickoff?
    │   │                         ├── SIM → SUCCESS
    │   │                         └── NÃO → FAILURE
    │   └── OurKickoffAction ─── executa nossa saída de bola
    │
    └── TheirKickoffAction ─── defende saída de bola deles
```

**Lógica:** Se é kickoff → verifica se é nosso ou deles → executa a tática correspondente.

---

### 4. Freekick — Falta

```
Freekick (Sequence)
│
├── CheckState ─── é situação de falta?
│                   (DIRECT_FREE_OURS ou DIRECT_FREE_THEIRS)
│
└── Selector
    │
    ├── Sequence
    │   ├── CheckIfOurFreekick ─── é NOSSA falta?
    │   └── OurFreekickAction ─── cobra a falta
    │
    └── TheirFreekickAction ─── defende a falta deles
```

---

### 5. NormalStart — Jogo em andamento (principal)

```
NormalStart (Sequence)
│
├── CheckState ─── jogo está rodando?
│                   (FORCE_START ou NORMAL_START)
│
└── Selector ─── decide entre atacar ou defender
    │
    ├── Sequence
    │   ├── CheckAtack ─── bola está no nosso campo?
    │   │                   (verifica posição da bola vs border_circle)
    │   │                   ├── SIM → SUCCESS (podemos atacar)
    │   │                   └── NÃO → FAILURE
    │   │
    │   └── AtackAction ─── executa tática de ATAQUE
    │                        (ver detalhes abaixo)
    │
    └── DefenseAction ─── executa tática de DEFESA
                           (bola está no campo deles)
```

**Lógica:** Se o jogo está rolando → verifica se a bola está no nosso campo. Se sim, ataca. Se não, defende.

---

## Detalhes das Táticas

### Ataque (tatics/running.py → Atack)

O ataque funciona assim para cada robô (exceto goleiro):

```
┌─────────────────────────────────────────────────────────────┐
│                    FLUXO DO ATAQUE                          │
│                                                             │
│  Para cada robô (exceto goleiro id=0):                      │
│                                                             │
│  1. Calcular ponto "atrás da bola"                          │
│     (70mm atrás, na linha bola→gol adversário)              │
│                                                             │
│  2. Robô está perto (<230mm)?                               │
│     │                                                       │
│     ├── NÃO → _go_to_ball()                                 │
│     │   - Move até o ponto atrás da bola                    │
│     │   - Alinha ângulo na direção do gol                   │
│     │   - Bola tratada como obstáculo (não toca ainda)      │
│     │                                                       │
│     └── SIM → _do_push()                                    │
│         - Avança 220mm à frente da bola (direção do gol)    │
│         - Empurra a bola                                    │
│         - Se pode chutar (bola perto do gol) → ativa kick   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

```
                    GOL ADVERSÁRIO
                    ┌───────────┐
                    │           │
                    └─────┬─────┘
                          │
            ux,uy         │  direção do empurrão
           (unitário)     │
                          │
                     ●────┘  ← push target (220mm à frente)
                     │
                   ⚽ bola
                     │
                     ● ← stage point (70mm atrás)
                     │
                   🤖 robô se posiciona aqui primeiro
```

### Defesa (tatics/running.py → Defense)

```
┌─────────────────────────────────────────────────────────────┐
│                    FLUXO DA DEFESA                          │
│                                                             │
│  Para cada robô (exceto goleiro):                           │
│                                                             │
│  1. Calcular ponto médio entre bola e nosso gol             │
│     defend_x = (bola.x + gol.x) / 2                        │
│     defend_y = (bola.y + gol.y) / 2                         │
│                                                             │
│  2. Move robô para esse ponto médio                         │
│     (fica entre a bola e o gol, bloqueando o caminho)       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

```
     NOSSO GOL                              ⚽ bola
     ┌───────┐                               │
     │       │          🤖 ← robô defensor   │
     └───────┘          (ponto médio)         │
                                              │
                   ←─────────────────────────→
                        o robô fica aqui,
                     entre o gol e a bola
```

### Goleiro (tatics/goalkeeper.py → Goalkeeper)

```
┌─────────────────────────────────────────────────────────────┐
│                    FLUXO DO GOLEIRO                          │
│                                                             │
│  Bola está na área do gol?                                  │
│  │                                                          │
│  ├── NÃO → Posiciona no centro do gol                      │
│  │         - x = posição do gol                             │
│  │         - y = posição y da bola (limitado a ±400mm)      │
│  │         - Acompanha a bola lateralmente                  │
│  │                                                          │
│  └── SIM → Modo "expulsão da bola"                          │
│       │                                                     │
│       ├── Longe da bola → posiciona atrás dela              │
│       │   (mesmo padrão do ataque: stage point)             │
│       │                                                     │
│       └── Perto da bola → empurra para fora da área         │
│           (push na direção gol → fora)                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

```
     NOSSO GOL
     ┌───────────┐
     │           │
     │  🤖──→⚽──→  ← goleiro empurra bola para fora
     │           │
     └───────────┘

     Modo normal (bola longe):
     ┌───────────┐
     │    🤖     │  ← goleiro acompanha Y da bola
     │     ↕     │     (limitado a ±400mm)
     └───────────┘
```

---

## Estrutura de Arquivos

```
strategy/
├── strategy.py          ← Nó principal ROS2 (executa a árvore a 10Hz)
├── behaviour.py         ← Framework da Behaviour Tree
│                          (TaskStatus, LeafNode, TreeNode, Sequence, Selector)
├── root.py              ← Monta a árvore raiz (RootTree)
│
├── plays/               ← QUANDO fazer (verificam estado do jogo)
│   ├── halt.py          ← Play: parada total
│   ├── stop.py          ← Play: parar e afastar da bola
│   ├── running.py       ← Play: jogo normal (ataque/defesa)
│   ├── kickoff.py       ← Play: saída de bola
│   └── freekick.py      ← Play: falta
│
├── tatics/              ← O QUE fazer (lógica de equipe)
│   ├── running.py       ← Atack: empurra bola ao gol
│   │                      Defense: bloqueia caminho ao gol
│   ├── goalkeeper.py    ← Goleiro: protege gol + expulsa bola
│   ├── halt.py          ← Para todos os robôs
│   ├── stop.py          ← Afasta da bola
│   ├── kickoff.py       ← Posicionamento de kickoff
│   └── freekick.py      ← Posicionamento de falta
│
└── skills/              ← COMO fazer (comandos individuais)
    └── skills.py        ← Skill: comando para 1 robô
                           Skills: fábrica de comandos
                           (move_to, move_with_angle, set_orientation,
                            obstacles, stop, activate_kick)
```

---

## Fluxo Completo (do referee ao robô)

```
1. REFEREE envia comando (STOP, HALT, NORMAL_START, etc.)
         │
         ▼
2. Tópico ROS2 "game_state" distribui para os LeafNodes
         │
         ▼
3. ÁRVORE DE DECISÃO percorre os plays
   Stop → Halt → Kickoff → Freekick → NormalStart
         │
         ▼
4. PLAY ativo verifica condições (CheckState, CheckAtack, etc.)
         │
         ▼
5. TÁTICA correspondente é executada (Atack, Defense, Goalkeeper)
         │
         ▼
6. TÁTICA gera lista de SKILLS (1 por robô)
   Skill = {robot_id, target_x, target_y, angle, kick, obstacles...}
         │
         ▼
7. STRATEGY NODE envia Skills via ROS2 Services
   ├── strategy_command  → move robô para posição
   ├── set_orientation   → gira robô para ângulo
   ├── update_obstacles  → configura desvio de obstáculos
   └── update_kick       → ativa/desativa chute
         │
         ▼
8. ROBÔ executa o comando
```

---

## Dados Importantes

### Dimensões do campo (em mm)

| Referência | Valor |
|------------|-------|
| Gol positivo (centro) | x=2250, y=0 |
| Gol negativo (centro) | x=-2250, y=0 |
| Área do gol (largura Y) | ±700 |
| Área do gol (profundidade X) | 1750 até borda |
| Border circle (ataque/defesa) | raio=500 do centro |

### IDs dos robôs

| ID | Papel |
|----|-------|
| 0 | Goleiro (sempre) |
| 1+ | Jogadores de linha |

### Valores de kick

| Valor | Significado |
|-------|-------------|
| 0.0 | Chute desativado |
| 1.5 | Chute ativado |

### Comandos do referee usados

| Comando | Play ativado |
|---------|-------------|
| `STOP` | Stop |
| `HALT` | Halt |
| `PREPARE_KICKOFF_OURS` / `PREPARE_KICKOFF_THEIRS` | Kickoff |
| `DIRECT_FREE_OURS` / `DIRECT_FREE_THEIRS` | Freekick |
| `FORCE_START` / `NORMAL_START` | NormalStart |
