from rich import print

from bookiemath import Bookmaker, reprice_from_liabilities

if __name__ == "__main__":

    OUTCOME_1 = "horse 1 wins"
    OUTCOME_2 = "horse 2 wins"
    OUTCOME_3 = "horse 3 wins"

    book = Bookmaker([OUTCOME_1, OUTCOME_2, OUTCOME_3])

    # Set current odds for the market
    book.set_odds(OUTCOME_1, 2.30)
    book.set_odds(OUTCOME_2, 3.20)
    book.set_odds(OUTCOME_3, 3.10)

    book.show_odds_and_overround()
    

    # Add some bets
    book.add_bet(OUTCOME_1, 50)
    book.add_bet(OUTCOME_2, 31)
    book.add_bet(OUTCOME_3, 32)

    # Let's see what our liability now looks like
    
    book.book_of_bets()
    book.summarise_risk_position()

    # Reprice by hand
    
    book.set_odds(OUTCOME_1, 1/0.51)
    book.set_odds(OUTCOME_2, 1/0.26)
    book.set_odds(OUTCOME_3, 1/0.26)

    book.show_odds_and_overround()

    # Some more bets come in

    
    book.add_bet(OUTCOME_1, 5)
    book.add_bet(OUTCOME_2, 10)
    book.add_bet(OUTCOME_3, 10)
    book.add_bet(OUTCOME_3, 10)
    

    book.book_of_bets()
    book.summarise_risk_position()
    
    
    print('Suggested repricing given current liabilities')
    print(reprice_from_liabilities(book.liabilities))
    

    
