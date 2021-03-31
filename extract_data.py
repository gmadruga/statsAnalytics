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


def extract_csv(csvpath, namepath, sucesspath, typepath,csv_result):
    df = pd.read_csv(csvpath)
    df_name = pd.read_csv(namepath)
    df_sucess = pd.read_csv(sucesspath)
    df_type = pd.read_csv(typepath)
    df_result = pd.read_csv(csv_result)
    df_rows = []
    for i in range(len(df)):

        data = df.iloc[i, 0]
        data_name = df_name.iloc[i, 0]
        data_type = df_type.iloc[i, 0]
        data_sucess = df_sucess.iloc[i, 0]

        data_json = json.loads(data)

        dataframe = pd.json_normalize(data_json)

        dataframe = stats_clean(dataframe, ['x', 'y', 'z'])

        # top10 = [420230887, 413061040, 421033487, 414190204, 420594875, 421033490, 420489284, 420606629, 420594830, 420594831]

        df_1 = [413890754, 400174858, 430214244, 430193602, 411631547, 414274365, 413816489, 411369770, 413015389,
                410150959]
        df_2 = [420520230, 420087193, 411020373, 414212811, 411369788, 421311698, 414091436, 420324756, 412465294]
        df_3 = [420544459, 410926376, 411452778, 411369795, 420594997, 414663660]
        df_4 = [20870391, 420489284, 413061040, 412359570, 421033487, 412465294, 411452778, 420599520, 414103773,
                412502176]
        df_5 = [413810369, 414024271, 420858445, 430179117, 411096199, 414740161, 411625529, 413159656, 413633694,
                412616870]

        #
        # if data_name in df_1:
        #     dataframe['index'] = range(len(dataframe))
        #     plot_scatter('df_1',
        #                   savename=data_name,
        #                   axis_y=dataframe['index'],
        #                   axis_x=dataframe['x'],
        #                   title='Campo no Eixo X - Medição:'+ str(data_name),
        #                   ylabel='Campo',
        #                   xlabel='Medições',
        #                   scale='linear')
        #
        # if data_name in df_2:
        #     dataframe['index'] = range(len(dataframe))
        #     plot_scatter('df_2',
        #                   savename=data_name,
        #                   axis_y=dataframe['index'],
        #                   axis_x=dataframe['x'],
        #                   title='Campo no Eixo X - Medição:'+ str(data_name),
        #                   ylabel='Campo',
        #                   xlabel='Medições',
        #                   scale='linear')
        #
        # if data_name in df_3:
        #     dataframe['index'] = range(len(dataframe))
        #     plot_scatter('df_3',
        #                   savename=data_name,
        #                   axis_y=dataframe['index'],
        #                   axis_x=dataframe['x'],
        #                   title='Campo no Eixo X - Medição:'+ str(data_name),
        #                   ylabel='Campo',
        #                   xlabel='Medições',
        #                   scale='linear')
        #
        # if data_name in df_4:
        #     dataframe['index'] = range(len(dataframe))
        #     plot_scatter('df_4',
        #                   savename=data_name,
        #                   axis_y=dataframe['index'],
        #                   axis_x=dataframe['x'],
        #                   title='Campo no Eixo X - Medição:'+str(data_name),
        #                   ylabel='Campo',
        #                   xlabel='Medições',
        #                   scale='linear')

        if data_name in df_5:
            dataframe['index'] = range(len(dataframe))
            plot_scatter('df_5',
                         savename=data_name,
                         axis_y=dataframe['index'],
                         axis_x=dataframe['x'],
                         title='Campo no Eixo X - Medição:' + str(data_name),
                         ylabel='Campo',
                         xlabel='Medições',
                         scale='linear')

        df_row = stats_generate(dataframe)

        df_row.append(data_name)
        df_row.append(data_type)
        df_row.append(data_sucess)
        df_rows.append(df_row)

    df = pd.DataFrame(df_rows,
                      columns=["X_mean", "Y_mean", "Z_mean", "X_var", "Y_var", "Z_var", "medicao", "tipo", "sucesso"])

    df_top10 = df.sort_values(by=['X_var'], ascending=False)[:10]
    df_2percent = df.sort_values(by=['X_var'], ascending=False)[:180]

    df_5percent = df.sort_values(by=['X_var'], ascending=False)[:int(len(df)*0.2)]

    # df_2percent = df_2percent[df_2percent['X_var'] < df_2percent['X_var'].quantile(0.90)]
    # df_5percent = df_5percent[df_5percent['X_var'] < df_5percent['X_var'].quantile(0.95)]


    df_5percent.to_csv('final/resultado4.csv')
    # df = df[df['X_var'] < df['X_var'].quantile(0.98)]

    std_analysis(df)

    return dataframe
