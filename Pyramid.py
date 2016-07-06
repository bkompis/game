from random import randint
from random import choice
"""
VYLEPSENIA:
1.) simulacia hraca s dvoma rukami. Hrac moze niest ziadnu, jednu jednorucnu,
dve jednorucne alebo jednu obojrucnu zbran. V hre su aj stity, brane ako jednorucne zbrane. 
    -> pridana metoda Player.equip(self, hand, weapon)     
    -> zmena suboja (utok a obrana sa pocitaju z oboch ruk)
    -> definovany predmet ruka =  Weapon(...)
2.) upraveny vyber cennych predmetov, zbrani a priser, aby hra bola hratelnejsia -> celkom hardcore ked hrac nema stastie, chcelo by to progresivne zvysovanie urovne priser 
3.) zavedena minimalna pauza medzi odpocinkami:
    premenna can_rest sa po kazdom odpocinku nastavi na 10, zmensuje sa kazdou platnou akciou hraca(-1 za "vezmi", "poloz", "vyzbroj", -3 za "jdi")
    odpocinok povoleny ked can_rest <= 0
4.) zavedene minimalne zranenie hracom, aby sa zabranilo nevyhratelnym bojom ("Tvuj utok zpusobil 0 zraneni.").

Zname PROBLEMY A NEDOSTATKY:
    - miestnosti start a trap maju neuplne vypisy (podla zadania (vzorovy priklad) nevypisuju udaje o predmetoch v miestnosti)
    - prisery raz porazene su porazene navzdy (stale sa odkazuje na objekt v zozname, tomu sa menia atributy v boji)
    - silna obrana priser (preto pridana minimalna hodnota utoku hraca)
    - zvlastne spravanie nahodnej generacie obsahu planu
Hra sa spusta prikazom play().
"""
class Item(object):
    def __init__(self, name, description, value, weight):
        self.name = name
        self.description = description
        self.value = value
        self.weight = weight
    def describe(self):
        print   self.name + ": " + self.description,
        print "cena: " + str(self.value) + ", hmotnost: " + str(self.weight)

class Weapon(object):
    def __init__(self, name, description, attack, defence, is_twohanded):
        self.name = name
        self.description = description
        self.attack = attack
        self.defence = defence
        self.is_twohanded = is_twohanded
    def describe(self):
        print self.name + ": " + self.description,
        print "(utok: " + str(self.attack) + ", obrana: " + str(self.defence)+ ").",
        if self.is_twohanded == True:
            print "Obourucna zbran."
        else:
            print "Jednorucna zbran."
    


items = [ # name, description, value, weight
    Item("zlato", "Volne polozeny kus zlata.", 200, 10),
    Item("prsten1", "Prsten s diamantem.", 150, 1),
    Item("prsten2", "Prsten bez diamantu.", 40, 1),
    Item("prsten3", "Zlaty prsten.", 85, 1),
    Item("prsten4", "Zelezny prsten.", 10, 1),
    Item("vaza", "Cenna vaza.", 185, 15),
    Item("miska", "Zlata miska osazena drahokamy.", 170, 5),
    Item("truhla", "Mosazna truhla plna zlatych minci.", 300, 115),
    Item("mince", "Zlata mince.", 20, 1),
    Item("diamant", "Diamant velky jako krepelci vejce.", 450, 5),
    Item("smaragd", "Krasny vybrouseny kus smaragdu.", 150, 3),
    Item("platy", "Tenke zlate platy.", 250, 30),
    Item("svitky", "Svitky popsane hieroglyfy.",125, 5),
    Item("sperky", "Sbirka zlatych sperku ve zdobene krabicce.", 200, 5),
    Item("kamen", "Hezky kamen, mozna ma nejakou hodnotu.", 10, 20),
    Item("naramek", "Zelezny naramek.", 25, 3),
    ]
superitem = Item("maska", "Faraonova maska. Velmi cenna.", 500, 10)

weapons = [ #name, description, attack, defence, is_twohanded
    Weapon("sekera", "Obrovska oborucni sekera. Uneses ji?", 14, 2, True),
    Weapon("kopi", "Dvoumetrove kopi.", 10, 3, True),
    Weapon("mec", "Uplne normalni mec.", 8, 2, False),
    Weapon("r_mec", "Rezavy mec.", 5, 1, False),
    Weapon("hul", "Obourucni okovana hul.", 12, 2, True),
    Weapon("kus", "Samostril. Ucinny, ale obtizne se natahuje.", 20, 0, True),
    Weapon("savle", "Savle s rukojeti posazenou drahokamy.", 7, 3, False),
    Weapon("d_stit", "Velky dreveny stit. Nebo dvere?", 0, 8,  False),
    Weapon("k_stit", "Maly kovovy stit.", 0, 10,  False),
    Weapon("sv_mec", "Svetelny mec. Kde se tady vzal?", 18, 8, False),
    Weapon("kladivo", "Jednorucne valecne kladivo.", 10, 1, False),
    Weapon("dyka", "Zlozite zdobena ritualni dyka.", 4, 1, False)
    ]
ruka = Weapon("ruka","Tvoje vlastni ruka. Co tak cumis?", 1, 1, False)


class Monster(object):
    def __init__(self, name, attack, defence, vigilance, health):
        self.name = name
        self.attack = attack
        self.defence = defence
        self.vigilance = vigilance
        self.health = health
        self.sleeping = True
    def react_to_noise(self):
        if randint(1,20) <= self.vigilance:
            self.sleeping = False

class Player(object):
    def __init__(self, name):
        self.name = name
        self.max_health = randint(150,200)
        self.health = self.max_health
        self.capacity = randint(150,200)
        self.left_hand = ruka       
        self.right_hand = weapons[3]
        self.bag = {}
    def rest(self):
        if self.max_health - self.health >= 50:
            self.health += 50
            return 50
        else:
            kolik = self.max_health - self.health
            self.health = self.max_health
            return kolik
    def add_to_bag(self, item):             #input object (tvaru items[x] alebo weapons[x])
        if item.weight >  self.capacity:
            print "Tento predmet neuneses."
            return False
        else:
            print "Predmet \"" + item.name + "\" vlozen do batohu."
            self.bag[item.name] = Item(item.name, item.description, item.value, item.weight)
            self.capacity -= item.weight
            return True 
    def equip(self, hand, weapon = ruka):         #input weapon ako object, moznost unequip nezadanim zbrane; vrati zoznam objektov
        previous_weapons = []
        if weapon.is_twohanded == False:                #prikaz equip jednorucnu zbran
            if self.right_hand.is_twohanded == True:    #prave equipnuta zbran je obojrucna
                if hand == "prava":
                    self.left_hand = ruka     
                    previous_weapons.append(self.right_hand)
                    self.right_hand = weapon
                else:
                    self_right_hand = ruka
                    previous_weapons.append(self.left_hand)
                    self.left_hand = weapon
            elif hand == "leva":                    #equipujem jednorucnu zbran ked bola equipnuta jednorucna
                if self.left_hand == ruka:   
                    self.left_hand = weapon
                else:   
                    previous_weapons.append(self.left_hand) 
                    self.left_hand = weapon                 
            elif hand == "prava":
                if self.right_hand == ruka:
                    self.right_hand = weapon
                else:
                    previous_weapons.append(self.right_hand)
                    self.right_hand = weapon
        elif weapon.is_twohanded == True:                   #vrati dva objekty v zozname 
            if self.left_hand == ruka != self.right_hand:
                previous_weapons.append(self.right_hand)
            elif self.right_hand == ruka != self.left_hand:
                previous_weapons.append(self.left_hand)
            else:
                previous_weapons.append(self.right_hand)
                previous_weapons.append(self.left_hand)
            self.left_hand = weapon
            self.right_hand = weapon
        return previous_weapons                
                
    def take_from_bag(self, item_name):     #input string
        if item_name in self.bag:
            vec = self.bag[item_name]
            self.capacity += vec.weight
            del self.bag[item_name]
            return vec                      #output object
        else:
            print "Tenhle predmet nemas."
            return None

    def describe(self):
        print "Jmeno hrace:", self.name
        print "Zdravi:", str(self.health) + "/" + str(self.max_health)
        print "Zbyvajici kapacita batohu:", str(self.capacity)
        if len(self.bag) == 0:
            print "Prazdny batoh."
        else:
            print "Obsah batohu:"
            for vec in self.bag:
                print " -",
                self.bag[vec].describe()
        print "Leva ruka:",
        self.left_hand.describe()
        print "Prava ruka:",
        self.right_hand.describe()
        
    def score(self):
        skore = 0
        for vec in self.bag:
            skore += self.bag[vec].value
        return skore

def attack_player(player, monster):
    print "Utocis na protivnika."
    damage  = int((randint(8,12)*0.1) * (player.left_hand.attack + player.right_hand.attack)) - monster.defence
    if damage <= 0:         #aby privysoka obrana neliecila
        damage = 1
    print "Tvuj utok zpusobil " + str(damage) + " zraneni."
    monster.health -= damage
    print "Protivnikovo zdravi: " + str(monster.health)
    raw_input("Stiskni enter: ")
    if monster.health <= 0:
        print "Protivnik je porazen!"
        return True
    
def attack_monster(player, monster):
    print "Protivnik \"" + monster.name + "\" na tebe utoci."
    damage = int((randint(8,12)*0.1) * monster.attack) - (player.left_hand.defence + player.right_hand.defence)
    if damage < 0:
        damage = 0
    print "Tento utok ti zpusobil " + str(damage) + " zraneni."
    player.health -= damage
    print "Tvoje zdravi:" + str(player.health) + "/" + str(player.max_health)
    raw_input("Stiskni enter: ")
    if player.health <= 0:
        print "Postava " + player.name + " umrela v boji s priserou \"" + monster.name + "\"."
        return False

def fight(player, monster):
    result = None
    print "Souboj s protivnikem: " + monster.name + " (" + str(monster.health) + " zdravi)"
    print "Tvoje zdravi: " + str(player.health) + "/" + str(player.max_health)
    if randint(1,20) > monster.vigilance:               #player starts
        while result == None:
            result = attack_player(player, monster)
            if monster.health <=0:
                break
            print 
            result = attack_monster(player, monster)
            print 
    else:                                               #monster starts
        while monster.health > 0 and player.health > 0:
            result = attack_monster(player, monster)
            if player.health <= 0:
               break
            print 
            result = attack_player(player, monster)
            print 
    return result

class Room(object):
    def __init__(self, description, ending=None):
        self.description = description
        self.ending = ending
        self.monster = None
        self.items = {}
        self.weapons = {}
        self.directions = {}
    def set_monster(self, monster):
        self.monster = monster
    def add_weapon(self, weapon):
        self.weapons[weapon.name] = Weapon(weapon.name, weapon.description, weapon.attack, weapon.defence, weapon.is_twohanded)
    def remove_weapon(self, weapon):
        del self.weapons[weapon]
    def add_item(self, item):
        self.items[item.name] = Item(item.name, item.description, item.value, item.weight)
    def remove_item(self, item):        #input string
        del self.items[item]
    def add_direction(self, name, room):
        self.directions[name] = room
    def describe(self):
        print self.description
        print "V mistnosti se nachazeji nasledujici predmety:"
        for i in self.items:
            print "-",
            self.items[i].describe()
        print "V mistnosti se nachazeji nasledujici zbrane:"
        for w in self.weapons:
            print "-",
            self.weapons[w].describe()
        print "Z mistnosti se da odejit nasledujicimi smery:"
        for d in self.directions:
            print "- ", d
        if self.monster != None:
            self.monster.react_to_noise()
            if  self.monster.sleeping == True:    
                print "V mistnosti je " + self.monster.name + ". Spi."
                return True
            else:
                print "V mistnosti je " + self.monster.name + ". Je vzhuru!"
                return False


monsters = [ # popis, utok, obrana, ostrazitost, zdravi
    Monster("mumie", 6, 1, 7, 55),
    Monster("zachovala mumie", 7, 1, 9, 50),
    Monster("odolna mumie", 6, 1, 7, 85),
    Monster("temer rozpadla mumie", 4, 0, 5, 45),
    Monster("slaba mumie", 5, 0, 5, 50),
    Monster("ostrazita mumie", 6, 1, 20, 50),
    Monster("pavouk", 6, 3, 11, 35),
    Monster("velky pavouk", 7, 4, 12, 55),
    Monster("velky zly pavouk", 10, 2, 15, 60),
    Monster("velky zly jedovaty pavouk", 12, 3, 10, 45),
    Monster("kobra", 11, 3, 18, 55),
    Monster("netopyr", 4, 3, 15, 40),
    Monster("stir", 8, 4, 11, 45),
    Monster("pisecny golem", 6, 6, 2, 85),
    Monster("duch", 5, 5, 18, 40),
    Monster("pekelny pes", 10, 0, 16, 50),
    Monster("ozivly sluzebnik", 8, 4, 13, 60),
    Monster("armada mravencu", 2, 8, 15, 100),
    Monster("letajici hlava", 4, 2, 17, 35),
    Monster("kostlivy bojovnik", 11, 4, 8, 65)
    ]

pharaoh = Monster("faraon", 25, 5, 10, 100)

exit = Room("Hura! Jsi venku z pyramidy a jsi nazivu.", True)
start = Room("Jsi ve vchodu do pyramidy.")
tomb = Room("Jsi ve slavne faraonove kobce.\n" +
        "Stena na zapade vypada, ze se da odsunout.")
tomb.set_monster(pharaoh)
tomb.add_item(superitem)

trap = Room("Vchazis do mistnosti, kdyz tu slysis, jak pod tebou cvaklo propadlo.")
snakes = Room("Padas do mistnosti plne hadu. Tim to pro tebe konci.", False)
rooms = [
    Room("Jsi v pyramide, chodby vedou na vychod a na jih."),
    Room("Jsi uprostred chodby, ktera vede zapadovychodnim smerem."),
    Room("Jsi v rohove mistnosti pyramidy. Chodby vedou na zapad a na jih."),
    Room("Jsi uprostred severojizni chodby. Stena na vychode vypada podezrele."),
    Room("Jsi uprostred severojizni chodby. Stena na zapade vypada uplne obycejne."),
    Room("Jsi v podlouhle mistnosti, ze ktere vede jedina chodba na sever.\n" +
        "Ve vzdalenem rohu mistnosti jsou schody nahoru."),
    Room("Jsi v pyramide, chodby vedou na sever, na jih a na vychod."),
    Room("Jsi v klikate chodbe, ze ktere se da pokracovat na sever a na vychod."),
    Room("Jsi v klikate chodbe, ze ktere se da pokracovat na sever a na zapad.\n" +
        "U steny chodby jsou schody nahoru."),
    Room("Jsi v obrovske mistnosti, severni stena je pokryta hieroglyfy.\n" +
        "Na jihu jsou dvoje dvere, v rohu mistnosti jsou schody nahoru."),
    Room("Jsi v druhem patre pyramidy, na severu jsou pootevrene dvere.\n" +
        "Chodba pokracuje na jih."),
    Room("Jsi v druhem patre pyramidy, na severu jsou pootevrene dvere.\n" +
        "Chodba pokracuje na jih."),
    Room("Jsi v rohove mistnosti v druhem patre pyramidy.\n" +
        "Chodby vedou na sever a na vychod. V rohu mistnosti jsou schody dolu."),
    Room("Jsi v rohove mistnosti v druhem patre pyramidy.\n" +
        "Chodby vedou na sever a na zapad. V rohu mistnosti jsou schody dolu."),
    Room("Jsi v nejvyssim patre pyramidy. Jedina chodba vede na jih.\n" +
        "Uprostred mistnosti jsou schody dolu."),
    Room("Jsi v nejvyssim patre pyramidy. Po prichodu za tebou zapadly dvere.\n" +
        "Uprostred mistnosti je skluzavka dolu. Je to zrejme jedina cesta ven."),
    ]

start.add_direction("ven", exit)
start.add_direction("dovnitr", rooms[6])
trap.add_direction("dolu", snakes)
tomb.add_direction("zapad", rooms[3])
rooms[0].add_direction("vychod", rooms[1])
rooms[0].add_direction("jih", rooms[3])
rooms[1].add_direction("vychod", rooms[2])
rooms[1].add_direction("zapad", rooms[0])
rooms[2].add_direction("zapad", rooms[1])
rooms[2].add_direction("jih", rooms[4])
rooms[3].add_direction("sever", rooms[0])
rooms[3].add_direction("jih", rooms[5])
rooms[4].add_direction("sever", rooms[2])
rooms[4].add_direction("jih", rooms[6])
rooms[5].add_direction("sever", rooms[3])
rooms[5].add_direction("nahoru", rooms[12])
rooms[6].add_direction("sever", rooms[4])
rooms[6].add_direction("jih", rooms[8])
rooms[6].add_direction("vychod", start)
rooms[7].add_direction("sever", trap)
rooms[7].add_direction("vychod", rooms[8])
rooms[8].add_direction("sever", rooms[6])
rooms[8].add_direction("zapad", rooms[7])
rooms[8].add_direction("nahoru", rooms[13])
rooms[9].add_direction("jihovychod", rooms[10])
rooms[9].add_direction("jihozapad", rooms[11])
rooms[9].add_direction("nahoru", rooms[14])
rooms[10].add_direction("sever", rooms[9])
rooms[10].add_direction("jih", rooms[12])
rooms[11].add_direction("sever", rooms[9])
rooms[11].add_direction("jih", rooms[13])
rooms[12].add_direction("sever", rooms[10])
rooms[12].add_direction("vychod", rooms[13])
rooms[12].add_direction("dolu", rooms[5])
rooms[13].add_direction("sever", rooms[11])
rooms[13].add_direction("zapad", rooms[12])
rooms[13].add_direction("dolu", rooms[8])
rooms[14].add_direction("jih", rooms[15])
rooms[14].add_direction("dolu", rooms[9])
rooms[15].add_direction("dolu", tomb)


 
def randomize(rooms, monsters, items, weapons):         
    for mistnost in rooms:
        seed = [randint(1,4), randint(0,2), randint(1,3)]
        if seed[0] != 1: mistnost.set_monster(choice(monsters)) #75% sanca na priseru v miestnosti
        for i in range (seed[1]): mistnost.add_item(choice(items))  #0-2 predmety v miestnosti; vyzera byt bugle, stretla som aj 4 itemy  
        if seed[2] == 1: mistnost.add_weapon(choice(weapons))   #33% sanca na zbran v miestnosti

def play(start = start):
    randomize(rooms, monsters, items, weapons)
    can_rest = 0
    game_over = False
    player = Player(str(raw_input("Jake je tve jmeno, odvazny dobrodruhu?\n")))
    player.describe()
    current_room = start
    print "Pro napovedu zadej \"napoveda\"."
    print
    while game_over == False:
        print "Do nejblizsiho odpocinku:", str(can_rest)
        if current_room not in [trap, start]:
            no_fight = current_room.describe()
            print
            if no_fight == False:
                fight_result = fight(player, current_room.monster)
                if fight_result == True:
                    current_room.monster = None
                    current_room.describe()
                else:
                    game_over = True
                    return
        else:
            print current_room.description
            print "Z mistnosti se da odejit nasledujicimi smery:"
            for d in current_room.directions:
                print "- ", d
        prikaz = str(raw_input("Zadej prikaz: "))
        while len(prikaz) == 0:
            prikaz = str(raw_input("Zadej prikaz: "))
        prikaz = prikaz.lower() 
        prikaz = prikaz.split()
        while prikaz[0] not in ["info", "jdi", "vezmi", "vyzbroj", "odpocinek", "poloz", "konec", "napoveda"]:     
            print "Nepodporovany vstup.",
            prikaz = str(raw_input("Zadej prikaz: "))
            prikaz = prikaz.lower()
            prikaz = prikaz.split()
        if prikaz[0] == "info":        
            player.describe()

        elif prikaz[0] == "jdi":        
            if prikaz[1] in current_room.directions:
                if can_rest > 0:                            #uprava pocitadla umoznujuceho odpocinok
                    can_rest -= 3
                current_room = current_room.directions[prikaz[1]]
                if current_room.ending == False:
                    print current_room.description
                    print "--- neuspesny konec hry ---"
                    game_over = True
                elif current_room.ending == True:
                    max_skore = 500         #faraonova maska       
                    for room in rooms:
                        for item in room.items:
                            max_skore += room.items[item].value
                    print current_room.description
                    print "Tvoje skore: " + str(player.score()) + "/" + str(max_skore)
                    game_over = True
            else:
                print "Tudy cesta nevede."

        elif prikaz[0] == "vyzbroj":
            if len(prikaz) == 1:
                print "Zadej ruku, do ktere chces zbran vzit nebo ze ktere chces zbran odebrat."
            elif prikaz[1] not in ["leva", "prava"]:
                print "Zadej ruku, do ktere chces zbran vzit."
            else:
                if len(prikaz) < 3:
                    if can_rest > 0:                            #uprava pocitadla umoznujuceho odpocinok   
                        can_rest -= 1
                    previous_weapons = player.equip(prikaz[1])
                    if previous_weapons != []:
                        for weapon in previous_weapons:
                            current_room.add_weapon(weapon)
                    player.describe()
                    print
                else: 
                    if prikaz[2] in current_room.weapons:
                        if can_rest > 0:                        #uprava pocitadla umoznujuceho odpocinok
                            can_rest -= 1
                        previous_weapons = player.equip(prikaz[1], current_room.weapons[prikaz[2]])
                        current_room.remove_weapon(prikaz[2])
                        if previous_weapons != []:
                            for weapon in previous_weapons:
                                current_room.add_weapon(weapon)
                        player.describe()
                        print
                    else:
                        print "Tato zbran v mistnosti neni."
        
        elif prikaz[0] == "vezmi":
            vec = prikaz[1]
            if vec in current_room.items:                
                can_take = player.add_to_bag(current_room.items[vec])
                if can_take == True:
                    current_room.remove_item(vec)
                    if can_rest > 0:                        #uprava pocitadla umoznujuceho odpocinok    
                        can_rest -= 1
            else:
                print "Tento predmet se v mistnosti nenachazi."

        elif prikaz[0] == "odpocinek":
            if current_room.monster == None:
                if can_rest <= 0:
                    added_health = player.rest()
                    print "Tvoje postava si odpocinula a nabrala " + str(added_health) + " zdravi."
                    print "Zdravi: " + str(player.health) + "/" + str(player.max_health)
                    can_rest = 10                           #zacne odpocitavanie, kedy postava bude moct znova odpocivat 
                else:
                    print "Jeste se ti nechce odpocivat."
            else: print "V mistnosti s priserou nemuzes odpocivat, ty blazne!"

        elif prikaz[0] == "poloz":
            if prikaz[1] in player.bag:
                if can_rest > 0:                            #uprava pocitadla umoznujuceho odpocinok
                    can_rest -= 1
                current_room.add_item(player.take_from_bag(prikaz[1]))
                print "Polozil jsi " + prikaz[1]
            else: player.take_from_bag(prikaz[1])

        elif prikaz[0] == "konec":
            return

        elif prikaz[0] == "napoveda":
            print   "info:\t\t\t vypise stav postavy"
            print   "jdi <smer>:\t\t postava odejde z mistnosti zadanym smerem"
            print   "vezmi <predmet>:\t postava sebere zadany predmet"
            print   "poloz <predmet>:\t postava odlozi predmet z batohu do mistnosti"
            print   "vyzbroj <ruka><zbran>:\t postava do zadane ruky vezme zadanou zbran z mistnosti"
            print   "\t\t\t - pri obourucnych zbranich vepis kteroukoliv ruku"
            print   "\t\t\t - pro unequip z dane ruky nech <zbran> prazdne."
            print   "odpocinek:\t\t pokud v mistnosti neni prisera, postava si odpocine a nabere zdravi"
            print   "konec:\t\t\t ukonceni hry"
            print   "napoveda:\t\t vypise tuto napovedu"
            print

