from sql_manager import SqlManager
import excel_manager
import time

class Arules:
    
    def __init__(self, sql_file, minsup):
        self.sql_manager = SqlManager(sql_file)
        self.sql_file = sql_file
        self.minsup = minsup

        tr_id = self.sql_manager.crs.execute("select DISTINCT  tr_id from transactions")
        self.total_item = len(list(tr_id))
        print("TOTAL ", self.total_item)
        self.minsup_count = self.minsup * self.total_item
    
    def get_frequent_item_sets(self, transactions, min_support, min_confidence):
        pass
    def apriori(self):
        sql_result = self.sql_manager.crs.execute(
            "select  description,count(description) from transactions group by description having count(description) > " + str(self.minsup_count)).fetchall()

        L = [[], []]
        start_time = time.time()
        L[1] = [[x[0]] for x in sql_result]
        print(len(L[1]))
        print("finding L for k=", 1)
        k = 2
        while len(L[k - 1]) != 0:
            print("finish and TIME=", time.time() - start_time)
            print("finding L for k=", k)
            start_time = time.time()
            L.append([])
            CK = self.apriori_gen(L, k)
            for ind, C in enumerate(CK):
                sql = 'select count(distinct tr_id) from transactions2 where '
                for item in C:
                    sql += 'descriptions like ' + '"%*' + str(item) + '%" and '

                sql = sql[:-4]
                size = self.sql_manager.crs.execute(sql).fetchall()[0][0]
                if size > self.minsup_count:
                    L[k].append(C)

            k += 1

        return L
    def apriori_gen(self, l, k):
        CK = []
        L = l
        for index1 in range(len(l[k - 1])):
            l1 = l[k - 1][index1]
            for index2 in range(index1 + 1, len(l[k - 1])):
                l2 = l[k - 1][index2]
                if l1 == l2:
                    continue
                flage = True
                for i in range(k - 2):
                    flage = flage and (l1[i] == l2[i])
                if flage:
                    try:
                        c = l1[:k - 2]
                    except:
                        c = []
                    c.append(l1[k - 2])
                    c.append(l2[k - 2])
                    if self.has_infrequent_subset(c, l, k):
                        continue
                    else:
                        CK.append(c)
        return CK

    def has_infrequent_subset(self, c, l, k):
        if k < 3:
            return False

        if [c[-2], c[-1]] in l[2]:
            return False
        else:
            return True

    def get_arules(self,min_support=None, min_confidence=None, min_lift=None, sort_by='lift'):
        pass
if __name__ == '__main__':
    # minsups = (0.1, 0.2, 0.3, 0.4, 0.05, 0.01)
    minsups = (0.005,)
    for minsup in minsups:
        excel_manager.create_sheet(excel_name="apriori", sheet_name=str(minsup), columns_name=[], base_address="out\\")
        start_time = time.time()
        apriory = Arules("information.sqlit3", minsup)
        large_items = apriory.apriori()
        excel_manager.add_rows(excel_name="apriori", sheet_name=str(minsup), base_address="out\\",
                              datas=[["minsup", str(minsup)], ["time", str(time.time() - start_time)]])

        print(large_items)
        for k, LK in enumerate(large_items):
            if len(LK) != 0:
                excel_manager.add_rows(excel_name="apriori", sheet_name=str(minsup), base_address="out\\", datas=LK)

        print("finish minsup =", minsup)