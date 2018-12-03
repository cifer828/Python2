def combine(n,m):
    """
    calculate combine
    """
    up = 1
    down = 1
    for step in range(m-n+1,m+1):
        up *= step
    for step in range(1,n+1):
        down *= step
    return up / down

def mymethod(health,damage):
    """
    my method for certain damage on an opponent and a minion with certain health
    """
    minion_death = 0
    for step in range(health,damage+1):
        minion_death += combine(step,damage)
    return float(minion_death) / 2 ** damage

def chaoshen(health,damage):
    """
    chaoshen's method
    """
    minion_death_pos = 0
    for step in range(health - 1, damage):
        minion_death_pos += float(combine(health -1 , step)) / 2 ** (step + 1)
    return minion_death_pos
    
    
health = int(raw_input("Enter minion health: "))
damage = int(raw_input("Enter total damage: "))
print "mythod:           ",mymethod(2, 4)
print "chaoshen's method:",chaoshen(2, 4)


