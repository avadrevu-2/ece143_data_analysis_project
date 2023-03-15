import pandas as pd
import logging
from read_data import ReadData

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


class ProcessData():
    def __init__(self, data_directory: str) -> None:
        self.data_directory = data_directory
        self.data = {}
        self.processed = {}
        """
        ******
        Add your functions to the lists below
        ******
        """
        self.layoff_functions = [self.__industry_layoffs, self.__country_layoffs, self.__company_layoffs, self.__company_funding_stage, self.__company_funding_raised]
        self.salary_functions = [self.__company_comp_salaries]
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
            elif data == 'salaries':
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
            results[func.__name__] = result
        return results
    
    # Processing Functions
    @staticmethod
    def __industry_layoffs(data) -> pd.DataFrame:
        industry: pd.DataFrame = data[['industry', 'total_laid_off']]
        industry = industry.groupby('industry').sum().sort_values(by='total_laid_off', ascending=False)
        return industry
    
    @staticmethod
    def __country_layoffs(data) -> pd.DataFrame:
        country: pd.DataFrame = data[['country', 'total_laid_off']]
        country = country.groupby('country').sum().sort_values(by='total_laid_off', ascending=False)
        return country

    @staticmethod
    def __company_layoffs(data) -> pd.DataFrame:
        company: pd.DataFrame = data[['company', 'total_laid_off']]
        company = company.groupby('company').sum().sort_values(by='total_laid_off', ascending=False)
        return company

    @staticmethod
    def __company_comp_salaries(data) -> pd.DataFrame:
        company: pd.DataFrame = data[['company', 'totalyearlycompensation']]
        salaries = company.groupby('company').sum().sort_values(by='totalyearlycompensation', ascending=False)
        return salaries
    
    @staticmethod
    def __company_funding_stage(data) -> pd.DataFrame:
        funds: pd.DataFrame = data[['company', 'stage', 'funds_raised', 'total_laid_off']]
        funds = funds[~funds['stage'].isin(['Post-IPO', 'Acquired', 'Unknown', 'Private Equity', 'Subsidiary'])]
        stage_data = funds.groupby('stage').mean().sort_values(by='total_laid_off', ascending=False)
        stage_data['Funds raised per Layoff'] = stage_data['funds_raised'].div(stage_data['total_laid_off'])
        return stage_data
    
    @staticmethod
    def __company_funding_raised(data) -> pd.DataFrame:
        funds: pd.DataFrame = data[['company', 'stage', 'funds_raised', 'total_laid_off']]
        funds = funds[~funds['stage'].isin(['Post-IPO', 'Acquired', 'Unknown', 'Private Equity', 'Subsidiary'])]
        return funds[['funds_raised', 'total_laid_off']]

if __name__ == '__main__':
    data_directory = 'data'
    data_processor = ProcessData(data_directory)
    data = data_processor.process()
    # print(data)
    