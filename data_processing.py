import pandas as pd
import logging
from read_data import ReadData

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ProcessData():
    def __init__(self, data_directory: str) -> None:
        self.data_directory = data_directory
        self.data = {}
        self.processed = {}
        """
        
        """
        self.layoff_functions = [self.__industry_layoffs, self.__country_layoffs]
        self.salary_functions = []
        logger.debug(f'Initialized ProcessData with data directory: {self.data_directory}')

    def process(self) -> dict:
        """
        Process the data and return a dictionary of processed data
        """
        data_reader = ReadData(self.data_directory)
        self.data = data_reader.process()
        for data in self.data:
            if data == 'layoffs':
                self.processed['layoff_processed'] = self.__process_layoffs(self.data[data])
            elif data == 'Levels_Fyi_Salary_Data':
                self.processed['salary_processed'] = self.__process_salary(self.data[data])
        return self.processed

    def __process_layoffs(self, data: pd.DataFrame) -> dict:
        """
        Call all the functions in self.layoff_functions and return a dictionary of results
        """
        logger.debug('Processing layoffs data')
        results = {}
        for func in self.layoff_functions:
            result = func(data)
            results[func.__name__] = result
        return results
        
    def __process_salary(self, data: pd.DataFrame) -> dict:
        """
        Call all the functions in self.salary_functions and return a dictionary of results
        """
        logger.debug('Processing salary data')
        results = {}
        for func in self.salary_functions:
            result = func(data)
            print(result)
            results[func.__name__] = result
        return results
    
    # Processing Functions
    @staticmethod
    def __industry_layoffs(data) -> pd.DataFrame:
        Industry: pd.DataFrame = data[['industry', 'total_laid_off']]
        Industry = Industry.groupby('industry').sum().sort_values(by='total_laid_off', ascending=False)[:10]
        return Industry
    
    @staticmethod
    def __country_layoffs(data) -> pd.DataFrame:
        Country: pd.DataFrame = data[['country', 'total_laid_off']]
        Country = Country.groupby('country').sum().sort_values(by='total_laid_off', ascending=False)[:10]
        return Country


if __name__ == '__main__':
    data_directory = 'data'
    data_processor = ProcessData(data_directory)
    data = data_processor.process()
    print(data)
    