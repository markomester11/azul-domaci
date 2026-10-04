class Agent:
    
    def __init__(self, game):
        self.game = game
        
    def decision(self, state):
        pass
    
    def game_loop(self):
        
        state = self.game.start_state
        
        test = True
        
        for _ in range(5):
            self.game.prikaz(state)
            while test:
                if state['na_potezu'] == 1: #robot na potezu
                    action = self.decision(state)
                    state = self.game.get_successor(state, action)
                    self.game.prikaz(state)
                    print(f"Potez bota: {action}")
                    if all(len(factory) == 0 for factory in state['fabrika'].values()):
                        test = False
                else: #covjek na potezu
                    print('Unesite potez sledecim redom (fabrika, plocica, destinacija): \n')
                    c1 = input()
                    c2 = input()
                    c3 = input()
                    action = (c1, c2, c3)
                    state = self.game.get_successor(state, action)
                    self.game.prikaz(state)
                    if all(len(factory) == 0 for factory in state['fabrika'].values()):
                        test = False
            #stigli do toga da su sve fabrike prazne
            niz_za_fabrike = []
            if state['flag']:
                print('unesi plocice fabrike 1 po 1')
                for i in range(20):
                    niz_za_fabrike.append(input())
            test = True
            state = self.game.kraj_runde(state, niz_za_fabrike)
            self.game.prikaz(state)
        
        print(f"KONACNI REZULTAT: IGRAC - {state['stanje_igraca'][0]['poeni']} :: {state['stanje_igraca'][1]['poeni']} - BOT")

import time

class AlphaBetaVremenski(Agent):
    def __init__(self, game, time_limit=9):
        super().__init__(game)
        self.time_limit = time_limit

    def decision(self, state):
        start_time = time.time()
        time_elapsed = 0
        best_a = None
        depth = 1

        while time_elapsed < self.time_limit:
            alpha = float('-inf')
            beta = float('+inf')
            best_v = float('-inf')
            best_action_at_this_depth = None
            
            try:
                actions = self.game.get_actions(state)
                for action in actions:
                    next_v = self.min_value(self.game.get_successor(state, action), 0, alpha, beta, depth, start_time)
                    if best_v < next_v:
                        best_v = next_v
                        best_action_at_this_depth = action
            except TimeoutError:
                break

            if best_action_at_this_depth is not None:
                best_a = best_action_at_this_depth

            depth += 1
            time_elapsed = time.time() - start_time

        return best_a

    def max_value(self, state, current_depth, alpha, beta, max_depth, start_time):
        if time.time() - start_time > self.time_limit:
            raise TimeoutError("Search time exceeded")
        
        if all(len(factory) == 0 for factory in state['fabrika'].values()) or current_depth == max_depth:
            return self.game.get_utility(state)

        actions = self.game.get_actions(state)
        v = float('-inf')

        for action in actions:
            next_v = self.min_value(self.game.get_successor(state, action), current_depth + 1, alpha, beta, max_depth, start_time)
            v = max(v, next_v)
            alpha = max(alpha, v)
            if alpha >= beta:
                break

        return v

    def min_value(self, state, current_depth, alpha, beta, max_depth, start_time):
        if time.time() - start_time > self.time_limit:
            raise TimeoutError("Search time exceeded")
        
        if all(len(factory) == 0 for factory in state['fabrika'].values()) or current_depth == max_depth:
            return self.game.get_utility(state)

        actions = self.game.get_actions(state)
        v = float('+inf')

        for action in actions:
            next_v = self.max_value(self.game.get_successor(state, action), current_depth + 1, alpha, beta, max_depth, start_time)
            v = min(v, next_v)
            beta = min(beta, v)
            if alpha >= beta:
                break

        return v

class AlphaBeta(Agent):

    def __init__(self, game, depth_limit):
        super().__init__(game)
        self.depth_limit = depth_limit

    def decision(self, state):

        alpha = float('-inf')
        beta = float('+inf') #dodali alpha i beta

        best_v = float('-inf')
        best_a = None 

        actions = self.game.get_actions(state)
        for action in actions:
            next_v = self.min_value(self.game.get_successor(state, action), 0, alpha, beta) #dodali alpha i beta
            if best_v < next_v:
                best_v = next_v
                best_a = action
        
        return best_a


    def max_value(self, state, depth, alpha, beta): #dodali alpha i beta
        if all(len(factory) == 0 for factory in state['fabrika'].values()) or depth == self.depth_limit:
            return self.game.get_utility(state)
        actions = self.game.get_actions(state)
        v = float('-inf') #utility trenutnog stanja
        for action in actions:
            next_v = self.min_value(self.game.get_successor(state, action), depth, alpha, beta) #ovo je da bi smo uzeli u obzir i protivnikove korake
            #dodali alpha i beta
            v = max(v, next_v) #indirektna rekurzija
            alpha = max(alpha, v) #alpha uvijek uzima max vrijednost koju moze da postigne
            if alpha > beta: # sa optimalnom strategijom min igraca, on ovo nece dozvoliti da se desi
                break
        return v

    def min_value(self, state, depth, alpha, beta):#dodali alpha i beta
        if all(len(factory) == 0 for factory in state['fabrika'].values()) or depth == self.depth_limit:
            return self.game.get_utility(state)
        actions = self.game.get_actions(state)
        v = float('+inf') 
        for action in actions:
            next_v = self.max_value(self.game.get_successor(state, action), depth+1, alpha, beta) #dodali alpha i beta
            #ovdje povecavamo depth jer sad 'zatvaramo' jedan krug igre 
            v = min(v, next_v) 
            beta = min(beta, v) #beta uvijek uzima min vrijednost koju moze da postigne
            if alpha > beta:
                break
        return v
                    