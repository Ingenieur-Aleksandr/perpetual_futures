# Perpetual Futures
Project provides an instrument for using perpetual futures trade strategy (connected with funding rates)

## Main Idea
Perpetual futures could be best described as derivatives, which in comparison with classic futures have no expiration. To make their behaviour similar to classic futures funding rates are used to provide fee, which is paid by one side of the market to another.\
For example, if the market is bull then traders more tend to buy perpetual futures, so their price increases. In this case an exchange (or smart-contract in case of DEX) takes parts of long positions according to current funding rate and pays them proportionally to traders in short-positions. More price grows then funding rates become more and more, so traders with long positions tend to close them, so the market goes to the opposite direction.
This instrument provides an opportunity for unique trade strategies. One of them realized in this repository.
