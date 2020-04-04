from function import *

def main():
    clock = pygame.time.Clock()
    infoObject = pygame.display.Info()
    WIN_WIDTH = infoObject.current_w
    WIN_HEIGHT = infoObject.current_h
    win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    dots = []
    for x in range(1000):
        dots.append(Dot())

    players = []
    players.append(Player(players,True))
    for x in range(25):
        players.append( Player(players))
    i=0
    run = True
    while run:
        clock.tick(30)
        i+=1
        #if i%2==0:
        dots.append(Dot())
        dots.append(Dot())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEMOTION:
                players[0].change_direction(event.pos[0],event.pos[1])

        rem = []
        for player in players:
            player.move()

        for x, player in enumerate(players):
            dots = player.eat_dots(dots)
            hoi = player.eat_player(players,x)
            if hoi[0]:
                rem.append(hoi[1])
        for r in rem:
            try:
                players.remove(r)
                players.append(Player(players))
            except: pass
        draw_window(win,players,dots,players[0].size)
    pygame.quit()
    quit()
main()
