class PokerCard:
    def __init__(self, cardstring):
        cardstring.strip()
        rank = cardstring[0]
        if rank.isdigit():
            self.rankvalue = int(rank)
        elif rank == 'T':
            self.rankvalue = 10
        elif rank == 'J':
            self.rankvalue = 11
        elif rank == 'Q':
            self.rankvalue = 12
        elif rank == 'K':
            self.rankvalue = 13
        elif rank == 'A':
            self.rankvalue = 14
        else:
            self.rankvalue = -1
        suit = cardstring[1]
        if suit == 'S':
            self.suitvalue = 0 #Spades
        elif suit == 'H':
            self.suitvalue = 1 #Hearts
        elif suit == 'C':
            self.suitvalue = 2 #Diamonds
        elif suit == 'D':
            self.suitvalue = 3 #Clubs
        else:
            self.suitvalue = -1



class PokerHand:
    def __init__(self, cardlist):
        self.size = 0
        self.cardlist = []
        for card in cardlist:
            self.addcard(card)
        if self.size == 5:
            self.setrank()

    def addcard(self, newcard):
        if self.size == 5:
            print("Error: five cards already in the hand")
        elif newcard.suitvalue == -1:
            print("Error: invalid suit")
        elif newcard.rankvalue == -1:
            print("Error: invalid rank")
        elif type(newcard) == PokerCard:
            self.cardlist.append(newcard)
            self.size += 1
            if self.size == 5:
                self.setrank()
        elif type(newcard) == str:
            self.cardlist.append(PokerCard(newcard))
            self.size += 1
            if self.size == 5:
                self.setrank()
        else:
            print("Error: invalid card type")

    def setrank(self):
        self.rankarray = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        for card in self.cardlist:
            self.rankarray[card.rankvalue] += 1
        self.rankorder = []
        for count in range(1,5):
            for rank in range(len(self.rankarray)):
                if self.rankarray[rank] == count:
                    self.rankorder.append([rank, self.rankarray[rank]])
        self.rankorder.reverse()


    def isflush(self):
        return(self.cardlist[0].suitvalue == self.cardlist[1].suitvalue == self.cardlist[2].suitvalue == self.cardlist[3].suitvalue == self.cardlist[4].suitvalue)
    def isstraight(self):
        for rankindex in range(2, 11):
            if self.rankarray[rankindex] == self.rankarray[rankindex+1] == self.rankarray[rankindex+2] == self.rankarray[rankindex+3] == self.rankarray[rankindex+4] == 1:
                return True
        if self.rankarray[14] == self.rankarray[2] == self.rankarray[3] == self.rankarray[4] == self.rankarray[5] == 1:
            return True
        return False
    def isfivehighstraight(self):
        if self.isstraight() and self.rankarray[14] == self.rankarray[2] == self.rankarray[3] == self.rankarray[4] == self.rankarray[5] == 1:
            return True
        else:
            return False

    def handvalue(self):
        if self.isflush() and self.isstraight() and not self.isfivehighstraight(): #Royal Flush or Straight Flush
            return 10
        elif self.isflush and self.isfivehighstraight(): #Five-high Straight Flush
            return 9
        elif self.rankorder[0][1] == 4: #Four of a Kind
            return 8
        elif self.rankorder[0][1] == 3 and self.rankorder[1][1] == 2: #Full House
            return 7
        elif self.isflush(): #Flush
            return 6
        elif self.isstraight() and not self.isfivehighstraight(): #Straight
            return 5
        elif self.isfivehighstraight(): #Five-high Straight
            return 4
        elif self.rankorder[0][1] == 3: #Three of a Kind
            return 3
        elif self.rankorder[0][1] == self.rankorder[1][1] == 2: #Two Pair
            return 2
        elif self.rankorder[0][1] == 2:
            return 1
        else:
            return 0

    def __lt__(self, other):
        if self.handvalue() < other.handvalue():
            return True
        elif self.handvalue() == other.handvalue() and self.rankorder < other.rankorder:
            return True
        return False
    def __gt__(self, other):
        return(other<self)

hand1wins = 0
with open("poker.txt") as pokerhands:
    for hand in pokerhands:
        player1cards = []
        player2cards = []
        pokercards = hand.strip('\n').split(" ") #Removes whitespace and converts into a string.
        for i in range(5):
            player1cards.append(PokerCard(pokercards[i]))
        for i in range(5,10):
            player2cards.append(PokerCard(pokercards[i]))
        hand1 = PokerHand(player1cards)
        hand2 = PokerHand(player2cards)
        if hand1 > hand2:
            hand1wins += 1
print(hand1wins)

#Hands for testing
#hand1 = PokerHand([PokerCard("AH"), PokerCard("2H"), PokerCard("3H"), PokerCard("4H"), PokerCard("7H")]) #Flush
#hand2 = PokerHand([PokerCard("2S"), PokerCard("3S"), PokerCard("4S"), PokerCard("5S"), PokerCard("6S")]) #Straight Flush
#hand3 = PokerHand([PokerCard("AS"), PokerCard("2S"), PokerCard("3S"), PokerCard("4S"), PokerCard("5D")]) #5-high Straight
#hand4 = PokerHand([PokerCard("2S"), PokerCard("3S"), PokerCard("4S"), PokerCard("5S"), PokerCard("6D")]) #6-high Straight
#hand5 = PokerHand([PokerCard("2S"), PokerCard("3S"), PokerCard("3H"), PokerCard("5S"), PokerCard("6D")]) #One Pair
#hand6 = PokerHand([PokerCard("2S"), PokerCard("3S"), PokerCard("3H"), PokerCard("6S"), PokerCard("6D")]) #Two Pair
