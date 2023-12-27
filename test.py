import pygame as pg, sys
pg.init()
screen = pg.display.set_mode((800, 600))
while True:
  screen.fill('cyan')
  pg.display.update()
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
