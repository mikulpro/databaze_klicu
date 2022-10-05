import pysqlite3


def export_to_csv(table, db="keys_test.db"):
    con = pysqlite3.connect(db)
    cursor_obj = con.cursor()

    statement = f"SELECT * FROM {table};"
    cursor_obj.execute(statement)
    output = cursor_obj.fetchall()

    with open(f"data/export_{table}.csv", "w") as outfile:
        for row in output:
            for i in range(len(row)):
                outfile.write(str(row[i]))
                if i < (len(row)-1):
                    outfile.write(";")
            outfile.write("\n")

    # Close the connection
    con.close()


if __name__ == "__main__":
    TABLE = "RoomTypes"
    export_to_csv(TABLE)