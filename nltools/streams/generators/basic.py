import os

import pandas as pd

from ..io_ import basic as basic_io
from ...exceptions import WrongExtensionError


def reader(filename,
           src=None,
           save_mini=False,
           save_dir='',
           **df_kwargs):

    base_name, extension = os.path.splitext(os.path.basename(filename))

    if src is None:
        if extension == '.xlsx':
            df = basic_io.read_xlsx(filename, lib='pd', **df_kwargs)

        elif extension == '.csv':
            return basic_io.read_csv(filename)

        else:
            raise WrongExtensionError('Only *.csv and *.xlsx formats are currently supported for this function.')

    else:
        if src == 'prp':
            return basic_io.read_csv(filename)

        elif src == 'raw':
            if extension == '.xlsx':
                df = basic_io.read_xlsx(filename, lib='pd', **df_kwargs)
            elif extension == '.csv':
                df = pd.read_csv(filename, **df_kwargs)

        else:
            raise WrongExtensionError('Only *.csv and *.xlsx formats are currently supported for this function.')

    if save_mini and save_dir:
        basic_io.df_to_csv(df.iloc[:100], os.path.join(save_dir, f'{base_name}_100.csv'),
                  get_array=False)
        basic_io.df_to_csv(df.iloc[:1000], os.path.join(save_dir, f'{base_name}_1k.csv'),
                  get_array=False)
        basic_io.df_to_csv(df.iloc[:10000], os.path.join(save_dir, f'{base_name}_10k.csv'),
                  get_array=False)
        basic_io.df_to_csv(df.iloc[:50000], os.path.join(save_dir, f'{base_name}_50k.csv'),
                  get_array=False)
        basic_io.df_to_csv(df.iloc[:100000], os.path.join(save_dir, f'{base_name}_50k.csv'),
                  get_array=False)

    return basic_io.df_to_csv(df, os.path.join(save_dir, f'{base_name}.csv'))
