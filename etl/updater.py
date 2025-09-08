# etl/updater.py
def check_update(record, check_list, flag):
    """
    بررسی اینکه آیا رکوردها تغییر کرده‌اند یا نه
    """

    return record == check_list.loc[flag, "Number"]

def merge_df_func(uncheck_df, flag, diff_sell_count=0):
    """
    ادغام داده‌های جدید فروش در صورت وجود تغییر
    """
    if flag:
        uncheck_df = uncheck_df.loc[diff_sell_count:].copy()
        return uncheck_df
    return None
