import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random
from scipy import stats


def stats_clean(df, column_list):
    df1 = df[column_list]
    df1 = df1[(np.abs(stats.zscore(df1)) < 3).all(axis=1)]
    df = pd.merge(df, df1)
    df = df.drop_duplicates()
    return df


def stats_generate(df):
    df_stats = []
    df_stats.append(df['X'].mean(axis=0))
    df_stats.append(df['Y'].mean(axis=0))
    df_stats.append(df['Z'].mean(axis=0))
    df_stats.append(df['X'].var(axis=0))
    df_stats.append(df['Y'].var(axis=0))
    df_stats.append(df['Z'].var(axis=0))

    return df_stats


def std_analysis(df):
    # cheater = ['7bed896a-238b-4c11-8a28-22c212c15986.magnet.json','e2f2c1f6-b71d-4cfa-b5a9-7eda0034ea38.magnet.json','509e0564-9fc0-4c81-8289-5704fcaff4f9.magnet.json','ee632fbe-2504-46bf-82ec-41aded0acf86.magnet.json','ae6088d4-e854-4e9d-b472-8945988f57fe.magnet.json','35eb536b-3386-49c7-9a1d-350a5947f9bf.magnet.json','43299760-e3e8-48b9-8a4b-9e7e44428bd8.magnet.json','2e593a9e-7368-4689-b724-25c1696766a6.magnet.json']
    # not_csv_index = [7,29,44,64,70,82,88,100,131,162,166,182,186,201,209,211,212,214,228,230,238,245,249,251,257,280,282,303,311,323,329,332,333,367,372,376,381,391,401,418,455,463,478,479,490,500,516,518,522,528,530,535,541,544,552]
    #
    # total_size = len(df)
    # true_size = len(df[df['sucesso'] == 1])
    # false_size = len(df[df['sucesso'] == 0])
    # labels_1 = ['Acertou', 'Errou']
    # sizes_1 = [true_size / total_size, false_size / total_size]
    # ponteiro_size = len(df[df['tipo'] == 'Ponteiro'])
    # ciclometrico_size = len(df[df['tipo'] == 'Ciclometrico'])
    # eletronico_size = len(df[df['tipo'] == 'Eletronico'])
    # else_size = total_size - (ponteiro_size + ciclometrico_size + eletronico_size)
    # labels_2 = ['Ponteiro', 'Ciclometrico','Eletronico','Null']
    # sizes_2 = [ponteiro_size / total_size, ciclometrico_size / total_size, eletronico_size / total_size, else_size / total_size]
    # fig1, ax1 = plt.subplots()


    return 'ok'


def df_stats(df):
    df_xmean = df['X_var'].mean(axis=0)
    df_ymean = df['Y_var'].mean(axis=0)
    df_zmean = df['Z_var'].mean(axis=0)

    df_xvar = df['X_var'].var(axis=0)
    df_yvar = df['Y_var'].var(axis=0)
    df_zvar = df['Z_var'].var(axis=0)

    statslist = [df_xmean, df_ymean, df_zmean, df_xvar, df_yvar, df_zvar]
    return statslist


def catch_cheater(df, stats, axis):
    axis_num = len(axis)
    i = 0
    df_var_result = None
    while i != axis_num:
        if axis[i] == 'X':
            df_var_x_up = df[df['X_var'] > stats[0] + 2 * stats[3]]
            df_var_x_down = df[df['X_var'] < stats[0] - 2 * stats[3]]
            df_var_append = df_var_x_up.append(df_var_x_down)
        elif axis[i] == 'Y':
            df_var_y_up = df[df['Y_var'] > stats[1] + 2 * stats[4]]
            df_var_y_down = df[df['Y_var'] < stats[1] - 2 * stats[4]]
            df_var_append = df_var_y_up.append(df_var_y_down)
        elif axis[i] == 'Z':
            df_var_z_up = df[df['Z_var'] > stats[2] + 2 * stats[5]]
            df_var_z_down = df[df['Z_var'] < stats[2] - 2 * stats[5]]
            df_var_append = df_var_z_up.append(df_var_z_down)
        if df_var_append is not None and df_var_result is None:
            df_var_result = df_var_append
        elif df_var_append is not None and df_var_result is not None:
            df_var_result = pd.merge(df_var_result, df_var_append)
        i = i + 1

    return df_var_result


def plot_scatter(df, savename, axis_y, axis_x, title, ylabel='', xlabel='', scale='linear', stats=[]):
    ax = plt.gca()
    ax.scatter(axis_y, axis_x, c='blue', edgecolors='none')
    ax.grid(which='major', axis='both', linestyle='--')
    ax.set_yscale(scale)
    ax.set_xscale('linear')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if (len(stats) != 0):
        plt.title('Mean: ' + str(round(stats[0], 2)) + '     ' + 'Var: ' + str(round(stats[1], 2)))
    plt.suptitle(title)
    plt.savefig('medicoes/'+'/'+ str(savename) + '.png')
    ax.clear()


def plot_hist(df, savename, axis_x, title, suptitle='', ylabel='', xlabel='', bins='auto'):
    plt.hist(x=axis_x, bins=bins, color='#0504aa')
    plt.title(title)
    plt.suptitle(suptitle)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig('medicoes/' + savename + '.png')


def df_splitter(df, column, min='under', max='over'):
    if min == 'under':
        df1 = df
    else:
        mask_min = df[column] > min
        df1 = df[mask_min]
    if max == 'over':
        df2 = df1
    else:
        mask_max = df1[column] < max
        df2 = df1[mask_max]
    return df2
