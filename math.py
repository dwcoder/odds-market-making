class Bookmaker:
    def __init__(self, outcomes: list[str]):
        self.outcomes = outcomes
        self.bets: dict[str, list[tuple[int, float]]] = {outcome: [] for outcome in self.outcomes}
        self.current_odds: dict[str, float | None] = {outcome: None for outcome in self.outcomes}

    def set_odds(self, outcome, odds):
        assert outcome in self.outcomes, f"Invalid outcome: {outcome}"
        self.current_odds[outcome] = odds

    def add_bet(self, outcome, stake, odds=None):
        assert outcome in self.outcomes, f"Invalid outcome: {outcome}"
        if odds is None:
            odds = self.current_odds[outcome]
            assert odds is not None, "No odds set for this outcome"
        self.bets[outcome].append((stake, odds))

    def book_of_bets(self):
        print("Book of bets (our exposure):")
        print(f"{'Outcome':<6} {'Stake':>8} {'Odds':>8} {'Payout':>10}")
        for outcome in self.outcomes:
            for stake, odds in self.bets[outcome]:
                payout = stake * odds
                print(f"{outcome:<6} {stake:>8.2f} {odds:>8.2f} {payout:>10.2f}")
        print()

    @property
    def liabilities(self):
        return {outcome: sum(stake * odds for stake, odds in self.bets[outcome]) for outcome in self.outcomes}

    def summarise_risk_position(self):
        total_taken = sum(stake for bets in self.bets.values() for stake, _ in bets)
        print(f"Total money taken: £{total_taken:.2f}\n")
        for outcome in self.outcomes:
            payout = sum(stake * odds for stake, odds in self.bets[outcome])
            profit = total_taken - payout
            print(f"If '{outcome.upper()}' happens:")
            print(f"  Total payout: £{payout:.2f}")
            print(f"  Bookmaker profit: £{profit:.2f}\n")

    def show_odds_and_overround(self):
        print("Current Odds & Implied Probabilities:")
        total_implied = 0
        for outcome in self.outcomes:
            odds = self.current_odds[outcome]
            if odds:
                implied = 1 / odds
                total_implied += implied
                print(f"{outcome:<6}: Odds = {odds:.2f}, Implied = {implied * 100:.2f}%")
            else:
                print(f"{outcome:<6}: Odds = N/A")

        print(f"\nTotal Implied Probability: {total_implied * 100:.2f}%")
        overround = total_implied - 1
        print(f"Overround: {overround * 100:.2f}%\n")


# Here is a naive way to reprice the book from the current liabilities

def reprice_from_liabilities(liabilities: dict[str, float], overround=1.07):
    total = sum(liabilities.values())
    new_odds = {}
    for outcome, liability in liabilities.items():
        share = liability / total
        implied_prob = share * overround
        new_odds[outcome] = round(1 / implied_prob, 2)
    return new_odds

