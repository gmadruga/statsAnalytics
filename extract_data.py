import pandas as pd
import json
from os import listdir
from os.path import isfile, join
from manipulate_data import stats_generate, std_analysis, stats_clean, plot_scatter


def run(folderpath):
    onlyfiles = [f for f in listdir(folderpath) if isfile(join(folderpath, f))]
    df = pd.DataFrame(columns=["x_mean", "y_mean", "z_mean", "x_var", "y_var", "z_var", "filename"])
    df_rows = []
    i = 0
    for filename in onlyfiles:
        filepath = folderpath + '/' + filename
        df_row = extract(filepath)
        df_row.append(filename)
        df_row.append(i)
        df_rows.append(df_row)
        i = i + 1
    df = pd.DataFrame(df_rows, columns=["X_mean", "Y_mean", "Z_mean", "X_var", "Y_var", "Z_var", "filename", "index"])
    dfstats = std_analysis(df, 'index')
    return dfstats


def extract(filepath):
    with open(filepath, 'r') as file:
        data = file.read()
        data_json = json.loads(data)
        dataframe = pd.json_normalize(data_json)
        dataframe = stats_clean(dataframe, ['x', 'y', 'z'])
        dataframe = stats_generate(dataframe)
        return dataframe


def extract_csv(csvpath):
    df = pd.read_csv(csvpath,sep=';')

    df_rows = []

    df_instalacao = df['INSTALACAO'].drop_duplicates()


    for i in df_instalacao:

        only_one_date = False

        df1 = df.loc[df['INSTALACAO'] == i]
        df1 = df1.sort_values('DT_REF',ascending=False)
        df1 = df1.reset_index()
        last_date = df1['DT_REF'][0]


        df_first = df1.loc[df1['DT_REF'] == last_date]
        df_first = stats_clean(df_first, ['X', 'Y', 'Z'])
        df_first['index'] = range(len(df_first))

        df_second = df1.loc[df1['DT_REF'] != last_date]
        df_second = df_second.reset_index()

        if(len(df_second) != 0):
            second_date = df_second['DT_REF'][0]
            df_second = df_second.loc[df_second['DT_REF'] == second_date]
            df_second = stats_clean(df_second,['X','Y','Z'])
            df_second['index'] = range(len(df_second))
        else:
            only_one_date = True


        df_row = stats_generate(df_first)
        if only_one_date == True:
            df_row = df_row +["","","","","",""]
        else:
            df_row = df_row + stats_generate(df_second)
        df_row.append(i)
        df_rows.append(df_row)
    df_final = pd.DataFrame(df_rows,
                      columns=["X_mean", "Y_mean", "Z_mean", "X_var", "Y_var", "Z_var",
                               "last_X_mean", "last_Y_mean", "last_Z_mean", "last_X_var", "last_Y_var", "last_Z_var","INSTALACAO"])
    df_final.to_csv('final/medicoes_stats_maio.csv')

    # for i in range(len(df)):
    #
    #     data = df.iloc[i, 0]
    #     data_name = df_name.iloc[i, 0]
    #     data_type = df_type.iloc[i, 0]
    #     data_sucess = df_sucess.iloc[i, 0]
    #
    #     data_json = json.loads(data)
    #
    #     dataframe = pd.json_normalize(data_json)
    #
    #     dataframe = stats_clean(dataframe, ['x', 'y', 'z'])



    #     df_row = stats_generate(dataframe)
    #
    #     df_row.append(data_name)
    #     df_row.append(data_type)
    #     df_row.append(data_sucess)
    #     df_rows.append(df_row)
    #
    # df = pd.DataFrame(df_rows,
    #                   columns=["X_mean", "Y_mean", "Z_mean", "X_var", "Y_var", "Z_var", "medicao", "tipo", "sucesso"])


    # df_5percent.to_csv('final/resultado4.csv')
    # df = df[df['X_var'] < df['X_var'].quantile(0.98)]

    std_analysis(df)

    return df
