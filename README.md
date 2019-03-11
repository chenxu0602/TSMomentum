# TSMomentum
Time Series Momentum in Global Futures

# Strategy Setup
Multiple research articles (including the JP Morgan research) identified that the global commoditiy futures has mid to long 
term time series momentum.

The strategy is based on the futures momentum in 1, 3, 6, 12 and 24 months. 

Data source is Quandl's Reference futures contracts data at https://www.quandl.com/data/SRF-Reference-Futures/documentation

The products are chosen so that no single category would dominate:

ATW, SB, CL, PA, PL, GC, ES, NE, AD, CD, S, C, TU

The continuous futures chain is generated based on liquidity. The data is attached in **SRF_Continuous**.

The code is in **srf_signals.py**.

# Strategy Explanation
1. Calculate the 1, 3, 6, 12 and 24 months total return for each continuous futures chain.

2. If the return is positive, generate a long signal of 1, else -1.

3. Calculate the historical sharpe ratio for those positions with a rolling window varies from 6 to 24 months.

4. If the sharpe ratio is less than -0.5, set the position to 0.

5. No optimization algorithm is used. So far I haven't found a better weighting scheme than equal weight.
So first aggregate the signals of different months for each product, then aggregate the signals of all products.
Trade the second front contracts.
   
# Results Analysis
The graph **CumPnL_Prod.png** shows the cumulative returns of each product while **PnL_Prod.csv** is the return time series.
The annualized return is CD: 0.3%, C: 0.5%, S: 5.8%, ATW: 5.2%, 5.5%, PA: 7.4%, SB: 8.4%, PL: 2.8%, GC: 1.5%, CL: 4.6%, A: 1.7% 
and TU: 0.4%. The currency (CD, AD) and fixed income (TU) returns are low because their low volatility. This indicates 
the equal weight method is not optimal and they should be tilted to higher weights. 

The correlation matrix is in **corr.csv**. In the whole period time range, there doesn't seem to be any significant correlation among
the products.

Assuming a 5bps slippage, the PnL curve is shown in **Aggregated_PnL.png**. The sharpe ratio is only around 0.6. 

# Potential Improvement
1. An optimization model
2. Adding more momentum indicators such as the front-second spread and cross-sectional ranks.
3. Adding more products.

