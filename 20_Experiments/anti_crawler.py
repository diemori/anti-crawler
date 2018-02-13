import pandas as pd
import matplotlib.pyplot as plt

class AntiCrawl:
    def __init__(self):
        self.df = None
        self.load()

    def load(self, path='access_log_jul95.csv'):
        self.df = pd.read_csv(path, sep='|', encoding='utf-8')
        print(self.df.head(5))
        self.add_day()

    def add_day(self):
        self.df['day'] = self.df.DATE.apply(lambda x: x.split('/')[0])
        self.df.day = pd.to_numeric(self.df.day)

    def get_item_count(self, df_input, col='URI'):
        dlist = list()
        gr = df_input.groupby(col)

        for uri in gr:
            dlist.append({"uri": uri[0], "count": uri[1].shape[0]})

        return pd.DataFrame(dlist).sort_values(by=['count'], ascending=False).reset_index()[['count', 'uri']]

    def _gen_td3(self, tot_item, _td3):
        td3 = pd.merge(tot_item, _td3[['count', 'uri']], how='outer', left_on='uri', right_on='uri')

        # print(td3[['uri', 'count']].head(5))

        td3['count'] = td3['count_y']

        td3 = td3.fillna(1)

        return td3[['uri', 'count']].sort_values(by=['count'], ascending=False).reset_index()

    def plot_dfcount(self, df_count, label=[0.005, 0.1, 0.25]):
        fig_size_x = 5
        fig_size_y = 5

        total = df_count.shape[0]

        zone_01 = int(total * label[0])
        zone_02 = int(total * label[1])
        zone_03 = int(total * label[2])

        print(zone_01, zone_02, zone_03)

        df_count['xlabel'] = df_count.index

        df_count[:zone_01].plot(x='xlabel', y='count', figsize=(fig_size_x, fig_size_y), linewidth=3)
        plt.show()
        print(df_count['count'][:zone_01].describe())

        df_count[zone_01:zone_02].plot(x='xlabel', y='count', figsize=(fig_size_x, fig_size_y), linewidth=3)
        plt.show()
        print(df_count['count'][zone_01:zone_02].describe())

        df_count[zone_02:zone_03].plot(x='xlabel', y='count', figsize=(fig_size_x, fig_size_y), linewidth=3)
        plt.show()
        print(df_count['count'][zone_02:].describe())

        td3 = df_count[zone_03:]
        td3.plot(x='xlabel', y='count', figsize=(fig_size_x, fig_size_y), linewidth=3)
        plt.show()
        print(df_count['count'][zone_02:].describe())

        return td3

    def get_td3(self):
        df_items = self.get_item_count(self.df)

        df_15 = self.df[self.df.day < 15]
        df_15_items = self.get_item_count(df_15)

        td3_15 = self._gen_td3(df_items, df_15_items)

        return self.plot_dfcount(td3_15)

if __name__ == '__main__':
    a = AntiCrawl()

    a.get_td3()