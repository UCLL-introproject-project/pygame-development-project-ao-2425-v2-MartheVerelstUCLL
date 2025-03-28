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
smaller_font = pygame.font.Font('freesansbold.ttf', 22)
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
hand_active = False
outcome = 0
add_score = False
showing_rules = False
player_name = ""
input = True


# allow user to enter their name
def enter_name():
    name_field = pygame.Rect(150, 300, 300, 50)
    pygame.draw.rect(screen, 'black', name_field)
    pygame.draw.rect(screen, 'white', name_field, 2)
    if player_name == "":
        text = smaller_font.render("Type your name and enter", True, 'gray')
    else:
        text = font.render(player_name, True, 'white')
    screen.blit(text, (name_field.x + 10, name_field.y + 10))

# create a button that shows the rules
def show_rules():
    global showing_rules
    rules_button = pygame.draw.circle(screen, 'white', (500, 50), 30)
    rules_text = font.render('?', True, 'black')
    text_rect = rules_text.get_rect(center=(500,50)) 
    screen.blit(rules_text, text_rect)

    # draw rectangle with text when you want to show the rules
    if showing_rules:
        pygame.draw.rect(screen, 'white',[100, 200, 400, 400], 0, 10)  
        pygame.draw.rect(screen, 'black', [100, 200, 400, 400], 5, 10)
        for i, line in enumerate ([
            "Blackjack Rules:",
            "- Get as close to 21 as possible.",
            "- Number cards: Face value.",
            "- Face cards (J, Q, K): 10 points.",
            "- Aces: 1 or 11 points.",
            "- Beat the dealer without busting!",
            "Click anywhere to return."
        ]):
            rule_text = smaller_font.render(line, True, 'black')
            screen.blit(rule_text, (120, 220 + i * 50))
    return rules_button

# deal cards by selecting randomly from deck, and make function for one card at a time
def deal_cards(current_hand, current_deck):
    card = random.randint(0, len(current_deck))
    current_hand.append(current_deck[card-1])
    current_deck.pop(card-1)
    return current_hand, current_deck

# draw scores for player and dealer on screen
def draw_scores(player, dealer):
    screen.blit(font.render(f'{player_name}[{player}]', True, 'white'), (350, 400))
    if reveal_dealer:
        screen.blit(font.render(f'Dealer[{dealer}]', True, 'white'), (350, 100))

# draw cards visually onto screen
def draw_cards(player, dealer, reveal):
    for i in range(len(player)):
        pygame.draw.rect(screen, 'white', [70 + (70 * i), 460 + (5 * i), 120, 220], 0, 5) 
        screen.blit(font.render(player[i], True, 'black'), (75 + 70*i, 465 + 5*i))
        screen.blit(font.render(player[i], True, 'black'), (75 + 70*i, 635 + 5*i))
        pygame.draw.rect(screen, 'red', [70 + (70 * i), 460 + (5 * i), 120, 220], 5, 5) 

    # if player hasn't finished turn, dealer will hide one card
    for i in range(len(dealer)):
        pygame.draw.rect(screen, 'white', [70 + (70 * i), 160 + (5 * i), 120, 220], 0, 5) 
        if i  != 0 or reveal:
            screen.blit(font.render(dealer[i], True, 'black'), (75 + 70*i, 165 + 5*i))
            screen.blit(font.render(dealer[i], True, 'black'), (75 + 70*i, 335 + 5*i))
        else:
            screen.blit(font.render('???', True, 'black'), (75 + 70*i, 165 + 5*i))
            screen.blit(font.render('???', True, 'black'), (75 + 70*i, 335 + 5*i))
        pygame.draw.rect(screen, 'yellow', [70 + (70 * i), 160 + (5 * i), 120, 220], 5, 5) 

# pass in player or dealer hand and get best score possible
def calculate_score(hand):
    # calculate hand score fresh every time, check how many aces we have
    hand_score = 0
    aces_count = hand.count('A')
    for i in range(len(hand)):
        # for 2,3,4,5,6,7,8,9 - just add the number to total
        for j in range(8):
            if hand[i] == cards[j]:
                hand_score += int(hand[i])
        # for 10 and face cards, add 10
        if hand[i] in ['10', 'J', 'Q', 'K']:
            hand_score += 10
        # for aces start by adding 11, we'll check if we need to reduce afterwards
        elif hand[i] == 'A':
            hand_score += 11
    # determine how many aces need to be 1 instead of 11 to get under 21 if possible
    if hand_score > 21 and aces_count > 0:
        for i in range(aces_count):
            if hand_score > 21:
                hand_score -= 10
    return hand_score

# draw game conditions and buttons
def draw_game(act, record, result):
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
    # if there is an outcome for the hand that was played, display a restart button and tell user what happened
    if result != 0:
        screen.blit(font.render(results[result], True, 'white'), (15, 25))
        deal = pygame.draw.rect(screen, 'white', [150, 220, 300, 100], 0, 5) # draw rectangle on the screen
        pygame.draw.rect(screen, 'blue', [150, 220, 300, 100], 3, 5) # border around the white button
        pygame.draw.rect(screen, 'blue', [153, 223, 294, 94], 3, 5) 
        deal_text = font.render('NEW HAND', True, 'black')
        screen.blit(deal_text, (165, 250))
        button_list.append(deal)
    return button_list

# check endgame conditions function
def check_endgame(hand_act, deal_score, play_score, result, totals, add):
    # check end game scenarios if player has stood, busted or blackjacked
    # result 1-player bust, 2-win, 3-loss, 4-push
    if not hand_act and deal_score >= 17:
        if play_score > 21:
            result = 1
        elif deal_score < player_score <= 21 or deal_score > 21:
            result = 2
        elif play_score < deal_score <= 21:
            result = 3
        else:
            result = 4
        if add:
            if result == 1 or result == 3:
                totals[1] += 1
            elif result == 2:
                totals[0] += 1
            else:
                totals[2] += 1
            add = False
    return result, totals, add

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
        initial_deal = False
    # once game is activated, and dealt, calculate scores and display cards
    if active:
        player_score = calculate_score(my_hand)
        draw_cards(my_hand, dealer_hand, reveal_dealer)
        if reveal_dealer:
            dealer_score = calculate_score(dealer_hand)
            if dealer_score < 17:
                dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        draw_scores(player_score, dealer_score)
    if input:
        enter_name()
    rules_button = show_rules()
    results = ['', f'{player_name} BUSTED o_O', f'{player_name} WINS! :)', 'DEALER WINS :(', 'TIE GAME...']
    buttons = draw_game(active, records, outcome)


    # event handling, if quit pressed, then exit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if input and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                input = False
            elif event.key == pygame.K_BACKSPACE:
                player_name = player_name[:-1]
            else:
                if len(player_name) < 12:
                    player_name += event.unicode
        if event.type == pygame.MOUSEBUTTONUP:
            if rules_button.collidepoint(event.pos):
                showing_rules = not showing_rules
            elif showing_rules:
                showing_rules = False
            if not active:
                if buttons[0].collidepoint(event.pos):
                    active = True
                    initial_deal = True
                    game_deck = copy.deepcopy(decks * one_deck)
                    my_hand = []
                    dealer_hand = []
                    outcome = 0
                    hand_active = True
                    outcome = 0
                    add_score = True
                    dealer_score = 0
                    player_score = 0
            else:
                # if player can hit, allow them to draw a card
                if buttons[0].collidepoint(event.pos) and player_score < 21 and hand_active:
                    my_hand, game_deck = deal_cards(my_hand, game_deck)
                # allow player to end turn (stand)
                elif buttons[1].collidepoint(event.pos) and not reveal_dealer:
                    reveal_dealer = True
                    hand_active = False
                elif len(buttons) == 3:
                    if buttons[2].collidepoint(event.pos):
                        active = True
                        initial_deal = True
                        game_deck = copy.deepcopy(decks * one_deck)
                        my_hand = []
                        dealer_hand = []
                        outcome = 0
                        hand_active = True
                        outcome = 0
                        add_score = True
                        dealer_score = 0
                        player_score = 0
                        reveal_dealer = False

    # if player busts, automatically end run - treat like a stand
    if hand_active and player_score >= 21:
        hand_active = False
        reveal_dealer = True

    outcome, records, add_score = check_endgame(hand_active, dealer_score, player_score, outcome, records, add_score)
    
    pygame.display.flip() # make sure everything is flipped onto the screen
pygame.quit() # while-loop exited