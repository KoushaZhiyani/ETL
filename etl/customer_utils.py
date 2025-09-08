# etl/customer_utils.py

import pandas as pd
def check_customer_id(list_customer, custom_df):
    """
    بررسی اینکه آیا مشتری جدید داریم یا نه
    """
    return [i for i in list_customer if i not in custom_df['Customer_ID'].tolist()]


def get_visitor_id(customer_id, map_df, map_df_temp):
    """
    گرفتن visitor_id برای یک مشتری مشخص یا گرفتن از کاربر در صورت نبود
    همچنین بروزرسانی map_df با مشتری جدید
    """
    result1 = map_df[map_df['Customer_ID'] == customer_id]
    result2 = map_df_temp[map_df_temp['Customer_ID'] == customer_id]
    # print(customer_id)
    # print(result1)
    # print(result2)
    if not result1.empty:
        # print("not result1.empty")
        return result1.iloc[0]['visitor_id'], map_df_temp
    elif not result2.empty:
        return result2.iloc[0]['visitor_id'], map_df_temp

    # در صورت نبود، از کاربر بپرس
    # visitor_id = int(input(f"{customer_id} not found! Enter visitor_id: "))
    visitor_id = 0

    # ساخت یک ردیف جدید به عنوان DataFrame
    new_row = pd.DataFrame([{
        'Customer_ID': customer_id,
        'visitor_id': visitor_id
    }])

    # اضافه کردن ردیف جدید
    map_df_temp = pd.concat([map_df_temp, new_row], ignore_index=True)

    return visitor_id, map_df_temp
