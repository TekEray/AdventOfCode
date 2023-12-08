class Hand:
    def __init__(self, cards, bid, type):
        self.cards = cards
        self.bid = bid
        self.type = type
    def __repr__(self):
        return repr((self.cards, self.bid, self.type))
    
    def __lt__(self, other):
        #card_order = "AKQJT98765432"    # PART A
        card_order = "AKQT98765432J"   # PART B
        if self.type < other.type:
            return True
        elif self.type > other.type:
            return False
        for idx, card in  enumerate(self.cards):
            if card_order.index(card) > card_order.index(other.cards[idx]):
                return True
            elif card_order.index(card) < card_order.index(other.cards[idx]):
                return False
        return False
    
def readInput():
    inputList = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if not line:
            break
        inputList.append(line)
    return [tuple( i.split() ) for i in inputList] 

def findType(hand, task):
    cards, bid = hand
    # 7: high and 1: low
    handType = 1
    cardCount =  {}
    for card in cards:
        cardCount[card] = cards.count(card)
    if task == 'B':
        newCards = list(cards)
        if 'J' in cardCount.keys():
            loopRange = range(cardCount['J'])
            cardCount['J'] = 0
            for i in loopRange:
                newCards[newCards.index('J')] = max(cardCount, key=cardCount.get)
        
        newCards = "".join(newCards)
        cardCount =  {}
        for card in newCards:
            cardCount[card] = newCards.count(card)

    if 5 in cardCount.values():
        handType = 7
    elif 4 in cardCount.values():
        handType = 6
    elif 3 in cardCount.values() and 2 in cardCount.values():
        handType = 5
    elif 3 in cardCount.values():
        handType = 4
    elif 2 in cardCount.values() and len(cardCount.values()) == 3:
        handType = 3
    elif 2 in cardCount.values():
        handType = 2
    
    return (cards, bid, handType)

def main():

    handsList = readInput()
    typedHandsList = []
    for hands in handsList:
        card, bid, type = findType(hands,'B')
        typedHandsList.append(Hand(card, bid, type))
    typedHandsList.sort()

    result = 0
    for idx, hand in enumerate(typedHandsList):
        result = result + (idx+1) * int(hand.bid)
    print (result)


if __name__ == '__main__':
    main()