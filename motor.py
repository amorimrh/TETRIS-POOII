import pygame
from config import *
from elementos import Grade
from estrategia import JogadorInteligente, JogadorIntermediario

class Jogo:
    """
    professor, utilizei o princípio do Encapsulamento. O motor instancia localmente a Grade
    e os componentes, permitindo escalar o jogo virtualmente na RAM em Modo Headless ou Gráfico.
    """
    def __init__(self, x_offset, y_offset, jogador, gerador, titulo="IA"):
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.jogador = jogador
        self.gerador = gerador
        self.titulo = titulo
        self.reset()

    def reset(self):
        self.grade = Grade()
        # Coleta os blocos utilizando a chamada de método CORRETA do python
        self.peca, self.proxima_peca = self.gerador.gerar() 
        self.tempo = 0
        self.alvo_x = None
        self.melhor_forma = None
        self.pontos = 0
        self.pecas_jogadas = 0
        self.game_over = False

    def update(self, dt, fator_tempo, modo_grafico):
        if self.game_over: return

        # Aceleração controlada do clock lógico
        self.tempo += (dt * fator_tempo)
        velocidade_base = 200 if isinstance(self.jogador, JogadorInteligente) else 300 if isinstance(self.jogador, JogadorIntermediario) else 400

        # Absorção contínua (While loop) permite avançar o jogo sem desenhar
        passos_logicos = 1 if not modo_grafico else 0
        if modo_grafico:
            while self.tempo >= velocidade_base and not self.game_over:
                self.tempo -= velocidade_base
                passos_logicos += 1

        for _ in range(passos_logicos):
            if self.game_over: break

            if self.alvo_x is None:
                self.alvo_x, self.melhor_forma = self.jogador.escolher_jogada(self.grade, self.peca, self.proxima_peca)

            movimentou_horizontal = False
            old_x = self.peca.x

            if self.peca.x < self.alvo_x:
                self.peca.x += 1
                movimentou_horizontal = True
                if self.grade.colidiu(self.peca):
                    self.peca.x = old_x
                    movimentou_horizontal = False
            elif self.peca.x > self.alvo_x:
                self.peca.x -= 1
                movimentou_horizontal = True
                if self.grade.colidiu(self.peca):
                    self.peca.x = old_x
                    movimentou_horizontal = False

            if self.peca.x == self.alvo_x or not movimentou_horizontal:
                self.peca.y += 1
                if self.peca.forma != self.melhor_forma:
                    old_forma = self.peca.forma
                    # Rotaciona dinamicamente a matriz bidimensional em 90 graus
                    self.peca.forma = [list(linha) for linha in zip(*self.peca.forma[::-1])]
                    # Aciona Wall-Kick para não prender o bloco contra a parede
                    if self.peca.x > COLUNAS - len(self.peca.forma[0]): self.peca.x = COLUNAS - len(self.peca.forma[0])
                    if self.grade.colidiu(self.peca):
                        self.peca.forma = old_forma
                        if self.peca.x > COLUNAS - len(self.peca.forma[0]): self.peca.x = COLUNAS - len(self.peca.forma[0])

            if self.grade.colidiu(self.peca):
                self.peca.y -= 1
                self.grade.fixar(self.peca)
                self.pecas_jogadas += 1
                
                linhas = self.grade.limpar_linhas()
                # Atualização do balanço de pontuação exponencial
                if linhas in TABELA_PONTOS:
                    self.pontos += TABELA_PONTOS[linhas]

                if self.grade.topo_ocupado():
                    self.game_over = True
                else:
                    self.peca, self.proxima_peca = self.gerador.gerar() 
                    self.alvo_x = None 

    def desenhar(self, tela, f_titulo, f_dados, f_valores, raio_x=False):
        tamanho = VISUAL["TAMANHO"]
        W_JOGO = COLUNAS * tamanho
        H_JOGO = LINHAS * tamanho
        W_SIDEBAR = 6 * tamanho 
        
        # Placa Mestra Base
        pygame.draw.rect(tela, (20, 24, 34), (self.x_offset - 10, self.y_offset - 40, W_JOGO + W_SIDEBAR + 20, H_JOGO + 50), border_radius=8)
        
        lbl_titulo = f_titulo.render(self.titulo, True, (255, 215, 0))
        tela.blit(lbl_titulo, (self.x_offset + (W_JOGO//2) - (lbl_titulo.get_width()//2), self.y_offset - 30))

        pygame.draw.rect(tela, (15, 18, 25), (self.x_offset, self.y_offset, W_JOGO, H_JOGO))
        
        self.grade.desenhar(tela, self.x_offset, self.y_offset, raio_x)
        if not self.game_over:
            self.peca.desenhar(tela, self.x_offset, self.y_offset, raio_x)

        # ================= DESENHO DA SIDEBAR =================
        sb_x = self.x_offset + W_JOGO + 10
        sb_y = self.y_offset
        
        lbl_prox = f_dados.render("PROXIMA", True, (150, 160, 180))
        tela.blit(lbl_prox, (sb_x, sb_y))

        box_tam = 4 * tamanho
        pygame.draw.rect(tela, (12, 14, 20), (sb_x, sb_y + 20, box_tam, box_tam), border_radius=4)
        pygame.draw.rect(tela, (40, 45, 60), (sb_x, sb_y + 20, box_tam, box_tam), 2, border_radius=4)
        
        if not self.game_over:
            offset_nx = sb_x + ((4 - len(self.proxima_peca.forma[0])) * tamanho) // 2
            offset_ny = sb_y + 20 + ((4 - len(self.proxima_peca.forma)) * tamanho) // 2
            self.proxima_peca.desenhar_absoluto(tela, offset_nx, offset_ny)

        info_y = sb_y + 20 + box_tam + 30
        
        lbl_pts = f_dados.render("PONTOS", True, (150, 160, 180))
        val_pts = f_valores.render(f"{self.pontos:06d}", True, (255, 255, 255))
        tela.blit(lbl_pts, (sb_x, info_y))
        tela.blit(val_pts, (sb_x, info_y + 20))

        lbl_pcs = f_dados.render("PECAS", True, (150, 160, 180))
        val_pcs = f_valores.render(f"{self.pecas_jogadas:04d}", True, (255, 255, 255))
        tela.blit(lbl_pcs, (sb_x, info_y + 60))
        tela.blit(val_pcs, (sb_x, info_y + 80))

        if self.game_over:
            texto_go = "COLAPSO"
            borda = f_titulo.render(texto_go, True, (0, 0, 0))
            msg = f_titulo.render(texto_go, True, (255, 50, 50))
            tela.blit(borda, ((W_JOGO // 2) - borda.get_width()//2 + self.x_offset + 2, (H_JOGO // 2) + self.y_offset + 2))
            tela.blit(msg, ((W_JOGO // 2) - msg.get_width()//2 + self.x_offset, (H_JOGO // 2) + self.y_offset))