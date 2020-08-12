import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def save_history_csv(EPOCH, train_loss_ls, train_acc_ls, test_acc_ls, save_path='out/'):
    # <<<set the name that won't let program auto cover it~~>>>
    name_mark = str(test_acc_ls[-1])[2:5]
    col_names = ["EPOCH", "train_acc", "train_loss", "test_acc"]
    col_datas = [EPOCH, train_acc_ls, train_loss_ls, test_acc_ls]
    cols_dict = {}
    for i in range(len(col_names)):
        if i == 0:
            col_dict = {col_names[i]: range(1, EPOCH + 1)}
        else:
            col_dict = {col_names[i]: col_datas[i]}
        cols_dict.update(col_dict)

    df = pd.DataFrame(cols_dict)
    df.to_csv("{}/{}_history.csv".format(save_path, name_mark), encoding='utf-8')


def draw_plot(EPOCH, train_loss_ls, train_acc_ls, test_acc_ls, save_path='out/'):
    # <<<set the name that won't let program auto cover it~~>>>
    name_mark = str(test_acc_ls[-1])[2:5]

    EPOCH_times = range(1, EPOCH + 1)
    plt.cla()
    plt.plot(EPOCH_times, train_loss_ls, marker='o',
             markerfacecolor='white', markersize=5)
    # 设置数字标签
    i = 0
    for a, b in zip(EPOCH_times, train_loss_ls):
        i += 1
        if i % 10 == 0 or i == EPOCH+1:
            if b != 1:
                b = np.round(b, 3)
            plt.text(a, b, b, ha='center',
                        va='bottom', fontsize=10)
    # 設定圖片標題，以及指定字型設定，x代表與圖案最左側的距離，y代表與圖片的距離
    plt.title("Train_loss", x=0.5, y=1.03)
    # 设置刻度字体大小
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    # 標示x軸(labelpad代表與圖片的距離)
    plt.xlabel("Epoch", fontsize=10)
    # 標示y軸(labelpad代表與圖片的距離)
    plt.ylabel("Loss", fontsize=10)
    plt.savefig("{}/{}train_loss.png".format(save_path, name_mark))

    plt.cla()
    plt.plot(EPOCH_times, train_acc_ls, marker='o',
             markerfacecolor='white', markersize=5)
    i = 0
    for d, e in zip(EPOCH_times, train_acc_ls):
        i += 1
        if i % 10 == 0 or i == EPOCH+1:
            if e != 1:
                try:
                    e = np.round(e, 3)
                except AttributeError:
                    e = np.round(e, 3)
            plt.text(d, e, e,
                     ha='center', va='bottom', fontsize=10)
    plt.plot(EPOCH_times, test_acc_ls, marker='o',
             markerfacecolor='white', markersize=5)
    i = 0
    for a, b in zip(EPOCH_times, test_acc_ls):
        i += 1
        if i % 10 == 0 or i == EPOCH+1:
            if b != 1:
                b = np.round(b, 3)
            plt.text(a, b, b,
                        ha='center', va='top', fontsize=10)
    # 設定圖片標題，以及指(定字型設定，x代表與圖案最左側的距離，y代表與圖片的距離
    plt.title("Accuracy", x=0.5, y=1.03)
    # 设置刻度字体大小
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    # 標示x軸(labelpad代表與圖片的距離)
    plt.xlabel("Epoch", fontsize=10)
    # 標示y軸(labelpad代表與圖片的距離)
    plt.ylabel("Accuracy", fontsize=10)
    plt.savefig("{}/{}acc.png".format(save_path, name_mark))
