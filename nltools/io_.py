import csv
import json
import os

import openpyxl as oxl
import pandas as pd


def read_xlsx(filename, lib='pd', **kwargs):
    if lib == 'pd':
        return pd.read_excel(filename, **kwargs)

    elif lib == 'oxl':
        wb = oxl.load_workbook(filename=filename, read_only=True)
        return wb.get_active_sheet()


def read_json(filename, **kwargs):
    return pd.read_json(filename, **kwargs)


def read_csv(filename, replace=u'\xa0'):
    if filename.endswith('.csv'):
        with open(filename, 'r', encoding='utf-8', newline='') as csvfile:
            num_cols = len(next(csv.reader(csvfile, delimiter=',')))
            for row in csv.reader(csvfile, delimiter=','):
                yield [row[i].replace(replace, u'') for i in range(num_cols)]

    else:
        raise IOError('Only *.csv format is currently supported for this function.')


def read_top_words(filename):
    if filename.endswith('.csv'):
        with open(filename, 'w') as csvfile:
            return [(row[0], row[1]) for row in csv.reader(csvfile, delimiter=',')]

    else:
        raise IOError('Only *.csv format is currently supported for this function.')


def write_csv(data, filename, arg='w'):
    if filename.endswith('.csv'):
        csvwriter = csv.writer(open(filename, arg))
        for d in data:
            csvwriter.writerow(d)

    else:
        raise IOError('Only *.csv format is currently supported for this function.')


def df_to_json(df, filename):
    return df.to_json(filename)


def oxl_sheet_to_csv(sheet, filename):
    with open(filename, 'w') as f:
        csvwriter = csv.writer(f)
        for r in sheet.rows:
            csvwriter.writerow([cell.value for cell in r])


def df_to_csv(df, filename, get_array=True):
    df.to_csv(filename, index=False)
    if get_array:
        return [df.columns.tolist()] + df.values.tolist()


def write_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)


def reader(filename, src=None, save_mini=True, **df_kwargs):
    base_name, extension = os.path.splitext(os.path.basename(filename))

    if src is None:
        if extension == '.xlsx':
            df = read_xlsx(filename, lib='pd', **df_kwargs)

        elif extension == '.csv':
            return read_csv(filename)

        else:
            raise IOError('Only *.csv and *.xlsx formats are currently supported for this function.')

    else:
        if src == 'prp':
            return read_csv(filename)

        elif src == 'raw':
            if extension == '.xlsx':
                df = read_xlsx(filename, lib='pd', **df_kwargs)
            elif extension == '.csv':
                df = pd.read_csv(filename, **df_kwargs)

        else:
            raise IOError('Only *.csv and *.xlsx formats are currently supported for this function.')

    # if df_preprocessing:
    #     df = preprocessing.preprocess_df(df, columns=columns)

    # if save_mini:
    #     df_to_csv(df.iloc[:100], os.path.join(, '', '', 'input', 'prp', base_name + '_100.csv'),
    #                   get_array=False)
    #     df_to_csv(df.iloc[:1000], os.path.join(, '', '', 'input', 'prp', base_name + '_1k.csv'),
    #                   get_array=False)
    #     df_to_csv(df.iloc[:10000], os.path.join(, '', '', 'input', 'prp', base_name + '_10k.csv'),
    #                   get_array=False)
    #     df_to_csv(df.iloc[:50000], os.path.join(, '', '', 'input', 'prp', base_name + '_50k.csv'),
    #                   get_array=False)
    #     df_to_csv(df.iloc[:100000], os.path.join(, '', '', 'input', 'prp', base_name + '_50k.csv'),
    #                   get_array=False)

    # return df_to_csv(df, os.path.join(, '', '', 'input', 'prp', base_name+'.csv'))
