import random
from copy import deepcopy

def bodovi_zid(red, kolona, zid):
        def count_adjacent(red, kolona, zid, pravac):
            br = 0
            if pravac == 'gd':
                for c in range(kolona - 1, -1, -1):
                    if zid[red][c][0]:
                        br += 1
                    else:
                        break
                for c in range(kolona + 1, len(zid[red])):
                    if zid[red][c][0]:
                        br += 1
                    else:
                        break
            elif pravac == 'ld':
                for r in range(red - 1, -1, -1):
                    if zid[r][kolona][0]:
                        br += 1
                    else:
                        break
                for r in range(red + 1, len(zid)):
                    if zid[r][kolona][0]:
                        br += 1
                    else:
                        break
            return br

        gdbr = count_adjacent(red, kolona, zid, 'gd')
        ldbr = count_adjacent(red, kolona, zid, 'ld')
        if gdbr == 0  and ldbr == 0:
            return 1
        elif gdbr == 0 and ldbr != 0:
            return ldbr + 1
        elif gdbr != 0 and ldbr == 0:
            return gdbr + 1
        else:
            return gdbr + ldbr + 2

class azulgame:
    def __init__(self, igrac=0, flag=False, niz=[]):
        
        self.start_state={
            'na_potezu' : igrac,
            'flag': flag,
            'stanje_igraca' : [
                {#covjek
                    'stepenice': [[0, 'E'] for x in range(5)],
                    'zid': [
                        [[False, 'B'], [False, 'Y'], [False, 'R'], [False, 'K'], [False, 'W']],
                        [[False, 'W'], [False, 'B'], [False, 'Y'], [False, 'R'], [False, 'K']],
                        [[False, 'K'], [False, 'W'], [False, 'B'], [False, 'Y'], [False, 'R']],
                        [[False, 'R'], [False, 'K'], [False, 'W'], [False, 'B'], [False, 'Y']],
                        [[False, 'Y'], [False, 'R'], [False, 'K'], [False, 'W'], [False, 'B']]
                    ],
                    'pod': [],
                    'poeni': 0
                },
                {#bot
                    'stepenice': [[0, 'E'] for x in range(5)],
                    'zid': [
                        [[False, 'B'], [False, 'Y'], [False, 'R'], [False, 'K'], [False, 'W']],
                        [[False, 'W'], [False, 'B'], [False, 'Y'], [False, 'R'], [False, 'K']],
                        [[False, 'K'], [False, 'W'], [False, 'B'], [False, 'Y'], [False, 'R']],
                        [[False, 'R'], [False, 'K'], [False, 'W'], [False, 'B'], [False, 'Y']],
                        [[False, 'Y'], [False, 'R'], [False, 'K'], [False, 'W'], [False, 'B']]
                    ],
                    'pod': [],
                    'poeni': 0
                }
            ],
            'fabrika' : {}
        }
        if flag and len(niz) == 20:
            self.start_state['fabrika'] = {
                str(i): list(niz[i * 4:(i + 1) * 4]) for i in range(5)
            }
            self.start_state['fabrika']['C'] = ['Q']
        else:
            self.start_state['fabrika'] = {
                str(i): [random.choice('BYRKW') for _ in range(4)] for i in range(5)
            }
            self.start_state['fabrika']['C'] = ['Q']
    
    def get_actions(self, state):
        actions = []
        igrac = state['na_potezu']
        fabrika = state['fabrika']
        stanje_igraca = state['stanje_igraca'][igrac]
        for fabrika_key, elementi in fabrika.items():
            c1 = fabrika_key
            if (fabrika_key == 'C' and len(elementi) == 1 and elementi[0] == 'Q') or (len(elementi) == 0):#da ne uzima kazneni poen bez neke druge plocice
                continue
            skup_el = set(elementi)
            for element in skup_el:
                c2 = element
                if c2 != 'Q':
                    for row_index, row in enumerate(stanje_igraca['stepenice']):
                        red_zid = stanje_igraca['zid'][row_index]
                        c3 = row_index
                        if (row[1] == 'E' or (row[1] == element and row[0] < (row_index + 1)) and any(plocica[1] == element and not plocica[0] for plocica in red_zid) and not any(plocica[1] == element and plocica[0] for plocica in red_zid)):
                            actions.append((c1, c2, c3))
                    actions.append((c1, c2, 'pod'))
        return actions
                
    def get_successor(self, state, action):
        successor_state = deepcopy(state)
        c1, c2, c3 = action
        na_potezu = successor_state['na_potezu']
        stanje_igraca = successor_state['stanje_igraca'][na_potezu]
        fabrika = successor_state['fabrika'][c1]
        
        izabrani = [plocica for plocica in fabrika if plocica == c2]
        ostali = [plocica for plocica in fabrika if plocica != c2]
        successor_state['fabrika'][c1] = ostali
        
        if c1 != 'C' and ostali:
            successor_state['fabrika']['C'].extend(ostali)
            successor_state['fabrika'][c1] = []
        elif c1 == 'C' and 'Q' in fabrika:
            stanje_igraca['pod'].extend('Q')
            successor_state['fabrika']['C'].remove('Q')
        
        if c3 != 'pod':
            red = stanje_igraca['stepenice'][int(c3)]
            red[1] = c2
            slobodno = int(c3) + 1 - red[0]
            postavljamo = min(len(izabrani), slobodno)
            red[0] += postavljamo
            preko = len(izabrani) - postavljamo
            stanje_igraca['pod'].extend([c2]*preko)
        elif c3 == 'pod':
            stanje_igraca['pod'].extend(izabrani)
            
        successor_state['na_potezu'] = 1 - na_potezu
        return successor_state
    
    def kraj_runde(self, state, niz1=[]):
        novo_stanje = deepcopy(state)
        niz = ['B', 'Y', 'R', 'K', 'W']
        score_igrac = novo_stanje['stanje_igraca'][0]['poeni']
        score_bot = novo_stanje['stanje_igraca'][1]['poeni']
        
        stanje_igraca = novo_stanje['stanje_igraca'][0]
        stanje_bota = novo_stanje['stanje_igraca'][1]
        
        for index, stepenice in enumerate(stanje_igraca['stepenice']):
            if stepenice[0] == (index + 1):
                i = index
                k = niz.index(stepenice[1])
                j = (i + k)%5
                stanje_igraca['zid'][i][j][0] = True
                temp = bodovi_zid(i, j, stanje_igraca['zid'])
                score_igrac += temp
                novo_stanje['stanje_igraca'][0]['stepenice'][index][0] = 0
                novo_stanje['stanje_igraca'][0]['stepenice'][index][1] = 'E'
                
        kazneni_igrac = 0
        if len(stanje_igraca['pod']) <= 2:
            kazneni_igrac = len(stanje_igraca['pod'])
        elif len(stanje_igraca['pod']) <= 5:
            kazneni_igrac = (2 * len(stanje_igraca['pod'])) - 2
        else:
            kazneni_igrac = (3 * len(stanje_igraca['pod'])) - 7
        
        score_igrac = score_igrac - kazneni_igrac
        
        novo_stanje['stanje_igraca'][0]['poeni'] = score_igrac
        
        ###
        
        for index, stepenice in enumerate(stanje_bota['stepenice']):
            if stepenice[0] == (index + 1):
                i = index
                k = niz.index(stepenice[1])
                j = (i + k)%5
                stanje_bota['zid'][i][j][0] = True
                temp = bodovi_zid(i, j, stanje_bota['zid'])
                score_bot += temp
                novo_stanje['stanje_igraca'][1]['stepenice'][index][0] = 0
                novo_stanje['stanje_igraca'][1]['stepenice'][index][1] = 'E'
                
        kazneni_bot = 0
        if len(stanje_bota['pod']) <= 2:
            kazneni_bot = len(stanje_bota['pod'])
        elif len(stanje_bota['pod']) <= 5:
            kazneni_bot = (2 * len(stanje_bota['pod'])) - 2
        else:
            kazneni_bot = (3 * len(stanje_bota['pod'])) - 7
        
        score_bot = score_bot - kazneni_bot
        
        novo_stanje['stanje_igraca'][1]['poeni'] = score_bot
        
        if novo_stanje['flag'] and len(niz1) == 20:
            novo_stanje['fabrika'] = {
                str(i): list(niz1[i * 4:(i + 1) * 4]) for i in range(5)
            }
            novo_stanje['fabrika']['C'] = ['Q']
        else:
            novo_stanje['fabrika'] = {
                str(i): [random.choice('BYRKW') for x in range(4)] for i in range(5)
            }
            novo_stanje['fabrika']['C'] = ['Q']
        
        if 'Q' in stanje_igraca['pod']:
            novo_stanje['na_potezu'] = 0
        elif 'Q' in stanje_bota['pod']:
            novo_stanje['na_potezu'] = 1
            
        novo_stanje['stanje_igraca'][0]['pod'] = []
        novo_stanje['stanje_igraca'][1]['pod'] = []
        
        return novo_stanje
    
    def get_utility(self, state):
        niz = ['B', 'Y', 'R', 'K', 'W']
        score_igrac = state['stanje_igraca'][0]['poeni']
        score_bot = state['stanje_igraca'][1]['poeni']
        
        stanje_igraca = state['stanje_igraca'][0]
        stanje_bota = state['stanje_igraca'][1]
        
        #prvo igrac
        for index, stepenice in enumerate(stanje_igraca['stepenice']):
            if stepenice[1] != 'E':
                temp = stepenice[0]/(index+1)
                if temp == 1:
                    temp = 3
                i = index
                k = niz.index(stepenice[1])
                j = (i + k)%5
                temp2 = bodovi_zid(i, j, stanje_igraca['zid'])
                temp3 = temp * temp2
                score_igrac += temp3
                if (i == 2 and j == 2) or (i == 1 and j == 2) or (i == 2 and j == 3) or (i == 3 and j == 3):
                    score_igrac += 0.8 #forsira bota da uzme zutu i plavu po sredini(strategija)
        kazneni_igrac = 0
        if len(stanje_igraca['pod']) <= 2:
            kazneni_igrac = len(stanje_igraca['pod'])
        elif len(stanje_igraca['pod']) <= 5:
            kazneni_igrac = (2 * len(stanje_igraca['pod'])) - 2
        else:
            kazneni_igrac = (3 * len(stanje_igraca['pod'])) - 7
            
        if 'Q' in stanje_igraca['pod']:
            score_igrac += 0.4
            
            
        score_igrac = score_igrac - kazneni_igrac
        
        #bot
        for index, stepenice in enumerate(stanje_bota['stepenice']):
            if stepenice[1] != 'E':
                temp = stepenice[0]/(index+1)
                if temp == 1:
                    temp = 3 #forsira poteze gdje se popune polja odjednom
                i = index
                k = niz.index(stepenice[1])
                j = (i + k)%5
                temp2 = bodovi_zid(i, j, stanje_bota['zid'])
                temp3 = temp * temp2
                score_bot += temp3
                if (i == 2 and j == 2) or (i == 1 and j == 2) or (i == 2 and j == 3) or (i == 3 and j == 3):
                    score_bot += 0.8 #forsira bota da uzme zutu i plavu po sredini(strategija)
        kazneni_bot = 0
        if len(stanje_bota['pod']) <= 2:
            kazneni_bot = len(stanje_bota['pod'])
        elif len(stanje_bota['pod']) <= 5:
            kazneni_bot = (2 * len(stanje_bota['pod'])) - 2
        else:
            kazneni_bot = (3 * len(stanje_bota['pod'])) - 7
            
        if 'Q' in stanje_bota['pod']:
            score_bot += 0.4
            
        score_bot = score_bot - kazneni_bot
        
        return (score_bot - score_igrac)
                
    def napuni_fabrike(self, state, niz=[]):
        novo_stanje = deepcopy(state)
        if novo_stanje['flag']:
            novo_stanje['fabrika'] = {
                str(i): list(niz[i * 4:(i + 1) * 4]) for i in range(5)
            }
            novo_stanje['fabrika']['C'] = ['Q']
        else:
            novo_stanje['fabrika'] = {
                str(i): [random.choice('BYRKW') for x in range(4)] for i in range(5)
            }
            novo_stanje['fabrika']['C'] = ['Q']
        return novo_stanje
    
    def prikaz(self, state):
        boje = {
            'B': 34,
            'Y': 33,
            'R': 31,
            'K': 30,
            'W': 29,
            'Q': 35,
            'E': 29
        }
        print(f"\033[32mNa potezu je: \033[1m{'Igrac' if state['na_potezu'] == 0 else 'Bot'}\033[0m\n\n")
        print("\033[1m\033[35mFabrike:\033[0m\n")
        
        for fabrika, plocice in state['fabrika'].items():
            print(f"Fabrika {fabrika}: ")
            for plocica in plocice:
                print(f"\033[{boje[plocica]}m{plocica} \033[0m", end="")
            print()
        
        print("-----------------------------------------")
        
        for igrac, stanje_igraca in reversed(list(enumerate(state['stanje_igraca']))):
            print(f"\033[1m\033[42m{'Igrac' if igrac == 0 else 'Bot'}\033[0m\n")
            print(f"\033[1mScore: \033[44m{stanje_igraca['poeni']}\033[0m\n")
            print("Stepenice: \n")
            for row_index, row in enumerate(stanje_igraca['stepenice']):
                for _ in range(4-row_index):
                    print('   ', end="")    
                for _ in range(row_index+1 - row[0]):
                    print('[ ]', end="")
                for _ in range(row[0]):
                    print(f"[\033[{boje[row[1]]}m{row[1]}\033[0m]", end="")
                print()
            print()
            print("Zid: \n")
            for zid_row in stanje_igraca['zid']:
                for plocica in zid_row:
                    print(f"\033[{boje[plocica[1]]}m[{plocica[1] if plocica[0] else ' '}]\033[0m", end="")
                print()
            print('\n')
                
            print("Pod:")
            for plocica in stanje_igraca['pod']:
                print(f"\033[{boje[plocica]}m[{plocica}]\033[0m", end="")
            print()
            print("-----------------------------------------")
            print('\n')
            