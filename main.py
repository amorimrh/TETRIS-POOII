import pygame
import random
import copy
from abc import ABC, abstractmethod

# Biblioteca principal que cria a janela, desenha tudo e controla o jogo
# Usada para sortear qual peça cai e em qual coluna ela aparece
# Cria cópias da matriz para a IA testar jogadas sem mexer no jogo original
# Ferramentas de POO usadas para criar a Classe Abstrata

# inicia o pygame (necessário pra usar tudo da biblioteca)
pygame.init()

# tamanho da tela do jogo
LARGURA = 400
ALTURA = 600

# tamanho de cada bloco (cada “quadradinho” do tetris)
TAMANHO = 20

# quantidade de colunas e linhas baseado no tamanho da tela
COLUNAS = LARGURA // TAMANHO
LINHAS = ALTURA // TAMANHO

# cria a janela do jogo
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Tetris")

# controla o FPS (quantas vezes o jogo atualiza por segundo)
CLOCK = pygame.time.Clock()

# fonte usada pra escrever na tela (pontuação e game over)
FONT = pygame.font.SysFont(None, 30)

# cada tipo de peça tem uma cor fixa (fica mais fácil visualizar)
# Ajustei um pouco as cores pra ficarem mais vibrantes como na sua foto
CORES_FORMAS = {
    0: (230, 20, 20),    # Vermelho
    1: (20, 230, 20),    # Verde
    2: (20, 20, 230),    # Azul
    3: (230, 230, 20),   # Amarelo
    4: (20, 200, 230)    # Ciano/Azul claro
}

# formatos das peças
# cada lista representa um formato diferente
# 1 = tem bloco / 0 = vazio
FORMAS = [
    [[1, 1, 1]],              # linha deitada

    [[1, 1],                  # quadrado (mais simples)
     [1, 1]],

    [[1, 0],                  # formato L
     [1, 0],
     [1, 1]],

    [[0, 1],                  # L invertido
     [0, 1],
     [1, 1]],

    [[1],                     # linha em pé (tipo I)
     [1],
     [1],
     [1]]
]

# ================= CLASSE ABSTRATA =================
class ElementoVisual(ABC):
    @abstractmethod
    def desenhar(self, tela):
        pass

    # Criei um MÉTODO ESTÁTICO. Como a Grade e a Peça precisam desenhar os blocos 
    # com o mesmo efeito 3D, eu coloco o código aqui para reaproveitar (Herança)!
    @staticmethod
    def desenhar_bloco_3d(tela, cor, px, py):
        # 1. Base (Pinto o interior do quadrado)
        pygame.draw.rect(tela, cor, (px, py, TAMANHO, TAMANHO))

        # 2. Lógica para gerar as cores de luz e sombra
        r, g, b = cor
        claro = (min(255, r + 80), min(255, g + 80), min(255, b + 80)) # Clareia a cor
        escuro = (max(0, r - 80), max(0, g - 80), max(0, b - 80))      # Escurece a cor

        # 3. Desenho as bordas chanfradas para dar o efeito de botão (espessura de 3 pixels)
        borda = 3
        # Topo (luz)
        pygame.draw.polygon(tela, claro, [(px, py), (px + TAMANHO, py), (px + TAMANHO - borda, py + borda), (px + borda, py + borda)])
        # Esquerda (luz)
        pygame.draw.polygon(tela, claro, [(px, py), (px + borda, py + borda), (px + borda, py + TAMANHO - borda), (px, py + TAMANHO)])
        # Fundo (sombra)
        pygame.draw.polygon(tela, escuro, [(px, py + TAMANHO), (px + TAMANHO, py + TAMANHO), (px + TAMANHO - borda, py + TAMANHO - borda), (px + borda, py + TAMANHO - borda)])
        # Direita (sombra)
        pygame.draw.polygon(tela, escuro, [(px + TAMANHO, py), (px + TAMANHO - borda, py + borda), (px + TAMANHO - borda, py + TAMANHO - borda), (px + TAMANHO, py + TAMANHO)])

        # 4. Adiciono aquele pontinho de brilho extra no canto superior esquerdo (igual da foto)
        pygame.draw.rect(tela, (255, 255, 255), (px + borda, py + borda, 3, 3))


# ================= CLASSE PEÇA =================
class Peca(ElementoVisual):
    
    # ATRIBUTO DE CLASSE: Funciona como um contador global para todas as peças.
    _contador_id = 0

    def __init__(self):
        # Cada vez que uma peça nasce, aumento o contador e dou esse número pra ela
        Peca._contador_id += 1
        self._id = Peca._contador_id
        
        # escolhe aleatoriamente qual tipo de peça vai aparecer (encapsulado com _)
        self._tipo = random.randint(0, len(FORMAS)-1)

        # pega o formato baseado no tipo
        self._forma = FORMAS[self._tipo]

        # define a cor da peça
        self._cor = CORES_FORMAS[self._tipo]

        # posição inicial (x aleatório pra espalhar melhor)
        self._x = random.randint(0, COLUNAS - len(self._forma[0]))
        self._y = 0  # sempre começa no topo

    # Getters e Setters para mover a peça com segurança
    @property
    def id(self):
        return self._id
        
    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, valor):
        self._x = valor

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, valor):
        self._y = valor

    @property
    def forma(self):
        return self._forma
        
    # Criei um SETTER para a forma também! Assim o Jogo pode mandar a peça girar.
    @forma.setter
    def forma(self, nova_forma):
        self._forma = nova_forma
        
    @property
    def cor(self):
        return self._cor

    def desenhar(self, tela):
        # peço para o método estático desenhar cada quadradinho da peça com o efeito 3D
        for i, linha in enumerate(self._forma):
            for j, valor in enumerate(linha):
                if valor:
                    px = (self._x + j) * TAMANHO
                    py = (self._y + i) * TAMANHO
                    # Uso o método herdado da ElementoVisual
                    self.desenhar_bloco_3d(tela, self._cor, px, py)


# ================= CLASSE GRADE =================
class Grade(ElementoVisual):
    def __init__(self):
        # cria a matriz do jogo (tabuleiro vazio) - encapsulada com _
        self._grid = [[None for _ in range(COLUNAS)] for _ in range(LINHAS)]

    def colidiu(self, peca):
        # verifica se a peça bateu no chão, parede ou outra peça
        for i, linha in enumerate(peca.forma):
            for j, valor in enumerate(linha):
                if valor:
                    x = peca.x + j
                    y = peca.y + i

                    # bateu nos limites da tela
                    if y >= LINHAS or x < 0 or x >= COLUNAS:
                        return True

                    # bateu em outro bloco já fixo
                    if y >= 0 and self._grid[y][x]:
                        return True
        return False

    def fixar(self, peca):
        # quando a peça para, eu gravo a cor E o ID único dela na grade
        for i, linha in enumerate(peca.forma):
            for j, valor in enumerate(linha):
                if valor:
                    x = peca.x + j
                    y = peca.y + i
                    if 0 <= y < LINHAS:
                        self._grid[y][x] = (peca.cor, peca.id)

    def copiar(self):
        # cria uma cópia da grade (a IA usa isso pra testar jogadas)
        return copy.deepcopy(self._grid)

    def simular_queda(self, forma, col):
        # simula até onde a peça cairia em uma coluna
        y = 0
        while True:
            colisao = False
            for i, linha in enumerate(forma):
                for j, v in enumerate(linha):
                    if v:
                        x = col + j
                        if y + i >= LINHAS or (y + i >= 0 and self._grid[y+i][x]):
                            colisao = True
            if colisao:
                return y - 1
            y += 1

    def avaliar(self, grid_temp):
        # dá uma “nota” pra jogada (quanto menor melhor)
        buracos = 0
        altura_total = 0

        for col in range(COLUNAS):
            encontrou = False
            for lin in range(LINHAS):
                if grid_temp[lin][col]:
                    encontrou = True
                    altura_total += LINHAS - lin
                elif encontrou:
                    # espaço vazio embaixo de bloco = buraco (ruim)
                    buracos += 1

        return buracos * 5 + altura_total

    def melhor_posicao(self, peca):
        # agora a IA precisa escolher não só o X, mas a ROTAÇÃO também!
        melhor_score = float('inf')
        melhor_x = peca.x
        melhor_forma = peca.forma  # guarda o formato ideal descoberto
        
        forma_teste = peca.forma

        # Criei um loop para testar as 4 posições de rotação (0, 90, 180 e 270 graus)
        for _ in range(4):
            # Para cada rotação, testo todas as colunas possíveis
            for col in range(COLUNAS - len(forma_teste[0]) + 1):
                y_final = self.simular_queda(forma_teste, col)
                grid_temp = self.copiar()

                # simula colocar a peça girada ali
                for i, linha in enumerate(forma_teste):
                    for j, v in enumerate(linha):
                        if v:
                            grid_temp[y_final+i][col+j] = 1

                score = self.avaliar(grid_temp)

                # se achar uma nota melhor, salvo a coluna e o formato da peça girada!
                if score < melhor_score:
                    melhor_score = score
                    melhor_x = col
                    melhor_forma = forma_teste

            # Antes da próxima iteração, eu rotaciono a matriz de teste 90 graus no sentido horário
            # A lógica `zip(*forma_teste[::-1])` inverte a matriz em Python
            forma_teste = [list(linha) for linha in zip(*forma_teste[::-1])]

        # Agora eu devolvo as duas coisas: Onde a peça tem que ir, e como ela tem que ficar!
        return melhor_x, melhor_forma

    def limpar_linhas(self):
        # remove linhas completas
        nova = [linha for linha in self._grid if None in linha]
        removidas = LINHAS - len(nova)

        # adiciona novas linhas vazias no topo
        for _ in range(removidas):
            nova.insert(0, [None for _ in range(COLUNAS)])

        self._grid = nova
        return removidas

    def topo_ocupado(self):
        # verifica se chegou no topo (game over)
        return any(self._grid[0][col] is not None for col in range(COLUNAS))

    def desenhar(self, tela):
        # percorre toda a grade para desenhar
        for i in range(LINHAS):
            for j in range(COLUNAS):
                px = j * TAMANHO
                py = i * TAMANHO
                
                # se estiver vazio, desenho a luz de fundo que combinamos
                if not self._grid[i][j]:
                    cor_fundo = (30, 40, 60) # Um azul bem escuro pro fundo da grade (tipo da foto)
                    pygame.draw.rect(tela, cor_fundo, (px, py, TAMANHO, TAMANHO), 1)
                
                # se tiver peça fixa, uso a função do efeito 3D
                elif self._grid[i][j]:
                    cor = self._grid[i][j][0]
                    self.desenhar_bloco_3d(tela, cor, px, py)


# ================= CLASSE JOGO =================
class Jogo:
    def __init__(self):
        self.reset()

    def reset(self):
        # reinicia tudo do zero
        self.grade = Grade()
        self.peca = Peca()
        self.tempo = 0

        # controla a velocidade da queda
        # quanto menor esse valor, mais rápido o jogo fica
        self.velocidade = 14

        self.pontos = 0
        self.game_over = False
        self.timer_game_over = 0

    def update(self, dt):
        # atualiza o jogo a cada frame

        # se perdeu, espera um tempo e reinicia
        if self.game_over:
            self.timer_game_over += dt
            if self.timer_game_over > 2000:
                self.reset()
            return

        # acumula tempo
        self.tempo += dt

        # controla quando a peça vai descer
        if self.tempo > self.velocidade:
            self.tempo = 0

            # Agora eu peço as DUAS coisas para a Grade: A coluna alvo e a forma rotacionada!
            alvo_x, melhor_forma = self.grade.melhor_posicao(self.peca)

            # Aplico a rotação na peça usando o Setter que eu criei
            self.peca.forma = melhor_forma
            
            # Ajuste de segurança: como a largura da peça mudou ao girar, 
            # verifico se ela não vazou da tela pela direita antes de mover
            if self.peca.x > COLUNAS - len(self.peca.forma[0]):
                self.peca.x = COLUNAS - len(self.peca.forma[0])

            # move a peça até o alvo
            if self.peca.x < alvo_x:
                self.peca.x += 1
            elif self.peca.x > alvo_x:
                self.peca.x -= 1
            else:
                # quando chega na posição certa (já rotacionada), começa a cair
                self.peca.y += 1

            # verifica colisão
            if self.grade.colidiu(self.peca):
                self.peca.y -= 1
                self.grade.fixar(self.peca)

                # calcula pontuação
                linhas = self.grade.limpar_linhas()
                self.pontos += linhas * 100

                # verifica game over
                if self.grade.topo_ocupado():
                    self.game_over = True
                else:
                    self.peca = Peca()

    def desenhar(self, tela):
        # desenha tudo na tela (mudei o fundo para um azul marinho bem escuro, estilo arcade)
        tela.fill((10, 15, 30))
        self.grade.desenhar(tela)

        if not self.game_over:
            self.peca.desenhar(tela)

        # mostra pontuação
        texto = FONT.render(f"Pontos: {self.pontos}", True, (255, 255, 255))
        tela.blit(texto, (10, 10))

        # tela de game over com a borda branca no texto vermelho
        if self.game_over:
            texto_go = "GAME OVER"
            
            # desenho o texto em branco deslocado para criar o contorno
            for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (2, -2), (-2, 2), (2, 2)]:
                borda = FONT.render(texto_go, True, (255, 255, 255))
                tela.blit(borda, (150 + dx, (ALTURA // 2) + dy))
            
            # desenho o texto principal vermelho por cima do contorno
            msg = FONT.render(texto_go, True, (255, 0, 0))
            tela.blit(msg, (150, ALTURA // 2))

        pygame.display.update()

# ================= LOOP PRINCIPAL =================

# cria o jogo
jogo = Jogo()
rodando = True

# loop infinito (simulação contínua)
while rodando:
    dt = CLOCK.tick(120)  # FPS (quanto maior, mais fluido)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    jogo.update(dt)
    jogo.desenhar(TELA)
