from spidersolitaire import Card, Sequence, Stack, SpiderSolitaire
import unittest
import types
import itertools


def skip_not_impl(obj, *attr):
    c_obj = obj
    # recursively check if 'attr' exists in 'obj'
    for name in attr:
        if not hasattr(c_obj, name):
            break
        c_obj = getattr(c_obj, name)
    else:
        if type(c_obj) == types.FunctionType:
            return lambda f: f
    
    return unittest.skip("{!r} is not yet implemented.".format(".".join(attr)))

def call_counter(func):
    count = 0

    def f(*args, **kwargs):
        nonlocal count
        count += 1
        return func(*args, *kwargs)

    def get_count():
        return count

    return f, get_count


class SequenceTests(unittest.TestCase):
    @skip_not_impl(Sequence, "__init__")
    def test_a(self):
        "'Konstruktor' - Test"
        lst = [Card(2, "hearts"), Card(1, "hearts")]
        seq = Sequence(list(lst))
        self.assertEqual(seq._cards, lst)
        
        # test inconsistent sequence (empty)
        seq = Sequence([])
        self.assertTrue(("_cards" not in dir(seq)) or (seq._cards is None), msg="Bei ungültiger Sequenz soll das Attribut '_cards' nicht gesetzt werden.")
        
        # test inconsistent sequence (wrong values)
        seq = Sequence([Card(4, "hearts"), Card(1, "hearts")])
        self.assertTrue(("_cards" not in dir(seq)) or (seq._cards is None), msg="Bei ungültiger Sequenz soll das Attribut '_cards' nicht gesetzt werden.")
        
        # test inconsistent sequence (wrong suit)
        seq = Sequence([Card(4, "spades"), Card(3, "hearts")])
        self.assertTrue(("_cards" not in dir(seq)) or (seq._cards is None), msg="Bei ungültiger Sequenz soll das Attribut '_cards' nicht gesetzt werden.")
    
    @skip_not_impl(Sequence, "last_card")
    def test_b(self):
        "'last_card' - Test"
        last = Card(5, "hearts")
        seq = Sequence([Card(7, "hearts"), Card(6, "hearts"), last])
        self.assertEqual(seq.last_card(), last)
    
    @skip_not_impl(Sequence, "is_full")
    def test_c(self):
        "'is_full' - Test"
        lst1 = [Card(v, "hearts") for v in range(13, 0, -1)]
        lst2 = [Card(v, "spades") for v in range(13, 0, -1)]

        self.assertEqual(Sequence(list(lst1)).is_full(), True)
        self.assertEqual(Sequence(lst1[:-1]).is_full(), False)
        self.assertEqual(Sequence(lst1[1:]).is_full(), False)
        self.assertEqual(Sequence(list(lst2)).is_full(), True)
        self.assertEqual(Sequence(lst2[:-1]).is_full(), False)
        self.assertEqual(Sequence(lst2[3:]).is_full(), False)
    
    @skip_not_impl(Sequence, "fits_to")
    def test_d(self):
        "'fits_to' - Test"
        seq1 = Sequence([Card(2, "hearts"), Card(1, "hearts")])
        seq2 = Sequence([Card(4, "hearts"), Card(3, "hearts")])
        seq3 = Sequence([Card(4, "spades"), Card(3, "spades")])
        
        self.assertEqual(seq1.fits_to(seq2), True)
        self.assertEqual(seq1.fits_to(seq2, matching_suit=True), True)
        self.assertEqual(seq1.fits_to(seq3), False)
        self.assertEqual(seq1.fits_to(seq3, matching_suit=True), False)
        
        self.assertEqual(seq1.fits_to(seq2, matching_suit=False), False)
        self.assertEqual(seq1.fits_to(seq3, matching_suit=False), True)
        
        self.assertEqual(seq2.fits_to(seq1), False)
        self.assertEqual(seq2.fits_to(seq1, matching_suit=True), False)
        self.assertEqual(seq2.fits_to(seq1, matching_suit=False), False)
    
    @skip_not_impl(Sequence, "merge")
    def test_e(self):
        "'merge' - Test"
        lst = [Card(9, "hearts"), Card(8, "hearts"), Card(7, "hearts"), Card(6, "hearts")]
        seq1 = Sequence(lst[:2])
        seq2 = Sequence(lst[2:])

        seq1.merge(seq2)
        self.assertEqual(seq1._cards, lst)
        
        # test inconsistent merge (wrong value)
        seq3 = Sequence([Card(3, "hearts"), Card(2, "hearts")])
        seq2.merge(seq3)
        self.assertEqual(seq2._cards, lst[2:])
        
        # test inconsistent merge (wrong suit)
        seq3 = Sequence([Card(5, "spades"), Card(4, "spades")])
        seq2.merge(seq3)
        self.assertEqual(seq2._cards, lst[2:])
    
    @skip_not_impl(Sequence, "split")
    def test_f(self):
        "'split' - Test"
        for i in range(2, 14):
            lst = [Card(13 - j, "hearts" if i%2 == 0 else "spades") for j in range(i)]

            for s_index in range(1, i):
                seq = Sequence(list(lst))
                seq2 = seq.split(s_index)
                self.assertIsInstance(seq2, Sequence, msg="Der Rueckgabewert von 'sequence.split' soll eine neues 'Sequence'-Objekt sein.")
                self.assertEqual(seq2._cards, lst[s_index:], msg="Die Karten der abgetrennten Sequenz soll alle Karten ab dem übergebenen Index beinhalten.")
                self.assertEqual(seq._cards, lst[:s_index], msg="Die Sequenz selbst soll nach 'split' nur noch den vorderen Teil der Karten beinhalten.")
        
        # split at index 0
        lst = [Card(9, "hearts"), Card(8, "hearts"), Card(7, "hearts"), Card(6, "hearts")]
        seq = Sequence(list(lst))
        seq2 = seq.split(0)
        self.assertIsNone(seq2, msg="Der Rueckgabewert von 'sequence.split' soll 'None' sein, wenn der split-Index 0 ist.")
        self.assertEqual(seq._cards, lst, msg="Die Sequenz selbst soll bei 'split' mit index 0 nicht verändert werden.")
        
        # split index out of range
        lst = [Card(9, "hearts"), Card(8, "hearts"), Card(7, "hearts"), Card(6, "hearts")]
        seq = Sequence(list(lst))
        seq2 = seq.split(len(lst) + 3)
        self.assertIsNone(seq2, msg="Der Rueckgabewert von 'sequence.split' soll 'None' sein, wenn der split-Index ungültig ist.")
        self.assertEqual(seq._cards, lst, msg="Die Sequenz selbst soll bei 'split' mit ungültigem Index nicht verändert werden.")


class StackTests(unittest.TestCase):
    @skip_not_impl(Stack, "__init__")
    def test_a(self):
        "'Konstruktor' - Test"
        card = Card(1, "hearts")
        down = [Card(v, "spades") for v in range(2, 5)]
        stack = Stack(card, list(down))
        
        self.assertIsInstance(stack._sequences, list, msg="'stack._sequences' soll eine Liste sein.")
        self.assertEqual(len(stack._sequences), 1, msg="'stack._sequences' sollte nach dem Konstruktor ein 'Sequence'-Objekt beinhalten.")
        self.assertIsInstance(stack._sequences[0], Sequence, msg="'stack._sequences' sollte nach dem Konstruktor ein 'Sequence'-Objekt beinhalten.")
        self.assertEqual(len(stack._sequences[0]._cards), 1, msg="Die Sequenz soll nur die uebergebene Karte beinhalten.")
        self.assertEqual(stack._sequences[0].first_card(), card)
        self.assertEqual(stack._face_down_cards, down)
        
    @skip_not_impl(Stack, "last_sequence")
    def test_b(self):
        "'last_sequence' - Test"
        stack = Stack(Card(2, "spades"), [])
        
        seq = Sequence([Card(1, "hearts")])
        stack._sequences.append(seq)
        stack._sequences.insert(0, Sequence([Card(3, "hearts")]))
        
        self.assertEqual(stack.last_sequence(), seq, msg="'stack.last_sequence' soll die letzte Sequenz in 'stack._sequences' zurueckgeben.")
        
        # inconsistency test (empty stack)
        stack._sequences.clear()
        self.assertEqual(stack.last_sequence(), None, msg="Der Rueckgabewert von 'stack.last_sequence' soll 'None' sein, wenn der stack leer ist.")
        
    @skip_not_impl(Stack, "append_sequence")
    def test_c(self):
        "'append_sequence' - Test"
        stack = Stack(Card(2, "hearts"), [])
        seq2 = Sequence([Card(1, "spades")])
        
        seq1 = stack.last_sequence()
        stack.append_sequence(seq2)

        self.assertEqual(stack._sequences, [seq1, seq2], msg="Die uebergebene Sequenz soll an 'stack._sequences' angehaengt werden.")

    @skip_not_impl(Stack, "remove_last_sequence")
    def test_d(self):
        "'remove_last_sequence' - Test"
        stack = Stack(Card(2, "hearts"), [])
        lst = list(stack._sequences)
        stack.append_sequence(Sequence([Card(1, "spades")]))

        stack.remove_last_sequence()
        self.assertEqual(stack._sequences, lst)
        
        stack.remove_last_sequence()
        self.assertEqual(stack._sequences, [])
        
        # inconsistency test (empty stack)
        stack.remove_last_sequence()
        self.assertEqual(stack._sequences, [], msg="Der Aufruf von 'stack.remove_last_sequence' bei leerem stack soll nichts bewirken.")
        
    @skip_not_impl(Stack, "test_fullsequence")
    def test_e(self):
        "'test_fullsequence' - Test"
        full = [Card(v, "hearts") for v in range(13, 0, -1)]
        down = [Card(v, "spades") for v in range(5, 0, -1)]
        
        # Case 1: The sequence is full
        stack = Stack(full[0], list(down))
        seq = stack.last_sequence()
        seq.merge(Sequence(full[1:]))
        
        seq.is_full, get_is_full_count = call_counter(seq.is_full)
        stack.test_revealcard, get_revealcard_count = call_counter(stack.test_revealcard)
        
        stack.test_fullsequence()
        
        self.assertNotIn(seq, stack._sequences, msg="Bei voller Sequenz soll die Sequenz aus 'stack._sequences' entfernt werden.")
        # check if Sequence.is_full was called
        self.assertEqual(get_is_full_count(), 1, msg="In 'stack.test_fullsequence' soll 'sequence.is_full' von der letzten Sequenz verwendet werden.")
        # check if Stack.test_revealcard was called
        self.assertEqual(get_revealcard_count(), 1, msg="Wenn eine volle Sequenz in 'stack.test_fullsequence' entfernt wurde soll 'Stack.test_revealcard' aufgerufen werden.")
        
        # Case 2: The sequence is not full
        stack = Stack(full[0], list(down))
        seq = stack.last_sequence()
        
        seq.is_full, get_is_full_count = call_counter(seq.is_full)
        stack.test_revealcard, get_revealcard_count = call_counter(stack.test_revealcard)
        
        stack.test_fullsequence()
        
        self.assertIn(seq, stack._sequences, msg="Bei nicht-voller Sequenz soll der Stapel unverändert bleiben.")
        # check if Sequence.is_full was called
        self.assertEqual(get_is_full_count(), 1, msg="In 'stack.test_fullsequence' soll 'sequence.is_full' von der letzten Sequenz          verwendet werden.")
        
    @skip_not_impl(Stack, "deal_card")
    def test_f(self):
        "'deal_card' - Test"
        card = Card(10, "hearts")
        
        # Case 1: Card fits to the last sequence
        stack = Stack(card, [])
        card1 = Card(9, "hearts")

        stack.test_fullsequence, get_fullsequence_count = call_counter(stack.test_fullsequence)
        stack.deal_card(card1)
        
        self.assertEqual(len(stack._sequences), 1, msg="Bei passender Karte soll der Stapel immer noch nur 1 Sequenz beinhalten (merge).")
        self.assertEqual(stack.last_sequence()._cards, [card, card1], msg="Bei passender Karte soll die letzte Sequenz zusätzlich die ausgeteilte Karte beinhalten.")
        self.assertEqual(get_fullsequence_count(), 1, msg="Bei passender Karte soll 'stack.test_fullsequence' aufgerufen werden.")
        
        # Case 2: Card doesn't fit to the last sequence
        stack = Stack(card, [])
        card1 = Card(9, "spades")

        stack.test_fullsequence, get_fullsequence_count = call_counter(stack.test_fullsequence)
        stack.deal_card(card1)

        self.assertEqual(len(stack._sequences), 2, msg="Bei nicht-passender Karte soll der Stapel aus 2 Sequenzen bestehen (append_sequence).")
        self.assertEqual(stack._sequences[0]._cards, [card], msg="Bei nicht-passender Karte soll die ursprüngliche letzte Sequenz nicht verändert werden.")
        self.assertEqual(stack.last_sequence()._cards, [card1], msg="Bei nicht-passender Karte soll die letzte Sequenz (nur) die ausgeteilte Karte beinhalten.")
        self.assertEqual(get_fullsequence_count(), 0, msg="Bei nicht-passender Karte muss 'stack.test_fullsequence' nicht aufgerufen werden.")


class SSTests(unittest.TestCase):
    @skip_not_impl(SpiderSolitaire, "deal")
    def test_a(self):
        "'deal' - Test"
        ss = SpiderSolitaire()
        
        get_dealcard_counts = []

        for stack in ss._stacks:
            stack.deal_card, get_dealcard_count = call_counter(stack.deal_card)
            get_dealcard_counts.append(get_dealcard_count)
        
        ss.deal()

        # Case 1: We can deal the cards
        self.assertEqual(len(ss._stack2deal), 40, msg="Es müssen insgesamt 10 Karten verteilt werden")
        self.assertEqual([f() for f in get_dealcard_counts], [1] * len(ss._stacks), msg="Auf jedem Stapel soll genau 1 Mal 'deal_card' aufgerufen werden")
        
        # Case 2: There is an empty stack
        ss._stacks[5]._sequences.clear()
        ss.deal()
        
        self.assertEqual(len(ss._stack2deal), 40, msg="Wenn es einen leeren Stapel gibt, darf nicht ausgeteilt werden.")
        
        # Case 3: no Cards to deal
        ss._stack2deal.clear()
        ss._stacks[5].append_sequence(Sequence([Card(5, "hearts")]))
        ss.deal()
        # no need for assert since Exceptions would raise anyways
    
    def test_b(self):
        "'abort_move' - Test"
        ss = SpiderSolitaire()
        
        # moving_sequence is None
        ss.abort_move()
        self.assertEqual(ss.moving_sequence, None)
        self.assertEqual(ss.origin_stack_index, None)


        lst = [Card(7, "hearts"), Card(6, "hearts"), Card(5, "hearts")]
        
        # moving_sequence fits to origin stack -> merge
        card = Card(8, "hearts")
        seq = Sequence([card])
        ss._stacks[0]._sequences = [seq]
        ss.moving_sequence = Sequence(list(lst))
        ss.origin_stack_index = 0
        ss.abort_move()
        
        self.assertEqual(len(ss._stacks[0]._sequences), 1, msg="Bei passender 'moving_sequence' soll diese mit der letzten Sequenz gemerged werden")
        self.assertEqual(ss._stacks[0]._sequences[0], seq, msg="Bei passender 'moving_sequence' soll diese mit der letzten Sequenz gemerged werden")
        self.assertEqual(ss._stacks[0]._sequences[0]._cards, [card]+lst, msg="Bei passender 'moving_sequence' soll diese mit der letzten Sequenz gemerged werden")
        # containers should be reset
        self.assertEqual(ss.moving_sequence, None)
        self.assertEqual(ss.origin_stack_index, None)

        # moving_sequence doesn't fit to origin stack -> append_sequence
        ss._stacks[0]._sequences = [Sequence([Card(3, "hearts")])]
        moving = Sequence(list(lst))
        ss.moving_sequence = moving
        ss.origin_stack_index = 0
        ss.abort_move()
        
        self.assertEqual(len(ss._stacks[0]._sequences), 2, msg="Bei nicht-passender 'moving_sequence' soll diese dem Stapel angehängt werden")
        self.assertEqual(ss._stacks[0]._sequences[-1], moving, msg="Bei nicht-passender 'moving_sequence' soll diese dem Stapel angehängt werden")
        self.assertEqual(ss._stacks[0]._sequences[-1]._cards, lst, msg="Die angehängte Sequenz soll nicht verändert werden")
        # containers should be reset
        self.assertEqual(ss.moving_sequence, None)
        self.assertEqual(ss.origin_stack_index, None)
    
    def test_c(self):
        "'move' - Test"
        ss = SpiderSolitaire()
        lst = [Card(7, "hearts"), Card(6, "hearts"), Card(5, "hearts")]
        ss._stacks[0].test_revealcard, get_revealcard_count = call_counter(ss._stacks[0].test_revealcard)
        
        # Case 1 - target stack is empty
        ss._stacks[2]._sequences.clear()
        moving = Sequence(list(lst))
        ss.moving_sequence = moving
        ss.origin_stack_index = 0
        ss.move(2)

        self.assertEqual(len(ss._stacks[2]._sequences), 1, msg="Bei leerem Zielstapel soll 'moving_sequence' angehängt werden.")
        self.assertEqual(ss._stacks[2]._sequences, [moving], msg="Bei leerem Zielstapel soll 'moving_sequence' angehängt werden.")
        self.assertEqual(ss._stacks[2]._sequences[0]._cards, lst, msg="Die angehängte Sequenz soll nicht verändert werden.")
        self.assertEqual(get_revealcard_count(), 1, msg="Auf dem Ursprungsstapel soll 'test_revealcard' aufgerufen werden.")

        # Case 2 - moving_sequence fits in value, but not in suit
        ss._stacks[2]._sequences = [Sequence([Card(8, "spades")])]
        moving = Sequence(list(lst))
        ss.moving_sequence = moving
        ss.origin_stack_index = 0
        ss.move(2)

        self.assertEqual(len(ss._stacks[2]._sequences), 2, msg="Passt 'moving_sequence' nur nicht in der Farbe, soll diese an den Stapel angehängt werden.")
        self.assertEqual(ss._stacks[2]._sequences[-1], moving, msg="Passt 'moving_sequence' nur nicht in der Farbe, soll diese unverändert an den Stapel angehängt werden.")
        self.assertEqual(get_revealcard_count(), 2, msg="Auf dem Ursprungsstapel soll 'test_revealcard' aufgerufen werden.")
        
        # Case 3 - moving_sequence fits
        card = Card(8, "hearts")
        seq = Sequence([card])
        ss._stacks[2]._sequences = [seq]
        ss.moving_sequence = Sequence(list(lst))
        ss.origin_stack_index = 0
        ss._stacks[2].test_fullsequence, get_fullsequence_count = call_counter(ss._stacks[2].test_fullsequence)
        ss.move(2)
        
        self.assertEqual(len(ss._stacks[2]._sequences), 1, msg="Bei passender 'moving_sequence' soll diese mit der letzten Sequenz gemerged werden.")
        self.assertEqual(ss._stacks[2]._sequences[0], seq, msg="Bei passender 'moving_sequence' soll diese mit der letzten Sequenz gemerged werden.")
        self.assertEqual(ss._stacks[2]._sequences[0]._cards, [card]+lst, msg="Bei passender 'moving_sequence' soll diese mit der letzten Sequenz gemerged werden")
        self.assertEqual(get_revealcard_count(), 3, msg="Auf dem Ursprungsstapel soll 'test_revealcard' aufgerufen werden.")
        self.assertEqual(get_fullsequence_count(), 1, msg="Auf dem Zielstapel soll 'test_fullsequence' aufgerufen werden.")
        
        # Case 4 - moving_sequence doesn't fit
        ss._stacks[2]._sequences = [Sequence([Card(3, "spades")])]
        ss.moving_sequence = Sequence(list(lst))
        ss.origin_stack_index = 0
        ss.abort_move, get_abort_count = call_counter(ss.abort_move)
        ss.move(2)
        
        self.assertEqual(get_abort_count(), 1, msg="Bei nicht passender 'moving_sequence' soll 'abort_move' aufgerufen werden.")


class Result(unittest.TextTestResult):
    def getDescription(self, test):
        doc_first_line = test.shortDescription()
        if self.descriptions and doc_first_line:
            return doc_first_line
        else:
            return str(test)

    def addSkip(self, test, reason):
        unittest.TestResult.addSkip(self, test, reason)
        if self.showAll:
            self.stream.writeln("skipped ({})".format(reason))
        elif self.dots:
            self.stream.write("s")
            self.stream.flush()
    
    def wasSuccessful(self):
        return len(self.failures) == len(self.errors) == len(self.skipped) == 0


_failed = False
def run_test(test, msg):
    global _failed
    if _failed:
        return

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(test)
    l = len(msg) + 8
    line = "+" + "-" * l + "+"
    print(line + "\n|    " + msg + "    |\n" + line)
    res = unittest.TextTestRunner(verbosity=2, failfast=True, resultclass=Result).run(suite)
    if not res.wasSuccessful():
        _failed = True


if __name__ == "__main__":
    #overwrite "repr" Function
    Card.__repr__ = Card.__str__
    Sequence.__repr__ = Sequence.__str__
    Stack.__repr__ = Stack.__str__

    run_test(SequenceTests, "Testing class 'Sequence'")
    
    print()
    run_test(StackTests, "Testing class 'Stack'")
    
    print()
    run_test(SSTests, "Testing class 'SpiderSolitaire'")
