
import numpy as np 
import pandas as pd 
import os, sys, re 
import argparse

from datetime import datetime, date  
from collections import defaultdict

import matplotlib.pyplot as plt  


commodities = [
   "ATW",
   "SB",
   "CL",
   "PA",
   "PL",
   "GC",
   "ES",
   "NE",
   "AD",
   "NE",
   "CD",
   "S",
   "C",
   "TU",
]


def Sharpe(x):
   if len(x) > 1:
      if x.std() > 0:
         s = 16. * x.mean() / x.std()
         return max(0, s)
   return 0.0


datadir = os.path.expandvars("SRF_Continuous")
files = os.listdir(datadir)

data = defaultdict(pd.DataFrame)
for filename in files:
   prod, _ = filename.split('.')
   if not prod in commodities:
      continue
   fl = os.path.join(datadir, filename)
   data[prod] = pd.read_csv(fl, parse_dates=["date"], index_col=["date"])

print("Done loading data.")

for prod, df in data.items():
   df["std"] = df["ret1"].rolling(window=200, min_periods=120).std()
   df["ret12"] = df["ret1"] - df["ret2"]
   df["ret1-1mon"]  = df["ret1"].rolling(window=25).sum()
   df["ret1-3mon"]  = df["ret1"].rolling(window=75).sum()
   df["ret1-6mon"]  = df["ret1"].rolling(window=125).sum()
   df["ret1-12mon"] = df["ret1"].rolling(window=250).sum()
   df["ret1-24mon"] = df["ret1"].rolling(window=500).sum()
   df["ret2-1mon"]  = df["ret2"].rolling(window=25).sum()
   df["ret2-3mon"]  = df["ret2"].rolling(window=75).sum()
   df["ret2-6mon"]  = df["ret2"].rolling(window=125).sum()
   df["ret2-12mon"] = df["ret2"].rolling(window=250).sum()
   df["ret2-24mon"] = df["ret2"].rolling(window=500).sum()
   data[prod] = df

for prod, df in data.items():
   df["target-1mon"]  = np.nan
   df["target-3mon"]  = np.nan
   df["target-6mon"]  = np.nan
   df["target-12mon"] = np.nan
   df["target-24mon"] = np.nan

   df.loc[df["ret1-1mon"].shift(1) > 0, "target-1mon"]     = 1.0
   df.loc[df["ret1-1mon"].shift(1) < 0, "target-1mon"]     = -1.0
   df.loc[df["ret1-3mon"].shift(1) > 0, "target-3mon"]     = 1.0
   df.loc[df["ret1-3mon"].shift(1) < 0, "target-3mon"]     = -1.0
   df.loc[df["ret1-6mon"].shift(1) > 0, "target-6mon"]     = 1.0
   df.loc[df["ret1-6mon"].shift(1) < 0, "target-6mon"]     = -1.0
   df.loc[df["ret1-12mon"].shift(1) > 0, "target-12mon"]   = 1.0
   df.loc[df["ret1-12mon"].shift(1) < 0, "target-12mon"]   = -1.0
   df.loc[df["ret1-24mon"].shift(1) > 0, "target-24mon"]   = 1.0
   df.loc[df["ret1-24mon"].shift(1) < 0, "target-24mon"]   = -1.0

   df["target-1mon"].fillna(method="ffill", inplace=True)
   df["target-3mon"].fillna(method="ffill", inplace=True)
   df["target-6mon"].fillna(method="ffill", inplace=True)
   df["target-12mon"].fillna(method="ffill", inplace=True)
   df["target-24mon"].fillna(method="ffill", inplace=True)

   df["PnL-1mon"]  = df["ret1"].mul(df["target-1mon"].shift(1))
   df["PnL-3mon"]  = df["ret1"].mul(df["target-3mon"].shift(1))
   df["PnL-6mon"]  = df["ret1"].mul(df["target-6mon"].shift(1))
   df["PnL-12mon"] = df["ret1"].mul(df["target-12mon"].shift(1))
   df["PnL-24mon"] = df["ret1"].mul(df["target-24mon"].shift(1))
   data[prod] = df

""" test sharpe """
for prod, df in data.items():
   df["sharpe-1mon"]  = 16 * (df["PnL-1mon"].rolling(window=120).mean().div(df["PnL-1mon"].rolling(window=120).std())).shift(1)
   df["sharpe-3mon"]  = 16 * (df["PnL-3mon"].rolling(window=120).mean().div(df["PnL-3mon"].rolling(window=120).std())).shift(1)
   df["sharpe-6mon"]  = 16 * (df["PnL-6mon"].rolling(window=250).mean().div(df["PnL-6mon"].rolling(window=120).std())).shift(1)
   df["sharpe-12mon"] = 16 * (df["PnL-12mon"].rolling(window=500).mean().div(df["PnL-12mon"].rolling(window=120).std())).shift(1)
   df["sharpe-24mon"] = 16 * (df["PnL-24mon"].rolling(window=500).mean().div(df["PnL-24mon"].rolling(window=120).std())).shift(1)
   data[prod] = df

for prod, df in data.items():
   df.loc[df["sharpe-1mon"]  < -0.5, "target-1mon"]   = 0.0
   df.loc[df["sharpe-3mon"]  < -0.5, "target-3mon"]   = 0.0
   df.loc[df["sharpe-6mon"]  < -0.5, "target-6mon"]   = 0.0
   df.loc[df["sharpe-12mon"] < -0.5, "target-12mon"]  = 0.0
   df.loc[df["sharpe-24mon"] < -0.5, "target-24mon"]  = 0.0
   data[prod] = df

for prod, df in data.items():
   df["PnL-1mon"]  = df["ret2"].mul(df["target-1mon"].shift(1))
   df["PnL-3mon"]  = df["ret2"].mul(df["target-3mon"].shift(1))
   df["PnL-6mon"]  = df["ret2"].mul(df["target-6mon"].shift(1))
   df["PnL-12mon"] = df["ret2"].mul(df["target-12mon"].shift(1))
   df["PnL-24mon"] = df["ret2"].mul(df["target-24mon"].shift(1))
   data[prod] = df

pnls    = defaultdict(pd.DataFrame)
weights = defaultdict(pd.DataFrame)
for prod, df in data.items():
   pnl = pd.DataFrame(index=df.index)
   pnl["PnL-1mon"] = df["PnL-1mon"]
   pnl["PnL-3mon"] = df["PnL-3mon"]
   pnl["PnL-6mon"] = df["PnL-6mon"]
   pnl["PnL-12mon"] = df["PnL-12mon"]
   pnl["PnL-24mon"] = df["PnL-24mon"]
   pnls[prod] = pnl.fillna(0)

all_dict = {}
for prod, pnl in pnls.items():
   weighted_pnl= pnl.mean(axis=1)
   all_dict[prod] = weighted_pnl

results = pd.DataFrame(all_dict)
results.fillna(0, inplace=True)

