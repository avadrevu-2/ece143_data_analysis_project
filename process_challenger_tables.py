# This was created as an aid in extracting the tables presented in
# the Job Cuts reports from https://www.challengergray.com/
# The randomly formatted table entries are copied from the PDF and pasted
# into a text file
# Limitations: Since the only consistent field delimiter is white space,
# fields filled with empty space in the PDF need to be manually
# filled in the text file.

import fileinput
import sys
import string
import os
from tkinter import simpledialog


def feed_words(ip_file:str) -> str:
    '''feed words one at a time from txt file'''
    with open(ip_file,'r') as ip_data:
        for line in ip_data:
            for word in line.split():
                yield word

def csv_from_txt(input_file:str,output_file,columns=4) -> None:
    '''Converts text tables extracted from Challenger pdf's to csv'''
    assert isinstance(columns,int) and columns>0, 'Should have at least 1 column...'
    with open(output_file,'w') as op_file:
        count=0
        new_line=[]
        for word in feed_words(input_file):
            new_line.append(word.replace(',','') +', ')
            count+=1
            if not count%columns:
                last_word=new_line.pop()
                new_line.append(last_word[:-2])
                new_line.append('\n')
                op_file.write(''.join(new_line))
                new_line=[]

def substitute_str(the_file: str, replacements: dict) -> None:
    '''Does specific string replacements in a text file.'''
    for line in fileinput.input(the_file, inplace=1):
        for search_exp,subst_exp in replacements.items():
            if search_exp in line:
                line=line.replace(search_exp,subst_exp)
        sys.stdout.write(line)

def underscore_text_entries(the_file: str) -> None:
    '''
    Specific for these tables where any text field is next
    to a numeric field. Underscores are not placed between
    (text or punctuation) and numbers.
    '''
    punct = string.punctuation
    for line in fileinput.input(the_file, inplace=1):
        for idx,ch in enumerate(line):
            if (ch.isspace() 
                and idx>0 
                and idx<len(line)-2
                and (line[idx-1].isalpha() 
                     or line[idx-1] in punct)
                and (line[idx+1].isalpha() 
                     or line[idx+1] in punct)
                ):
                search_exp=line[idx-1:idx+2]
                subst_exp=line[idx-1]+'_'+line[idx+1]
                line=line.replace(search_exp,subst_exp)
        sys.stdout.write(line)

def remove_multiple_space(the_file: str) -> None:
    '''Changes done inline on text files'''
    for line in fileinput.input(the_file, inplace=1):
        line=(' '.join(line.split()))
        line=(' '.join([line,'\n']))
        sys.stdout.write(line)

        
if __name__=="__main__":
    temp_file='challenger.txt'
    assert os.path.isfile(temp_file),"check the input file"
    # Purpose of replacements: we have space separated fields
    # with field entries that contain spaces...
    # Need to ensure the only spaces in the text
    # are between fields.
    replacements = {'9 R':'9_R',    # ex: ..vid-19 Recov...
                    ',':'',
                    }
    output_file=simpledialog.askstring('Process Challenger Tables', 'Enter file name:\t\t\t')
    if not output_file:
        raise ValueError
    output_file=os.path.join('data/challenger_data',output_file+'.csv')
    substitute_str(temp_file,replacements)
    remove_multiple_space(temp_file)
    underscore_text_entries(temp_file)
    columns=simpledialog.askinteger('Process Challenger Tables', 'Enter number of columns:\t\t\t')
    if not columns:
        raise ValueError
    csv_from_txt(temp_file,output_file,columns)
