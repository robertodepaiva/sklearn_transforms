from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.impute import SimpleImputer
import numpy as numpy
import pandas as pandas

# All sklearn Transforms must have the `transform` and `fit` methods
class DropColumns(BaseEstimator, TransformerMixin):
    def __init__(self, columns):
        self.columns = columns

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        # Primeiro realizamos a cópia do dataframe 'X' de entrada
        data = X.copy()
        # Retornamos um novo dataframe sem as colunas indesejadas
        return data.drop(labels=self.columns, axis='columns')


class AjusteDesafio2(BaseEstimator, TransformerMixin):
    def __init__(self, columns):
        self.columns = columns

    def fit(self, X, y=None):
        return self

    def transform(self, inputdata):
        #altera valores nulos para 6.6 nas notas
        si = SimpleImputer(
            missing_values=numpy.nan,  # os valores faltantes são do tipo ``numpy.nan`` (padrão Pandas)
            strategy='constant',  # a estratégia escolhida é a alteração do valor faltante por uma constante
            fill_value=6.6,  # a constante que será usada para preenchimento dos valores faltantes é um int64=0.
            verbose=0,
            copy=True
        )        # Aplicamos o SimpleImputer ``si`` ao conjunto de dados df_data_2 (resultado da primeira transformação)
        si.fit(X=inputdata)
        # Reconstrução de um novo DataFrame Pandas com o conjunto imputado (df_data_3)
        df_data_3 = pandas.DataFrame.from_records(
            data=si.transform(
                X=inputdata
            ),
            columns=inputdata.columns  # as colunas originais devem ser conservadas nessa transformação
        )

        #recria a coluna INGLES que tera um valor default 1 para os nulos
        # Instanciando uma transformação DropColumns
        rm_columns2 = DropColumns(
            columns=['INGLES']  # Essa transformação recebe como parâmetro uma lista com os nomes das colunas indesejadas
        )
        # Aplicando a transformação ``DropColumns`` ao conjunto de dados base
        rm_columns2.fit(X=df_data_3)

        # Reconstruindo um DataFrame Pandas com o resultado da transformação
        df_data_4 = pandas.DataFrame.from_records(
            data=rm_columns2.transform(
                X=df_data_3
            ),
        )
        df_data_4['INGLES'] = df_data_2['INGLES']
        # Criação de um objeto SimpleImputer
        si = SimpleImputer(
            missing_values=numpy.nan,  # os valores faltantes são do tipo ``numpy.nan`` (padrão Pandas)
            strategy='constant',  # a estratégia escolhida é a alteração do valor faltante por uma constante
            fill_value=1,  # a constante que será usada para preenchimento dos valores faltantes é um int64=0.
            verbose=0,
            copy=True
        )
        si.fit(X=df_data_4)

        df_data_5 = pandas.DataFrame.from_records(
            data=si.transform(
                X=df_data_4
            ),
            columns=df_data_4.columns
        )

        #ajuste dos valores de notas acima de 10.0
        df_data_5['NOTA_DE'] = df_data_4[df_data_4['NOTA_DE'] < 10.0]['NOTA_DE'].copy()
        df_data_5['NOTA_EM'] = df_data_4[df_data_4['NOTA_EM'] < 10.0]['NOTA_EM'].copy()
        df_data_5['NOTA_MF'] = df_data_4[df_data_4['NOTA_MF'] < 10.0]['NOTA_MF'].copy()
        df_data_5['NOTA_GO'] = df_data_4[df_data_4['NOTA_GO'] < 10.0]['NOTA_GO'].copy()
        si = SimpleImputer(
            missing_values=numpy.nan,  # os valores faltantes são do tipo ``numpy.nan`` (padrão Pandas)
            strategy='constant',  # a estratégia escolhida é a alteração do valor faltante por uma constante
            fill_value=10.0,  # a constante que será usada para preenchimento dos valores faltantes é um int64=0.
            verbose=0,
            copy=True
        )
        # Aplicamos o SimpleImputer ``si`` ao conjunto de dados df_data_2 (resultado da primeira transformação)
        si.fit(X=df_data_5)
        df_data_6 = pandas.DataFrame.from_records(
            data=si.transform(
                X=df_data_5
            ),  # o resultado SimpleImputer.transform(<<pandas dataframe>>) é lista de listas
            columns=df_data_5.columns  # as colunas originais devem ser conservadas nessa transformação
        )

        #criacao de novas colunas MENOR_H, MENOR_E e BAD
        df_data_6['MENOR_H'] = df_data_6['NOTA_DE']
        df_data_6['MENOR_E'] = df_data_6['NOTA_MF']

        for index, row in df_data_6.iterrows():
            #alunos com reprovacao necessitam mentoria, entao a nota nao eh zero (diferenciar)
            if row.REPROVACOES_DE > 0.0 :
                df_data_6.at[index, 'NOTA_DE'] = -10.0;
            if row.REPROVACOES_EM > 0.0 :
                df_data_6.at[index, 'NOTA_EM'] = -10.0;
            if row.REPROVACOES_MF > 0.0 :
                df_data_6.at[index, 'NOTA_MF'] = -10.0;
            if row.REPROVACOES_GO > 0.0 :
                df_data_6.at[index, 'NOTA_GO'] = -10.0;

            #calculo das menores notas
            df_data_6.at[index, 'MENOR_E'] = min(df_data_6.at[index, 'NOTA_MF'], df_data_6.at[index, 'NOTA_GO']);
            df_data_6.at[index, 'MENOR_H'] = min(df_data_6.at[index, 'NOTA_EM'], df_data_6.at[index, 'NOTA_DE']);

            #calculo dos outliers diferenciando os motivos
            if (row.PERFIL == 'HUMANAS' and (df_data_6.at[index, 'MENOR_H'] > 8 or df_data_6.at[index, 'MENOR_E'] < 6)) :
                df_data_6.at[index, 'BAD'] = 1;
            elif (row.PERFIL == 'EXATAS' and (df_data_6.at[index, 'MENOR_E'] > 7 or df_data_6.at[index, 'MENOR_H'] < 6)) :
                df_data_6.at[index, 'BAD'] = 2;
            elif (row.PERFIL == 'DIFICULDADE' and (df_data_6.at[index, 'MENOR_E'] > 6.6 or df_data_6.at[index, 'MENOR_H'] > 6.6)) :
                df_data_6.at[index, 'BAD'] = 3;
            elif (row.PERFIL == 'EXCELENTE' and (df_data_6.at[index, 'MENOR_E'] < 8 and df_data_6.at[index, 'MENOR_H'] < 8)) :
                df_data_6.at[index, 'BAD'] = 4;
            elif (row.PERFIL == 'MUITO_BOM' and (df_data_6.at[index, 'MENOR_E'] < 6 and df_data_6.at[index, 'MENOR_H'] < 6)) :
                df_data_6.at[index, 'BAD'] = 5;
            else:
                df_data_6.at[index, 'BAD'] = 0;

        return df_data_6;
