


def check_count_flag(recorder_df, filter_df, flag):

    df_temp = filter_df.copy()

    if flag == 0:
        return df_temp.shape[0] - recorder_df.loc[0, "Number"], df_temp
    else:
        return df_temp.shape[0] - recorder_df.loc[1, "Number"], df_temp


