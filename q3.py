import xlsxwriter
from sql_manager import SqlManager
import excel_manager
import itertools
from itertools import combinations, chain

def read_frequents(excel_name , sheet_name , base):
    info = excel_manager.read_rows(excel_name, sheet_name, base)
    freq = []
    for row in range(3, len(info)):
        temp = []
        for val in info[row]:
            if val != None:
                temp.append(val)
        freq.append(temp)
    return freq

# make sub set
def make_subset(frequents):
    possiable_rules = []
    for freq in frequents:
        for k in range(2,len(freq)):
            l1 = list(map(set, itertools.combinations(freq, k)))
            for i in range(len(l1)):
                possiable_rules.append((list(l1[i]), [x for x in freq if x not in list(l1[i])]))
    return possiable_rules

def prepare_data(sql_file, rules):
    sql_manager = SqlManager(sql_file)
    data = {}
    for rule in rules:
        rule = rule + (rule[0]+ rule[1],)
        for side in rule:
            query = 'select count(Descriptions) from transactions2 where '
            temp = ''
            for sub in side:
                query += 'Descriptions like ' + '"%' + str(sub).replace('"', "'") + '%" and '
                temp += str(sub) + ','
            query = query[:-4]
            result = sql_manager.crs.execute(query).fetchall()[0][0]
            temp = temp[:-1]
            data[temp] = result
    tr_number = sql_manager.crs.execute('select COUNT(tr_id) from transactions2').fetchall()[0][0]
    return data, tr_number

# generating rules
def generate_strongs(data, rules_p, tr_number, minconf):
    rules = []
    lefts = []
    rights =[]
    lifts = []
    confs = []
    for rule in rules_p:
        left_str = ','.join(rule[0])
        right_str = ','.join(rule[1])
        left_c = data.get(left_str)
        right_c = data.get(right_str)
        both = data.get(left_str+','+right_str)
        if float(both/left_c) > minconf and both/left_c !=1:
            conf = float(both/left_c)
            lift = (conf * tr_number)/right_c
            confs.append(conf)
            lifts.append(lift)
            rights.append(right_str)
            lefts.append(left_str)
            rules.append(left_str + '---->' + right_str)
        if float(both/right_c) > minconf and both/right_c !=1:
            conf = float(both/right_c)
            lift = (conf * tr_number)/left_c
            confs.append(conf)
            lifts.append(lift)
            rights.append(left_str)
            lefts.append(right_str)
            rules.append(right_str + '---->' + left_str)
    # sort by lift
    data = list(zip(lefts, rights, lifts,rules, confs))
    return sorted(data, key=lambda x:x[2], reverse=True)

def write_strongs(data,wsn, book):
    if(data):
        worksheet = book.add_worksheet(wsn)
        worksheet.write('A1', 'Left')
        worksheet.write('B1', 'Right')
        worksheet.write('C1', 'Lift')
        worksheet.write('D1', 'Rule')
        worksheet.write('E1', 'Confidence')
        for i in range(0, len(data)):
            worksheet.write(i + 1, 0, data[i][0])
            worksheet.write(i + 1, 1, data[i][1])
            worksheet.write(i + 1, 2, data[i][2])
            worksheet.write(i + 1, 3, data[i][3])
            worksheet.write(i + 1, 4, data[i][4])
    return book


if __name__ == '__main__':
    minsups = (0.1, 0.2, 0.3, 0.4, 0.05, 0.01, 0.005)
    # minsups = (0.005,)

    min_cofs = (0.2, 0.6, 0.7, 0.8)
    # min_cofs = (0.6,)

    workbook_apriori = xlsxwriter.Workbook('out' + '\\' + 'rules_apriori' + '.xlsx')
    try:
        for min_sup in minsups:
            frequents = read_frequents('apriori', str(min_sup), 'out')
            rules = make_subset(frequents)
            data, tr_number = prepare_data('information.sqlite3', rules)
            if data and rules:
                for min_cof in min_cofs:
                    result = generate_strongs(data, rules ,tr_number, min_cof)
                    book = write_strongs(data=result,wsn=str(min_sup) + str(min_cof),book=workbook_apriori)
        book.close() 
    except Exception as e:
        raise e