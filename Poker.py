# Poker.py

from random import shuffle

# function to turn a 1D list to 2D, separated by every n term
def two_dim (list, n):                                          
    return [list[i:i+n] for i in range(0, len(list), n)]


class Card (object):
    # define ranks and names of suits (no significant order, but alphabetical)
    RANKS = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)
    SUITS = ("C", "D", "H", "S")

    # constructor
    def __init__(self, rank = 12, suit = "S"):
        if (rank in Card.RANKS):
            self.rank = rank
        else:
            self.rank = 12

        if (suit in Card.SUITS):
            self.suit = suit
        else:
            self.suit = "S"

    # string representation of a Card object
    def __str__(self):
        if (self.rank == 14):
            rank = "A"
        elif (self.rank == 13):
            rank = "K"
        elif (self.rank == 12):
            rank = "Q"
        elif (self.rank == 11):
            rank = "J"
        else:
            rank = str(self.rank)

        return rank + self.suit


    # equality tests
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


# create Deck and the process to deal cards out
class Deck (object):
  # constructor to create deck of cards with rank and suit
  def __init__ (self, num_decks = 1):
    self.deck = []
    for i in range (num_decks):
      for suit in Card.SUITS:
        for rank in Card.RANKS:
          card = Card (rank, suit)
          self.deck.append (card)

  # shuffle the deck
  def shuffle (self):
    shuffle(self.deck)

  # deal a card
  def deal (self):
    if (len(self.deck) == 0):
      return None
    else:
        # return deck with first card removed
        return self.deck.pop(0)

# simulate play of Poker
class Poker (object):

    # create a deck
    def __init__(self, num_players=2, num_cards=5):
        self.deck = Deck()
        self.deck.shuffle()
        self.hands = []                     # list of player hands
        self.total_points = []              # list of total points in game
        self.numCards_in_hand = 5   # number of cards in hand, default 5

        # deal cards to players
        for i in range (num_players):
            hand = []
            for n in range (num_cards):
                hand.append(self.deck.deal())
            self.hands.append(hand)

    # simulate play of poker
    # sort hands of each of the players in descending order, and print
    def play(self):
        for i in range (len(self.hands)):
            # sort hand = hand
            hand = sorted(self.hands[i], reverse = True)
            # self.hands[i] = hand

            hand_str = ''
            for card in hand:
                hand_str = hand_str + str(card) + ' '

            print("Player " + str(i + 1) + ": " + hand_str)

    # DETERMINE IF HAND IS A CERTAIN TYPE AND RETURN POINTS OF HAND

    # (10) Determine if hand Royal Flush and return points >>  5 royal cards, all same suit
    def is_Royal (self, hand):
        hand_ = sorted(hand, reverse = True)
        royal = True

        current_suit = hand_[0].suit
        # sorted hand must begin with 14 (ace) to be a royal flush
        current_rank = 14

        same_suit = True
        for i in range(len(hand_) - 1):
            same_suit = same_suit and (hand_[i].suit == hand_[i + 1].suit)

        if (not same_suit):
            royal = False

        rank_order = True
        for i in range(len(hand_)):
            rank_order = rank_order and (hand_[i].rank == 14 - i)

        if (not rank_order):
            royal = False

        points = 10 * 15 ** 5 + (hand_[0].rank) * 15 ** 4 + (hand_[1].rank) * 15 ** 3
        points = points + (hand_[2].rank) * 15 ** 2 + (hand_[3].rank) * 15 ** 1
        points = points + (hand_[4].rank)

        if same_suit and rank_order:
            self.total_points.append(points)
            return points, 'Royal Flush'
        else:
            return self.is_Straight_Flush (hand_)


    # (9) Determine is hand is straight flush >>  5 cards in rank order (not all Royals), same suit
    def is_Straight_Flush (self, hand):
        hand_ = sorted(hand, reverse = True)

        straight_flush = True

        # start checking if cards are of same suit, and ordered rank
        current_suit = hand_[0].suit
        current_rank = hand_[0].rank

        points = 9 * 15 ** 5 + (hand_[0].rank) * 15 ** 4 + (hand_[1].rank) * 15 ** 3
        points = points + (hand_[2].rank) * 15 ** 2 + (hand_[3].rank) * 15 ** 1
        points = points + (hand_[4].rank)

        # iterate through each card in player hand
        for card in hand_:
            # if ever reach a card in which cards are not equal to first in suit and/or rank, not straight flush
            if card.suit!=current_suit or card.rank!=current_rank:
                straight_flush = False
                break
            # else, keep checking next ranks
            else:
                current_rank -= 1

        if straight_flush:
            self.total_points.append(points)
            return points, "Straight Flush"

        else:
            return self.is_four_kind(hand_)


    # (8) Determine if hand is 4 of a kind >> 4 cards have same numerical rank (suit is no matter)
    def is_four_kind (self, hand):
        hand_ = sorted(hand, reverse=True)
        four = False

        if (hand_[0].rank == hand_[1].rank) and (hand_[1].rank == hand_[2].rank) and (hand_[2].rank == hand_[3].rank):
            four =  True
        elif (hand_[1].rank == hand_[2].rank) and (hand_[2].rank == hand_[3].rank) and (hand_[3].rank == hand_[4].rank):
            four = True
        else:
            four = False

        if four == True:
            points = 8 * 15 ** 5 + (hand_[0].rank) * 15 ** 4 + (hand_[1].rank) * 15 ** 3
            points = points + (hand_[2].rank) * 15 ** 2 + (hand_[3].rank) * 15 ** 1
            points = points + (hand_[4].rank)

            self.total_points.append(points)
            return points, "Four of a Kind"
        else:
            return self.is_Full_House(hand_)


    # (7) determine if hand is Full House >> 2 cards of equal rank, 3 cards of separate equal rank
    def is_Full_House (self, hand):
        hand_ = sorted(hand, reverse=True)

        full = True

        points = 7 * 15 ** 5 + (hand_[0].rank) * 15 ** 4 + (hand_[1].rank) * 15 ** 3
        points = points + (hand_[2].rank) * 15 ** 2 + (hand_[3].rank) * 15 ** 1
        points = points + (hand_[4].rank)

        lst = []

        for card in hand_:
            lst.append(card.rank)

        # define where first and last ranks will be found (will always be first and last positions, no matter which order)
        rank1 = hand_[0].rank
        rank2 = hand_[-1].rank

        # number of occurances of rank1 and rank2
        n_rank1 = lst.count(rank1)
        n_rank2 = lst.count(rank2)


        if (n_rank1==2 and n_rank2==3) or (n_rank1==3 and n_rank2==2):
            full = True
            self.total_points.append(points)
            return points, "Full House"

        else:
            full = False
            return self.is_Flush(hand_)


    # (6) determine is hand is a Flush  - all of same suit, but not in rank order
    def is_Flush (self, hand):
        hand_ = sorted(hand, reverse=True)

        flush = True

        points = 6 * 15 ** 5 + (hand_[0].rank) * 15 ** 4 + (hand_[1].rank) * 15 ** 3
        points = points + (hand_[2].rank) * 15 ** 2 + (hand_[3].rank) * 15 ** 1
        points = points + (hand_[4].rank)

        #check if all of same suit, start with first and see if rest are the same
        current_suit = hand_[0].suit

        for card in hand_:
            if not (card.suit == current_suit):
                flush = False
                break

        if flush:
            self.total_points.append(points)
            return points, "Flush"

        else:
            return self.is_Straight(hand_)

    # (5) determine if hand is straight - all in rank order, but not of same suit
    def is_Straight (self, hand):
        hand_ = sorted (hand, reverse = True)

        straight = True

        points = 5 * 15 ** 5 + (hand_[0].rank) * 15 ** 4 + (hand_[1].rank) * 15 ** 3
        points = points + (hand_[2].rank) * 15 ** 2 + (hand_[3].rank) * 15 ** 1
        points = points + (hand_[4].rank)

        current_rank = hand_[0].rank

        for card in hand_:
            if card.rank != current_rank:
                straight = False
                break # stop checking
            else:
                current_rank -= 1

        if straight:
            self.total_points.append(points)
            return points, "Straight"

        else:
            return self.is_three_kind(hand_)


    # (4) determine is hand has three of a rank, other two are unrelated
    def is_three_kind (self, hand):
        hand_ = sorted(hand, reverse = True)

        type = True

        points = 4 * 15 ** 5 + (hand_[0].rank) * 15 ** 4 + (hand_[1].rank) * 15 ** 3
        points = points + (hand_[2].rank) * 15 ** 2 + (hand_[3].rank) * 15 ** 1
        points = points + (hand_[4].rank)

        current_rank = hand_[2].rank

        lst = []
        for card in hand_:
            lst.append(card.rank)

        if lst.count(current_rank) == 3:
            type = True
            self.total_points.append(points)
            return points, "Three of a Kind"
        else:
            type = False
            return self.is_two_pair(hand_)


    # (3) determine if hand has two pairs - 2 of equal rank and another 2 of different rank but equal to each other
    def is_two_pair(self, hand):
        hand_ = sorted(hand, reverse = True)

        rank1 = hand_[1].rank
        rank2 = hand_[2].rank

        points = 3 * 15 ** 5 + (hand_[0].rank) * 15 ** 4 + (hand_[1].rank) * 15 ** 3
        points = points + (hand_[2].rank) * 15 ** 2 + (hand_[3].rank) * 15 ** 1
        points = points + (hand_[4].rank)

        lst = []
        for card in hand_:
            lst.append(card.rank)
        if lst.count(rank1) == 2 and lst.count(rank2) == 2:
            self.total_points.append(points)
            return points, "Two Pair"

        else:
            return self.is_one_pair(hand_)


    # (2) determine if a hand is one pair - just 2 of the same rank (no more or less)
    def is_one_pair(self, hand):
        hand_ = sorted(hand, reverse=True)

        one_pair = True

        points = 2 * 15 ** 5 + (hand_[0].rank) * 15 ** 4 + (hand_[1].rank) * 15 ** 3
        points = points + (hand_[2].rank) * 15 ** 2 + (hand_[3].rank) * 15 ** 1
        points = points + (hand_[4].rank)

        lst  = []
        p_count =[]

        for card in hand_:
            lst.append(card.rank)

        for item in lst:
            count = lst.count(item)
            p_count.append(count)


        if p_count.count(2) == 2 and p_count.count(1) == 3:   # 2 same (1 pair), other different
            one_pair = True
            self.total_points.append(points)
            return points, "One Pair"

        else:
            one_pair = False
            return self.is_High(hand_)


    # (1) determine if none of the above and player simply has a high card
    def is_High (self, hand):
        hand_ = sorted(hand, reverse = True)

        high = True

        points = 1 * 15 ** 5 + (hand_[0].rank) * 15 ** 4 + (hand_[1].rank) * 15 ** 3
        points = points + (hand_[2].rank) * 15 ** 2 + (hand_[3].rank) * 15 ** 1
        points = points + (hand_[4].rank)

        lst = []
        for card in hand_:
            lst.append(card.rank)

        self.total_points.append(points)
        return points, "High Card"



def main():
    # prompt the user to enter the number of players
    num_players = int (input ('Enter number of players: '))
    while ((num_players < 2) or (num_players > 6)):
        num_players = int (input ('Enter number of players: '))

    # create the Poker object
    game = Poker (num_players)

    # play the game
    game.play()

    # return type of hand for each player
    print()
    points_list = []
    type_list = []
    all_list = []
    for i in range (num_players):
        current_hand = game.hands[i]
        print("Player " + str(i + 1) + ": ", end='' )
        player_list = game.is_Royal(current_hand)
        # only return type of hand, not points
        print (str(player_list[1]))
        # for use when determining the ties
        points_list.append(player_list[0])
        type_list.append(player_list[1])
        all_list.append(player_list)

    # determine winner
    max_point = max(game.total_points)
    max_point_player = game.total_points.index(max_point)

    print()
    print("Player " + str(max_point_player + 1) + " wins")
    print()

    # ties with winning hand type only

    tie_list = []
    winner_i = max_point_player
    winner_type = type_list[winner_i]

    for i in range(0, len(points_list)):
        # if type matches (and is not index of winner) it is a tie
        if (type_list[i] == winner_type) and (winner_i != i):
            tie_list.append(i)

    # print player ties in descending order of points in hand
    point_of_ties = []
    for i in range(len(tie_list)):
        point_of_ties.append(points_list [tie_list[i]] )

    tie_points_index = []
    for i in range(len(tie_list)):
        tie_points_index.append(point_of_ties[i])
        tie_points_index.append(tie_list[i])

    tie_points_ind = two_dim (tie_points_index, 2)

    # sort list based on first term (the points)
    tie_points_indexed = sorted(tie_points_ind, key=lambda l:l[0], reverse=True)

    for n in range(len(tie_points_indexed)):
        print("Player " + str(int(tie_points_indexed[n][1]) + 1 ) + " ties")

main()
