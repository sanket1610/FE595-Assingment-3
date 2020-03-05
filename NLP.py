import pandas as pd
import csv
import ast
import json
import nltk
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer as SIA

# -----------file = companys.csv--------#
df1 = pd.read_csv("companys.csv")

# -----------file = napu (1)--------#
df2 = pd.read_csv("napu (1).csv")
df2.drop("Unnamed: 0", axis=1, inplace=True)

# -----------file = ListOfCompanies JVansant (1).csv--------#
df3 = pd.read_csv("ListOfCompanies JVansant (1).csv")
df3.drop("Unnamed: 0", axis=1, inplace=True)

# -----------file = output_Webscrap_HW2.txt--------#
f1 = open("output_Webscrap_HW2.txt", "r")
Name = []
Purpose = []
for i in f1.readlines():
    Purpose.append(i.split(",")[-1][8:])
    n = i.split(",")[:-1]
    n1 = ",".join(n[:2])
    Name.append(n1[5:])
df4 = pd.DataFrame({"Name": Name, "Purpose": Purpose})

# -----------file = result.txt---------#
f = open("result.txt", "r")
Name = []
Purpose = []
for i in f.readlines():
    if i[0:5] == "Name:":
        Name.append(i[6:-1])
    elif i[0:8] == "Purpose:":
        Purpose.append(i[8:])
df5 = pd.DataFrame({"Name": Name, "Purpose": Purpose})


# -----------file = output_file_Option_2.txt---------#
Name = []
Purpose = []
f2 = open("output_file_Option_2.txt", "r")
for i in f2.readlines()[3:53]:
    Name.append(i.split("|")[2].strip())
    Purpose.append(i.split("|")[3].strip())
df6 = pd.DataFrame({"Name": Name, "Purpose": Purpose})

# -----------file = Company.txt---------#
Name = []
Purpose = []
f3 = open("Company.txt", "r")
x = f3.readlines()
for i in range(len(x)):
    if i % 2 == 0:
        Name.append(x[i].split(")")[1].strip())
    else:
        Purpose.append(x[i].strip())
df7 = pd.DataFrame({"Name": Name, "Purpose": Purpose})


# -----------file = Webscrp_company.txt---------#
f4 = open("Webscrp_company.txt", "r").read()
result = json.loads(f4)
x = [(k, v) for k, v in result.items()]
Name = []
Purpose = []
for i in x:
    Name.append(i[0])
    Purpose.append(i[1])
df8 = pd.DataFrame({"Name": Name, "Purpose": Purpose})


# -----------file = text_scrap.txt---------#
f5 = open("text_scrap.txt", "r").read()
result = ast.literal_eval(f5)
Name = []
Purpose = []
for i in result:
    Name.append(i[0][5:])
    Purpose.append(i[1][9:])
df9 = pd.DataFrame({"Name": Name, "Purpose": Purpose})

# -----------file = Company Details.txt---------#
f6 = open("Company Details.txt", "r").readlines()
Name = []
Purpose = []
for i in f6[1:]:
    if i[:5] == "Name:":
        Name.append(i[5:-1])
    elif i[:8] == "Purpose:":
        Purpose.append((i[8:]))
df10 = pd.DataFrame({"Name": Name, "Purpose": Purpose})


frames = [df1, df2, df3, df4, df5, df6, df7, df8, df9, df10]
df = pd.concat(frames)
df = df.reset_index()
df.drop("index", axis=True, inplace=True)
df.drop_duplicates(subset="Name")


result = []
for row in df["Purpose"]:
    pol_score = SIA().polarity_scores(row)
    pol_score["Purpose"] = row
    result.append(pol_score)

df["Score"] = pd.DataFrame(result)["compound"]
df1 = df.sort_values(by="Score", ascending=False)