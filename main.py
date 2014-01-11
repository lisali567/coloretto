from random import shuffle
from random import randint
import cmd
import string, sys

class Deck():

    #constructor
    def __init__(self):
        self.deck = []
        self.startingColorList = []

    #assume numPlayer is either 3, 4, or 5
    #constraint checked in Game init
    def newDeck(self, numPlayer):
        self.deck =[]
        colorList = ['brown', 'yellow', 'green', 'orange', 'pink', 'gray', 'blue']
        self.startingColorList = []
        #edit this later if/when asking players for initial color
        for i in range(numPlayer):
            randomInt = randint(0, len(colorList)-1)
            self.startingColorList.append(colorList[randomInt])
            del colorList[randomInt]         
        #if not 3 players, use all colors
        if (numPlayer!=3):
            Deck.makeNewDeck(self, colorList, self.startingColorList)
        #otherwise remove a color from the list
        else:
            del colorList[randint(0,len(colorList)-1)]
            Deck.makeNewDeck(self, colorList, self.startingColorList)
        shuffle(self.deck)
        #adds the "last round" card as the 16th from last card in the deck
        self.deck.insert(15, 'last round')

    def makeNewDeck(self, colorList, startingColorList):
        #adds 9 color cards for each non-starting color
        for color in colorList:
            for num in range(9):
                self.deck.append(color)
        #adds 8 (i.e 9 - 1) cards of the starting colors since 1 of each has already been distributed
        for color in startingColorList:
            for num in range(8):
                self.deck.append(color)
        #adds in 10 +2 cards
        for num in range(10):
            self.deck.append('+2')
        #adds in 3 joker cards
        for num in range(3):
            self.deck.append('joker')    

class Player():

    #constructor
    def __init__(self, name):
        self.hand = []
        self.name = name

    def addCard(self, card):
        self.hand.append(card)

#this class is now unnecessary...for now
class Card():
    def __init__(self, card):
        self.card = card

    def setCard(self, card):
        self.card = card

    def getCard(self):
        return self.card

class PlaceCmd(cmd.Cmd):
    def __init__(self, card, CLIparent):
        cmd.Cmd.__init__(self)
        self.card = card
        self.CLI = CLIparent
    
    def do_PLACE(self, pileNumber):
        CLI.moveCard(self.CLI, self.card, pileNumber)
        print("you placed " + self.card + " on pile " +pileNumber)
        CLI.printPiles(self.CLI, self.CLI.pileList)
        return True

class gamePlay(cmd.Cmd):
    
    def __init__(self, playerList, playNum, myDeck, pileList, turnList):
        cmd.Cmd.__init__(self)
        self.playerList = playerList
        self.playNum = playNum
        self.myDeck = myDeck
        self.pileList = pileList
        self.turnList = turnList
        self.intro = 'player 0 go!'
        self.prompt = '>>> '

    def do_play(self, arg):
        i = CLI(self.myDeck, self.pileList, self)
        i.prompt = self.prompt[:-1]+':'+self.playerList[self.turnList[self.playNum]].name+':'
        i.cmdloop()
       # while not self.turnList:
        self.do_play(self)
        #if not self.turnList:
        #self.resetTurns(self)

    def resetTurns(self):
        for i in range(len(self.playerList)):
            self.turnList.append(i)
        
class CLI(cmd.Cmd):
    
    def __init__(self, myDeck, pileList, gamePlay):
        cmd.Cmd.__init__(self)
        self.myDeck = myDeck
       # self.playerList = playerList
        self.pileList = pileList
        self.gamePlay = gamePlay
       # self.intro = 'player 0 go!'
       # self.curPlayNum = 0
       # self.prompt = '>>> '

    #def cmdloop(self, currentCard):        
        #return cmd.Cmd.cmdloop(self, currentCard)

    def do_DRAW(self, arg):
        card = self.myDeck.deck.pop()
        print(self.gamePlay.playerList[self.gamePlay.turnList[self.gamePlay.playNum]].name+" drew " + card)
        print("on which pile will you PLACE it?")
        CLI.printPiles(self, self.pileList)
        i = PlaceCmd(card, self)
        i.prompt = self.prompt[:-1]+':Draw:'
        i.cmdloop()
        print(self.gamePlay.playerList[self.gamePlay.turnList[self.gamePlay.playNum]].name+"'s turn over")
        self.gamePlay.playNum = (self.gamePlay.playNum+1) % len(self.gamePlay.turnList)
        return True

    def printPiles(self, pileList):
        x = 0
        for p in self.pileList:
            print("Pile "+str(x)+": ")
            print((p.pile))
            x +=1

    def moveCard(self, card, pileNumber):
        self.pileList[int(pileNumber)].pile.append(card)

    def do_TAKE(self, pileNumber):
        print("you took pile" + pileNumber)
        print(self.gamePlay.playerList[self.gamePlay.turnList[self.gamePlay.playNum]].name+"'s turn over")
        self.gamePlay.turnList.pop(self.gamePlay.playNum)
        #self.gamePlay.playNum = (self.gamePlay.playNum+1) % len(self.gamePlay.turnList)
        return True
        

class Pile():
    #constructor
    def __init__(self):
        self.pile = []
    
    def addToPile(self, card):
        self.pile.append(card)

    def clearPile(self):
        self.pile[:] = []

class Game():
    
    #constructor
    def __init__(self, numPlayers):
        if 2 < numPlayers < 6:
            self.numPlayers = numPlayers
        else:
            print("Must have between 3-5 players!")
    
    def game_init(self):
        #make and initialize Deck
        myDeck = Deck()
        myDeck.newDeck(self.numPlayers)
        print((myDeck.deck))

        #create Players, give each one a starting card
        playerList = []
        pileList = []
        for num in range(self.numPlayers):
            playerList.append(Player("player"+str(num)))
            playerList[num].addCard(myDeck.startingColorList.pop())
            pileList.append(Pile())
            print((playerList[num].hand))
            print((pileList[num].pile))
       # currentCard = Card('')
        turnList = []
        for i in range(len(playerList)):
            turnList.append(i)
            print(turnList[i])
        play = gamePlay(playerList, 0, myDeck, pileList, turnList)
        #currentCard = 'brown'
        play.cmdloop()
        

def main():
    theGame = Game(3)
    theGame.game_init()
    #theGame2 = Game(6)

main()
