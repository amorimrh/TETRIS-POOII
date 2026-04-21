# 🕹️ Tetris Automático com IA (POO II)

![Status](https://img.shields.io/badge/Status-Em_Desenvolvimento-warning?style=for-the-badge&logo=github)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-informational?style=for-the-badge&logo=python)

> **Aviso:** Este projeto está atualmente em desenvolvimento! Novas funcionalidades e refatorações estão sendo aplicadas constantemente. 🚧

Um simulador interativo onde uma **Inteligência Artificial** joga uma partida infinita de Tetris de forma autônoma. Desenvolvido como projeto prático para a disciplina de Programação Orientada a Objetos II (POO II), o foco principal é a construção de uma arquitetura limpa, escalável e o uso de algoritmos de decisão em tempo real.

---

## ✨ O que já está funcionando (Features atuais)

- [x] **Arquitetura POO Sólida:** Uso de Classes Abstratas, Encapsulamento de matrizes (Getters/Setters) e Métodos Estáticos para reaproveitamento de código visual.
- [x] **Sistema de Identificação (ID):** Contorno inteligente do *Garbage Collector* do Python usando **Atributos de Classe** para evitar a fusão visual de blocos da mesma cor.
- [x] **Cérebro da IA (V1):** Algoritmo heurístico que avalia o peso de "buracos vazios" vs "altura da pilha" para encontrar a melhor jogada.
- [x] **Rotação Inteligente de Matrizes:** A IA é capaz de simular e testar as 4 rotações possíveis (0°, 90°, 180° e 270°) através da transposição de matrizes antes de tomar a decisão final.
- [x] **Motor Gráfico Clássico:** Renderização usando Pygame com física de colisão, iluminação de fundo da grade e blocos em estilo fliperama retrô.

## 🚀 O que vem por aí (Roadmap)

- [ ] Implementar sistema de Níveis de Dificuldade da IA (Fácil, Médio, Impossível) manipulando a velocidade e a heurística.
- [ ] Otimização do tempo de cálculo (Delta Time) para simulações mais precisas.
- [ ] Adicionar efeitos sonoros clássicos.

---

## 💻 Como rodar na sua máquina

Como o projeto está em desenvolvimento, você pode testar o estado atual da IA clonando o repositório. Siga os passos abaixo:

1. **Instale o Python 3.x:**
   Certifique-se de ter o Python 3 instalado no seu computador. Caso não tenha, você pode baixar a versão mais recente no site oficial: [python.org](https://www.python.org/downloads/).
   *(Dica: Durante a instalação no Windows, não esqueça de marcar a caixa "Add Python to PATH").*

2. **Clone este repositório:**
   Abra o seu terminal (ou prompt de comando) e digite:
   ```bash
   git clone [Repositório Tetris](https://github.com/amorimrh/TETRIS-POOII.git)
