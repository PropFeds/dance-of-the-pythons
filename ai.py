# Basic factory
def get_ai(string):
    #if string=='guard':         return Guard()          # only enemy
    if string=='reptile_head':  return ReptileHead()
    #if string=='reptile_body':  return ReptileBody()
    #if string=='neutral_aggro': return NeutralAggro()   # snakes bears
    #if string=='neutral':       return Neutral()        # sometimes dogs, turns into aggro when provoked
    #if string=='neutral_tame':  return NeutralTame()    # kripto the bunny
    
    return None

class ReptileHead:
    def take_turn(self):
        print('Thhhhh')