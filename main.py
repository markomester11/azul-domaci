from azul import azulgame
from agents import AlphaBeta, AlphaBetaVremenski

niz = ['W', 'R', 'Y', 'Y', 'W', 'W', 'R', 'Y', 'R', 'W', 'Y', 'K', 'K', 'W', 'Y', 'B', 'W', 'B', 'K', 'R']

game = azulgame(0, False, niz)

agent = AlphaBetaVremenski(game)
agent.game_loop()