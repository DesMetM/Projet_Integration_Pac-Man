import os

import pandas as pd


class Leaderboard:

    def __init__(self):
        self.file = os.path.join("ressource", "leaderboard", "Leaderboard.pkl")
        self.load_lead()

    def load_lead(self):
        self.df = pd.read_pickle(self.file)
        self.sort_df()

    def save_lead(self):
        self.sort_df()
        self.df.to_pickle(self.file)

    def sort_df(self):
        self.df = self.df.sort_values(by='score', axis=0, ascending=False)
        self.df = self.df.reset_index(drop=True)

    def compare_lead(self, score, name):
        #Ajoute la nouvelle valeur, trie les valeur et enlève celui à la dernière position pour garder 5 positions
            self.df = self.df.append({'name':name,'score':score}, ignore_index=True)
            self.sort_df()
            self.df = self.df.drop(self.df.tail(1).index)