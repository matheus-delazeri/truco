import numpy as np
import pandas as pd
from os import path
from tabulate import tabulate

class Analyser:
    def __init__(self, cases_file="cases.csv"):
        self.cases_path = path.join(path.dirname(__file__), cases_file)
        self.df = pd.read_csv(self.cases_path, header=0)

    def __str__(self):
        file_size = "{}mb".format(round(path.getsize(self.cases_path) / pow(1024, 2),2))
        return "\n---- Analyser ----\n> {}\n\n{}".format(
            "Data analysis of the case dataset used in bot training",
            tabulate(
                [[path.basename(self.cases_path), file_size, self.df.shape[0], self.df.shape[1]]], 
                headers=['Cases File', 'File Size', 'N. Cases', 'N. Columns'], 
                tablefmt='rounded_outline'
            )
        )
