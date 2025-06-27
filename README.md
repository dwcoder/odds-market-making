# Odds Manager

A simulation project to explore the way in which a bookmaker's
book of bets evolves over time, and how to reprice odds to ensure
a well-balanced book.

```python
OUTCOME_1 = "horse 1"
OUTCOME_2 = "horse 2"
OUTCOME_3 = "horse 3"

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
```

```
Current Odds & Implied Probabilities:
horse 1: Odds = 2.30, Implied = 43.48%
horse 2: Odds = 3.20, Implied = 31.25%
horse 3: Odds = 3.10, Implied = 32.26%

Total Implied Probability: 106.99%
Overround: 6.99%

Book of bets (our exposure):
Outcome    Stake     Odds     Payout
horse 1    50.00     2.30     115.00
horse 2    31.00     3.20      99.20
horse 3    32.00     3.10      99.20

Total money taken: £113.00

If 'HORSE 1 wins' happens:
  Total payout: £115.00
  Bookmaker profit: £-2.00

If 'HORSE 2 wins' happens:
  Total payout: £99.20
  Bookmaker profit: £13.80

If 'HORSE 3 wins' happens:
  Total payout: £99.20
  Bookmaker profit: £13.80
```