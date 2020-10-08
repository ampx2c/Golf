import random

#calculates the average point value of cards remaining in the deck
def calculateAvg(deck):
    total = 0
    for card in deck:
        total += getValue(card)
    return total / len(deck)

def calculateX(deck, hands, handsShowing): #don't go out if opponent has better
    total = 0
    numCards = len(deck)
    for card in deck:
        total += getValue(card)
    for i in range(len(hands)):
        for j in range(len(hands[0])):
            if (handsShowing[i][j] == 'X'):
                total += getValue(hands[i][j])
                numCards += 1
    return total / numCards

#if two cards in the same row match, add 0 to point total, otherwise add their normal point value (which is outlined in function "getValue" below)
def calculateHand(hand):
    handTotal = 0
    if (hand[0][0] == hand[1][0] and hand[0][0] != 'X' and hand[0][0] != '-'):
        handTotal += 0
    else:
        handTotal += getValue(hand[0])
        handTotal += getValue(hand[1])
    if (hand[2][0] == hand[3][0] and hand[2][0] != 'X' and hand[2][0] != '-'):
        handTotal += 0
    else:
        handTotal += getValue(hand[2])
        handTotal += getValue(hand[3])
    if (hand[4][0] == hand[5][0] and hand[4][0] != 'X' and hand[4][0] != '-'):
        handTotal += 0
    else:
        handTotal += getValue(hand[4])
        handTotal += getValue(hand[5])
    return handTotal

def getValue(card): #point value for each card
    denom = card[0]
    if (denom == '2'):
        value = 2
    elif (denom == '3'):
        value = 3
    elif (denom == '4'):
        value = 4
    elif (denom == '5'):
        value = 5
    elif (denom == '6'):
        value = 6
    elif (denom == '7'):
        value = 7
    elif (denom == '8'):
        value = 8
    elif (denom == '9'):
        value = 9
    elif (denom == '1'):
        value = 10
    elif (denom == 'j'):
        value = 10
    elif (denom == 'q'):
        value = 10
    elif (denom == 'k'):
        value = 0
    elif (denom == 'a'):
        value = 1
    elif (denom == '-'):
        value = -2
    elif (denom == 'X'): #X represents a face down card
        #Value of a face down card is based on the average point value of cards remaining in the deck
        value = calculateX(deck, hands, handsShowing)
    return value

deck = []
suits = ['♥', '♦', '♠', '♣']
values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'j', 'q', 'k', 'a']

# generate deck
for suit in suits:
    for value in values:
        deck.append(value + suit)
deck.append('-j')
deck.append('-j')
# shuffle
random.shuffle(deck)

numPlayers = int(input("How many players (including one AI)? "))

hands = []
handsShowing = []
for i in range(numPlayers):
    hand = []
    handShowing = []
    for j in range(6):
        hand.append(deck.pop())
        handShowing.append('X')
    hands.append(hand)
    handsShowing.append(handShowing)

discardPile = []

finishPlayer = -1
end = False
while (len(deck) > 0):
    for i in range(numPlayers):
        
        if (i == finishPlayer): #GAME IS OVER
            for j in range(numPlayers):
                score = calculateHand(hands[j])
                print(f'Player {j + 1}: {score}')
            exit()
        
        if (i == numPlayers - 1): #AI's turn
            #~~~~~~~~~~~~~~~~~~~~~~~~~~AI~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            print('AI')
            print(f'\n{handsShowing[i][0]:2} {handsShowing[i][1]:2}') #print hand before AI's turn
            print(f'{handsShowing[i][2]:2} {handsShowing[i][3]:2}')
            print(f'{handsShowing[i][4]:2} {handsShowing[i][5]:2}\n')
            numX = 0 #number of cards still face down
            snagDiscard = False
            snagTop = False
            for card in handsShowing[i]:
                if (card == 'X'):
                    numX += 1
                if (card[0] == discardPile[-1][0]):
                    snagDiscard = True
                if (card[0] == deck[-1][0]):
                    snagTop = True
        
            if (numX == 1): #AI is about to go out (one card unflipped)
                minPlayerVal = 60
                #print("one")
                for p in range(numPlayers - 1):
                    playerPval = calculateHand(handsShowing[p])
                    if (playerPval < minPlayerVal):
                        minPlayerVal = playerPval
                if ((getValue(discardPile[-1]) + calculateHand(handsShowing[i]) - calculateX(deck, hands, handsShowing) < playerPval - 2 and getValue(discardPile[-1]) < calculateAvg(deck)) or snagDiscard == True): #discard
                        print("taken from discard:")
                        currentCard = discardPile.pop()
                        takeChoice = 'y'
                elif (snagTop == True): #deck
                        print("taken from deck:")
                        currentCard = deck.pop()
                        takeChoice = 'y'
                elif (getValue(deck[-1]) + calculateHand(handsShowing[i]) - calculateX(deck, hands, handsShowing) < playerPval - 2 and getValue(currentCard) < calculateX(deck, hands, handsShowing)):
                        print("taken from deck:")
                        currentCard = deck.pop()
                        takeChoice = 'y'
                elif (end == True and getValue(discardPile[-1]) < calculateAvg(deck)): #last round
                        #if top card in discard pile is less than the average value of cards that are face down or in the deck, take discrard
                        print("taken from discard:")
                        currentCard = discardPile.pop()
                        takeChoice = 'y'
                else:
                        print("taken from deck:")
                        currentCard = deck.pop()
                        if (end == True and getValue(currentCard) < calculateX(deck, hands, handsShowing)):
                            takeChoice = 'y'
                        else:
                            takeChoice = 'n'
        
            elif (getValue(discardPile[-1]) < calculateAvg(deck) or snagDiscard == True): #take from discard
                print("taken from discard:")
                currentCard = discardPile.pop()
                takeChoice = 'y'
            else: #take from deck
                print("taken from deck:")
                currentCard = deck.pop()
                if (snagTop == True):
                    takeChoice = 'y'
                elif (getValue(currentCard) < calculateX(deck, hands, handsShowing) + 1.5):
                    #since you cannot match with face down cards, more cards face up gives an advantage hence the allowance to accept cards that are 1.5 points greater than the average of all cards unflipped or remaining in the deck
                    takeChoice = 'y'
                else:
                    takeChoice = 'n'
            print(currentCard, '\n')
            if (takeChoice == 'y'):
                minValue = 60
                for j in range(6):
                    tempHand = handsShowing[i].copy()
                    tempHand[j] = currentCard
                    #print(j)
                    #print(tempHand)
                    currentValue = calculateHand(tempHand)
                    if (currentValue < minValue):
                        minValue = currentValue
                        putWhere = j
                    if (currentValue == minValue and (j == 1 or j == 3)):
                        if (tempHand[j][0] != tempHand[j - 1][0] and tempHand[j + 1] == 'X' and tempHand[j - 1] != 'X'):
                            putWhere = j + 1
                        elif (j == 1 and tempHand[j][0] != tempHand[j - 1][0] and tempHand[j + 3] == 'X' and tempHand[j - 1] != 'X'):
                            putWhere = j + 3
                discardPile.append(hands[i][putWhere])
                handsShowing[i][putWhere] = currentCard
                hands[i][putWhere] = currentCard
            elif (takeChoice == 'n'):
                discardPile.append(currentCard)
            print(f'{handsShowing[i][0]:2} {handsShowing[i][1]:2}') #print hand after AI's turn
            print(f'{handsShowing[i][2]:2} {handsShowing[i][3]:2}')
            print(f'{handsShowing[i][4]:2} {handsShowing[i][5]:2}\n')

        else: #players' turns
            #~~~~~~~~~~~~~~~~~~~~~~~~PLAYERS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            print('Player', i + 1, '\n')
            print(f'{handsShowing[i][0]:2} {handsShowing[i][1]:2}') #print hand before player's turn
            print(f'{handsShowing[i][2]:2} {handsShowing[i][3]:2}')
            print(f'{handsShowing[i][4]:2} {handsShowing[i][5]:2}\n')
            if (len(discardPile) != 0):
                str = discardPile[-1] + " (0) or pull from deck (1)? "
                #pileChoice = input(discardPile.pop(), '(0) or pull from deck (1)? ')
                pileChoice = int(input(str))
            else:
                pileChoice = 1

            if (pileChoice == 0): #taking from discard pile
                currentCard = discardPile.pop()
                print(currentCard)
            elif (pileChoice == 1): #drawing from deck
                currentCard = deck.pop()
                print(currentCard)

            if (pileChoice == 1):
                takeChoice = input("Take card (y/n)? ")
            else:
                takeChoice = 'y'

            if (takeChoice == 'y'):
                putWhere = int(input("Where to put (1-6)? "))
                discardPile.append(hands[i][putWhere - 1])
                handsShowing[i][putWhere - 1] = currentCard
                hands[i][putWhere - 1] = currentCard
            elif (takeChoice == 'n'):
                discardPile.append(currentCard)

            print(f'\n{handsShowing[i][0]:2} {handsShowing[i][1]:2}') #print hand after player's turn
            print(f'{handsShowing[i][2]:2} {handsShowing[i][3]:2}')
            print(f'{handsShowing[i][4]:2} {handsShowing[i][5]:2}')
            print('')

        #game finish check
        if (end == False):
            k = 0
            for hand in handsShowing:
                gameFinished = True
                for card in hand:
                    if (card == 'X'): #if every player has at least one un-flipped card (represented by 'X', the game is not complete
                        gameFinished = False
                if (gameFinished == True):
                    end = True
                    finishPlayer = k #player k is the first to go out
                k += 1
