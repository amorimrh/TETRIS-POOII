import sys
import os
import random
import pygame
import csv
import datetime
from config import *
from elementos import GeradorDePecas
from estrategia import JogadorInteligente, JogadorIntermediario, JogadorLimitado
from motor import Jogo

# ================= INTERFACE INICIAL TERMINAL =================
print("="*60)
print("SIMULADOR DE IA TETRIS (MULTIVERSO ARQUITETURAL)")
print("="*60)
print("[G] Modo Gráfico: 3 Motores | Raio-X | Risco vs Recompensa")
print("[S] Modo Simulação: 5 Motores | Laboratório (300 Peças)")
escolha = input("Digite o modo desejado (G ou S): ").strip().upper()

MODO_GRAFICO = True if escolha != 'S' else False

# Extração parametrizada dos 3 pesos operacionais de cada IA
peso_b_int = config_data['ia_avancada']['peso_buracos']
peso_a_int = config_data['ia_avancada']['peso_altura']
peso_t_int = config_data['ia_avancada']['peso_tetris']

peso_b_mid = config_data['ia_intermediaria']['peso_buracos']
peso_a_mid = config_data['ia_intermediaria']['peso_altura']
peso_t_mid = config_data['ia_intermediaria']['peso_tetris']

peso_b_lim = config_data['ia_limitada']['peso_buracos']
peso_a_lim = config_data['ia_limitada']['peso_altura']
peso_t_lim = config_data['ia_limitada']['peso_tetris']

# Constante de término exato restaurada para 300
MAX_PECAS = 300

# ================= MODO GRAFICO (3 MOTORES - APRESENTAÇÃO) =================
if MODO_GRAFICO:
    pygame.init()
    # Detecção de monitor (Responsividade)
    info = pygame.display.Info()
    W_TELA = info.current_w
    H_TELA = info.current_h
    
    # Elevação de prioridade para Fullscreen nativo
    TELA = pygame.display.set_mode((W_TELA, H_TELA), pygame.FULLSCREEN)
    pygame.display.set_caption("Simulador Tetris POO")
    CLOCK = pygame.time.Clock()
    
    font_name = "consolas" if "consolas" in pygame.font.get_fonts() else "courier new"
    F_TITULO = pygame.font.SysFont(font_name, 22, bold=True)
    F_DADOS = pygame.font.SysFont(font_name, 16)
    F_VALORES = pygame.font.SysFont(font_name, 20, bold=True)
    F_DASH = pygame.font.SysFont(font_name, 26, bold=True)

    max_w = W_TELA // 4 
    max_h = int(H_TELA * 0.70)
    tamanho_calc = min(max_w // 16, max_h // LINHAS)
    VISUAL["TAMANHO"] = max(12, tamanho_calc) 

    W_SISTEMA = (COLUNAS * VISUAL["TAMANHO"]) + (6 * VISUAL["TAMANHO"])
    ALTURA_JOGO = LINHAS * VISUAL["TAMANHO"]
    
    gap = (W_TELA - (W_SISTEMA * 3)) // 4 
    pos_y = int(H_TELA * 0.12) 
    pos_x = [gap + (W_SISTEMA + gap) * i for i in range(3)]

    # Construtores consolidados passando os 3 argumentos rigorosamente
    geradores = [GeradorDePecas(SEMENTE) for _ in range(3)]
    jogadores = [
        JogadorLimitado(peso_b_lim, peso_a_lim, peso_t_lim),
        JogadorIntermediario(peso_b_mid, peso_a_mid, peso_t_mid),
        JogadorInteligente(peso_b_int, peso_a_int, peso_t_int)
    ]
    jogos = [Jogo(pos_x[i], pos_y, jogadores[i], geradores[i], ["IA LIMITADA", "IA INTERMEDIARIA", "IA AVANCADA"][i]) for i in range(3)]

    fator_tempo = 1.0  
    raio_x_ativo = False
    rodando = True

    while rodando:
        dt = CLOCK.tick(120) 
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: rodando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE: rodando = False
                elif evento.key == pygame.K_UP: fator_tempo = min(32.0, fator_tempo * 2.0)
                elif evento.key == pygame.K_DOWN: fator_tempo = max(0.25, fator_tempo / 2.0)
                elif evento.key == pygame.K_TAB: raio_x_ativo = not raio_x_ativo

        for jogo in jogos:
            if jogo.pecas_jogadas >= MAX_PECAS: jogo.game_over = True
            jogo.update(dt, fator_tempo, True)

        TELA.fill((10, 12, 18)) 

        for jogo in jogos:
            jogo.desenhar(TELA, F_TITULO, F_DADOS, F_VALORES, raio_x_ativo)
            
        # ================= LEGENDA DE CORRIDA DE RISCO =================
        pygame.draw.rect(TELA, (20, 24, 34), (20, 20, 240, 140), border_radius=8)
        pygame.draw.rect(TELA, (40, 50, 70), (20, 20, 240, 140), 2, border_radius=8)
        TELA.blit(F_DADOS.render("TABELA DE RISCO EXPONENCIAL", True, (255, 215, 0)), (30, 30))
        for idx, (linhas, pts) in enumerate(TABELA_PONTOS.items()):
            cor = (100, 255, 100) if linhas == 4 else (200, 200, 200)
            TELA.blit(F_DADOS.render(f"{linhas} LINHA{'S' if linhas>1 else ' '} = {pts:03d} PTS", True, cor), (30, 60 + (idx*20)))

        # ================= DASHBOARD INFERIOR =================
        painel_y = pos_y + ALTURA_JOGO + int(H_TELA * 0.08)
        largura_painel = W_TELA - (gap * 2)
        pygame.draw.rect(TELA, (18, 22, 32), (gap, painel_y, largura_painel, 80), border_radius=12)
        pygame.draw.rect(TELA, (40, 50, 70), (gap, painel_y, largura_painel, 80), 2, border_radius=12)

        cor_vel = (100, 255, 150) if fator_tempo > 1.0 else (255, 180, 50) if fator_tempo < 1.0 else (200, 200, 200)
        t_vel = F_DASH.render(f"CLOCK DO SIMULADOR: {fator_tempo:.2f}x", True, cor_vel)
        t_dica = F_DADOS.render("[SETAS UP/DOWN] Alterar Tempo  |  [TAB] Raio-X Telemetria  |  [ESC] Desligar", True, (120, 130, 150))
        
        TELA.blit(t_vel, (W_TELA // 2 - t_vel.get_width() // 2, painel_y + 15))
        TELA.blit(t_dica, (W_TELA // 2 - t_dica.get_width() // 2, painel_y + 50))

        pygame.display.update()

# ================= MODO SIMULAÇÃO (LABORATÓRIO HEADLESS - 5 MOTORES) =================
else:
    # Mutantes aleatórios nascem do zero para testar teorias empíricas contra os mestres
    peso_mutante1 = round(random.uniform(0.0, 10.0), 2)
    peso_mutante2 = round(random.uniform(0.0, 10.0), 2)

    print("\nIniciando Processamento em Batch de Alta Performance (Sem interface)...")
    print(f"Métrica de Corte: Encerramento compulsório ao computar exatamente {MAX_PECAS} peças.")
    print("Tags do Console: [L] Limitada | [I] Intermediária | [A] Avançada | [MA/MB] Mutantes Genéticos\n")
    
    geradores = [GeradorDePecas(SEMENTE) for _ in range(5)]
    jogadores = [
        JogadorLimitado(peso_b_lim, peso_a_lim, peso_t_lim),
        JogadorIntermediario(peso_b_mid, peso_a_mid, peso_t_mid),
        JogadorInteligente(peso_b_int, peso_a_int, peso_t_int),
        JogadorInteligente(peso_mutante1, 1.0, 10.0), 
        JogadorInteligente(peso_mutante2, 1.0, 10.0)
    ]
    titulos = ["Limitada", "Intermediaria", "Avancada", f"MutanteA_({peso_mutante1})", f"MutanteB_({peso_mutante2})"]
    jogos = [Jogo(0, 0, jogadores[i], geradores[i], titulos[i]) for i in range(5)]
    
    rodando = True
    while rodando:
        todos_finalizados = True
        for jogo in jogos:
            # Trava estrita nos 300
            if jogo.pecas_jogadas >= MAX_PECAS: jogo.game_over = True
            jogo.update(500, 1, False)
            if not jogo.game_over: todos_finalizados = False

        # Feedback interativo em 1 única linha no terminal para não flodar a tela
        sys.stdout.write(f"\rPeças | L: {jogos[0].pecas_jogadas:03d} | I: {jogos[1].pecas_jogadas:03d} | A: {jogos[2].pecas_jogadas:03d} | MA: {jogos[3].pecas_jogadas:03d} | MB: {jogos[4].pecas_jogadas:03d} de {MAX_PECAS}")
        sys.stdout.flush()

        if todos_finalizados:
            # Sorteio computado via Lambda para ditar o Pódio Baseado em Pontos Acumulados
            ranking_final = sorted(jogos, key=lambda j: j.pontos, reverse=True)
            
            print("\n\n=============== CLASSIFICAÇÃO DA SESSÃO ===============")
            for posicao, jogo in enumerate(ranking_final, start=1):
                st = "CONCLUIDO" if jogo.pecas_jogadas >= MAX_PECAS else "COLAPSO"
                print(f"{posicao} Lugar | {jogo.titulo.ljust(16)} | Pontos: {jogo.pontos:06d} | Peças: {jogo.pecas_jogadas:03d} [{st}]")
            print("=======================================================")
            
            sessao_id = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            arquivo_existe = os.path.isfile('relatorio_ia.csv')
            
            # Anexa os resultados (Modo a - Append) com detalhes ricos da pontuação de cada I.A
            with open('relatorio_ia.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                if not arquivo_existe: writer.writerow(['Data_Sessao', 'Posicao_Ranking', 'IA_Modelo', 'Pontos_Finais', 'Pecas_Utilizadas'])
                for pos, jogo in enumerate(ranking_final, start=1):
                    writer.writerow([sessao_id, pos, jogo.titulo, jogo.pontos, jogo.pecas_jogadas])
            print("Histórico cumulativo registrado com sucesso no banco de dados relatorio_ia.csv.")
            rodando = False
