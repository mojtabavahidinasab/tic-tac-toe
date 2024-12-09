import pygame, sys
from pygame.locals import *

# Constant Variables
WWIDTH = 800  # Window Width
WHEGHT = 600  # Window Height
ROW = 3  # Board Rows
COL = 3  # Board Columns
BOXWTH = 6  # Box Width
BOXIZE = 150  # Box Size
GAPIZE = 9
XMRGIN = (WWIDTH - (BOXIZE * COL + GAPIZE * (COL - 1))) // 2
YMRGIN = (WHEGHT - (BOXIZE * ROW + GAPIZE * (ROW - 1))) // 2
FPS = 25
LFSZ = 256  # Large Font Size
SFSZ = 36  # Small Font Size
fpsClock = pygame.time.Clock()
X, O = "X", "O"

# Colors
BLCK = (000, 000, 000)
CYAN = (000, 255, 255)
LIME = (000, 255, 000)
PINK = (255, 192, 192)
WHTE = (255, 255, 255)
BKGC = BLCK  # Background Color

# Win Conditions
WCDS = ((0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6))
# Constant Variables

# Initialize pygame
pygame.init()
DISPLAYSURF = pygame.display.set_mode((WWIDTH, WHEGHT))
pygame.display.set_caption("دوز")
LFNT = pygame.font.SysFont("29lt arapix", size = LFSZ)  # Large Font
SFNT = pygame.font.SysFont("29lt arapix", size = SFSZ)  # Small Font
LFNT.set_script("Arab")
SFNT.set_script("Arab")
LFNT.set_direction(DIRECTION_RTL)
SFNT.set_direction(DIRECTION_RTL)
LPX = LFNT.render(X, True, WHTE)  # Large Prompt X
LPO = LFNT.render(O, True, WHTE)  # Large Prompt O
SPX = SFNT.render(X, True, WHTE)  # Small Prompt X
SPO = SFNT.render(O, True, WHTE)  # Small Prompt O
micex, micey, button = 0, 0, 0


def animation(isWin, winner = None):
    global board
    animationSpan = 10  # How long should the winning animation play?
    if isWin:
        text = f"آقای {winner} برنده بازی است"
    else:
        text = "هیچکس برنده نشد"
    WP1 = SFNT.render(text, True, BLCK)  # Win Prompt 1
    WP2 = SFNT.render(text, True, CYAN)  # Win prompt 2
    board = [*[""] * 9]
    while animationSpan >= 0:
        text2 = f"نوبازی در {animationSpan} آغاز میشود"
        WP3 = SFNT.render(text2, True, BLCK)  # Win Prompt 3
        DISPLAYSURF.fill(WHTE)
        DISPLAYSURF.blit(WP1, (WWIDTH // 2 - WP1.width // 2, WHEGHT // 2 - WP1.height // 2))
        DISPLAYSURF.blit(WP3, (WWIDTH // 2 - WP3.width // 2, WHEGHT // 2 + WP3.height))
        pygame.display.update()
        pygame.time.wait(350)
        animationSpan -= 1
        text2 = f"نوبازی در {animationSpan} آغاز میشود"
        WP3 = SFNT.render(text2, True, CYAN)  # Win Prompt 3
        DISPLAYSURF.fill(BLCK)
        DISPLAYSURF.blit(WP2, (WWIDTH // 2 - WP2.width // 2, WHEGHT // 2 - WP2.height // 2))
        DISPLAYSURF.blit(WP3, (WWIDTH // 2 - WP3.width // 2, WHEGHT // 2 + WP3.height))
        pygame.display.update()
        pygame.time.wait(350)
        animationSpan -= 1


def checkWin():
    """Check if anyone has won the game after each player move"""
    global board
    for condition in WCDS:
        # preparation to draw a line from (x0, y0) to (x1, y1)
        br, bc = condition[0] // 3, condition[0] % 3
        er, ec = condition[2] // 3, condition[2] % 3
        br, bc = getLeftTopCords(br, bc)
        er, ec = getLeftTopCords(er, ec)
        br += BOXIZE // 2
        bc += BOXIZE // 2
        er += BOXIZE // 2
        ec += BOXIZE // 2
        if board[condition[0]] == board[condition[1]] == board[condition[2]] == X:
            pygame.draw.line(DISPLAYSURF, WHTE, (br, bc), (er, ec), BOXWTH)
            pygame.display.update()
            pygame.time.wait(1000)
            animation(True, X)
        elif board[condition[0]] == board[condition[1]] == board[condition[2]] == O:
            pygame.draw.line(DISPLAYSURF, WHTE, (br, bc), (er, ec), BOXWTH)
            pygame.display.update()
            pygame.time.wait(1000)
            animation(True, O)
        else:
            if all(board):
                animation(False)


def eventHandler(turn):
    """Handle game events:
quit

mouse motion

mouse click

keypad key press"""
    global micex, micey, button
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION:
            micex, micey = event.pos
        elif event.type == MOUSEBUTTONUP:
            micex, micey = event.pos
            button = event.button
            turn = makeMove(micex, micey, button, turn)
        elif event.type == KEYUP:
            button = event.scancode
            turn = makeMove(micex, micey, button, turn)
    return micex, micey, button, turn


def getLeftTopCords(row, col):
    """Get coordination of left top point of a box"""
    lft = XMRGIN + col * (BOXIZE + GAPIZE)
    top = WHEGHT - YMRGIN - BOXIZE - row * (BOXIZE + GAPIZE)
    return (lft, top)


def drawBoard(micex, micey, turn):
    """Draw boaed"""
    global board
    for i in range(ROW):
        for j in range(COL):
            lft, top = getLeftTopCords(i, j)


            # Draw boxes pink if they are occupied, white otherwise
            if board[i * 3 + j]:
                rect = pygame.draw.rect(DISPLAYSURF, BLCK, (lft, top, BOXIZE, BOXIZE), BOXWTH)
            else:
                rect = pygame.draw.rect(DISPLAYSURF, WHTE, (lft, top, BOXIZE, BOXIZE), BOXWTH)
            # Draw boxes pink if they are occupied, white otherwise


            # Blit player exactly on box pink if they are occupied, cyan otherwise
            if rect.collidepoint(micex, micey):
                # Only blit if board is not occupied
                if not board[i * 3 + j]:
                    match turn:
                        case "X":
                            DISPLAYSURF.blit(LPX, (lft + BOXIZE // 7, top - BOXIZE // 1.1))
                        case "O":
                            DISPLAYSURF.blit(LPO, (lft + BOXIZE // 7, top - BOXIZE // 1.1))
                # Only blit if board is not occupied
            else:
                match turn:
                    case "X":
                        DISPLAYSURF.blit(LPX, (micex - (LPX.width + LFSZ) // 8, micey - (LPX.height + LFSZ) // 2.8))
                    case "O":
                        DISPLAYSURF.blit(LPO, (micex - (LPO.width + LFSZ) // 8, micey - (LPO.height + LFSZ) // 2.8))
            # Blit player exactly on box pink if they are occupied, cyan otherwise


            # Draw played moves
            if board[i * 3 + j]:
                match board[i * 3 + j]:
                    case "X":
                        DISPLAYSURF.blit(LPX, (lft + BOXIZE // 7, top - BOXIZE // 1.1))
                    case "O":
                        DISPLAYSURF.blit(LPO, (lft + BOXIZE // 7, top - BOXIZE // 1.1))
            # Draw played moves


def makeMove(micex, micey, button, turn):
    """Make a move"""
    global board
    # Play by mouse button press
    if button == 1:
        for i in range(ROW):
            for j in range(COL):
                lft, top = getLeftTopCords(i, j)
                if pygame.draw.rect(DISPLAYSURF, WHTE, (lft, top, BOXIZE, BOXIZE), 1).collidepoint(micex, micey):
                    if not board[i * 3 + j]:
                        board[i * 3 + j] = turn
                        button = 0
                        match turn:
                            case "X":
                                turn = "O"
                            case "O":
                                turn = "X"
    # Play by mouse button press
    # Play by NumPad keys
    elif button >= 89 and button <= 97:
        if not board[button - 89]:
            board[button - 89] = turn
            button = 0
            match turn:
                case "X":
                    turn = "O"
                case "O":
                    turn = "X"
    # Play by NumPad keys
    # Play by number keys
    elif button >= 30 and button <= 38:
        if not board[button - 30]:
            board[button - 30] = turn
            button = 0
            match turn:
                case "X":
                    turn = "O"
                case "O":
                    turn = "X"
    # Play by number keys
    checkWin()
    return turn


def main():
    """Main game loop"""
    turn = X
    micex, micey, button = 0, 0, 0
    micex, micey, button, turn = eventHandler(turn)
    while True:
        DISPLAYSURF.fill(BKGC)
        micex, micey, button, turn = eventHandler(turn)
        drawBoard(micex, micey, turn)
        pygame.display.update()
        fpsClock.tick(FPS)


board = [*[""] * 9]
main()
