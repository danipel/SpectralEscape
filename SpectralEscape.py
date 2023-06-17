from classes import *



def main(character):
    import pygame
    import pygame.mixer
    from main_menu import menu


    pygame.init()
    pygame.mixer.init()

    # Create an 800x600 sized screen
    screen = pygame.display.set_mode((800, 600), pygame.SRCALPHA, pygame.NOFRAME)

    # Set the title of the window
    pygame.display.set_caption('Spectral Escape')

    #  Sounds
    pygame.mixer.music.load("sounds/Memoraphile - Spooky Dungeon.wav")
    get_key_sound = pygame.mixer.Sound("sounds/get_key_sound.wav")
    success_sound = pygame.mixer.Sound("sounds/success_sound.mp3")
    game_over_sound = pygame.mixer.Sound("sounds/fail_sound.mp3")


    # Create the player
    player = Player(380, 470)

    #  Add the idle images to the player's walking frames
    if character == 1:
        player.walking_frames_l.append(pygame.image.load("characters/player_1/idle_left.png").convert())
        player.walking_frames_r.append(pygame.image.load("characters/player_1/idle_right.png").convert())
        player.walking_frames_u.append(pygame.image.load("characters/player_1/idle_up.png").convert())
        player.walking_frames_d.append(pygame.image.load("characters/player_1/idle_down.png").convert())
        npc_img = pygame.image.load("characters/player_2/idle_down.png").convert()
        #  Add the walking images to the player's walking frames
        for animation in ["walk_left", "walk_right", "walk_up", "walk_down"]:
            for i in range(1, 3):
                image_path = f"characters/player_1/{animation}_{i}.png"
                image = pygame.image.load(image_path).convert()
                if animation == "walk_left":
                    player.walking_frames_l.append(image)
                elif animation == "walk_right":
                    player.walking_frames_r.append(image)
                elif animation == "walk_up":
                    player.walking_frames_u.append(image)
                elif animation == "walk_down":
                    player.walking_frames_d.append(image)
    elif character == 2:
        player.walking_frames_l.append(pygame.image.load("characters/player_2/idle_left.png").convert())
        player.walking_frames_r.append(pygame.image.load("characters/player_2/idle_right.png").convert())
        player.walking_frames_u.append(pygame.image.load("characters/player_2/idle_up.png").convert())
        player.walking_frames_d.append(pygame.image.load("characters/player_2/idle_down.png").convert())
        npc_img = pygame.image.load("characters/player_1/idle_down.png").convert()
        # Add the walking images to the player's walking frames
        for animation in ["walk_left", "walk_right", "walk_up", "walk_down"]:
            for i in range(1, 3):
                image_path = f"characters/player_2/{animation}_{i}.png"
                image = pygame.image.load(image_path).convert()
                if animation == "walk_left":
                    player.walking_frames_l.append(image)
                elif animation == "walk_right":
                    player.walking_frames_r.append(image)
                elif animation == "walk_up":
                    player.walking_frames_u.append(image)
                elif animation == "walk_down":
                    player.walking_frames_d.append(image)

    

    moving_sprites = pygame.sprite.Group()
    # Add the player to a list of moving sprites
    moving_sprites.add(player)

    # Create the rooms list
    rooms = []
    room = Room1()
    rooms.append(room)
    room = Room2()
    rooms.append(room)
    room = Room3()
    rooms.append(room)
    room = Room4()
    rooms.append(room)
    room = Room5()
    rooms.append(room)
    room = Room6()
    rooms.append(room)

    # Create the NPC
    npc = NPC(386, 286, npc_img)
    #  Add the NPC to the final room
    rooms[3].interactives_list.add(npc)

    #  Set the current room
    current_room_no = 0
    current_room = rooms[current_room_no]

    #  Create the clock
    clock = pygame.time.Clock()

    #  Create the font for messages
    font = pygame.font.Font(None, 25)
    msg = None

    #  Create the game over variable
    game_over = False

    #  Create the variables for the player's walking animation
    walk_index = 0
    walk_dir = None

    #  Create the variables for the player's animation cooldown
    last_update = pygame.time.get_ticks()
    animation_cooldown = 200

    #  Start music
    pygame.mixer.music.play(-1)
    while not game_over:
        

        # --- Event Processing ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            #  If the user presses a key down, check if it is a key that moves the player
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player.changespeed(-2, 0)
                    msg = None
                    walk_dir = "left"
                if event.key == pygame.K_d:
                    player.changespeed(2, 0)
                    msg = None
                    walk_dir = "right"
                if event.key == pygame.K_w:
                    player.changespeed(0, -2)
                    msg = None
                    walk_dir = "up"
                if event.key == pygame.K_s:
                    player.changespeed(0, 2)
                    msg = None
                    walk_dir = "down"

                #  If the user presses c, check if the player is colliding with a door
                #  or an interactive and all the actions within.
                if event.key == pygame.K_c:
                    for door in current_room.door_list:
                        if player.rect.colliderect(door.rect):
                            if door.room == 1:
                                current_room_no = 1
                                player.rect.x = 620
                                player.rect.y = 500
                                #  Kill the previous ghosts
                                if len(current_room.enemy_list) != 0:
                                    for enemy in current_room.enemy_list:
                                        moving_sprites.remove(enemy)  # Remove the ghost from the sprite group
                                        enemy.kill()  # Kill the ghost
                                #  Respawn the ghosts if the player is in the same room
                                for enemy in current_room.enemy_list:                                  
                                    enemy.respawn()
                            elif door.room == 2:
                                current_room_no = 2
                                player.rect.x = 245
                                player.rect.y = 490
                                #  Kill the previous ghosts
                                if len(current_room.enemy_list) != 0:
                                    for enemy in current_room.enemy_list:
                                        moving_sprites.remove(enemy)  #  Remove the ghost from the sprite group
                                        enemy.kill()  #  Kill the ghost
                                #  Respawn the ghosts if the player is in the same room
                                for enemy in current_room.enemy_list:
                                    enemy.respawn()
                            elif door.room == 0:
                                current_room_no = 0
                                player.rect.x = 380
                                player.rect.y = 470
                                #  Kill the previous ghosts
                                if len(current_room.enemy_list) != 0:
                                    for enemy in current_room.enemy_list:
                                        moving_sprites.remove(enemy)  #  Remove the ghost from the sprite group
                                        enemy.kill()  #  Kill the ghost
                                            #  Respawn the ghosts if the player is in the same room
                                        for enemy in current_room.enemy_list:
                                            enemy.respawn()
                            else:
                                if len(player.key_list) != 0:
                                    for key in player.key_list:
                                        if key.room == 3 and door.room == 3:
                                            current_room_no = 3
                                            player.rect.x = 360
                                            player.rect.y = 485
                                            #  Kill the previous ghosts
                                            if len(current_room.enemy_list) != 0:
                                                for enemy in current_room.enemy_list:
                                                    moving_sprites.remove(enemy)  #  Remove the ghost from the sprite group
                                                    enemy.kill()  #  Kill the ghost
                                            #  Respawn the ghosts if the player is in the same room
                                            for enemy in current_room.enemy_list:
                                                enemy.respawn()
                                        elif key.room == 4 and door.room == 4:
                                            current_room_no = 4
                                            player.rect.x = 366
                                            player.rect.y = 500
                                            #  Kill the previous ghosts
                                            if len(current_room.enemy_list) != 0:
                                                for enemy in current_room.enemy_list:
                                                    moving_sprites.remove(enemy)  #  Remove the ghost from the sprite group
                                                    enemy.kill()  #  Kill the ghost
                                            #  Respawn the ghosts if the player is in the same room
                                            for enemy in current_room.enemy_list:      
                                                enemy.respawn()
                                        elif key.room == 5 and door.room == 5:
                                            current_room_no = 5
                                            player.rect.x = 120
                                            player.rect.y = 510
                                            #  Kill the previous ghosts
                                            if len(current_room.enemy_list) != 0:
                                                for enemy in current_room.enemy_list:                      
                                                    moving_sprites.remove(enemy)  # Remove the ghost from the sprite group
                                                    enemy.kill()  #  Kill the ghost
                                            #  Respawn the ghosts if the player is in the same room
                                            for enemy in current_room.enemy_list:
                                                enemy.respawn()
                                        #  If the player is colliding with the wardrobe, check if the player has the key
                                        elif key.room == 6 and door.room == 6:  # 6 is the wardrobe and the final clue
                                            msg = font.render("Check behind the stereo!", True, RED)
                                            #  Unlock The final key
                                            rooms[4].interactives_list.append(Key(643, 204))
                                            #  Add the room every key leads to.
                                            rooms[4].interactives_list[0].room = 3
                                        else:
                                            msg = font.render("You do not have the key...", True, WHITE)
                                else:
                                    msg = font.render("You do not have any key...", True, WHITE)
                            current_room = rooms[current_room_no]

                    #  If the player is colliding with an item, add it to the player's key list  
                    for item in current_room.interactives_list:
                        if player.rect.colliderect(item.rect):
                            player.key_list.add(item)
                            get_key_sound.play()
                            current_room.interactives_list.remove(item)
                            
            #  If the user lets go of a key...
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    player.changespeed(2, 0)
                    #  Set idle frame to player's left
                    player.image = player.walking_frames_l[0]
                    walk_dir = None
                if event.key == pygame.K_d:
                    player.changespeed(-2, 0)
                    #  Set idle frame to player's right
                    player.image = player.walking_frames_r[0]
                    walk_dir = None
                if event.key == pygame.K_w:
                    player.changespeed(0, 2)
                    #  Set idle frame to player's up
                    player.image = player.walking_frames_u[0]
                    walk_dir = None
                if event.key == pygame.K_s:
                    player.changespeed(0, -2)
                    #  Set idle frame to player's down
                    player.image = player.walking_frames_d[0]
                    walk_dir = None
        
        # --- Game Logic ---

        #  Move the player
        player.move(current_room.wall_list)
        if walk_dir != None:
            player.walk(walk_dir, walk_index)
            if animation_cooldown < pygame.time.get_ticks() - last_update:
                last_update = pygame.time.get_ticks()
                walk_index += 1
            if walk_index > 2:
                walk_index = 1        
            
        #  Move and update the ghosts
        control = 0
        if len(current_room.enemy_list) != 0:
            for enemy in current_room.enemy_list:
                control += 1
                if type(enemy) == WhiteGhost:
                    if isinstance(enemy, WhiteGhost) and control%2 != 0:
                        enemy.ghost_move("right")
                        enemy.change_sprite("right")
                    elif isinstance(enemy, WhiteGhost) and control%2 == 0:
                        enemy.ghost_move("left")
                        enemy.change_sprite("left")
                elif type(enemy) == BlueGhost:
                    if isinstance(enemy, BlueGhost) and control%2 != 0:
                        enemy.ghost_move("up")
                        enemy.change_sprite("up")
                    elif isinstance(enemy, BlueGhost) and control%2 == 0:
                        enemy.ghost_move("down")
                        enemy.change_sprite("down")
                elif type(enemy) == BlackGhost:
                    enemy.ghost_move()
                    enemy.change_sprite()                    
        
        #  If the player collides with a ghost, the player dies
        for enemy in current_room.enemy_list:
            if player.rect.colliderect(enemy.rect):
                player.kill()
                game_over_sound.play()
                clock.tick(0.8)
                print("Game Over")
                game_over = True
        
        #  If the player collides with the npc, the player wins
        if current_room_no == 3:
            if player.rect.colliderect(npc.rect):
                print("You Win!")
                success_sound.play()
                clock.tick(0.8)
                game_over = True

        # --- Drawing ---

        #  Background
        screen.blit(current_room.background, (0, 0))

        #  Draw the door message if aproaching a door
        for door in current_room.door_list:
            if player.rect.colliderect(door.rect):
                if msg == None:
                    msg = font.render("Press C to enter", True, WHITE)
                screen.blit(msg, [door.rect.x -40, door.rect.y - 20]) 

        #  Draw the interactive message if aproaching an interactive object
        for item in current_room.interactives_list:
            if player.rect.colliderect(item.rect):
                if msg == None:
                    msg = font.render("Press C to collect", True, WHITE)
                screen.blit(msg, [item.rect.x -40, item.rect.y - 20])

        #  Draw the keys of the player if any
        if len(player.key_list) != 0:
            add = -10
            for key in player.key_list:
                add += 20
                screen.blit(key.image, [10 + add, 566])
                
        #  Add ghosts to moving sprites
        if len(current_room.enemy_list) != 0:
            for enemy in current_room.enemy_list:
                moving_sprites.add(enemy)

        #  Draw npc if in the final room
        if current_room_no == 3:
            current_room.interactives_list.draw(screen)

        #  Draw the the entities
        moving_sprites.draw(screen)
        
        #  Update the screen
        pygame.display.flip()

        #  Limit to 60 frames per second
        clock.tick(60)

    
    menu()
    
if __name__ == "__main__":
    pygame.display.quit()
    pygame.quit()
    pygame.mixer.quit()


        