from sql_manager import SqlManager
import matplotlib.pyplot as plt



def read_data(sql_file):
    sql_manager = SqlManager(sql_file)
    data = sql_manager.crs.execute("select  description,count(description) from transactions group by description order by count(description) desc").fetchall()
    x_axis_data = []
    y_axis_data = []
    for item in data:
        x_axis_data.append(item[0])
        y_axis_data.append(item[1])
    return x_axis_data, y_axis_data

def chart_item_frequency(base_dir, file_name, x, y, top):
    fig, axs = plt.subplots(figsize=(250, 150))
    plt.xticks(rotation=30, fontsize=100)
    plt.yticks(fontsize=100)
    if top != 'all':
        x = x[:top]
        y = y[:top]
    axs.bar(x, y)
    fig.suptitle('item _ frequency', fontsize=150)
    fig.savefig(base_dir+file_name+ str(top) +'.png')
    plt.close()
if __name__ == '__main__':
    top_frequency = [10, 25, 35, 'all']
    print("Q1")
    x, y = read_data('information.sqlit3')
    for top in top_frequency:
        chart_item_frequency('.\\out\\', 'q1_item_frequency_', x, y, top)