import csv
import json
import gzip

import openpyxl as oxl
import pandas as pd

from ...exceptions import WrongExtensionError


def read_xlsx(filename, lib='pd', **kwargs):
    if lib == 'pd':
        return pd.read_excel(filename, **kwargs)

    elif lib == 'oxl':
        wb = oxl.load_workbook(filename=filename, read_only=True, **kwargs)
        return wb.get_active_sheet()


def read_json(filename, **kwargs):
    return pd.read_json(filename, **kwargs)


def read_csv(filename,
             msg_brd=20000,
             replace=u'\xa0'):

    if filename.endswith('.csv'):
        opened_file = open(filename, 'r', encoding='utf-8', newline='')
    elif filename.endswith('.csv.gz'):
        opened_file = gzip.open(filename, 'rt')
    else:
        raise WrongExtensionError('Using this function for reading non-*.csv/*.csv.gz '
                                  'files is forbidden.')

    with opened_file as csvfile:
        num_cols = len(next(csv.reader(csvfile, delimiter=',')))
        for i, row in enumerate(csv.reader(csvfile, delimiter=',')):
            if i+1 <= msg_brd:
                yield [row[j].replace(replace, u'') for j in range(num_cols)]
            else:
                return


def read_top_words(filename):
    if filename.endswith('.csv'):
        with open(filename, 'w') as csvfile:
            return [(row[0], row[1]) for row in csv.reader(csvfile, delimiter=',')]

    else:
        raise WrongExtensionError('Only *.csv format is currently supported for this function.')


def list_to_csv(data, filename, arg='w'):
    if filename.endswith('.csv.gz'):
        filename = filename[:-3]

    if filename.endswith('.csv'):
        csvwriter = csv.writer(open(filename, arg))
        for d in data:
            csvwriter.writerow(d)

    else:
        raise WrongExtensionError('Using this function with non-*.csv/*.csv.gz '
                                  'files is forbidden.')


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


def json_data_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)
