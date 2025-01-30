# blackjack in python with pygame!
import copy
import random
import pygame

pygame.init() 
# game variables
cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
one_deck = 4 * cards
decks = 4
game_deck = copy.deepcopy(decks * one_deck)
WIDTH = 600
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Pygame Blackjack!')
fps = 60
timer = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 44)
smaller_font = pygame.font.Font('freesansbold.ttf', 36)
active = False
# win, loss, draw/push
records = [0, 0, 0]
player_score = 0
dealer_score = 0
initial_deal = True
my_hand = []
dealer_hand = []
outcome = 0
reveal_dealer = False

# deal cards by selecting randomly from deck, and make function for one card at a time
def deal_cards(current_hand, current_deck):
    card = random.randint(0, len(current_deck))
    current_hand.append(current_deck[card-1])
    current_deck.pop(card-1)
    print(current_hand, current_deck)
    return current_hand, current_deck

# draw cards visually onto screen
def draw_cards(player, dealer, reveal):
    for i in range(len(player)):
        pygame.draw.rect(screen, 'white', [70 + (70 * i), 460 + (5 * i), 120, 220], 0, 5) #70 * i = move to the right
        screen.blit(font.render(player[i], True, 'black'), (75 + 70*i, 465 + 5*i))
        screen.blit(font.render(player[i], True, 'black'), (75 + 70*i, 635 + 5*i))
        pygame.draw.rect(screen, 'red', [70 + (70 * i), 460 + (5 * i), 120, 220], 5, 5) 

    # if player hasn't finished turn, dealer will hide one card
    for i in range(len(dealer)):
        pygame.draw.rect(screen, 'white', [70 + (70 * i), 160 + (5 * i), 120, 220], 0, 5) #70 * i = move to the right
        if i  != 0 or reveal:
            screen.blit(font.render(player[i], True, 'black'), (75 + 70*i, 165 + 5*i))
            screen.blit(font.render(player[i], True, 'black'), (75 + 70*i, 335 + 5*i))
        else:
            screen.blit(font.render(player[i], True, 'black'), (75 + 70*i, 165 + 5*i))
            screen.blit(font.render(player[i], True, 'black'), (75 + 70*i, 335 + 5*i))
        pygame.draw.rect(screen, 'red', [70 + (70 * i), 160 + (5 * i), 120, 220], 5, 5) 

# draw game conditions and buttons
def draw_game(act, record):
    button_list = []
    # initially on startup (not active) only option is to deal new hand
    if not act:
        deal = pygame.draw.rect(screen, 'white', [150, 20, 300, 100], 0, 5) # draw rectangle on the screen
        pygame.draw.rect(screen, 'blue', [150, 20, 300, 100], 3, 5) # border around the white button
        deal_text = font.render('DEAL HAND', True, 'black')
        screen.blit(deal_text, (165, 50))
        button_list.append(deal)
    # once game started, show hit and stand buttons and win/loss records
    else: 
        hit = pygame.draw.rect(screen, 'white', [0, 700, 300, 100], 0, 5) # draw rectangle on the screen
        pygame.draw.rect(screen, 'blue', [0, 700, 300, 100], 3, 5) # border around the white button
        hit_text = font.render('HIT ME', True, 'black')
        screen.blit(hit_text, (55, 735))
        button_list.append(hit)
        stand = pygame.draw.rect(screen, 'white', [300, 700, 300, 100], 0, 5) # draw rectangle on the screen
        pygame.draw.rect(screen, 'blue', [300, 700, 300, 100], 3, 5) # border around the white button
        stand_text = font.render('STAND', True, 'black')
        screen.blit(stand_text, (355, 735))
        button_list.append(stand)
        score_text = smaller_font.render(f'Wins: {record[0]}   Losses: {record[1]}   Draws: {record[2]}', True, 'white')
        screen.blit(score_text, (15, 840))

    return button_list


# main game loop
run = True
while run:
    # run game at our framerate and fill screen with bg color
    timer.tick(fps)
    screen.fill('black')
    # intial deal to player and dealer
    if initial_deal:
        for i in range(2):
            my_hand, game_deck = deal_cards(my_hand, game_deck)
            dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        print(my_hand, dealer_hand)
        initial_deal = False
    # once game is activated, and dealt, calculate scores and display cards
    if active:
        draw_cards(my_hand, dealer_hand, reveal_dealer)
    buttons = draw_game(active, records)


    # event handling, if quit pressed, then exit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            if not active:
                if buttons[0].collidepoint(event.pos):
                    active = True
                    initial_deal = True
                    my_hand = []
                    dealer_hand = []
                    outcome = 0
    
    pygame.display.flip() # make sure everything is flipped onto the screen
pygame.quit() # while-loop exited


# 27:24: initial deal https://youtu.be/e3YkdOXhFpQ?t=1644