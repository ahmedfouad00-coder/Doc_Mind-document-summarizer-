
# data_prep stub: looks for functions named load_data / prepare_data in notebook_code.py
import os
from importlib import util

nb_path = os.path.join(os.path.dirname(__file__), 'notebook_code.py')
spec = util.spec_from_file_location('deepseek_nb', nb_path)
nb = util.module_from_spec(spec)
spec.loader.exec_module(nb)

if __name__ == '__main__':
    for fn in ('prepare_data','load_data','data_prep'):
        if hasattr(nb, fn):
            print(f'Calling {fn}() from notebook_code.py')
            try:
                getattr(nb, fn)()
            except Exception as e:
                print('Error when calling', fn, e)
            break
    else:
        print('No data preparation function found in notebook_code.py. Inspect the file and adapt scripts/data_prep.py accordingly.')
