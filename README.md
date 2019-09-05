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
* __dump_player__ : calculate the square values of the board, perform a move that tries to get a square with the highest value

* __evil_player__ : calculates the game score by the evaluation function, performing the move that gets the highest score in that state

* __forward_player__ : always move the piece that is in the rows with the highest index and try to capture whenever possible

* __mirror_player__ : whenever possible, try to make the same move as your opponent

* __team_player__ : moves a piece following the neighbors and capturing whenever possible

* __killer_palyer__ : calculates the shortest distance for an opponent in order to eliminate it

* __zigzag_player__ : moves only across the diagonals alternately, capturing whenever possible

* __dodge_player__ : checks if the destination square is occupied and defended, if not defended moves to it

* __conn_player__ : calculates the connectivity of the pieces by performing the movement that will assign a higher connectivity value

* __sup_player__ : check if the destination house is defended by allies, if it is, performes the move

