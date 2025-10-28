# Zoológico Interativo 

Este projeto é uma simulação interativa de um zoológico desenvolvida em Python, utilizando as bibliotecas: thinker é a interface gráfica do projeto. A biblioteca playsound funciona como reprodutor de arquivos mp3 em ambiente local. A pillow é o processamento de imagens para exibição. A threading permite a perda de energia dos animais no segundo plano, sem bloquear a GUI.

## 🎯 Objetivo

O objetivo é gerir um grupo de animais virtuais (como onças, macacos, elefantes, etc.), garantindo que sejam alimentados antes que fiquem exaustos:

- **Simulação de Energia**: Cada animal possui um nível de energia que diminui 5% a cada 5 segundos;

- **Interface Gráfica (GUI)**: Interface simples e amigável construída para interagir com os animais;

- **Monitoramento em Tempo Real**: Barras de progresso atualizadas a cada 2 segundos exibem o nível de energia e o estado de cada animal (Ativo, Fraco ou Exausto);
  
- **Falar/Som**: Ao interagir, o animal emite o seu som, consome 10% de energia;

- **Visualização**: A imagem do animal é exibida num pop-up por 10 segundos durante a interação;

- **Estados Visuais**: Imagens diferentes são mostradas se o animal estiver ativo ou com pouca energia/exausto;

- **Classes POO**: Estrutura organizada usando Programação Orientada a Objetos, permitindo fácil adição de novos tipos de animais;

- ## 💻 Tecnologias Utilizadas:
- **Python;**
- **Tkinter** (Interface Gráfica);
- **Playgroud** (Reprodução de arquivos de som);
- **Pillow** (Procesamento de imagens para exibição;
- **Threading** (Funcioamento de uma segunda tela, sem bloquear a GUI).

- ## Antes de rodar o código, necessário instalar as bibliotecas do Pillow e Playground, no terminal:
  pip install Pillow playsound
   
