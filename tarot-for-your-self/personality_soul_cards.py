"""
Personality and Soul Cards

According to Mary K. Greer, you can calculate which tarot cards dominate your
life, based on the numerology of your birthday.

First, calculate the sum of the month, day, and year of your birthdate.

To calculate your personality card:

* If the sum of your birthdate is less than 22, that is your personality card.
* If the sum is greater than 22, add the digits again to get your personality card.

To calculate your soul card, take the sum of your personality card:

* If the number is less than 10, your personality and soul cards are the same.
* If the number is greater than 10, add the digits to get your soul card.

If sum of your birthdate (or personality card reduction) is 19, then you have
three cards that act as your both your personality and soul cards:

* 19
* 10 (1 + 9)
* 1 (1 + 0)

The purpose of this script is twofold:

1. Given a birthdate, find the personality and soul cards.
2. Are there any cards that are more likely to be a personality/soul card?
   * For the century from 1900-1999?
   * For the century from 2000-2999?

NOTE: Some tarot decks swap 'Justice' and 'Strength'.
"""

from datetime import datetime, timedelta

MAJOR_ARCANA = {
    0: 'The Fool',
    1: 'The Magician',
    2: 'The High Priestess',
    3: 'The Empress',
    4: 'The Emperor',
    5: 'The Hierophant',
    6: 'The Lovers',
    7: 'The Chariot',
    8: 'Strength',
    9: 'The Hermit',
    10: 'The Wheel of Fortune',
    11: 'Justice',
    12: 'The Hangman',
    13: 'Death',
    14: 'Temperance',
    15: 'The Devil',
    16: 'The Tower',
    17: 'The Star',
    18: 'The Moon',
    19: 'The Sun',
    20: 'Judgment',
    21: 'The World',
}


def display_name(card):
    return MAJOR_ARCANA[card]


def display_names(cards):
    return [display_name(card) for card in cards]


def get_personality_and_soul_cards(birthdate):
    def sum_digits(num):
        return sum(int(char) for char in str(num))

    def birthdate_sum(birthdate):
        return sum_digits(birthdate.day + birthdate.month + birthdate.year)

    def reduce_to(max_value, birthdate_sum):
        if birthdate_sum > max_value:
            return sum_digits(birthdate_sum)
        return birthdate_sum

    def personality_card_numbers(birthdate):
        base_number = reduce_to(22, birthdate_sum(birthdate))
        if base_number == 19:
            return set([19, 10, 1])
        return set([base_number])

    def soul_card_numbers(birthdate):
        base_numbers = personality_card_numbers(birthdate)
        if len(base_numbers) > 1:
            return base_numbers
        return set([reduce_to(9, num) for num in base_numbers])

    return (personality_card_numbers(birthdate),
            soul_card_numbers(birthdate))


def personality_and_soul_cards_by_popularity(start_date, end_date):
    tallies = {
        'p': {},
        's': {},
    }

    pntr_date = start_date
    while pntr_date < end_date:
        pcards, scards = get_personality_and_soul_cards(pntr_date)
        for cardset, cardtype in ((pcards, 'p'), (scards, 's')):
            for card in cardset:
                tallies[cardtype][card] = tallies[cardtype].get(card, 0) + 1
        pntr_date = pntr_date + timedelta(days=1)

    key = lambda tally: -tally[1]
    return (sorted(tallies['p'].items(), key=key),
            sorted(tallies['s'].items(), key=key))

if __name__ == '__main__':
    divider = '-----'
    print(divider)

    pcards, scards = get_personality_and_soul_cards(datetime.now())
    print(f'Soul cards for today: {display_names(pcards)}')
    print(f'Personality cards for today: {display_names(scards)}')

    print(divider)

    def print_top_three(pops, display_word, display_century):
        print(f'Top 3 {display_word} cards for the {display_century} century:')
        for i in range(3):
            card = pops[i][0]
            print(f'{i+1}. {display_name(card)}')

    ppop20, spop20 = personality_and_soul_cards_by_popularity(
        datetime(day=1, month=1, year=1900),
        datetime(day=31, month=12, year=1999),
    )
    print_top_three(ppop20, 'personality', '20th')
    print('')
    print_top_three(spop20, 'soul', '20th')

    print(divider)

    ppop21, spop21 = personality_and_soul_cards_by_popularity(
        datetime(day=1, month=1, year=2000),
        datetime(day=31, month=12, year=2199),
    )
    print_top_three(ppop21, 'personality', '21st')
    print('')
    print_top_three(spop21, 'soul', '21st')

    print(divider)
