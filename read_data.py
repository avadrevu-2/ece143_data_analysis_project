import glob
import os
import pandas as pd
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ReadData():
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
        logger.debug(f'Initialized ReadData with data directory: {self.data_dir}')
    
    def process(self) -> dict:
        """
        Finds all CSVs in the data directory, processes them into
        DataFrames, and returns a dictionary w/ all of them.
        """
        all_data = {}
        csv_names = self.__find_csvs()
        for csv_name in csv_names:
            try:
                csv_data = self.__process_csv(csv_name)
                data_name = os.path.split(csv_name)[-1].split('.')[0]
                all_data[data_name] = csv_data
            except Exception as e:
                logger.error(f'Error processing {csv_name}: {e}')
        logger.debug(f'Processed {len(all_data)} datasets')
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
        data = pd.read_csv(filepath)
        return data


if __name__ == '__main__':
    data_directory = 'data'
    processor = ReadData(data_directory)
    data = processor.process()
    print(data)
    