import glob
import os
import pandas as pd


class DataProcessing():
    """
    A class for dataprocessing CSV files in a directory.

    Attributes
    ----------
    data_directory: str
        The filepath of the data directory

    Public Methods
    ----------
    process():
        Returns a dictionary, key is the name of the dataset
        value is the DataFrame for that dataset

    """
    def __init__(self, data_directory: str) -> None:
        self.data_dir = data_directory
    
    def process(self) -> dict:
        """
        Finds all CSVs in the data directory, processes them into
        DataFrames, and returns a dictionary w/ all of them.
        """
        all_data = {}
        csv_names = self.__find_csvs()
        for csv_name in csv_names:
            csv_data = self.__process_csv(csv_name)
            data_name = csv_name.split('\\')[-1].replace('.csv', '')
            all_data[data_name] = csv_data
        return all_data

    def __find_csvs(self) -> list:
        """
        Uses glob module to recursively find all .csv files in the directory
        """
        return glob.glob(os.path.join(self.data_dir, '*.csv'), recursive=True)
            
    def __process_csv(self, filepath: str) -> pd.DataFrame:
        """
        Uses Pandas read_csv method to load the data into a dataframe
        """
        return pd.read_csv(filepath)


if __name__ == '__main__':
    data_directory = 'data'
    processor = DataProcessing(data_directory)
    data = processor.process()
    print(data)
    