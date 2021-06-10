import pandas as pd
import numpy as np

df = pd.read_csv(r"Unconventional_Oil_Gas\Data\info_pozos.csv")

filtered = df[df['sub_tipo_recurso']== 'TIGHT']
filtered = filtered.to_dict()

dff = pd.DataFrame.from_dict(filtered)
dff = dff[dff['empresa'] == 'OILSTONE ENERGIA S.A.']
dff = dff[dff['tipopozo'] == 'Petrolífero']



n_pozos_petroleo = dff.shape[0]
pozos_petroleo = f'Pozos Petróleros: {n_pozos_petroleo}'  
