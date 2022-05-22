import os
from typing import List
import matplotlib
import matplotlib.pyplot as plt
from PIL import Image

matplotlib.use('AGG')


class ModelPerform(object):
    def __init__(
        self,
        train_loss_ls: List[float] or None = None,
        test_loss_ls: List[float] or None = None,
        train_acc_ls: List[float] or None = None,
        test_acc_ls: List[float] or None = None,
        saveDir: str = './out',
    ) -> None:
        self.num_epoch = len(train_loss_ls)
        self.train_loss_ls = train_loss_ls
        self.test_loss_ls = test_loss_ls
        self.train_acc_ls = train_acc_ls
        self.test_acc_ls = test_acc_ls
        self.saveDir = saveDir

    def save_history_csv(self):
        import pandas as pd

        df = pd.DataFrame(
            {
                'EPOCH': range(1, self.num_epoch + 1),
                'train_acc': self.train_acc_ls if self.train_acc_ls is not None else [None] * self.num_epoch,
                'train_loss': self.train_loss_ls if self.train_loss_ls is not None else [None] * self.num_epoch,
                'test_acc': self.test_acc_ls if self.test_acc_ls is not None else [None] * self.num_epoch,
                'test_loss': self.test_loss_ls if self.test_loss_ls is not None else [None] * self.num_epoch,
            }
        )
        df.to_csv(f'{self.saveDir}/e{self.num_epoch}_history.csv')

    def draw_plot(self, startNumEpoch: int = 10, endNumEpoch: int or None = None, isShow: bool = False, isSave: bool = False):
        if endNumEpoch is None:
            endNumEpoch = self.num_epoch
        epochs = range(startNumEpoch + 1, endNumEpoch + 1)
        plt.clf()

        for key, values_ls in {'Loss': [self.train_loss_ls, self.test_loss_ls], 'Acc': [self.train_acc_ls, self.test_acc_ls]}.items():
            for idx, values in enumerate(values_ls):
                if values is not None:
                    values = values[startNumEpoch:endNumEpoch]
                    best_value = min(values) if key == 'Loss' else max(values)
                    plt.plot(epochs, values)
                    # 設置數字標籤
                    i = startNumEpoch
                    for epoch, value in zip(epochs, values):
                        i += 1
                        if i % (endNumEpoch // 5) == 0 or i == endNumEpoch or best_value == value:
                            plt.text(epoch, value, f'{value:.3e}', ha='center', va=('bottom' if idx == 0 else 'top'), fontsize=10)

            if [True for values in values_ls if values is not None]:
                # 設定圖片標題，以及指定字型設定，x代表與圖案最左側的距離，y代表與圖片的距離
                plt.title(key, x=0.5, y=1.03)
                # 設置刻度字體大小
                plt.xticks(fontsize=10)
                plt.yticks(fontsize=10)
                # 標示x軸(labelpad代表與圖片的距離)
                plt.xlabel('Epoch', fontsize=10)
                # 標示y軸(labelpad代表與圖片的距離)
                plt.ylabel(key, fontsize=10)

                plt.legend(['Train', 'Val'])

                graph_path = f'{self.saveDir}/e{endNumEpoch}_{key}.png'
                plt.savefig(graph_path)
                if isShow:
                    Image.open(graph_path).show()
                if not isSave:
                    os.remove(graph_path)

                plt.clf()
