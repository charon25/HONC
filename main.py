from game import Game


game = Game()
game.start()

while not game.is_ended:
    game.loop()

game.stop()
