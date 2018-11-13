#! python3

import random, sys

# Base Player Attributes
playerAttr = {'Strength': '5', 'Vitality': '5'}
level = 1
exp = 0
reqExp = 100

# Base Monster Attributes
normMonst = ['skeleton', 'zombie', 'bat']
skeleton = {'Strength': '3', 'Vitality': '1'}
zombie = {'Strength': '1', 'Vitality': '3'}
bat = {'Strength': '1', 'Vitality': '1'}

rareMonst = ['dragon']
dragon = {'Strength': '2', 'Vitality': '2'}

# Functions
def displayAttr():
    for x in playerAttr:
        print(x + ': ' + playerAttr.get(x))
        
def spendAttr(attrPoints):
    while attrPoints > 0:
        print('\n### You have ' + str(attrPoints) + ' unassigned attribute points, what would you like to spend them on?\n1. Strength: ' + playerAttr.get('Strength') + '\n2. Vitality: ' + playerAttr.get('Vitality'))
        spendPoints = input()
        if spendPoints == '1':
            playerAttr['Strength'] = str(int(playerAttr.get('Strength')) + 1)
            attrPoints -= 1
        elif spendPoints == '2':
            playerAttr['Vitality'] = str(int(playerAttr.get('Vitality')) + 1)
            attrPoints -= 1

def calcStats(strength, vitality):
    damage = (int(strength) * 10)
    health = (int(vitality) * 10) + 100
    return damage, health

def attack(playerDamage, playerHealth, monstDamage, monstHealth):
    # Player attack, 5% crit chance + minor RNG to make damage feel less static
    attackMod = random.randint(0, 9)
    critical = random.randint(1, 100)
    if critical >= 95:
        playerDamage *= 1.5
        playerDamage += attackMod
        print('\n### You critically hit the ' + monstName + ' dealing ' + str(int(playerDamage)) + ' damage')
        monstHealth -= int(playerDamage)
    else:
        playerDamage += attackMod
        print('\n### You swing your sword dealing ' + str(playerDamage) + ' damage to the ' + monstName)
        monstHealth -= playerDamage
    # Monster dead
    if monstHealth <= 0:
        print('\n### You defeated the ' + monstName + '!')
        return playerHealth, monstHealth
    
    # Monster attack, 5% crit chance + minor RNG to make damage feel less static
    attackMod = random.randint(0, 9)
    critical = random.randint(1, 100)
    if critical >= 95:
        monstDamage *= 1.5
        monstDamage += attackMod
        print('### The ' + monstName + ' critically hits you, dealing ' + str(int(monstDamage)) + ' damage')
        playerHealth -= int(monstDamage)
    else:
        monstDamage += attackMod
        print('### The ' + monstName + ' attacks you, dealing ' + str(monstDamage) + ' damage')
        playerHealth -= monstDamage
    # Player dead
    if playerHealth <= 0:
        print('\n### You have been defeated, better luck next time!')
        
    return playerHealth, monstHealth

def heal(playerHealth, maxHealth):
    # Minor RNG added to the heal to make it feel less static
    healMod = random.randint(0, 9)
    heal = playerHealth * .25
    heal = int(heal) + healMod
    playerHealth += heal
    # Preventing overhealing
    if playerHealth > maxHealth:
        healDiff = playerHealth - maxHealth
        heal -= healDiff
        playerHealth = maxHealth
    print('\n### You have healed for ' + str(heal) + ' health!')
    return playerHealth

def levelUp(level, exp, reqExp):
    level += 1
    exp -= reqExp
    print('\n### Congrats you are now level ' + str(level))
    spendAttr(1)
    return level, exp

# Character Creation
print('### Welcome Adventurer, what is your name?\n')
name = input()

print('\n### Hello ' + name + ' spend your attribute points to begin your adventure!')
spendAttr(5)

print('\n### You step into the cave entrance, ready to begin your adventure!\n')

# The game
playerDamage, playerHealth = calcStats(playerAttr.get('Strength'), playerAttr.get('Vitality'))
maxHealth = playerHealth

while playerHealth > 0:
    # Determine which monster will spawn
    monstRarity = random.randint(1, 10)
    if monstRarity < 10:
        monstSpawn = random.randint(0, 2)
        monster = eval(normMonst[monstSpawn])
        monstName = normMonst[monstSpawn]
    elif monstRarity == 10:
        monstSpawn = 0
        monster = eval(rareMonst[monstSpawn])
        monstName = rareMonst[monstSpawn]
        
    monstDamage, monstHealth = calcStats(monster.get('Strength'), monster.get('Vitality'))
    print('\n### You come across a ' + monstName + ' blocking your path')
    while monstHealth > 0 and playerHealth > 0:
        print('\n### The ' + monstName + '\'s health: ' + str(monstHealth) + '\n### Your health: ' + str(playerHealth))
        print('\n### What will you do?\n1. Attack\n2. Heal your wounds\n3. Attempt to run')
        choice = input()
        if choice == '1':
            playerHealth, monstHealth = attack(playerDamage, playerHealth, monstDamage, monstHealth)
        # Check if player is already full hp before healing
        elif choice == '2' and playerHealth >= maxHealth:
            print('\n### You are already at full health!')
        elif choice == '2' and playerHealth != maxHealth:
            playerHealth = heal(playerHealth, maxHealth)
        elif choice == '3':
            runChance = random.randint(1, 2)
            if runChance == 1:
                print('\n### You successfully ran away from the ' + monstName)
                break
            elif runChance == 2:
                print('\n### You failed to get away!')      
        if monstHealth <= 0:
            exp += 20
            if exp >= reqExp:
                level, exp = levelUp(level, exp, reqExp)
                playerDamage, playerHealth = calcStats(playerAttr.get('Strength'), playerAttr.get('Vitality'))
                maxHealth = playerHealth
                
            print('\n### What would you like to do next?\n1. Explore deeper in the cave\n2. Exit the game')
            choice = input()
            if choice == '1':
                print('\n### Down we go...')
                break
            elif choice == '2':
                print('\n### Thanks for playing our game!')
                sys.exit()



