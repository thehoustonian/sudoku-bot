import random
import re
#from sudoku import sudoku_game
import sudoku

# import argparse

from twisted_bot import Bot, BotFactory
from twisted.internet import reactor

from time import sleep

game = sudoku.sudoku_game()

class SudokuBot(Bot):

    def __init__(self):
        self.command_words = ["play", "go", "start"]
        self.input_words = ["guess"]

    def printrow(self, row):
        self.say(self.factory.channel, "{0} [{1}] [{2}] [{3}]   [{4}] [{5}] [{6}]   [{7}] [{8}] [{9}]\n".format(row, game.outArray[row - 1][0], game.outArray[row - 1][1], game.outArray[row - 1][2], game.outArray[row - 1][3], game.outArray[row - 1][4], game.outArray[row - 1][5], game.outArray[row - 1][6], game.outArray[row - 1][7], game.outArray[row - 1][8]))
        
    def command(self, prefix, msg):
        play = False
        guess = False
        for com in self.command_words:
            if com in msg.lower():
                play = True
        if play:
            self.play(prefix)
            
        for com2 in self.input_words:
            #self.say(self.factory.channel, com2)
            if com2 in msg.lower():
                guess = True
        if guess:
            self.guess(prefix)
            
            
    def play(self, prefix):
        self.say(self.factory.channel, "Honorable sudoku starts now!")
        game.play_sudoku()
        self.say(self.factory.channel, "   A   B   C     D   E   F     G   H   I")
        #self.say(self.factory.channel, " \ __ __ __ __ __ __ __ __ __")
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

    def guess(self, prefix):
        self.say(self.factory.channel, prefix + ", ayy lmao")
    
    def privmsg(self, user, channel, msg):
        if not user:
            return
        com_regex = re.compile(self.first_name + "[ _]" + self.last_name + "[:,]* ?", re.I)
        if com_regex.search(msg):
            msg = com_regex.sub("", msg)
            prefix = "%s: " % (user.split("!", 1)[0], )
        else:
            prefix = ""
        if prefix:
            self.command(prefix, msg)


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
