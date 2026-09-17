import random

def generate_maze(linhas=31, colunas=31, tamanho_centro=5, densidade_loops=0.15):
    # Garantir dimensões ímpares para manter o grid alinhado
    if linhas % 2 == 0: linhas += 1
    if colunas % 2 == 0: colunas += 1
    if tamanho_centro % 2 == 0: tamanho_centro += 1

    # 1. Inicializa a grade cheia de paredes (#)
    grid = [["#" for _ in range(colunas)] for _ in range(linhas)]

    # 2. Define o Centro do Labirinto
    cx_inicio = (linhas // 2) - (tamanho_centro // 2)
    cx_fim = cx_inicio + tamanho_centro
    cy_inicio = (colunas // 2) - (tamanho_centro // 2)
    cy_fim = cy_inicio + tamanho_centro

    # Escava o espaço central
    for r in range(cx_inicio, cx_fim):
        for c in range(cy_inicio, cy_fim):
            grid[r][c] = "."

    # 3. Escava o restante do labirinto via DFS adaptado
    def cavar(x, y):
        direcoes = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        random.shuffle(direcoes)

        for dx, dy in direcoes:
            nx, ny = x + dx, y + dy
            if 1 <= nx < linhas - 1 and 1 <= ny < colunas - 1:
                # Se ainda não foi visitado (continua parede)
                if grid[nx][ny] == "#":
                    grid[x + dx // 2][y + dy // 2] = "."
                    grid[nx][ny] = "."
                    cavar(nx, ny)

    # Começa escavando do canto superior esquerdo
    grid[1][1] = "."
    cavar(1, 1)

    # 4. Criar múltiplos caminhos e loops (remover paredes aleatórias)
    # Isso transforma o labirinto em um modelo clássico/confuso com várias rotas
    for r in range(2, linhas - 2, 2):
        for c in range(2, colunas - 2, 2):
            if grid[r][c] == "#":
                if random.random() < densidade_loops:
                    grid[r][c] = "."

    # 5. Conectar o centro ao restante do labirinto com múltiplas entradas
    conexoes_centro = [
        (cx_inicio - 1, colunas // 2),  # Entrada Norte
        (cx_fim, colunas // 2),        # Entrada Sul
        (linhas // 2, cy_inicio - 1),  # Entrada Oeste
        (linhas // 2, cy_fim)          # Entrada Leste
    ]
    
    for rx, cy in conexoes_centro:
        if 0 < rx < linhas - 1 and 0 < cy < colunas - 1:
            grid[rx][cy] = "."

    # Entrada e Saída externas padrão
    grid[0][1] = "."
    grid[linhas - 1][colunas - 2] = "."

    MAZE_LAYOUT = ["".join(linha) for linha in grid]
    return MAZE_LAYOUT

def set_cell_size():
    
    return 50


