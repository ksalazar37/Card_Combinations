# A game of Blackjack

# for shuffling deck
import random


class Card(object):
    RANKS = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13)

    SUITS = ('C', 'D', 'H', 'S')

    # constructor
    def __init__(self, rank=12, suit='S'):
        if (rank in Card.RANKS):
            self.rank = rank
        else:
            self.rank = 12

        if (suit in Card.SUITS):
            self.suit = suit
        else:
            self.suit = 'S'

    # string representation of card object
    def __str__(self):
        if (self.rank == 1):
            rank = 'A'
        elif (self.rank == 13):
            rank = 'K'
        elif (self.rank == 12):
            rank = 'Q'
        elif (self.rank == 11):
            rank = 'J'
        else:
            rank = str(self.rank)
        return rank + self.suit

    #overriding equality operators
    def __eq__(self, other):
        return (self.rank == other.rank)

    def __ne__(self, other):
        return (self.rank != other.rank)

    def __lt__(self, other):
        return (self.rank < other.rank)

    def __le__(self, other):
        return (self.rank <= other.rank)

    def __gt__(self, other):
        return (self.rank > other.rank)

    def __ge__(self, other):
        return (self.rank >= other.rank)


class Deck(object):
    #constructor, default number of decks = 1
    def __init__(self, num_decks = 1):
        self.deck = []

        for d in range (num_decks):
            for suit in Card.SUITS:
                for rank in Card.RANKS:
                    card = Card(rank, suit)
                    self.deck.append(card)

    # shuffle deck
    def shuffle(self):
        random.shuffle(self.deck)

    # deal
    def deal(self):
        if (len(self.deck) == 0):
            return None
        else:
            return self.deck.pop(0)


class Player(object):
    # cards = list of Card objects
    def __init__(self, cards):
        self.cards = cards
        self.bust = False

    # when a player hits append another card
    def hit(self, card):
        self.cards.append(card)

    # get string of the player's cards
    def get_cards(self):
        hand_str = ''
        for card in self.cards:
            hand_str += str(card) + ' '

        return hand_str

    # get point total of the player's cards
    def get_points(self):
        count = 0
        for card in self.cards:
            if card.rank > 9:
                count += 10
            elif card.rank == 1:
                count += 11
            else:
                count += card.rank

        # deduct 10 if Ace is there and and needed as 1
        for card in self.cards:
            if count <= 21:
                break
            elif card.rank == 1:
                count = count - 10

        return count

    # when player goes over 21
    def busted(self):
        self.bust = True


    # def has_blackjack (Self):
        return(len(self.cards) == 2) and (self.get_points() == 21)



# Dealer class that inherits from Player class
#  but plays by some different rules
class Dealer(Player):
    def __init__(self, cards):
        Player.__init__(self, cards)
        #or
        # super(Dealer, self).__init__(cards)

        self.show_one_card = True


    # return string of dealer's first - face up - card
    def get_first_card(self):
        if (self.show_one_card):
            return str(self.cards[0])
        else:
            return Player.__str__(self)

    # override hit () function in parent class
    # def hit(self, deck):
    #     self.show_one_card = False
    #     while (self.get_points() < 17):
    #         self.cards.append(deck.deal())



class Blackjack(object):
    def __init__(self, num_players=1):
        self.deck = Deck()  # create a deck and shuffle
        self.deck.shuffle()

        self.players = []
        self.num_players = num_players
        num_cards_in_hand = 2   # each player is originally dealt 2 cards

        for i in range(self.num_players):
            # deal hands
            hand = []
            for j in range(num_cards_in_hand):
                hand.append(self.deck.deal())
            self.players.append(Player(hand))

        # create the Dealer object with list of cards
        # Dealer gets 2 cards (one face up)
        dealer_hand = []
        for j in range(num_cards_in_hand):
            dealer_hand.append(self.deck.deal())
        self.dealer = (Dealer(dealer_hand))


    # play a game of Blackjack
    def play(self):
        print()
        # print each player's cards and points
        for i in range(len(self.players)):
            print('Player ' + str(i + 1) + ": " + self.players[i].get_cards() + "- " + str(
                self.players[i].get_points()) + " points")

        # print dealer's cards and points

        print('Dealer: ' + self.dealer.get_first_card())
        print()

        # let each player have a turn to hit (y) or stand (n) unless
        # they already have 21, then skip turn
        for i in range (len(self.players)):
            player = self.players[i]

            answer = 'y'
            while answer != 'n' and player.get_points() < 21:
                answer = (input("Player " + str(i + 1) + ", do you want to hit? [y / n]: "))
                if (answer == 'y'):
                    player.hit(self.deck.deal())
                    print('Player ' + str(i + 1) + ": " + self.players[i].get_cards() + "- " + str(self.players[i].get_points()) + " points")

            # if the player points >  21 points, he busts and stop asking
            if player.get_points() > 21:
                player.busted()

            print()

        # play dealer's hand and print dealer cards and points
        # dealer must hit if his point total is less than 17
        while (self.dealer.get_points() < 17):
            self.dealer.hit(self.deck.deal())

        print('Dealer: ' + self.dealer.get_cards() + "- " + str(self.dealer.get_points()) + " points")

        # if dealer busts while hitting
        if self.dealer.get_points() >= 21:
            self.dealer.busted()

        print()

        # create list of the players who remain standing
        standing = []
        for player in self.players:
            if not player.bust:
                standing.append(player)

        # determine who wins, loses, and ties by checking all points
        # if dealer busts, standing players all win but busted players lose
        if self.dealer.bust:
            for i, player in enumerate(self.players):
                if player in standing:
                    print('Player', str(i + 1), 'wins')
                else:
                    print('Player', str(i + 1), 'loses')
        # if dealer does not bust than players win by getting above their points
        # ties by getting equal to dealer points
        # and lose otherwise
        elif not self.dealer.bust:
            for i, player in enumerate(self.players):
                if player in standing:
                    if (player.get_points() > self.dealer.get_points()):
                        print('Player', str(i + 1), 'wins')
                    elif player.get_points() == self.dealer.get_points():
                        print('Player', str(i + 1), 'ties')
                    else:
                        print('Player', str(i + 1), 'loses')
                else:
                    # players who busted always lsoe
                    print('Player', str(i + 1), 'loses')
        print()

    # if player has natural blackjack, he got 21 with only 2 card
    def has_blackjack(self):
        return (len(self.cards) == 2) and (self.get_points() == 21)



def main():
    # prompt user to enter  number of players
    num_players = int(input('Enter number of players: '))

    while ((num_players < 1) or (num_players > 6)):
        num_players = int(input('Enter number of players: '))

    # create a blackjack game object with given number of players and dealer
    game = Blackjack(num_players)

    # initiate game play
    game.play()


main()
