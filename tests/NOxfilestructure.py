import pandas as pd
import os


with open("data/raw/airNO2monthly/air_monthlyNO2|21-25.csv", "r") as f:
    for i in range(20):
        print(f"Line {i+1}: {f.readline().rstrip()}")