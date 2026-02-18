"""
Minimal-Test für Pygbag
"""
import asyncio
import pygame

async def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Test")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 74)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((50, 150, 200))
        text = font.render("Pygbag funktioniert!", True, (255, 255, 255))
        screen.blit(text, (100, 250))
        pygame.display.flip()
        clock.tick(60)
        
        await asyncio.sleep(0)  # Wichtig!
    
    pygame.quit()

asyncio.run(main())
