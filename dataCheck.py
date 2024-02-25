import re
import pandas as pd
import json
import matplotlib.pyplot as plt



def null_check(df, column):
    # print(df[column])
    return df[column].isnull().sum()


def range_check(df, column, minimum, maximum):
    s = pd.Series(df[column].astype(str))
    # print(s)
    return len(s) - s.between(minimum, maximum).sum()


def total_error_percentage(df, errors):
    return (errors / df.size) * 1000


def format_check(df, column, regex):
    errors = 0

    s = pd.Series(df[column])
    wrong = list()
    total_matches = s.str.match(rf'{regex}').sum()

    for val in s.astype(str):
        if not bool(re.match(regex, val)):
            wrong.append(val)

    # print(wrong[:10])
    errors = len(s) - total_matches
    return errors


def value_check(df, column, value):
    errors = 0

    if isinstance(value, list):
        for row in df[column].astype(str):
            if row not in value:
                errors += 1

    else:
        for row in df[column].astype(str):
            if row != value:
                errors += 1

    return errors


def run_quality_checks(dataset_index):
    result_map = {}

    with open('config.json', 'r') as file:
        errors = 0
        total_nulls = 0
        total_format_errors = 0
        total_value_errors = 0

        config = json.loads(file.read())

        dataset_profile = config[dataset_index]

        print(dataset_profile['dataset'])

        dataframe = pd.read_csv(dataset_profile['dataset'])

        # checks object
        checks = dataset_profile['checks'][0]

        # print(checks)

        # checks to run on the dataset
        keys = list(checks.keys())

        # print(keys)
        null_output = {}
        range_output = {}
        format_output = {}
        value_output = {}

        for i, check in enumerate(checks):

            # print(check)
            if check == 'null_check':

                for column in checks[check]:
                    # print(dataframe[column])
                    nulls = null_check(dataframe, column)

                    perc = (nulls / dataframe.size) * 100

                    null_output[column] = perc

                    total_nulls += nulls
                    errors += nulls
                    # print(nulls)


            elif check == "range_check":
                # print(list(checks[keys[i]].keys())) #columns
                # print(list(checks[keys[i]].values())) #ranges
                if isinstance(checks[keys[i]], list):
                    columns = list(checks[keys[i]].keys())
                    ranges = list(checks[keys[i]].values())
                else:
                    columns = list(checks[check])
                for i, column in enumerate(columns):
                    constraints = ranges[i].split('-')
                    # print(constraints[0], constraints[1])
                    range_errors = range_check(dataframe, column, constraints[0], constraints[1])
                    range_output[column] = (range_errors / dataframe.size )*100



            elif check == "total_error_percentage":
                print("Total errors: ", total_error_percentage(dataframe, errors))

            elif check == "format_check":
                columns = list(checks[check].keys())
                regex = list(checks[check].values())
                for i, column in enumerate(columns):
                    format_errors = format_check(dataframe, column, regex[i])
                    errors += format_errors
                    total_format_errors += format_errors
                    format_output[column] = (format_errors / dataframe.size )*100


            elif check == "value_check":
                columns = list(checks[check].keys())
                values = list(checks[check].values())
                for i, column in enumerate(columns):
                    value_errors = value_check(dataframe, column, values[i])
                    errors += value_errors
                    total_value_errors += value_errors
                    value_output[column] = (value_errors / dataframe.size )*100


            elif check == "total_null_errors":
                print("Total nulls: ", total_nulls)

            elif check == "total_format_errors":
                print("Total format errors: ", total_format_errors)

            elif check == "total_value_errors":
                print("Total value errors: ", total_value_errors)

            elif check == "total_number_errors":
                print("Total errors: ", errors)
                
        print("null", null_output)
        print("range", range_output)
        print("format", format_output)
        print("value", value_output)




if __name__ == '__main__':
    run_quality_checks(2)

# "Start Date": "^(0[1-9]|1[0-2])/(0[1-9]|[12][0-9]|3[01])/\\d{4} (0\\d|1[0-2]):([0-5]\\d)$",
# "End Date": "^(0[1-9]|1[0-2])/(0[1-9]|[12][0-9]|3[01])/\\d{4} (0\\d|1[0-2]):([0-5]\\d)$",
# "Total Duration (hh:mm:ss)": "^([01]\\d|2[0-3]):[0-5]\\d:[0-5]\\d$",
# "Charging Time (hh:mm:ss)": "^([01]\\d|2[0-3]):[0-5]\\d:[0-5]\\d$"
