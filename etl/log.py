from datetime import datetime


def write_massege(a, b, flag):

    message1 = f"Sell Record Prev: {a}, Sell Record Now: {b}"
    message2 = f"Return Record Prev: {a}, Return Record Now: {b}"
    message3 = f"Hash Record Prev: {a}, Hash Record Now: {b}"

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if flag == 0:
        log_message = f"{timestamp} - {message1}"

        with open("log/my_log_sell.txt", "a", encoding="utf-8") as f:
            f.write(log_message + "\n")
    elif flag == 1:
        log_message = f"{timestamp} - {message2}"

        with open("log/my_log_return.txt", "a", encoding="utf-8") as f:
            f.write(log_message + "\n")

    else:

        log_message = f"{timestamp} - {message3}"

        with open("log/my_log_hash.txt", "a", encoding="utf-8") as f:
            f.write(log_message + "\n")


    print("Done LOG!")