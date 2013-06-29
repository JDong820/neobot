import re
import requests
import json
import getpass

lunarGetURL = 'http://www.neopets.com/shenkuu/lunar/?show=puzzle'
lunarPostURL = 'http://www.neopets.com/shenkuu/lunar/results.phtml'

omeletteURL = 'http://www.neopets.com/prehistoric/omelette.phtml'
jellyURL = 'http://www.neopets.com/jelly/jelly.phtml'

bankPostURL = 'http://www.neopets.com/process_bank.phtml'
bankGetURL = 'http://www.neopets.com/bank.phtml'

slorgURL = 'http://www.neopets.com/shop_of_offers.phtml'

toyURL = 'http://www.neopets.com/petpetpark/daily.phtml'

obsidianURL = 'http://www.neopets.com/magma/quarry.phtml'

appleURL = 'http://www.neopets.com/halloween/applebobbing.phtml?bobbing=1'

krawkenURL = 'http://www.neopets.com/pirates/anchormanagement.phtml'

marrowURL = 'http://www.neopets.com/medieval/process_guessmarrow.phtml'

tombolaURL = 'http://www.neopets.com/island/tombola2.phtml'

tombURL = 'http://www.neopets.com/worlds/geraptiku/process_tomb.phtml'

fruitURL = 'http://www.neopets.com/desert/fruit/index.phtml'

coltzanURL = 'http://www.neopets.com/desert/shrine.phtml'

meteorURL = 'http://www.neopets.com/moon/process_meteor.phtml'

plushieURL = 'http://www.neopets.com/faerieland/tdmbgpop.phtml'

fishingURL = 'http://www.neopets.com/water/fishing.phtml'

hideURL = 'http://www.neopets.com/games/process_hideandseek.phtml'

def hide(session):
    '''
    needs testing
    '''
    for i in range(1, 16):
        query = {'p':i,'game':17}
        hidePage = session.get(hideURL+'?p='+str(i)+'&game=17').content
        result = re.findall('You win <b>(\d+)', hidePage)
        if(result):
            print 'win'
            return result
        else:
            print 'no: '
            return hidePage
    return False

def metor(session):
    query = {'pickstep':1, 'meteorSubmit':'Submit'}
    meteorPage = session.post(meteorURL, query)
    if(re.findall('dream', meteorURL)):
        return False
    return True

def coltzan(session):
    '''
    does not work
    '''
    coltzanPage = session.post(coltzanURL).content
    if(re.findall('young', coltzanURL)):
        return True
    return False

def tombola(session):
    '''
    Does not work
    '''
    tombolaPage = session.post(tombolaURL).content
    with open('DUMP.html', 'w') as dump:
        dump.write(tombolaPage.encode('ascii', 'xmlcharrefreplace'))
    if(re.findall('win', tombolaPage)):
        return True
    return False

def marrow(session):
    '''
    Needs avail. checking
    '''
    query = {'guess':642}
    #query = {'guess':int(raw_input('Marrow weight? '))}
    marrowPage = session.post(marrowURL, query).content
    if(re.findall('WRONG!', marrowPage)):
        return False
    return True

'''
FINISHED METHODS
'''


def getToys(session):
    query = {'go': 1}
    toyPage = session.post(toyURL, query).content
    with open('dumpToy.html', 'w') as dump:
        dump.write(toyPage.encode('ascii', 'xmlcharrefreplace'))
    winnings = re.findall('items/([\d\w, _]+)', toyPage)
    if(winnings):
        return winnings[0]
    return False

def getTomb(session):
    tombPage = session.post(tombURL).content
    with open('dumpTomb.html', 'w') as dump:
        dump.write(tombPage.encode('ascii', 'xmlcharrefreplace'))
    winnings = re.findall('items/([\d\w, _]+)\.gif', tombPage)
    if(winnings):
        return winnings[0]
    if(re.findall('laughing', tombPage)):
        return 'Jackpot'
    return False

def getKrawken(session):
    krawkenPage = session.get(krawkenURL).content
    if(re.findall('more, huh?', krawkenPage)):
        print 'Krawken on cooldown.'
        return False
    ck = re.findall('action" type="hidden" value="([a-f\d]+)"', krawkenPage)
    query = {'action' : ck}
    krawkenPage = session.post(krawkenURL, query).content
    with open('dumpKrawken.html', 'w') as dump:
        dump.write(krawkenPage.encode('ascii', 'xmlcharrefreplace'))
    if(re.findall('prize-item-name">([\w\d ,\._]+)<', krawkenPage)):
        return re.findall('prize-item-name">([\w\d ,\._]+)<', krawkenPage)[0]
    return False

def getObsidian(session):
    obsidianPage = session.get(obsidianURL).content
    with open('dumpObsidian.html', 'w') as dump:
        dump.write(obsidianPage.encode('ascii', 'xmlcharrefreplace'))
    if(re.findall('shakes', obsidianPage)):
        return False
    return 'Obsidian get'

def getFruit(session):
    '''
    Works, win condition untested.
    '''
    fruitPage = session.get(fruitURL).content
    ck = re.findall('ck" value="([a-f\d]+)', fruitPage)
    if(ck):
        query = {'spin':1, 'ck':ck}
    else:
        return False
    fruitPage = session.post(fruitURL, query).content
    with open('dumpFruit.html', 'w') as dump:
        dump.write(fruitPage.encode('ascii', 'xmlcharrefreplace'))
    if(re.findall('this is not a win', fruitURL)):
        return 'nothing'
    winnings = re.findall('you won a <b>([\d\w ]+)</b>', fruitPage)
    if(len(winnings)):
        return winnings[0]
    return False

def getApple(session):
    #query = {'bobbing': 1}
    applePage = session.get(appleURL).content
    with open('dumpApple.html', 'w') as dump:
        dump.write(applePage.encode('ascii', 'xmlcharrefreplace'))
    if(re.findall('<b>inventory</b>', applePage)):
        winnings = re.findall('80\'><br><b>([\d\w ,\.]+)</b></center>', applePage)
        if winnings:
            return winnings[0]
        return True
    return False

def getPlushie(session):
    query = {'talkto':1}
    plushiePage = session.post(plushieURL, query).content
    with open('dumpPlushie.html', 'w') as dump:
        dump.write(plushiePage.encode('ascii', 'xmlcharrefreplace'))
    winnings = re.findall('items/([\d\w, _]+)\.gif', plushiePage)
    if(winnings):
        return winnings[0]
    if(re.findall('!</b>', plushiePage)):
        return re.findall('<b>([\d\w ,_\.]+)</b>!</div>', plushiePage)
    return False

def getFish(session):
    query = {'go_fish':1}
    fishingPage = session.post(fishingURL, query).content
    with open('dumpFishing.html', 'w') as dump:
        dump.write(fishingPage.encode('ascii', 'xmlcharrefreplace'))
    winnings = re.findall('items/([\d\w, _]+)\.gif', fishingPage)
    if(winnings):
        return winnings[0]
    return 'unknown state'

def getSlorg(session):
    query = {'slorg_payout': 'yes'}
    slorgPage = session.post(slorgURL, query).content
    with open('dumpSlorg.html', 'w') as dump:
        dump.write(slorgPage.encode('ascii', 'xmlcharrefreplace'))
    if(re.findall('rich', slorgPage)):
        return re.findall('<strong>([\d\.,]+) N', slorgPage)[0]
    return False

def getInterest(session):
    query = {'type':'interest'}
    session.post(bankPostURL, query)
    bankPage = session.get(bankGetURL).content
    with open('dumpBank.html', 'w') as dump:
        dump.write(bankPage.encode('ascii', 'xmlcharrefreplace'))
    interest = re.findall('([\d, ]+)NP', bankPage)
    if(re.findall('You have', bankPage)):
        return interest[0]
    return False

def getJelly(session):
    query = {'type':'get_jelly'}
    jellyPage = session.post(jellyURL, query).content
    with open('dumpJelly.html', 'w') as dump:
        dump.write(jellyPage.encode('ascii', 'xmlcharrefreplace'))
    if(re.findall('You take some', jellyPage)):
        return re.findall('items/([\d\w, _]+)', jellyPage)[0]
    if(re.findall('eaten!!!', jellyPage)):
        print 'Jelly has been eaten.'
        return False
    return False

def getOmelette(session):
    query = {'type':'get_omelette'}
    omelettePage = session.post(omeletteURL, query).content
    with open('dumpOmelette.html', 'w') as dump:
        dump.write(omelettePage.encode('ascii', 'xmlcharrefreplace'))
    if(re.findall('Sabre-X', omelettePage)):
        print 'Aready taken'
        return False
    if(re.findall('... and', omelettePage)):
        return re.findall('items/([\d\w, _]+)\.gif\' width=80',
                omelettePage)[0]
    return False

def getLunar(session):
    lunarPage = session.get(lunarGetURL).content
    angle = int(re.findall('Kreludor=([\d\.]+)', lunarPage)[0])
    answer = int(round(angle/22.5)%16)
    if answer > 7:
        answer -= 8
    else:
        answer += 8
    answer = {'submitted':'true','phase_choice':answer}
    lunarPage = session.post(lunarPostURL, answer).content
    with open('dumpLunar.html', 'w') as dump:
        dump.write(lunarPage.encode('ascii', 'xmlcharrefreplace'))
    if(re.findall('correct', lunarPage)):
        return re.findall('items/([\w\d _,]+)\.gif', lunarPage)[0]
    return False

def login():
    s = requests.session()
    login = {'username':raw_input('Username: '),'password':getpass.getpass()}
    s.post('http://www.neopets.com/login.phtml', login).content
    if('neoremember' in s.cookies.keys()):
        print 'Login successful as:', s.cookies['neoremember']
        return s
    return False

if __name__ == '__main__':
    s = login()
    #print hide(s), hide(s),hide(s),hide(s)
'''    for f in DailyFreebies.__dict__.keys():
        if f[:3] == 'get' and f[3] != 'p':
            freebie = getattr(DailyFreebies, f)()
            freebie(s)

'''



