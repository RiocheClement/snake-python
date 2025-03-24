import pygame
import time
import random

pygame.init()

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (213, 50, 80)
VERT = (0, 255, 0)
BLEU = (50, 153, 213)

# Dimensions de l'écran
LARGEUR = 600
HAUTEUR = 400

# Taille d'une cellule du serpent
TAILLE_BLOC = 10

# Vitesse du jeu (FPS)
VITESSE = 15

# Initialisation de l'écran
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption('Snake Game')

horloge = pygame.time.Clock()

police = pygame.font.SysFont("bahnschrift", 25)
grande_police = pygame.font.SysFont("comicsansms", 20)

def afficher_score(score):
    """Affiche le score actuel"""
    texte = police.render("Score: " + str(score), True, BLANC)
    fenetre.blit(texte, [0, 0])

def dessiner_serpent(taille_bloc, liste_serpent):
    """Dessine le serpent"""
    for bloc in liste_serpent:
        pygame.draw.rect(fenetre, VERT, [bloc[0], bloc[1], taille_bloc, taille_bloc])

def dessiner_pomme(x, y):
    """Dessine la pomme"""
    pygame.draw.rect(fenetre, ROUGE, [x, y, TAILLE_BLOC, TAILLE_BLOC])

def afficher_message(msg, couleur, y_deplace=0):
    """Affiche un message"""
    texte_surface = grande_police.render(msg, True, couleur)
    texte_rect = texte_surface.get_rect(center=(LARGEUR/2, HAUTEUR/2 + y_deplace))
    fenetre.blit(texte_surface, texte_rect)

def pause():
    """Met le jeu en pause"""
    en_pause = True
    afficher_message("Pause", BLANC)
    afficher_message("Appuyez sur Espace pour continuer", BLANC, 50)
    pygame.display.update()
    
    while en_pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    en_pause = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        horloge.tick(5)

def game_loop():
    """Boucle principale du jeu"""
    game_over = False
    game_exit = False
    
    # Position initiale du serpent
    x1 = LARGEUR / 2
    y1 = HAUTEUR / 2
    
    # Changement de position
    x1_change = 0
    y1_change = 0
    
    # Liste contenant les segments du serpent
    liste_serpent = []
    longueur_serpent = 1
    
    # Position de la première pomme
    pomme_x = round(random.randrange(0, LARGEUR - TAILLE_BLOC) / 10.0) * 10.0
    pomme_y = round(random.randrange(0, HAUTEUR - TAILLE_BLOC) / 10.0) * 10.0
    
    while not game_exit:
        
        while game_over:
            fenetre.fill(NOIR)
            afficher_message("Game Over!", ROUGE, -50)
            afficher_message("Appuyez sur C pour rejouer ou Q pour quitter", BLANC, 50)
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
                    game_over = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_exit = True
                        game_over = False
                    if event.key == pygame.K_c:
                        game_loop()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -TAILLE_BLOC
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = TAILLE_BLOC
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -TAILLE_BLOC
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = TAILLE_BLOC
                    x1_change = 0
                elif event.key == pygame.K_p:
                    pause()
        
        # Vérifier si le serpent touche les bords
        if x1 >= LARGEUR or x1 < 0 or y1 >= HAUTEUR or y1 < 0:
            game_over = True
            
        x1 += x1_change
        y1 += y1_change
        fenetre.fill(NOIR)
        
        dessiner_pomme(pomme_x, pomme_y)
        
        tete_serpent = []
        tete_serpent.append(x1)
        tete_serpent.append(y1)
        liste_serpent.append(tete_serpent)
        
        if len(liste_serpent) > longueur_serpent:
            del liste_serpent[0]
            
        # Vérifier si le serpent se touche lui-même
        for segment in liste_serpent[:-1]:
            if segment == tete_serpent:
                game_over = True
                
        dessiner_serpent(TAILLE_BLOC, liste_serpent)
        afficher_score(longueur_serpent - 1)
        
        pygame.display.update()
        
        # Vérifier si le serpent a mangé la pomme
        if x1 == pomme_x and y1 == pomme_y:
            pomme_x = round(random.randrange(0, LARGEUR - TAILLE_BLOC) / 10.0) * 10.0
            pomme_y = round(random.randrange(0, HAUTEUR - TAILLE_BLOC) / 10.0) * 10.0
            longueur_serpent += 1
            
        horloge.tick(VITESSE)
    
    pygame.quit()
    quit()

def ecran_accueil():
    """Affiche l'écran d'accueil"""
    intro = True
    
    while intro:
        fenetre.fill(NOIR)
        afficher_message("Snake Game", VERT, -100)
        afficher_message("Le but du jeu est de manger des pommes", BLANC, -30)
        afficher_message("Plus vous mangez, plus vous grandissez", BLANC, 10)
        afficher_message("Si vous touchez les bords ou vous-même, vous perdez", BLANC, 50)
        afficher_message("Appuyez sur C pour jouer, P pour pause, Q pour quitter", BLANC, 110)
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
    
    game_loop()

# Démarrage du jeu
ecran_accueil()
