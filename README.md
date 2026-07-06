# 🕹️ Tetris Automático com IA (POO II)

![Status](https://img.shields.io/badge/Status-Em_Desenvolvimento-warning?style=for-the-badge&logo=github)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-informational?style=for-the-badge&logo=python)

> **Aviso:** Este projeto está atualmente em desenvolvimento! Novas funcionalidades e refatorações estão sendo aplicadas constantemente. 🚧

Um simulador interativo onde uma **Inteligência Artificial** joga uma partida infinita de Tetris de forma autônoma. Desenvolvido como projeto prático para a disciplina de Programação Orientada a Objetos II (POO II), o foco principal é a construção de uma arquitetura limpa, escalável e o uso de algoritmos de decisão em tempo real.

---

## ✨ O que já está funcionando (Features atuais)

- [x] **Arquitetura POO Sólida:** Uso de Classes Abstratas, Encapsulamento de matrizes (Getters/Setters) e Métodos Estáticos para reaproveitamento de código visual.
- [x] **Modularidade de Projeto:** Código dividido em 6 partes: `settings.json` (pesos), `config.py` (constantes), `elementos.py` (física), `estrategia.py` (cérebro das IAs), `motor.py` (motor de jogo) e `main.py` (gerenciador).
- [x] **Inteligência Artificial (Estratégia Avançada):** Três níveis de IA (Limitada, Intermediária e Avançada). A versão Avançada utiliza **Lookahead (Visão de Futuro)**, projetando na memória o encaixe da peça atual + a próxima peça (via *Buffer*) para maximizar o score.
- [x] **Cérebro Heurístico:** Algoritmo que utiliza "pesos de penalidade" (ex: peso 8.0 para buracos). A IA calcula o custo de cada jogada, onde o "medo" de buracos a força a escolher posições mais estáveis.
- [x] **Sistema de Simulação em Batch (Terminal):** Modo de teste de estresse (5 IAs simultâneas, incluindo mutantes genéticos aleatórios). Computa 300 peças por IA, gera ranking de performance e exporta para `relatorio_ia.csv` via *append*.
- [x] **Interface Gráfica Responsiva:** Ajuste automático de resolução e tela cheia via `pygame.display.Info()`. Inclui um "Modo Raio-X" (tecla TAB) para visualização em tempo real das falhas estruturais (buracos) detectadas pela IA.
- [x] **Otimização de Performance:** Substituição do `deepcopy` por fatiamento de lista (`[linha[:] for linha in grid]`), reduzindo drasticamente o consumo de memória e permitindo processamento em alta velocidade.
- [x] **Motor Gráfico Clássico:** Renderização em *Flat Design* com sidebar 3D para próxima peça e fontes otimizadas para leitura de dados.

## 🚀 O que vem por aí (Roadmap)

- [ ] Implementar sistema de evolução genética automática (ajuste fino dos pesos via IA).
- [ ] Adicionar trilha sonora e efeitos sonoros clássicos.
- [ ] Otimização do tempo de cálculo (Delta Time) para simulações ainda mais precisas.

---

## 💻 Como rodar na sua máquina

Como o projeto está em desenvolvimento, você pode testar o estado atual da IA clonando o repositório. Siga os passos abaixo:

1. **Instale o Python 3.x:**
   Certifique-se de ter o Python 3 instalado no seu computador. Caso não tenha, você pode baixar a versão mais recente no site oficial: [python.org](https://www.python.org/downloads/).
   *(Dica: Durante a instalação no Windows, não esqueça de marcar a caixa "Add Python to PATH").*

2. **Clone este repositório:**
   Abra o seu terminal (ou prompt de comando) e digite:
   
```bash
   git clone [https://github.com/amorimrh/TETRIS-POOII.git](https://github.com/amorimrh/TETRIS-POOII.git)
