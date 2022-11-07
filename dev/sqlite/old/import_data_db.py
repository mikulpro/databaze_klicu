import pysqlite3
import glob
import os


def do_directory(dirname, db):
    for filename in glob.glob(os.path.join(dirname, '*.csv')):
        do_file(filename, db)


def do_file(filename, db):
        with open(filename, 'r') as f:
            data = []
            for row in f.readlines():
                if row:
                    row_lst = []
                    for i in row.strip().split(';'):
                        try:
                            row_lst.append(int(i))
                        except ValueError:
                            row_lst.append(i)
                data.append(row_lst)

            table = os.path.splitext(os.path.basename(filename))[0].split('_')[1]
            print(table)

            sql = 'insert into "{table}" values ( {vals} )'.format(
                table=table,
                vals=','.join('?' for col in data[0]))

            for i in data:
                print(i)

            db.executemany(sql, data)


if __name__ == '__main__':
    con = pysqlite3.connect("keys_test.db")
    do_directory('data', con)
    con.commit()

