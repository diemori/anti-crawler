import pandas as pd
import matplotlib.pyplot as plt

class AntiCrawl:
    def __init__(self, path='access_log_jul95.csv'):
        self.df = None
        self.load(path)
        self.df_tdall = None

    def load(self, path):
        self.df = pd.read_csv(path, sep='|', encoding='utf-8')
        print("Loading %s" % path)

        print("Removing failed requests..")
        self.df = self.df[self.df['RESULT'] == 200]

        print("Adding day column..")
        self.add_day()

        print("Load Complete %d items" % self.df.shape[0])

    def add_day(self):
        self.df['day'] = self.df.DATE.apply(lambda x: x.split('/')[0])
        self.df.day = pd.to_numeric(self.df.day)

    # return a data frame which is a groupby(uri) result of input data frame
    def get_item_count(self, df_input, col='URI'):
        dlist = list()
        gr = df_input.groupby(col)

        for uri in gr:
            dlist.append({"uri": uri[0], "count": uri[1].shape[0]})

        return pd.DataFrame(dlist).sort_values(by=['count'], ascending=False).reset_index()[['count', 'uri']]

    def _merge_train(self, tot_item, _td3):
        td3 = pd.merge(tot_item, _td3[['count', 'uri']], how='outer', left_on='uri', right_on='uri')

        td3['count'] = td3['count_y']

        self.df = pd.merge(self.df, td3[['uri']], how='outer', left_on='URI', right_on='uri')

        td3 = td3.fillna(0)

        return td3[['uri', 'count']].sort_values(by=['count'], ascending=False).reset_index()

    def plot_dfcount(self, df_count, label=[0.005, 0.1, 0.3]):
        fig_size_x = 5
        fig_size_y = 5

        total = df_count.shape[0]

        zone_01 = int(total * label[0])
        # zone_02 = int(total * label[1])
        zone_03 = int(total * label[2])

        df_count['xlabel'] = df_count.index

        df_count[:zone_01].plot(x='xlabel', y='count', figsize=(fig_size_x, fig_size_y), linewidth=3)
        plt.show()
        print(df_count['count'][:zone_01].describe())

        df_count[zone_01:zone_03].plot(x='xlabel', y='count', figsize=(fig_size_x, fig_size_y), linewidth=3)
        plt.show()
        print(df_count['count'][zone_01:zone_03].describe())

        td3 = df_count[zone_03:]
        td3.plot(x='xlabel', y='count', figsize=(fig_size_x, fig_size_y), linewidth=3)
        plt.show()
        print(df_count['count'][zone_03:].describe())

        return td3

    # td3 taggin 기능
    def get_td3(self, train_date, _label=[0.005, 0.1, 0.3]):
        df_items = self.get_item_count(self.df)

        df_train = self.df[self.df.day < train_date]
        df_train_items = self.get_item_count(df_train)

        td3_train = self._merge_train(df_items, df_train_items)

        self.df_tdall = td3_train
        df_td3 = self.plot_dfcount(td3_train, label=_label)

        all_cnt = df_items.shape[0]
        td3_cnt = df_td3.shape[0]

        print("Count: %d / %d" % (td3_cnt, all_cnt))

        return df_td3


if __name__ == '__main__':
    a = AntiCrawl()

    df_td3 = a.get_td3(25)

