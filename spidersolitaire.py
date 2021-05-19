import random

# Dieses dictionary dient lediglich zur Ausgabe in der Console.
# Es wird in der Klasse Card und Stack für die magische Methode '__str__' verwendet
n = [i for i in range(14) if i != 11]
uni_cards = {
    'hearts': {v+1: chr(127153 + n[v]) for v in range(13)},
    'spades': {v+1: chr(127137 + n[v]) for v in range(13)},
    'face_down': chr(127136)
}
# Falls die Kartensymbole schlecht lesbar sind:
#uni_cards = {
#    'hearts': {v+1: "H{:02}".format(v+1) for v in range(13)},
#    'spades': {v+1: "S{:02}".format(v+1) for v in range(13)},
#    'face_down': "|X|"
#}


class Card:
    """
    Eine einzelne Spielkarte, die Informationen bzgl Kartenwert und -Farbe speichert.
    """
    def __init__(self, value, suit):
        self._value = value
        self._suit = suit
    
    def get_value(self):
        "Liefert den Wert der Karte"
        return self._value

    def get_suit(self):
        "Liefert die Farbe der Karte"
        return self._suit

    def fits_to(self, card, matching_suit=True):
        "Prueft, ob diese Karte an eine andere angehaengt werden kann"
        if matching_suit:
            return self._value + 1 == card.get_value() and self._suit == card.get_suit()
        else:
            return self._value + 1 == card.get_value() and self._suit != card.get_suit()

    def __str__(self):
        return uni_cards[self._suit][self._value]


class Sequence:
    """
    Diese Klasse modelliert eine absteigende Sequenz von Karten
    """
    # TODO: Hier kommt Ihr Code
    def __init__(self, list_of_cards):

    # leere Liste ist keine Sequenz
        if not list_of_cards:
            print("Leere Liste übergeben")
            return
        # wir starten mit der ersten Karte
        card = list_of_cards[0]
        for current_card in list_of_cards[1:]:
            # aktuelle Karte muss zur letzten Karte passen
            if not current_card.fits_to(card):
                print("Übergebene Liste ist keine Sequence")
                return
            # aktualisiere "letzte Karte"
            card = current_card
        
        self._cards = list_of_cards

    def first_card(self):
        "Liefert die erste Karte dieser Sequenz"
        return self._cards[0]
    
    # TODO: Hier kommt Ihr Code
    def last_card(self):
        "Liefert die erste Karte dieser Sequenz"
        return self._cards[-1]

    def is_full(self):
        if len(self._cards) != 13:
            return False
        return True
    
    def fits_to(self, target_sequence, matching_suit=True):
        "Prueft, ob diese Sequenz an eine andere angehaengt werden kann"
        # die erste Karte der ersten Sequenz muss zur letzten Karte der Zweiten passen
        return self.first_card().fits_to(target_sequence.last_card(), matching_suit=matching_suit)
    
    def merge(self, target_sequence):
        # hier muss die target_sequence zu der eigenen passen nicht anders rum
        if not target_sequence.fits_to(self): 
            print("Die Sequencen können nicht zusammengefügt werden")
            return
        self._cards += target_sequence._cards
            
    def split(self, idx):
        if idx == 0 or idx >= len(self._cards):
            print("Abtrennen nicht möglich")
            return
        else: 
            splitted_cards = Sequence(self._cards[idx:])
            self._cards = self._cards[:idx]
            return splitted_cards

    def __str__(self):
        return "-".join(map(str, self._cards))
    

class Stack:
    """
    Ein Stapel von Sequenzen. Diese Klasse modelliert die einzelnen Stapel des Spiels.
    Neben den Sequenzen, welche den aufgedeckten Karten entsprechen, merkt sich ein Stapel noch die umgedrehten/verdeckten Karten.
    """
    # TODO: Hier kommt Ihr Code
    def __init__(self, card, face_down_cards):
        self._sequences = [Sequence([card])]
        self._face_down_cards = face_down_cards


    def is_empty(self):
        "Prueft, ob dieser Stapel leer ist, es also keine offenen Karten mehr gibt."
        return not self._sequences

    # TODO: Hier kommt Ihr Code
    def last_sequence(self):
        if self.is_empty():
            print("Es existiert keine Sequence auf diesem Stapel")
            return
        return self._sequences[-1]
    
    def append_sequence(self, sequence):
        self._sequences.append(sequence)
    
    def remove_last_sequence(self):
        if self.is_empty():
            print("Es existiert keine Sequence auf diesem Stapel")
            return
        self._sequences.pop()

    def test_revealcard(self):
        """
        Deckt, wenn moeglich, eine neue Karte von den zugedeckten Karten auf.
        Dafuer muss der Stapel leer sein und es muss noch zugedeckte geben.
        """
        if self.is_empty() and self._face_down_cards:
            self.append_sequence(Sequence([self._face_down_cards.pop()]))
    
    # TODO: Hier kommt Ihr Code

    def test_fullsequence(self):
        if self.last_sequence().is_full():
            self.remove_last_sequence()
            self.test_revealcard()
    
    def deal_card(self, card):
        seq = Sequence([card])
        if seq.fits_to(self.last_sequence()):
            self.last_sequence().merge(seq)
            self.test_fullsequence()
        else:
            self.append_sequence(seq)

    def __str__(self):
        return " ".join(len(self._face_down_cards) *  [uni_cards['face_down']] + list(map(str, self._sequences)))


class SpiderSolitaire:
    ALL_CARDS = [Card(value, suit) for value in range(1, 14) for suit in ["hearts", "spades"]]
    """
    Klasse, die das ganze Spielfeld an sich verwaltet.
    """
    def __init__(self):
        # wir starten mit allen Karten (4 ganze Kartendecks mit jeweils 13 Herz und 13 Pik)
        self._stack2deal = 4 * SpiderSolitaire.ALL_CARDS
        # Durchmischen aller Karten
        random.shuffle(self._stack2deal)

        # Anzahl verdeckter Karten pro Stapel
        cards2deal_perstack = [5, 5, 5, 5, 4, 4, 4, 4, 4, 4]

        # Es werden 10 Stapel erzeugt und in self._stacks gespeichert. 
        # Jeder Stapel bekommt hierbei die entsprechende Anzahl verdeckter Karten und die eine aufgedeckte Karte uebergeben.
        self._stacks = []
        for k in range(10):
            face_down_cards = [self._stack2deal.pop() for _ in range(cards2deal_perstack[k])]
            self._stacks.append(Stack(self._stack2deal.pop(), face_down_cards))
        
        # Sequenz unter dem Mauszeiger/bewegende Sequenz
        self.moving_sequence = None
        # Woher kam die bewegte Sequenz
        self.origin_stack_index = None
    
    # TODO: Hier kommt Ihr Code

    
    def pick_up(self, stack_index, card_index):
        """
        'Aufheben' einer Sequenz
        """
        if self.moving_sequence is not None:
            print("Already moving!")
            return
        
        if not (0 <= stack_index < 10):
            print("Wrong index for stack!")
            return
        
        stack = self._stacks[stack_index]
        # kann nicht von leerem Stapel aufheben
        if stack.is_empty():
            print("Stack is empty!")
            return
        
        if card_index == 0:
            self.moving_sequence = stack.last_sequence()
            stack.remove_last_sequence()
        else:
            splitted = stack.last_sequence().split(card_index)
            # card_index war nicht zulaessig
            if splitted is None:
                return
            else:
                self.moving_sequence = splitted
        
        self.origin_stack_index = stack_index
    
    def abort_move(self):
        "'Abbruch' des Bewegvorgangs"
        if self.moving_sequence is not None:
            source_stack = self._stacks[self.origin_stack_index]

            # Ursprungsstapel leer oder bewegende Sequenz passt nicht zum Ursprungsstapel -> append
            if source_stack.is_empty() or not self.moving_sequence.fits_to(source_stack.last_sequence()):
                source_stack.append_sequence(self.moving_sequence)
            # Sequenz passt zum Urspringsstapel -> merge
            else:
                source_stack.last_sequence().merge(self.moving_sequence)
            
            # reset containers
            self.moving_sequence = None
            self.origin_stack_index = None
    
    def move(self, stack_index):
        "'Bewegen' einer (Teil-) Sequenz"
        if self.moving_sequence is None:
            print("There is nothing to move. Call 'pick_up' first.")
            return
        
        if stack_index is None or stack_index == self.origin_stack_index:
            self.abort_move()
            return
        
        if not (0 <= stack_index < 10):
            self.abort_move()
            print("Wrong index for stack")
            return

        target_stack = self._stacks[stack_index]
        source_stack = self._stacks[self.origin_stack_index]

        # TODO: Hier kommt Ihr Code
        

        # reset containers
        self.moving_sequence = None
        self.origin_stack_index = None

    def is_won(self):
        "Gibt True zurück, wenn das Spiel gewonnen wurde."
        return all(stack.is_empty() for stack in self._stacks)

    def play(self):
        "Die Spielschleife. Gibt True zurück, wenn das Spiel gewonnen wurde."
        # Wir sind gerade dabei eine Sequenz zu bewegen
        if self.moving_sequence is not None:
            print("picked up: " + str(self.moving_sequence))
            print("Options:")
            print("k    move sequence to stack k")
            print('"b"  move sequence back to original stack {}'.format(self.origin_stack_index))
            
            user_in = input("Input: ").strip().lower()
            
            # Zuruecklegen auf den ursprungsstapel (Abbruch)
            if user_in == "b":
                self.abort_move()
                return
            
            try:
                stack_index = int(user_in)
            except ValueError:
                print("Wrong input!")
                return
                
            self.move(stack_index)
            
            # Gewinnabfrage
            if self.is_won():
                print("Congratulations, you won!")
                return True
        else:
            print("Options:")
            # es gibt noch Karten zum Austeilen
            if self._stack2deal:
                print('"d"   deal (there are still {} cards to deal)'.format(len(self._stack2deal)))                
            print("k, n  pick up the last subsequence (part [n:]) of stack k")
            print("k     pick up the last sequence of stack k")
            user_in = input("Input: ").strip().lower()
        
            # Austeilen
            if user_in == "d" :
                self.deal()
                return

            try:
                splitted = user_in.split(",")
                # nur Stacknummer eingegeben
                if len(splitted) == 1:
                    stack_index, card_index = int(splitted[0]), 0
                # beides eingegeben
                else:
                    stack_index, card_index = map(int, splitted)
            except ValueError:
                print("Wrong input!")
                return
            
            self.pick_up(stack_index, card_index)
    
    
    def __str__(self):
        res = [f"{i} {stack}" for i, stack in enumerate(self._stacks)]
        return "\n".join(res)


if __name__ == "__main__":
    ss = SpiderSolitaire()

    is_won = False
    while not is_won:
        print()
        print(ss)

        is_won = ss.play()
