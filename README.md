# 🕹️ Tetris Automático com IA 

![Status](https://img.shields.io/badge/Status-Em_Desenvolvimento-warning?style=for-the-badge&logo=github)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-informational?style=for-the-badge&logo=python)

> **Aviso:** Este projeto está atualmente em desenvolvimento! Novas funcionalidades e refatorações estão sendo aplicadas constantemente. 🚧

Um simulador interativo onde uma **Inteligência Artificial** joga uma partida infinita de Tetris de forma autônoma. Desenvolvido como projeto prático para a disciplina de Programação Orientada a Objetos (POO), o foco principal é a construção de uma arquitetura limpa, escalável e o uso de algoritmos de decisão em tempo real.

---

## ✨ O que já está funcionando (Features atuais)

- [x] **Motor Gráfico Pygame:** Renderização da grade, blocos clássicos e iluminação de fundo (estilo fliperama retrô).
- [x] **Motor de Física Clássico:** Detecção de colisão precisa nas bordas, no fundo e entre as peças.
- [x] **Sistema de Identificação (ID):** Contorno de bug do *Garbage Collector* do Python usando atributos de classe para evitar fusão visual de blocos da mesma cor.
- [x] **Cérebro da IA (V1):** Algoritmo heurístico que avalia o peso de "buracos vazios" vs "altura da pilha" para encontrar a melhor jogada.
- [x] **Rotação Inteligente:** IA capaz de simular e testar as 4 rotações possíveis (0°, 90°, 180° e 270°) através de transposição de matrizes antes de tomar a decisão final.

## 🚀 O que vem por aí (Roadmap)

- [ ] Implementar sistema de Níveis de Dificuldade da IA (Fácil, Médio, Impossível).
- [ ] Adicionar controle de velocidade da simulação através de eventos de teclado.
- [ ] Otimização do tempo de cálculo da IA para matrizes maiores.
- [ ] Adicionar efeitos sonoros clássicos.

---

## 💻 Como rodar o teste na sua máquina

Como o projeto está em desenvolvimento, você pode clonar o repositório para testar o estado atual da IA:

1. Clone este repositório:
   ```bash
   git clone [https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git](https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git)
