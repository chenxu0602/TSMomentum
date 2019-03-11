# TSMomentum
Time Series Momentum in Global Futures

# Strategy Setup
Multiple research articles (including the JP Morgan research) identified that the global commoditiy futures has mid to long 
term time series momentum.

The strategy is based on the futures momentum in 1, 3, 6, 12 and 24 months. 

Data source is Quandl's Reference futures contracts data at https://www.quandl.com/data/SRF-Reference-Futures/documentation

The products are chosen so that no single category would dominate:

ATW, SB, CL, PA, PL, GC, ES, NE, AD, CD, S, C, TU

The continuous futures chain is generated based on liquidity.

# Strategy Explanation
1. Calculate the 1, 3, 6, 12 and 24 months total return for each continuous futures chain.

2. If the return is positive, generate a long signal of 1, else -1.

