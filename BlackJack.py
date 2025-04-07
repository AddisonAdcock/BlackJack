import pygame, random, sys

pygame.init()
WIN_WIDTH, WIN_HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Blackjack")
icon = pygame.image.load("cards/back.png").convert_alpha()
icon = pygame.transform.scale(icon, (32, 32))
pygame.display.set_icon(icon)

clock = pygame.time.Clock()
full_screen = False
CARD_WIDTH, CARD_HEIGHT = 160, 160
CARD_SPACING = 10

card_names = ["AS", "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "10S", "JS", "QS", "KS",
              "AC", "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "10C", "JC", "QC", "KC",
              "AD", "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "10D", "JD", "QD", "KD",
              "AH", "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "10H", "JH", "QH", "KH"]

card_images = {}
for name in card_names:
    img = pygame.image.load(f"cards/{name}.png").convert_alpha()
    card_images[name] = pygame.transform.scale(img, (CARD_WIDTH, CARD_HEIGHT))
    
back_image = pygame.image.load("cards/back.png").convert_alpha()
back_image = pygame.transform.scale(back_image, (CARD_WIDTH, CARD_HEIGHT))

cards = {
    "AS": 11, "2S": 2, "3S": 3, "4S": 4, "5S": 5, "6S": 6, "7S": 7, "8S": 8, "9S": 9, "10S": 10, "JS": 10, "QS": 10, "KS": 10,
    "AC": 11, "2C": 2, "3C": 3, "4C": 4, "5C": 5, "6C": 6, "7C": 7, "8C": 8, "9C": 9, "10C": 10, "JC": 10, "QC": 10, "KC": 10,
    "AD": 11, "2D": 2, "3D": 3, "4D": 4, "5D": 5, "6D": 6, "7D": 7, "8D": 8, "9D": 9, "10D": 10, "JD": 10, "QD": 10, "KD": 10,
    "AH": 11, "2H": 2, "3H": 3, "4H": 4, "5H": 5, "6H": 6, "7H": 7, "8H": 8, "9H": 9, "10H": 10, "JH": 10, "QH": 10, "KH": 10
}

def new_game():
    """Reset game state and deal initial cards."""
    global deck, player_hand, dealer_hand, state, result_text, dealer_last_draw_time
    deck = list(cards.keys())
    random.shuffle(deck)
    player_hand = []
    dealer_hand = []
    deal_card(player_hand)
    deal_card(player_hand)
    deal_card(dealer_hand)
    deal_card(dealer_hand)
    state = "player_turn"
    result_text = ""
    dealer_last_draw_time = pygame.time.get_ticks()

def deal_card(hand):
    if deck:
        hand.append(deck.pop())

def calculate_total(hand):
    total = sum(cards[card] for card in hand)
    aces = sum(1 for card in hand if card.startswith("A"))
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total

new_game()
state = "player_turn"
result_text = ""
dealer_last_draw_time = pygame.time.get_ticks()
DEALER_DELAY = 700

font = pygame.font.SysFont("arial", 32)
title_font = pygame.font.SysFont("arial", 48, bold=True)

def draw_centered_text(text, font_obj, color, center):
    text_surface = font_obj.render(text, True, color)
    text_rect = text_surface.get_rect(center=center)
    screen.blit(text_surface, text_rect)

def draw_button(text, rect, base_color=(70, 130, 180), text_color=(255, 255, 255)):
    pygame.draw.rect(screen, base_color, rect, border_radius=8)
    txt_surface = font.render(text, True, text_color)
    txt_rect = txt_surface.get_rect(center=rect.center)
    screen.blit(txt_surface, txt_rect)

BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50
BUTTON_GAP = 40
def get_button_positions(state):
    total_width = BUTTON_WIDTH * 2 + BUTTON_GAP
    start_x = (WIN_WIDTH - total_width) // 2
    y = WIN_HEIGHT - BUTTON_HEIGHT - 30
    if state == "player_turn":
        return {"hit": pygame.Rect(start_x, y, BUTTON_WIDTH, BUTTON_HEIGHT),
                "stand": pygame.Rect(start_x + BUTTON_WIDTH + BUTTON_GAP, y, BUTTON_WIDTH, BUTTON_HEIGHT)}
    elif state == "game_over":
        return {"play_again": pygame.Rect(start_x, y, BUTTON_WIDTH, BUTTON_HEIGHT),
                "quit": pygame.Rect(start_x + BUTTON_WIDTH + BUTTON_GAP, y, BUTTON_WIDTH, BUTTON_HEIGHT)}
    else:  # dealer_turn: only show Quit button.
        return {"quit": pygame.Rect((WIN_WIDTH - BUTTON_WIDTH) // 2, y, BUTTON_WIDTH, BUTTON_HEIGHT)}

def draw_hand_centered(hand, y, hide_first=False):
    num_cards = len(hand)
    total_width = num_cards * CARD_WIDTH + (num_cards - 1) * CARD_SPACING
    start_x = (WIN_WIDTH - total_width) // 2
    for i, card in enumerate(hand):
        x = start_x + i * (CARD_WIDTH + CARD_SPACING)
        if hide_first and i == 0:
            screen.blit(back_image, (x, y))
        else:
            screen.blit(card_images[card], (x, y))

running = True
while running:
    screen.fill((0, 100, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                full_screen = not full_screen
                if full_screen:
                    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            if state == "player_turn":
                buttons = get_button_positions(state)
                if buttons["hit"].collidepoint(pos):
                    deal_card(player_hand)
                    if calculate_total(player_hand) > 21:
                        result_text = "Player busts! Dealer wins."
                        state = "game_over"
                elif buttons["stand"].collidepoint(pos):
                    state = "dealer_turn"
                    dealer_last_draw_time = pygame.time.get_ticks()
            elif state == "game_over":
                buttons = get_button_positions(state)
                if buttons["play_again"].collidepoint(pos):
                    new_game()
                elif buttons["quit"].collidepoint(pos):
                    running = False
            elif state == "dealer_turn":
                buttons = get_button_positions(state)
                if buttons["quit"].collidepoint(pos):
                    running = False

    if state == "dealer_turn":
        current_time = pygame.time.get_ticks()
        if current_time - dealer_last_draw_time >= DEALER_DELAY:
            if calculate_total(dealer_hand) < 17:
                deal_card(dealer_hand)
                dealer_last_draw_time = current_time
            else:
                dealer_total = calculate_total(dealer_hand)
                player_total = calculate_total(player_hand)
                if dealer_total > 21:
                    result_text = "Dealer busts! Player wins."
                elif dealer_total > player_total:
                    result_text = "Dealer wins."
                elif dealer_total < player_total:
                    result_text = "Player wins."
                else:
                    result_text = "It's a tie!"
                state = "game_over"

    if state == "player_turn":
        draw_hand_centered(dealer_hand, 50, hide_first=True)
    else:
        draw_hand_centered(dealer_hand, 50, hide_first=False)

    draw_hand_centered(player_hand, 350, hide_first=False)

    buttons = get_button_positions(state)
    for btn in buttons.values():
        if state == "player_turn":
            if btn == buttons["hit"]:
                draw_button("Hit", btn)
            elif btn == buttons["stand"]:
                draw_button("Stand", btn)
        elif state == "game_over":
            if btn == buttons["play_again"]:
                draw_button("Play Again", btn)
            elif btn == buttons["quit"]:
                draw_button("Quit", btn)
        elif state == "dealer_turn":
            draw_button("Quit", btn)

    if state == "game_over":
        draw_centered_text(result_text, title_font, (255, 255, 0), ((WIN_WIDTH // 2), WIN_HEIGHT // 2 - 50))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
