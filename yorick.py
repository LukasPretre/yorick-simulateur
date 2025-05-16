import pygame
import random
import math

# Initialisation
pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Yorick E Trainer")
clock = pygame.time.Clock()

# Couleurs
GRASS_GREEN = (50, 150, 50)
YORICK_COLOR = (200, 0, 0)
TARGET_COLOR = (0, 100, 200)
E_PROJECTILE_COLOR = (255, 200, 0)

# Yorick
yorick = {
    "x": screen_width // 2,
    "y": screen_height // 2,
    "speed": 5,
    "size": 20,
    "e_cooldown": 0
}

# Cibles
targets = []
for _ in range(5):
    targets.append({
        "x": random.randint(0, screen_width),
        "y": random.randint(0, screen_height),
        "size": 25,
        "dx": random.uniform(-2, 2),
        "dy": random.uniform(-2, 2)
    })

# Projectile E
e_projectile = None

# Score
score = 0
font = pygame.font.SysFont(None, 36)

def spawn_target():
    targets.append({
        "x": random.randint(0, screen_width),
        "y": random.randint(0, screen_height),
        "size": 25,
        "dx": random.uniform(-2, 2),
        "dy": random.uniform(-2, 2)
    })

# Game loop
running = True
while running:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e and yorick["e_cooldown"] == 0:  # Lancer E
                mouse_x, mouse_y = pygame.mouse.get_pos()
                angle = math.atan2(mouse_y - yorick["y"], mouse_x - yorick["x"])
                e_projectile = {
                    "x": yorick["x"],
                    "y": yorick["y"],
                    "dx": math.cos(angle) * 10,
                    "dy": math.sin(angle) * 10,
                    "size": 10
                }
                yorick["e_cooldown"] = 20  # Cooldown

    # Déplacement de Yorick (clic droit)
    if pygame.mouse.get_pressed()[2]:  # Clic droit
        mouse_x, mouse_y = pygame.mouse.get_pos()
        angle = math.atan2(mouse_y - yorick["y"], mouse_x - yorick["x"])
        yorick["x"] += math.cos(angle) * yorick["speed"]
        yorick["y"] += math.sin(angle) * yorick["speed"]

    # Mouvement des cibles
    for target in targets:
        target["x"] += target["dx"]
        target["y"] += target["dy"]
        
        # Rebond sur les bords
        if target["x"] <= 0 or target["x"] >= screen_width:
            target["dx"] *= -1
        if target["y"] <= 0 or target["y"] >= screen_height:
            target["dy"] *= -1

    # Mouvement du projectile E
    if e_projectile:
        e_projectile["x"] += e_projectile["dx"]
        e_projectile["y"] += e_projectile["dy"]
        
        # Collision avec les cibles
        for target in targets[:]:
            distance = math.sqrt((e_projectile["x"] - target["x"])**2 + (e_projectile["y"] - target["y"])**2)
            if distance < (e_projectile["size"] + target["size"]) / 2:
                targets.remove(target)
                spawn_target()
                score += 1
                e_projectile = None
                break
        
        # Sortie de l'écran
        if (e_projectile["x"] < 0 or e_projectile["x"] > screen_width or
            e_projectile["y"] < 0 or e_projectile["y"] > screen_height):
            e_projectile = None

    # Cooldown du E
    if yorick["e_cooldown"] > 0:
        yorick["e_cooldown"] -= 1

    # Dessin
    screen.fill(GRASS_GREEN)  # Fond herbe
    
    # Cibles
    for target in targets:
        pygame.draw.rect(screen, TARGET_COLOR, (target["x"] - target["size"] // 2, target["y"] - target["size"] // 2, target["size"], target["size"]))
    
    # Yorick
    pygame.draw.circle(screen, YORICK_COLOR, (yorick["x"], yorick["y"]), yorick["size"])
    
    # Projectile E
    if e_projectile:
        pygame.draw.circle(screen, E_PROJECTILE_COLOR, (int(e_projectile["x"]), int(e_projectile["y"])), e_projectile["size"])
    
    # Score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()