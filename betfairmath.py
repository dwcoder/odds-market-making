"""
Class to include math to see things from _the bookmaker's perspective_.

This is slightly different from viewing things on the Betfair exchange.
"""

from rich import print

from collections import defaultdict
import pandas as pd
from datetime import datetime



class BetfairMarket:
    def __init__(self):
        super().__init__()
        self.market_back_odds = {}
        self.market_lay_odds = {}

    def set_market_odds(self, back_odds=None, lay_odds=None):
        """
        back_odds: dict like {"Home": 2.5, "Draw": 3.2, "Away": 4.1}
        lay_odds: dict like {"Home": 2.6, "Draw": 3.3, "Away": 4.2}
        """
        if back_odds:
            self.market_back_odds = back_odds
        if lay_odds:
            self.market_lay_odds = lay_odds

    def show_market_prices(self, fractional=False):
        outcomes = sorted(set(self.market_back_odds) | set(self.market_lay_odds))

        data = [
            {
                "Outcome": outcome,
                "Back Odds": f"{self.market_back_odds[outcome]:0.2f}({1/self.market_back_odds[outcome]:4.3f})" ,
                "Lay Odds": f"{self.market_lay_odds[outcome]:0.2f}({1/self.market_lay_odds[outcome]:4.3f})" ,
            }
            for outcome in outcomes
        ]

        if fractional:
            for dd in data:
                outcome = dd["Outcome"]
                dd["Lay Fractional"] = self._decimal_to_fraction(
                    self.market_lay_odds[outcome]) if outcome in self.market_lay_odds else None
                dd["Back Fractional"] = self._decimal_to_fraction(
                    self.market_lay_odds[outcome]) if outcome in self.market_back_odds else None

        return pd.DataFrame(data)

    @staticmethod
    def _decimal_to_fraction(dec_odds):
        from math import gcd
        numer = round((dec_odds - 1) * 100)
        denom = 100
        d = gcd(numer, denom)
        return f"{numer // d}/{denom // d}"

class BetfairPunterBook():
    def __init__(self, market : BetfairMarket):
        self.bets = []
        self.market = market

    def add_bet(self, outcome, stake, bet_type, timestamp=None):
        assert bet_type in {"back", "lay"}, "bet_type must be 'back' or 'lay'"

        back_odds = market.market_back_odds.get(outcome)
        lay_odds = market.market_lay_odds.get(outcome)
        odds = back_odds if bet_type == "back" else lay_odds

        self.bets.append({
            "timestamp": timestamp or datetime.now(),
            "outcome": outcome,
            "odds": odds,
            "stake": stake,
            "type": bet_type
        })

    # Wrapper for back bet
    def add_bet_back(self, outcome, stake):
        self.add_bet(outcome, stake, "back")

    # Wrapper for lay bet
    def add_bet_lay(self, outcome, stake):
        self.add_bet(outcome, stake, "lay")


    def compute_position(self):
        outcomes = set(bet["outcome"] for bet in self.bets)
        position = {outcome: 0.0 for outcome in outcomes}

        for outcome in outcomes:
            for bet in self.bets:
                stake = bet["stake"]
                odds = bet["odds"]
                if bet["type"] == "back":
                    if bet["outcome"] == outcome:
                        position[outcome] += (odds - 1) * stake
                    else:
                        position[outcome] -= stake
                elif bet["type"] == "lay":
                    if bet["outcome"] == outcome:
                        position[outcome] -= (odds - 1) * stake
                    else:
                        position[outcome] += stake
        return position

    def show_table(self):
        position = self.compute_position()
        df_bets = pd.DataFrame(self.bets).sort_values("timestamp")
        df_summary = pd.DataFrame({
            "Outcome": list(position.keys()),
            "Net P&L": list(position.values())
        }).sort_values("Outcome")
        return df_bets, df_summary


if __name__ == "__main__":

    market = BetfairMarket()

    # Set current market odds
    market.set_market_odds(
        back_odds={"Kamala": 1.68, "Biden": 5.4},
        lay_odds = {"Kamala": 1.69, "Biden": 5.5}
    )

    print(market.show_market_prices().to_markdown(index=False))

    book = BetfairPunterBook(market)

    book.add_bet_back('Kamala', 59.52)
    book.add_bet_back('Biden', 18.52)

    df_bets, df_summary = book.show_table()
    print(df_bets.to_markdown(index=False))
    print(df_summary.to_markdown(index=False))

    book2 = BetfairPunterBook(market)

    book2.add_bet_lay('Biden', 0)
    book2.add_bet_lay('Kamala', 1)

    df_bets, df_summary = book2.show_table()
    print(df_bets.to_markdown(index=False))
    print(df_summary.to_markdown(index=False))

