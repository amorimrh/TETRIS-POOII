from abc import ABC, abstractmethod
from config import *

class Jogador(ABC):
    """
    professor, apliquei aqui o padrão de projeto 'Strategy' (Padrão Comportamental).
    A classe mãe 'Jogador' define a interface e o construtor dinâmico de 3 pesos analíticos,
    permitindo criar IAs com perfis diferentes sem replicar o núcleo da equação.
    """
    def __init__(self, peso_buracos, peso_altura, peso_tetris=0.0):
        self.peso_buracos = peso_buracos
        self.peso_altura = peso_altura
        self.peso_tetris = peso_tetris

    @abstractmethod
    def escolher_jogada(self, grade, peca, proxima_peca): pass

    def _copiar_matriz(self, matriz):
        return [linha[:] for linha in matriz]

    def avaliar(self, grid_temp):
        buracos = 0
        altura_total = 0
        linhas_completas = 0
        
        # Quantifica a pontuação bruta preditiva
        for lin in grid_temp:
            if None not in lin: linhas_completas += 1

        for col in range(COLUNAS):
            encontrou = False
            for lin in range(LINHAS):
                if grid_temp[lin][col]:
                    encontrou = True
                    altura_total += LINHAS - lin
                elif encontrou:
                    buracos += 1
                    
        # Cálculo Heurístico Padrão
        score = (buracos * self.peso_buracos) + (altura_total * self.peso_altura)
        
        # Sistema 'Risco vs Recompensa': Incentiva estruturalmente a fazer 4 linhas
        if self.peso_tetris > 0:
            if linhas_completas == 4:
                score -= self.peso_tetris * 100 
            elif linhas_completas > 0 and altura_total < 40:
                score += self.peso_tetris * 12 
                
        return score
        
    def _simular_queda_matriz(self, matriz, forma, col):
        y = 0
        while True:
            colisao = False
            for i, linha in enumerate(forma):
                for j, v in enumerate(linha):
                    if v:
                        x = col + j
                        if y + i >= LINHAS or (y + i >= 0 and matriz[y+i][x]): colisao = True
            if colisao: return y - 1
            y += 1

class JogadorInteligente(Jogador):
    """
    professor, a IA Avançada implementa 'Lookahead'.
    Ela avalia o impacto conjunto da peça atual com as possibilidades projetadas da próxima peça.
    """
    def __init__(self, peso_buracos, peso_altura, peso_tetris):
        # Repassa os 3 parâmetros corretamente para a superclasse
        super().__init__(peso_buracos, peso_altura, peso_tetris)

    def escolher_jogada(self, grade, peca, proxima_peca):
        melhor_score_global = float('inf')
        melhor_x = peca.x
        melhor_forma = peca.forma  

        forma_atual = peca.forma
        for _ in range(4): # Simula Rotação Presente
            for col in range(COLUNAS - len(forma_atual[0]) + 1):
                y_final = grade.simular_queda(forma_atual, col)
                grid_temp = grade.copiar()
                for i, linha in enumerate(forma_atual):
                    for j, v in enumerate(linha):
                        if v: grid_temp[y_final+i][col+j] = 1

                forma_futura = proxima_peca.forma
                melhor_score_futuro = float('inf')
                
                for _ in range(4): # Simula Rotação Futura na projeção isolada
                    for col_futuro in range(COLUNAS - len(forma_futura[0]) + 1):
                        y_futuro = self._simular_queda_matriz(grid_temp, forma_futura, col_futuro)
                        grid_temp_2 = self._copiar_matriz(grid_temp)
                        for i, linha in enumerate(forma_futura):
                            for j, v in enumerate(linha):
                                if v: grid_temp_2[y_futuro+i][col_futuro+j] = 1
                        
                        score = self.avaliar(grid_temp_2)
                        if score < melhor_score_futuro: melhor_score_futuro = score
                    
                    forma_futura = [list(linha) for linha in zip(*forma_futura[::-1])]

                if melhor_score_futuro < melhor_score_global:
                    melhor_score_global = melhor_score_futuro
                    melhor_x = col
                    melhor_forma = forma_atual

            forma_atual = [list(linha) for linha in zip(*forma_atual[::-1])]
        return melhor_x, melhor_forma

class JogadorIntermediario(Jogador):
    """
    professor, a IA Intermediária sofre de imediatismo. 
    Livre fisicamente para girar, mas incapaz de projetar as intenções na peça futura.
    """
    def __init__(self, peso_buracos, peso_altura, peso_tetris=0.0):
        super().__init__(peso_buracos, peso_altura, peso_tetris)

    def escolher_jogada(self, grade, peca, proxima_peca):
        melhor_score = float('inf')
        melhor_x = peca.x
        melhor_forma = peca.forma  
        forma_teste = peca.forma

        for _ in range(4):
            for col in range(COLUNAS - len(forma_teste[0]) + 1):
                y_final = grade.simular_queda(forma_teste, col)
                grid_temp = grade.copiar()
                for i, linha in enumerate(forma_teste):
                    for j, v in enumerate(linha):
                        if v: grid_temp[y_final+i][col+j] = 1

                score = self.avaliar(grid_temp)
                if score < melhor_score:
                    melhor_score = score
                    melhor_x = col
                    melhor_forma = forma_teste
            forma_teste = [list(linha) for linha in zip(*forma_teste[::-1])]
        return melhor_x, melhor_forma

class JogadorLimitado(Jogador):
    """
    professor, a IA Limitada possui deficiência cognitiva total.
    Ela ignora o futuro, e está presa à orientação de spawn (não executa rotação).
    """
    def __init__(self, peso_buracos, peso_altura, peso_tetris=0.0):
        super().__init__(peso_buracos, peso_altura, peso_tetris)

    def escolher_jogada(self, grade, peca, proxima_peca):
        melhor_score = float('inf')
        melhor_x = peca.x
        melhor_forma = peca.forma  
        forma_teste = peca.forma

        for col in range(COLUNAS - len(forma_teste[0]) + 1):
            y_final = grade.simular_queda(forma_teste, col)
            grid_temp = grade.copiar()
            for i, i_linha in enumerate(forma_teste):
                for j, v in enumerate(i_linha):
                    if v: grid_temp[y_final+i][col+j] = 1

            score = self.avaliar(grid_temp)
            if score < melhor_score:
                melhor_score = score
                melhor_x = col
                melhor_forma = forma_teste
        return melhor_x, melhor_forma