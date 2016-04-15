import random
import re
import string
import sudoku

# import argparse

from twisted_bot import Bot, BotFactory
from twisted.internet import reactor

from time import sleep

game = sudoku.sudoku_game()

class SudokuBot(Bot):

    def __init__(self):
        self.command_words = ["play", "go", "start"]
        self.guess_words = ["guess"]
        self.help_words = ["help"]
        self.inGame = False

    def printrow(self, row):
        self.say(self.factory.channel, "{0} [{1}] [{2}] [{3}]   [{4}] [{5}] [{6}]   [{7}] [{8}] [{9}]\n".format(row, game.outArray[row - 1][0], game.outArray[row - 1][1], game.outArray[row - 1][2], game.outArray[row - 1][3], game.outArray[row - 1][4], game.outArray[row - 1][5], game.outArray[row - 1][6], game.outArray[row - 1][7], game.outArray[row - 1][8]))
        
    def command(self, prefix, msg):
        play = False
        helpMsg = False
        
        for hel in self.help_words:
            if hel in msg.lower():
                helpMsg = True
        
        if helpMsg:
            self.say(self.factory.channel, "What? You actually need me to explain this to you? Ugh. Fine. Let me explain like you're 5. Actually, let's make that 3 instead. Big box. Lots of boxes in box. 9 lines of boxes going up/down and left/right. 9 small boxes inside bigger box. We use numbers 1 through 9. Numbers go in box. Only one of each number in each row, column, or small box. This isn't theCount, you might actually have to use your brain. Guess with 'guess 1 in a1', except don't actually guess that unless you know there's a 1 in a1. Idiot.")
        
        elif not self.inGame:
            for com in self.command_words:
                if com in msg.lower():
                    play = True
            if play:
                self.play(prefix)
        #else:
        #    for com2 in self.guess_words:
        #        if com2 in msg.lower():
        #            guess = True
        #    if guess:
        #        self.guess(prefix)
            
            
    def play(self, prefix):
        self.inGame = True
        self.say(self.factory.channel, "Honorable sudoku starts now!")
        game.play_sudoku()
        self.drawBoard(prefix)
        
    def drawBoard(self, prefix):
        self.say(self.factory.channel, "   A   B   C     D   E   F     G   H   I")
        for row in range(1, 4):
            self.printrow(row)
        sleep(1)
        self.say(self.factory.channel, "-                            \n")
        for row in range(4, 7):
            self.printrow(row)
        sleep(1)
        self.say(self.factory.channel, "-                             \n")
        for row in range(7, 10):
            self.printrow(row)
        #self.say(self.factory.channel, "                             \n")

    def guess(self, prefix, msg):
        if self.inGame:
            guessValueRegex = re.compile("^([1-9])\s+(?:in){0,1}\s*([a-i])([1-9])$")
            guessValueSearch = guessValueRegex.search(msg.strip().lower())
            if guessValueSearch is not None:
                guessValue = int(guessValueSearch.group(1))
                guessRow = int(guessValueSearch.group(3)) - 1
                guessColumn = string.lowercase.index(guessValueSearch.group(2))

                #self.say(self.factory.channel, prefix + "You guessed" + msg)
                #self.say(self.factory.channel, "Value guessed: " + str(guessValue))
                #self.say(self.factory.channel, "Row: " + str(guessRow))
                #self.say(self.factory.channel, "Column: " + str(guessColumn))

                if game.outArray[guessRow][guessColumn] != '_':
                    self.say(self.factory.channel, prefix + "You guessed an already revealed tile, ya dingus!")
                elif guessValue == int(game.answerArray[guessRow][guessColumn]):
                    self.say(self.factory.channel, prefix + "Correct you are~!")
                    game.outArray[guessRow][guessColumn] = str(guessValue)
                    self.drawBoard(prefix)
                else:
                    self.say(self.factory.channel, prefix + "WRONG, SHAME AND DISHONOR UPON YOU")
                self.checkIfOver(prefix, msg)
    def checkIfOver(self, prefix, msg):
        if not any('_' in cell for cell in game.outArray):
            self.inGame = False
            self.say(self.factory.channel, "You have honored your ancestors by committing this great act.")
    
    def privmsg(self, user, channel, msg):
        if not user:
            return
        com_regex = re.compile(self.first_name + "[ _]" + self.last_name + "[:,]* ?", re.I)
        guess_regex = re.compile("^(guess|answer)")
        prefix = "%s: " % (user.split("!", 1)[0], )
        if com_regex.search(msg):
            msg = com_regex.sub("", msg)
            self.command(prefix, msg)
        elif guess_regex.search(msg):
            msg = guess_regex.sub("", msg)
            self.guess(prefix, msg)
        else: 
            prefix = ""
            #prefix = "%s: " % (user.split("!", 1)[0], )
        #else:
        #    prefix = ""
        #if prefix:
            #self.command(prefix, msg)


class SudokuBotFactory(BotFactory):
    protocol = SudokuBot

    def __init__(self, channel, nickname):
        BotFactory.__init__(self, channel, nickname)


if __name__ == "__main__":
    host = "coop.test.adtran.com"
    port = 6667
    chan = "Sudoku_Room" # "THE_MAGIC_CONCH_ROOM" "test" 
    reactor.connectTCP(host, port, SudokuBotFactory("#" + chan, "Sudoku"))
    reactor.run()
