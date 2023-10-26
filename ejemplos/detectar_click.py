import pygame

# Configuración
pygame.init()
fps = 60
clock = pygame.time.Clock()

ancho, altura = (480, 320)
pantalla = pygame.display.set_mode((ancho, altura))



# delta time
current_time = pygame.time.get_ticks()
previous_time = current_time
clicks = []
while True:
    pantalla.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
        # AQUI SE DETECTA EL CLICK DENTRO DE LOS EVENTOS
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                mouse_x, mouse_y = event.pos
                print(mouse_x, mouse_y)
                # O tambien lo puedes hacer de esta manera
                mouse_x, mouse_y = pygame.mouse.get_pos()
                print(mouse_x, mouse_y)
                clicks.append((mouse_x, mouse_y))
                
    # update
    deltatime = (current_time - previous_time) / 1000.0  # Tiempo en segundos
    previous_time = deltatime
    
    # Draw
    for x, y in clicks:
        # surface / pantalla, color, rectangulo(x, y, ancho, alto)
        pygame.draw.rect(pantalla, (255, 0, 0), (x, y, 10, 10))
    # Final
    pygame.display.flip()
    clock.tick(fps)
