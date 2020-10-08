# Golf
Command-line tool for playing the card game "Golf" against other players or AI

The goal of the game is to score the lowest number possible. jacks and queens are worth 10, aces are worth 1, jokers are worth -2, kings are worth 0, and all other cards are worth their normal value. Cards with matching values (i.e two queens, two threes, etc) in the same row regardless of suit are worth 0.

At the beginning of the game each player has 6 cards face down arranged in two columns and three rows. A player can either pick up a card from the deck or use the card that the player prior to them discarded, and use that card to replace any card of their six, whether the card be face down or face up. When the player replaces a card the new card is placed face up. When all of a players cards are face up they are said to be "out" and all the remaining players have one turn left to replace a card. Nine rounds, or "holes", are played and the player with the least points at the end of these rounds is the winner.

The AI is assumed to have perfect card-counting ability and makes their moves based on probability and the state of other players hands (ex, it ill make more risky moves if another player has gone out since it only has one more turn).

Start the game by navigating to the folder the game is in and running the following command: python3 golf.py

Golf rules: https://bicyclecards.com/how-to-play/six-card-golf/ (this site assigns slightly different point values for cards (point values for this tool are outlined above) but the rest is the same.
