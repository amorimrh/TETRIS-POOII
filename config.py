import json

# ================= CONFIGURAÇÕES GERAIS =================
# Desacoplamento: Lê os parâmetros da IA via JSON externo
with open('settings.json', 'r') as f:
    config_data = json.load(f)

SEMENTE = config_data['semente_competicao']

# Dimensões da matriz do Tetris original (Fliperama)
COLUNAS = 10
LINHAS = 20

# Tamanho base em pixels que será manipulado para responsividade
VISUAL = {
    "TAMANHO": 20
}

# Tabela Exponencial de Risco vs Recompensa para o "Greed System" da IA
TABELA_PONTOS = {
    1: 100,
    2: 300,
    3: 500,
    4: 800
}

# Paleta de cores RGB Flat Design
CORES_FORMAS = {
    0: (235, 50, 50),
    1: (50, 235, 50),
    2: (50, 100, 255),
    3: (240, 200, 20),
    4: (20, 220, 240)
}

# Matrizes binárias dos Tetrominós
FORMAS = [
    [[1, 1, 1, 1]],           # I (Reta)
    [[1, 1], [1, 1]],         # O (Quadrado)
    [[1, 0], [1, 0], [1, 1]], # L
    [[0, 1], [0, 1], [1, 1]], # J
    [[0, 1, 0], [1, 1, 1]]    # T
]