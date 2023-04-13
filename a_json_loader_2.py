import numpy as np
import matplotlib.pyplot as plt

import pandas as pd
from spykes.plot.neurovis import NeuroVis
from spykes.plot.popvis import PopVis
from spykes.io.datasets import load_reward_data

all_psth = pop.get_all_psth(
    event=event, df=data_df, conditions=condition, window=window,
    binsize=binsize, plot=True)
pop.plot_heat_map(all_psth, normalize='each', show=True)