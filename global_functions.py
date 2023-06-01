from PySide2.QtWidgets import QTableWidgetItem



def insert_data_to_table(df, table):
    """
        df [obejct: pandas.DataFrame] - dataset to insert to QTableWidget as a pandas DataFrame object
        table - a PySide2 QTableWidget object
    """
    print(df)
    for row in df.itertuples(): # row iterator
        for item in range(len(df)): # iteration over columns (as integer position)
            table.setItem(row[0], item, QTableWidgetItem(str(row[item+1]))) # to debug why only 5 columns are visible, not 7
    