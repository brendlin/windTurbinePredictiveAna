
import pandas as pd

def LoadFile(filename) :
    
    df = pd.read_csv(filename,compression='gzip')
    
    return 0
