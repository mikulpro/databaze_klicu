# import dev.sqlite.utils as utils

def print_select(statement, cursor_obj):
    cursor_obj.execute(statement)

    print("All the data")
    output = cursor_obj.fetchall()
    print(len(output))
    print(output[0].keys())
    for row in output:
        print(row)