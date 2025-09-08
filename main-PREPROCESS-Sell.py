# main.py
import pandas as pd
from etl.config import read_table_from_sql, save_table_to_sql
from etl.preprocess import preprocessing
from etl.updater import check_update, merge_df_func
from etl.customer_utils import check_customer_id, get_visitor_id
from etl.check_count_flag import check_count_flag
from etl.log import write_massege


def main():

    recorder_df = read_table_from_sql("Fact_Recorder")
    first_record = recorder_df.loc[0, "Number"]
    df = read_table_from_sql("AlirezaSales")


    # input("دیتا بارگذاری شد. ادامه؟")

    filtered_df = preprocessing(df)
    sell_flag = 0

    if not check_update(df.shape[0], recorder_df, 0):
        map_df = read_table_from_sql("Bridge_Vistor_Customer")

        sell_count_flag, sell_df_temp = check_count_flag(recorder_df, filtered_df, 0)

        if sell_count_flag != 0:
            sell_flag = 1

            uncheck_sell_df = sell_df_temp.tail(int(sell_count_flag)).copy()
            uncheck_sell_df.loc[:, "Date"] = uncheck_sell_df["shamsi_date"].str[:7] + "/01"

            visitor_ids = []
            map_df_temp = pd.DataFrame(columns=['Customer_ID','visitor_id'])
            for customer_id in uncheck_sell_df['Customer_ID']:
                visitor_id, map_df_temp = get_visitor_id(customer_id, map_df, map_df_temp)

                visitor_ids.append(visitor_id)

            uncheck_sell_df['visitor_id'] = visitor_ids

            save_table_to_sql(uncheck_sell_df, "Fact_Sell", "append")
            recorder_df.loc[0, "Number"] = sell_df_temp.shape[0]

        save_table_to_sql(recorder_df, "Fact_Recorder", "replace")


        save_table_to_sql(map_df_temp, "Bridge_Vistor_Customer", "append")
        sec_record = recorder_df.loc[0, "Number"]
        write_massege(first_record, sec_record, 0)


    if sell_flag:

        uncheck_df = merge_df_func(uncheck_sell_df, sell_flag)
        custom_df = read_table_from_sql("Dim_Custom")

        new_customers = check_customer_id(uncheck_df['Customer_ID'].unique(), custom_df)

        if new_customers:
            # ادامه همان ساخت custom_df_temp و map_df_temp
            custom_df_temp = pd.DataFrame(columns=['name', 'Customer_ID', 'Geographic_Customer_Group', 'Customer_Group'])

            custom_df_temp[['Customer_ID', 'name']]= uncheck_df[uncheck_df['Customer_ID'].isin(new_customers)][
                ['Customer_ID', 'custname']]

            custom_df_temp.drop_duplicates(inplace=True)
            custom_df_temp.reset_index(drop=True, inplace=True)

            custom_df_temp['Customer_Group'] = 'مشهد'
            custom_df_temp['Geographic_Customer_Group'] = '0'


            save_table_to_sql(custom_df_temp, "Dim_Custom", "append")


if __name__ == "__main__":
    main()
