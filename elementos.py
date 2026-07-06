import pygame
import random
from abc import ABC, abstractmethod
from config import *

class GeradorDePecas:
    """
    Aplica o padrão de projeto 'Factory' aliado a um 'Buffer'.
    Mantenho uma peça no presente e sorteio a do futuro. Isso é fundamental para que a 
    IA Avançada consiga ler o futuro sem roubar ou dessincronizar a semente aleatória geral.
    """
    def __init__(self, semente):
        self._random = random.Random(semente)
        self.proxima_peca = Peca(self._random.randint(0, len(FORMAS) - 1))

    def gerar(self):
        # Desloca o bloco do futuro para o presente e cria um novo futuro
        peca_atual = self.proxima_peca
        self.proxima_peca = Peca(self._random.randint(0, len(FORMAS) - 1))
        return peca_atual, self.proxima_peca

class ElementoVisual(ABC):
    """
    Utilizo herança e polimorfismo a partir desta classe base abstrata.
    O método de renderização 3D é estático para ser reutilizado sem instanciar novos objetos.
    """
    @abstractmethod
    def desenhar(self, tela, x_offset, y_offset, raio_x=False):
        pass

    @staticmethod
    def desenhar_bloco_3d(tela, cor, px, py):
        # Renderização Flat Arcade via inner shadows
        tamanho = VISUAL["TAMANHO"]
        borda = 2
        
        escuro = (max(0, cor[0]-60), max(0, cor[1]-60), max(0, cor[2]-60))
        claro = (min(255, cor[0]+60), min(255, cor[1]+60), min(255, cor[2]+60))

        # Fundo, Miolo e Brilho Acrílico
        pygame.draw.rect(tela, escuro, (px, py, tamanho, tamanho), border_radius=3)
        pygame.draw.rect(tela, cor, (px + borda, py + borda, tamanho - borda*2, tamanho - borda*2), border_radius=2)
        altura_brilho = max(2, tamanho // 5)
        pygame.draw.rect(tela, claro, (px + borda, py + borda, tamanho - borda*2, altura_brilho), border_top_left_radius=2, border_top_right_radius=2)

class Peca(ElementoVisual):
    _contador_id = 0
    def __init__(self, tipo):
        Peca._contador_id += 1
        self._id = Peca._contador_id
        self._tipo = tipo
        self._forma = FORMAS[self._tipo]
        self._cor = CORES_FORMAS[self._tipo]
        # Centraliza horizontalmente
        self._x = COLUNAS // 2 - len(self._forma[0]) // 2
        self._y = 0  

    @property
    def id(self): return self._id
    @property
    def x(self): return self._x
    @x.setter
    def x(self, valor): self._x = valor
    @property
    def y(self): return self._y
    @y.setter
    def y(self, valor): self._y = valor
    @property
    def forma(self): return self._forma
    @forma.setter
    def forma(self, nova_forma): self._forma = nova_forma
    @property
    def cor(self): return self._cor

    def desenhar(self, tela, x_offset, y_offset, raio_x=False):
        tamanho = VISUAL["TAMANHO"]
        for i, linha in enumerate(self._forma):
            for j, valor in enumerate(linha):
                if valor:
                    px = (self._x + j) * tamanho + x_offset
                    py = (self._y + i) * tamanho + y_offset
                    # Modo Raio-X desenha wireframes (fios) em vez de sólidos
                    if raio_x:
                        pygame.draw.rect(tela, (200, 200, 200), (px, py, tamanho, tamanho), 2)
                    else:
                        self.desenhar_bloco_3d(tela, self._cor, px, py)

    def desenhar_absoluto(self, tela, start_x, start_y):
        # Renderização absoluta para a Sidebar ignorando limites da Grade
        tamanho = VISUAL["TAMANHO"]
        for i, linha in enumerate(self._forma):
            for j, valor in enumerate(linha):
                if valor:
                    px = start_x + (j * tamanho)
                    py = start_y + (i * tamanho)
                    self.desenhar_bloco_3d(tela, self._cor, px, py)

class Grade(ElementoVisual):
    def __init__(self):
        self._grid = [[None for _ in range(COLUNAS)] for _ in range(LINHAS)]

    def colidiu(self, peca):
        # Varredura de limites espaciais
        for i, linha in enumerate(peca.forma):
            for j, valor in enumerate(linha):
                if valor:
                    x = peca.x + j
                    y = peca.y + i
                    if y >= LINHAS or x < 0 or x >= COLUNAS: return True
                    if y >= 0 and self._grid[y][x]: return True
        return False

    def fixar(self, peca):
        # Congela o id e cor do bloco na matriz RAM
        for i, linha in enumerate(peca.forma):
            for j, valor in enumerate(linha):
                if valor:
                    x = peca.x + j
                    y = peca.y + i
                    if 0 <= y < LINHAS: self._grid[y][x] = (peca.cor, peca.id)

    def copiar(self):
        # Otimização Crítica: O List Slicing é absurdamente mais veloz que deepcopy()
        return [linha[:] for linha in self._grid]

    def simular_queda(self, forma, col):
        y = 0
        while True:
            colisao = False
            for i, linha in enumerate(forma):
                for j, v in enumerate(linha):
                    if v:
                        x = col + j
                        if y + i >= LINHAS or (y + i >= 0 and self._grid[y+i][x]): colisao = True
            if colisao: return y - 1
            y += 1

    def limpar_linhas(self):
        nova = [linha for linha in self._grid if None in linha]
        removidas = LINHAS - len(nova)
        for _ in range(removidas): nova.insert(0, [None for _ in range(COLUNAS)])
        self._grid = nova
        return removidas

    def topo_ocupado(self):
        # Retorna Game Over se o teto matriz[0] foi violado
        return any(self._grid[0][col] is not None for col in range(COLUNAS))

    def desenhar(self, tela, x_offset, y_offset, raio_x=False):
        tamanho = VISUAL["TAMANHO"]
        
        # Leitura topográfica para a visão raio-x
        alturas = [0] * COLUNAS
        if raio_x:
            for col in range(COLUNAS):
                for lin in range(LINHAS):
                    if self._grid[lin][col]:
                        alturas[col] = LINHAS - lin
                        break

        for i in range(LINHAS):
            for j in range(COLUNAS):
                px = j * tamanho + x_offset
                py = i * tamanho + y_offset
                
                if not self._grid[i][j]:
                    # Telemetria: Evidencia buracos em vermelho
                    if raio_x and alturas[j] > LINHAS - i:
                        pygame.draw.rect(tela, (255, 30, 30), (px, py, tamanho, tamanho)) 
                        pygame.draw.rect(tela, (255, 150, 150), (px+2, py+2, tamanho-4, tamanho-4), 1)
                    else:
                        pygame.draw.rect(tela, (25, 30, 45), (px, py, tamanho, tamanho), 1)
                else:
                    if raio_x:
                        # Telemetria: Apaga a cor sólida e grifa torres altas de amarelo
                        pygame.draw.rect(tela, (40, 50, 60), (px, py, tamanho, tamanho), 1)
                        if alturas[j] > 14:
                            pygame.draw.rect(tela, (200, 180, 0), (px, py, tamanho, tamanho), 2)
                    else:
                        cor = self._grid[i][j][0]
                        self.desenhar_bloco_3d(tela, cor, px, py)
