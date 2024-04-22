import numpy as np
import matplotlib.pyplot as plt

WeightedTips = [
    {
        "site" : "WinDrawWin",
        "weight" : 1.5
    },
    {
        "site" : "Vitibet",
        "weight" : 1.0
    },
    {
        "site" : "FootballPredictions",
        "weight" : 1.2
    },
    {
        "site" : "Forebet",
        "weight" : 1.0
    },
    {
        "site" : "FreeSuperTips",
        "weight" : 0.8
    },
    {
        "site" : "101greatgoals",
        "weight" : 0.7
    },
    {
        "site" : "FootballBettingTips",
        "weight" : 0.8
    }
]

ScoreTips = [
    {
        "team1" : 2,
        "team2" : 1
    },
    {
        "team1" : 2,
        "team2" : 2
    },
    {
        "team1" : 1,
        "team2" : 1
    },
    {
        "team1" : 1,
        "team2" : 1
    },
    {
        "team1" : 1,
        "team2" : 4
    },
    {
        "team1" : 1,
        "team2" : 1
    },
    {
        "team1" : 1,
        "team2" : 2
    }
]

for i in range (len(WeightedTips)):
    print(ScoreTips[i]['team1'], " - ", ScoreTips[i]['team2'])
    s1 = ScoreTips[i]['team1']
    weight = WeightedTips[i]['weight']
    s2 = ScoreTips[i]['team2']
    avgScore1 = s1 * weight
    avgScore2 = s2 * weight
print(avgScore1, " - ", avgScore2)