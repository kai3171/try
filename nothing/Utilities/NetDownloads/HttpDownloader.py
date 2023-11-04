'''
@author: SHENGKUN
@Time  : 2022/10/02 12:28
'''
import os
import time
import urllib
import logging
import requests
import subprocess
from multiprocessing import Process
from urllib import request, error
from MethylationEvaluation.Utilities.FileDealers.FileSystem import *

class HTTP:
    """
    Downloading specific data source files with responding url in config file.
    """

    @staticmethod
    def DownLoad( url:str, local_path:str, file_name:str):
        p1 = Process(target=HTTP.GetData, args=(url, local_path, file_name), name=file_name)
        p1.start()
        return os.getpid()

    @staticmethod
    def GetData( url:str, local_path:str, file_name:str):
        log_path = './test.log'
        logger = logging.getLogger('HttpDownloader')
        logger.setLevel(logging.INFO)
        fh = logging.FileHandler(log_path)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        logger.info('supprocess : %s，parent process : %s' % (os.getpid(), os.getppid()))

        try:
            start = time.time()
            folder_is_exists.__func__(local_path)
            file_is_exists.__func__(file_name)
            subprocess.call(f"wget {url} -O {local_path + file_name}", timeout=600, shell=True)

        except subprocess.TimeoutExpired as e:
            raise subprocess.SubprocessError("%s was terminated as of timeout!!" % e.cmd)

        except error.URLError as e:
            raise urllib.error.URLError(" :TIME OUT!!")

        except requests.exceptions.ConnectionError:
            logger.error('ConnectionError')
            raise requests.exceptions.ConnectionError

        except requests.exceptions.ChunkedEncodingError:
            logger.error('ChunkedEncodingError')
            raise requests.exceptions.ChunkedEncodingError

        except Exception as e:
            logger.info("UnKnown error ：{}".format(e))

        else:
            logger.info(f'{file_name} Success')


        finally:
            end = time.time()
            timeusage = end-start
            logger.info("Time usage: %.2f" %(end - start) + " second")
        return timeusage

if __name__ == '__main__':
    url = 'https://ftp.ncbi.nlm.nih.gov/geo/series/GSE72nnn/GSE72775/matrix/GSE72775_series_matrix.txt.gz'
    local_path = './'
    file_name = 'GSE72775_series_matrix.txt.gz'

    task = HTTP.DownLoad(url,local_path, file_name)

    # task = HTTP.DownLoad('https://smpdb.ca/downloads/smpdb_pathways.csv.zip',
    #                   '../../data_kk/smpdb/pathway/', '6')


