# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-2vnJA75vOP-HNX3T9ciMQTQhQWfJHMO
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

from google.colab import files
uploaded=files.upload()

df = pd.read_csv("alloc.csv")
df

df['puts'] = df['puts'].replace(" ", 0).astype('float32')
df['puts']

ax = sns.catplot(y="cached", kind="count", data=df, height=2.6, aspect=2.5, orient='h')#create categorical plots

g = sns.PairGrid(df, y_vars=["time"], x_vars=["ls_int", "ls_long"], height=4.5, hue="cached", aspect=1.1)
ax = g.map(plt.scatter, alpha=0.6)

#KDE can produce a plot that is less cluttered and more interpretable, especially when drawing multiple distributions.

def kdeplot(puts):
    plt.figure(figsize=(9, 4))
    plt.title("KDE for {}".format(puts))
    ax0 = sns.kdeplot(df[df['cached'] == 'No'][puts].dropna(), color= 'navy', label= 'Churn: No')
    ax1 = sns.kdeplot(df[df['cached'] == 'Yes'][puts].dropna(), color= 'orange', label= 'Churn: Yes')
kdeplot('time')
kdeplot('ls_long')
kdeplot('ls_int')

df['puts_to_time_ratio'] = df['puts'] / df['time']
df['ls_long'] = df['ls_int'] - df['puts_to_time_ratio']
kdeplot('ls_long')

df["time"] = df["puts"].replace("No", 0).replace("Yes", 1)
g = sns.FacetGrid(df, col="time", height=4, aspect=.9)
ax = g.map(sns.barplot,"ls_int",  "ls_long", "cached")

fig, axis = plt.subplots(1, 2, figsize=(12,4))
axis[0].set_title("Has ls_long")
axis[1].set_title("Has cached ")
axis_y = "percentage of customers"
# Plot Partner column
gp_partner = df.groupby('ls_long')["time"].value_counts()/len(df)
gp_partner = gp_partner.to_frame().rename({"time": axis_y}, axis=1).reset_index()
ax = sns.barplot(x='ls_long', y= axis_y, hue='time', data=gp_partner, ax=axis[0])
# Plot Dependents column
gp_dep = df.groupby('cached')["time"].value_counts()/len(df)
gp_dep = gp_dep.to_frame().rename({"time": axis_y}, axis=1).reset_index()
ax = sns.barplot(x='cached', y= axis_y, hue='time', data=gp_dep, ax=axis[1])

ax = sns.catplot(x="time", y="ls_long", hue="puts", kind="violin",
                  palette="pastel", data=df, height=4.2, aspect=1.4)

ax = sns.catplot(x="ls_long", y="ls_int", hue="puts", kind="box", data=df, height=4.2, aspect=1.4)