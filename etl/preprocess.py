# etl/preprocess.py
import pandas as pd

def preprocessing(filtered_df, flag=0):
    """
    حذف ستون‌های اضافی و استانداردسازی نام ستون‌ها
    """
    # print(filtered_df)
    filtered_df.drop(['مبلغ', 'کاهنده', 'عنوان گروه مشتری'], axis=1, inplace=True)
    filtered_df['کد تگ 1'] = 0
    # print(filtered_df.head())
    if flag == 1:
        filtered_df.columns = ['ID', 'invckind','invcno', 'shamsi_date', 'Customer_ID', 'custname',
                               'itemno', 'description', 'qty','fee', 'netvalue', 'visitor_id']
    else:
        filtered_df.columns = ['ID', 'invckind', 'invcno', 'shamsi_date', 'Customer_ID', 'custname',
                               'itemno', 'description', 'qty', 'fee', 'netvalue', 'visitor_id']

    filtered_df['Tarikh_komaki'] = filtered_df['shamsi_date'].str.replace("/", "")
    # print(filtered_df.head())
    return filtered_df
