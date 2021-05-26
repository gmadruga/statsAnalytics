from extract_data import run
from extract_data import extract,extract_csv

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #run('readings/SECALL')
    #extract('readings/SEC0001/ef1fd0db-af7d-4e38-9133-010faf8a6178.magnet.json')
    extract_csv('readings/sr_magnet_full.csv')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
