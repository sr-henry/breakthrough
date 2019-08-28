# py_breakthrough
 SI202 : Resolução de Problemas I


## Trabalho 1 (individual).
Cada aluno será responsável por analisar o jogo de breakthrough e criar 10 estratégias para verificar se consegue vencer a partida contra um adversário que joga ao acaso. As estratégias podem ser simples e baseadas simplesmente em heurísticas, o seu objetivo é garantir que entende bem o que funciona e o que não funciona no jogo. Por exemplo, algumas estratégias podem ser:

1. Mover sempre o jogador da frente. 
1. Mover sempre o jogador de trás. 
1. Mover em blocos de jogadores. 
1. Capturar sempre que possível.

O que você deverá fazer é implementar programas com alguma dessas estratégias e analisar esses programas. Você deverá implementar o seu programa em um kernel no jupyter e adicionar as suas análises no próprio kernel. Desse modo, ao compartilhar com o professor o seu kernel, ele poderá ver as suas análises e o seus códigos.


## Players
* __dump_player__ : calculate board squares values, making a move that try to get a biggest value

* __evil_player__ : get a game score by evaluation function, making a move for get a biggest game score

* __forward_player__ : always moves the piece that is in a biggest row number and try to capture whenever possible

* __mirror_player__ : whenever possible try to make the same move as your opponent