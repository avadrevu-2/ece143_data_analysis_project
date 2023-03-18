# ECE143 Data Analysis Project

## A look into mass layoffs!
This is the codebase for the ECE143 Data Analysis project. In this project, we performed analysis on datasets relating to layoffs.

## Third-Party Modules
```
pandas
numpy
matplotlib
tkinter
scipy
```
We used Pandas to process our data, and Matplotlib and Scipy for plotting. See our requirements.txt file for the full details of all the modules we used, but those three are the main ones.

## How to use

### Create a new python virtual environment:
- Linux/MacOS
```
python3 -m venv path/to/venv
```
- Windows
```
python3 -m venv C:\path\to\venv
```
### Activate the Virtual Environment
- Linux/MacOS
```
source path/to/venv/bin/activate
```
- Windows
```
C:\path\to\venv\Scripts\activate.bat
```
### Install the requirements
```
pip install -r requirements.txt
```

### Data Processing
The data processing functions are stored within data_processing.py. To run all the functions on the data, use the following code:
```
data_directory = 'data'
data_processor = ProcessData(data_directory)
data = data_processor.process()
```

The process() function will first call `read_data.py` to look through the given `data_directory` for files ending in `.csv`. After reading the csv data and converting them to Pandas Dataframes, the `process()` function will run each of the processing functions for their respective files. The processing functions are defined as static methods in the `ProcessData` class. 

To add a new processing function, simply declare it as a static method in the `ProcessData` class with one input parameter which is a Pandas Dataframe. The processing function should then return a Pandas Dataframe with its processed data, which the `process()` function will add into the output dictionary with the key being the name of the function.

### Data Visualization
The data viz code is stored within the `data_viz.ipynb` file. The easiest way to run this is with the Visual Studio Code Jupyter Notebook Extension. This allows you to select the kernel as the Virtual Environment that you created, as we've included the Jupyter Notebook Kernel in the `requirements.txt` so it should already be installed.

Simply run the cells! We've declared a `ProcessData` object as shown above, and we're accessing the processed data through the dictionary that the `process()` function provides. Then we just setup our matplotlib plots and perform the plotting. To add new plots, you can access the processed data you need by refrencing the dictionary with the key being the name of the processing function. See the `data_viz.ipynb` file for examples.

Alternatively, `data_viz.py` is also available and contains the same plotting scripts from `data_viz.ipynb`. Running this opens each plot in sequence.