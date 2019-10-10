# LambdaLottery
A basic lottery number scraper for MA, intended usage was for AWS lambda to be used along with Amazon Lex.

# Usage
currently written for Python 2.7, but with some minor changes should work flawlessly on 3.x

simply run the following
```python
pip install -r requirements.txt 
```

# Example Usage
```python
# input
print(get_winning_numbers("Mass cash"))

# output
Mass Cash
The Winning Numbers for Wed, Oct 09, 2019 are 3, 4, 7, 13, 27! Jackpot: $100,000
```
