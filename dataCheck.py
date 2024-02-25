import re
import pandas as pd
import json


def null_check(df,column):
    return df[column].isnull().sum()


def range_check(df, column, min, max):
    s = pd.Series(df[column].astype(str))
    #print(s)
    return len(s) - s.between(min, max).sum()


def percentage_check(df, errors):
    return errors / len(df)


def format_check(df, column, format):
    regex_check = re.compile(format)
    errors = 0
    s = pd.Series(df[column])
    for val in s:
        if not re.fullmatch(regex_check, val):
            errors += 1

    return errors


def value_check(df, column, value):
    errors = 0
    if isinstance(value, list):
        for row in df[column]:
            if row not in value:
                errors += 1
    else:
        for row in df[column]:
            if row != value:
                errors += 1

    return errors


def run_quality_checks(dataset_index):
    with open('config.json', 'r') as file:
        errors = 0
        total_nulls = 0


        config = json.loads(file.read())

        dataset_profile = config[dataset_index]

        dataframe = pd.read_csv(dataset_profile['dataset'])

        # checks object
        checks = dataset_profile['checks'][0]

        # checks to run on the dataset
        keys = list(checks.keys())

        for i, check in enumerate(checks):
            #print(checks)
            if check == 'null_check':
                for column in checks[check]:
                    #print(dataframe[column])
                    total_nulls += null_check(dataframe, column)
                    #print(nulls)

            if check == "range_check":
               # print(list(checks[keys[i]].keys())) #columns
                #print(list(checks[keys[i]].values())) #ranges
                columns = list(checks[keys[i]].keys())
                ranges = list(checks[keys[i]].values())
                for i, column in enumerate(columns):
                    constraints = ranges[i].split('-')
                   # print(constraints[0], constraints[1])
                    errors = range_check(dataframe, column, constraints[0], constraints[1])
            if check == "percentage_check":
                print(total_nulls)



              #      for column in columns:
              #      print(range_check(dataframe, 'age', 0, 100))
              #  for column in columns:
            #if check == 'null_check':
             #   nulls = null_check(dataframe)
             #   total_nulls += nulls
             #   print(nulls)
           # elif check == 'range_check':
           ##     print(range_check(dataframe, 'age', 0, 100))
           # elif check == 'percentage_check':
          #      print(percentage_check(dataframe, total_nulls))
           # elif check == 'format_check':
         #       print(format_check(dataframe, 'email', r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'))
         #   elif check == 'value_check':
         #       print(value_check(data)








if __name__ == '__main__':
    run_quality_checks(0)
