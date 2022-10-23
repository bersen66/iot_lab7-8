import pandas as pd
import matplotlib.pyplot as plt
import collections


def make_csv_from_json(src: str = 'res.json', dest: str = 'res.csv'):
    with open(src, encoding='utf-8') as inputfile:
        df = pd.read_json(inputfile)

    df.to_csv(dest, encoding='utf-8', index=False)


def render_values_by_time(dataframe: pd.DataFrame, x_column_name: str, y_column_name: str):
    fig = plt.figure()
    fig.suptitle(f"Значения {y_column_name} во времени", fontsize=16)

    x = dataframe[x_column_name]
    y = dataframe[y_column_name]
    plt.xticks(rotation=90)
    plt.plot(x, y)
    plt.show()


def render_frequency_distribution(dataframe: pd.DataFrame, column_name: str):
    values = dataframe[column_name]

    fig, ax = plt.subplots(nrows=1, ncols=1)
    ax.set_title(f'Распределение {column_name} по частоте')

    ax.set_xlabel('Показание прибора')
    ax.set_ylabel('Частота')
    
    plt.hist(values, color='g', histtype='barstacked')
    plt.show()


def render_pie(dataframe: pd.DataFrame, column_name: str):
    cnt = collections.Counter(dataframe[column_name])
    fig = plt.figure()
    fig.suptitle(f"Частотное распределение датчика {column_name}", fontsize=16)

    labels = [*cnt.keys()]
    values = [*cnt.values()]
    explode = []
    for i in range(len(values)):
        explode.append(float(values[i] / len(dataframe)))
    

    print(labels)
    print(values)

    plt.pie(values,labels=labels,explode=explode,shadow=True,autopct='%1.1f%%',startangle=180)
    plt.axis('equal')   
    plt.show()
    



def main(src: str = 'res.csv'):
    df = pd.read_csv(src)
    print(df.head(5).to_string())
    render_pie(df, 'Illuminance')
    render_values_by_time(df, x_column_name='time', y_column_name='CO2')
    render_frequency_distribution(df, column_name='Temperature')


if __name__ == '__main__':
    make_csv_from_json()
    main()
