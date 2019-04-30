#  File: Combinations.py
#  A program that prints a table listing the number of possible hands of cards in a deck.

def factorial(num):
    factorial = 1
    while num >= 1:
        factorial *= num
        num -= 1

    return factorial


def combinations(n, r):

    # n C r = (n! / ( r!(n-r)! )
    # n = int,  number of cards in deck (always 52)
    # r = int, number of cards to draw from the deck to create a hand (0 to 52)
    # combinations = number of combinations of r cards that can be dealt from a deck of n cards

    numerator = factorial(n)
    denominator = factorial(r) * factorial(n-r)

    combinations = numerator // denominator

    return combinations

def main():

    print()
    print("Cards", format("Combinations", ">16s"))
    print("======================")

    # cards r (0 - 52)     combinations(52, r)
    for r in range(0,53):
        print(format(r, ">3d"), format(combinations(52, r), ">18d"))

    print()

main()
