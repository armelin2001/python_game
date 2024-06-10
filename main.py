import pygame as pg
from random import randrange

# Inicializar Lib do Pygame
pg.init()

# Constantes de dificuldade
FACIL, MEDIO, DIFICIL = 150, 100, 50
LISTA_PONTUACAO_DIFFICULDADE = [10, 20, 30]

# Constantes do jogo
TAMANHO_JANELA = 1000  # tamanho total da janela
TAMANHO_BLOCO = 50  # tamanho de cada quadrado
DISTANCIA = (TAMANHO_BLOCO // 2, TAMANHO_JANELA - TAMANHO_BLOCO // 2, TAMANHO_BLOCO)  # define distância que a cobra pode se mover

def retorna_maior_pontuacao(lista_pontuacao):
    return max(lista_pontuacao)

def mostrar_texto(tela, texto, fonte, cor, posicao):
    render = fonte.render(texto, True, cor)
    tela.blit(render, posicao)

def criar_menu():
    font = pg.font.Font('freesansbold.ttf', 20)
    menu = True
    dificuldade = MEDIO

    while menu:

        tela.fill('black')
        mostrar_texto(tela, "Jogo da Cobra", font, (255, 255, 255), (TAMANHO_JANELA // 2 - 100, TAMANHO_JANELA // 2 - 100))
        mostrar_texto(tela, "1. Iniciar Jogo", font, (255, 255, 255), (TAMANHO_JANELA // 2 - 100, TAMANHO_JANELA // 2 - 50))
        mostrar_texto(tela, f"2. Mudar Dificuldade (Atual: {['FACIL', 'MEDIO', 'DIFICIL'][[FACIL, MEDIO, DIFICIL].index(dificuldade)]})", font, (255, 255, 255), (TAMANHO_JANELA // 2 - 100, TAMANHO_JANELA // 2))
        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    exit()
                if event.key == pg.K_1:
                    return dificuldade
                if event.key == pg.K_2:
                    dificuldade = [FACIL, MEDIO, DIFICIL][([FACIL, MEDIO, DIFICIL].index(dificuldade) + 1) % 3]

def fim_jogo(): 
    font = pg.font.Font('freesansbold.ttf', 50)
    tela.fill('black')
    mostrar_texto(tela, "Fim de Jogo Parabens!!!!", font, (255, 255, 255), (TAMANHO_JANELA // 2 - 100, TAMANHO_JANELA // 2 - 100))
    pg.display.flip()
    pg.time.wait(3000)
    criar_menu()

def jogo(dificuldade):
    pontuacoes = [0]
    textX, textY = 10, 10
    get_posicao_aleatoria = lambda: [randrange(*DISTANCIA), randrange(*DISTANCIA)]  # pegar posição aleatória
    time, time_step = 0, dificuldade    
    font = pg.font.Font('freesansbold.ttf', 20)
    dirs = {pg.K_w: (0, -TAMANHO_BLOCO), pg.K_s: (0, TAMANHO_BLOCO), pg.K_a: (-TAMANHO_BLOCO, 0), pg.K_d: (TAMANHO_BLOCO, 0)}  # definir direções
    cobra = pg.Rect([0, 0, TAMANHO_BLOCO - 2, TAMANHO_BLOCO - 2])  # criar cobra
    cobra.center = get_posicao_aleatoria()  # posicionar cobra
    tamanho_cobra = 1  # tamanho inicial da cobra
    segmentos = [cobra.copy()]  # criar segmentos da cobra
    cobra_dir = (0, 0)
    mostra_diminuir = True

    comida = cobra.copy()  # criar comida
    diminuir = cobra.copy()  # diminuir tamanho
    comida.center = get_posicao_aleatoria()  # posicionar comida
    tela = pg.display.set_mode([TAMANHO_JANELA] * 2)  # criar tela do jogo
    clock = pg.time.Clock()  # criar clock

    while True:
        if dificuldade == FACIL:
            mostra_diminuir = False
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:  # definir movimento da cobra nas teclas w, a, s, d
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    exit()
                if event.key == pg.K_w and dirs[pg.K_w]:
                    cobra_dir = (0, -TAMANHO_BLOCO)
                    dirs = {pg.K_w: 1, pg.K_s: 0, pg.K_a: 1, pg.K_d: 1}
                if event.key == pg.K_s and dirs[pg.K_s]:
                    cobra_dir = (0, TAMANHO_BLOCO)
                    dirs = {pg.K_w: 0, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}
                if event.key == pg.K_a and dirs[pg.K_a]:
                    cobra_dir = (-TAMANHO_BLOCO, 0)
                    dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 0}
                if event.key == pg.K_d and dirs[pg.K_d]:
                    cobra_dir = (TAMANHO_BLOCO, 0)
                    dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 0, pg.K_d: 1}
        tela.fill('black')
        self_eating = pg.Rect.collidelist(cobra, segmentos[:0]) != -1  # verificar se a cobra se comeu
        if cobra.left < 0 or cobra.right > TAMANHO_JANELA or cobra.top < 0 or cobra.bottom > TAMANHO_JANELA or self_eating:  # verificar se a cobra saiu da tela
            pontuacoes.append(tamanho_cobra)
            cobra.center, comida.center = get_posicao_aleatoria(), get_posicao_aleatoria()
            tamanho_cobra, cobra_dir = 1, (0, 0)
            segmentos = [cobra.copy()]
        if cobra.center == comida.center:
            comida.center = get_posicao_aleatoria()
            tamanho_cobra += 1
        if cobra.center == diminuir.center:        
            diminuir.center = get_posicao_aleatoria()
            if len(segmentos) > 1:
                segmentos.pop()
                tamanho_cobra -= 1
        if len(segmentos) > 1 and mostra_diminuir:
            pg.draw.rect(tela, 'blue', diminuir)
        pg.draw.rect(tela, 'red', comida)  # desenhar comida na tela
        [pg.draw.rect(tela, 'green', segmento) for segmento in segmentos]  # desenhar segmentos da cobra
        time_now = pg.time.get_ticks()  # pegar tempo atual
        if time_now - time > time_step:  # adicionar segmento a cada 100ms
            time = time_now
            cobra.move_ip(cobra_dir)  # mover cobra
            segmentos.append(cobra.copy())  # adicionar segmento
            segmentos = segmentos[-tamanho_cobra:]  # definir tamanho da cobra
        pontuacao_atual_texto = font.render("Pontuacao: " + str(tamanho_cobra), True, (255, 255, 255))
        pontuacao_maxima_texto = font.render("Maior Pontuacao: " + str(retorna_maior_pontuacao(pontuacoes)), True, (255, 255, 255))
        tela.blit(pontuacao_atual_texto, (textX, textY))
        tela.blit(pontuacao_maxima_texto, (textX, textY + 40))
        pg.display.flip()
        clock.tick(60)  # definir fps do jogo

        #encerra o jogo baseado na lista de pontuações usando a dificuldade selecionada
        if tamanho_cobra >= LISTA_PONTUACAO_DIFFICULDADE[[FACIL, MEDIO, DIFICIL].index(dificuldade)]:
            tamanho_cobra = 1
            fim_jogo()
            


if __name__ == '__main__':
    tela = pg.display.set_mode([TAMANHO_JANELA] * 2)
    dificuldade_selecionada = criar_menu()
    jogo(dificuldade_selecionada)  # iniciar jogo
