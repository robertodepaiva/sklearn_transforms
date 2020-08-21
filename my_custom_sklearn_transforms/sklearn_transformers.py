from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.impute import SimpleImputer
import numpy
import pandas

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
    def __init__(self, min_excelente, min_muitobom, min_exatas, min_humanas):
        self.MIN_EXCELENTE = min_excelente
        self.MIN_MUITO_BOM = min_muitobom
        self.MIN_EXATAS = min_exatas
        self.MIN_HUMANAS = min_humanas
        self.MAX_NOTA = 10.0

    def fit(self, inputdata, results=None):
        self.calcula(
            inputdata=inputdata, 
            results=results,
            dofit=True)
        return self
    
    def transform(self, inputdata):
        print("transform inputdata.columns = ")
        print(inputdata.columns)
        return self.calcula(
            inputdata=inputdata, 
            results=None,
            dofit=False
        )
        

    #def transform(self, inputdata):
    def calcula(self, inputdata, results=None, dofit=False):
        print("fit inputdata.columns = ")
        print(inputdata.columns)
        if not results is None:
            print("fit results exist = ")
            print(results[1])
        #altera valores nulos para 6.6 nas notas
        si = SimpleImputer(
            missing_values=numpy.nan,  # os valores faltantes são do tipo ``numpy.nan`` (padrão Pandas)
            strategy='constant',  # a estratégia escolhida é a alteração do valor faltante por uma constante
            fill_value=6.6,  # a constante que será usada para preenchimento dos valores faltantes é um int64=0.
            verbose=0,
            copy=True
        )
        si.fit(X=inputdata)

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
        df_data_4['INGLES'] = inputdata['INGLES']
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
        df_data_5['NOTA_DE'] = df_data_4[df_data_4['NOTA_DE'] < self.MAX_NOTA]['NOTA_DE'].copy()
        df_data_5['NOTA_EM'] = df_data_4[df_data_4['NOTA_EM'] < self.MAX_NOTA]['NOTA_EM'].copy()
        df_data_5['NOTA_MF'] = df_data_4[df_data_4['NOTA_MF'] < self.MAX_NOTA]['NOTA_MF'].copy()
        df_data_5['NOTA_GO'] = df_data_4[df_data_4['NOTA_GO'] < self.MAX_NOTA]['NOTA_GO'].copy()
        si = SimpleImputer(
            missing_values=numpy.nan,  # os valores faltantes são do tipo ``numpy.nan`` (padrão Pandas)
            strategy='constant',  # a estratégia escolhida é a alteração do valor faltante por uma constante
            fill_value=self.MAX_NOTA,  # a constante que será usada para preenchimento dos valores faltantes é um int64=0.
            verbose=0,
            copy=True
        )
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
                df_data_6.at[index, 'NOTA_DE'] = 0.0 - self.MAX_NOTA;
            if row.REPROVACOES_EM > 0.0 :
                df_data_6.at[index, 'NOTA_EM'] = 0.0 - self.MAX_NOTA;
            if row.REPROVACOES_MF > 0.0 :
                df_data_6.at[index, 'NOTA_MF'] = 0.0 - self.MAX_NOTA;
            if row.REPROVACOES_GO > 0.0 :
                df_data_6.at[index, 'NOTA_GO'] = 0.0 - self.MAX_NOTA;

            #calculo das menores notas
            df_data_6.at[index, 'MENOR_E'] = min(df_data_6.at[index, 'NOTA_MF'], df_data_6.at[index, 'NOTA_GO']);
            df_data_6.at[index, 'MENOR_H'] = min(df_data_6.at[index, 'NOTA_EM'], df_data_6.at[index, 'NOTA_DE']);
            if dofit:
                if (results[index] == 'HUMANAS' and (df_data_6.at[index, 'MENOR_E'] < self.MIN_EXATAS or df_data_6.at[index, 'MENOR_H'] > self.MIN_HUMANAS)) :
                    df_data_6.at[index, 'BAD'] = 1;
                elif (results[index] == 'EXATAS' and (df_data_6.at[index, 'MENOR_E'] > self.MIN_EXATAS or df_data_6.at[index, 'MENOR_H'] < self.MIN_HUMANAS)) :
                    df_data_6.at[index, 'BAD'] = 2;
                elif (results[index] == 'DIFICULDADE' and (df_data_6.at[index, 'MENOR_E'] > self.MIN_EXATAS or df_data_6.at[index, 'MENOR_H'] > self.MIN_HUMANAS)) :
                    df_data_6.at[index, 'BAD'] = 3;
                elif (results[index] == 'EXCELENTE' and (df_data_6.at[index, 'MENOR_E'] < self.MIN_EXCELENTE and df_data_6.at[index, 'MENOR_H'] < self.MIN_EXCELENTE)) :
                    df_data_6.at[index, 'BAD'] = 4;
                elif (results[index] == 'MUITO_BOM' and (df_data_6.at[index, 'MENOR_E'] < self.MIN_EXATAS and df_data_6.at[index, 'MENOR_H'] < self.MIN_HUMANAS)) :
                    df_data_6.at[index, 'BAD'] = 5;
                else:
                    df_data_6.at[index, 'BAD'] = 0;
            else:
                #calculo das avaliacoes de notas
                if ((df_data_6.at[index, 'MENOR_H'] > self.MIN_HUMANAS and df_data_6.at[index, 'MENOR_E'] < self.MIN_EXATAS)) :
                    df_data_6.at[index, 'BAD'] = 1;#EXATAS
                elif ((df_data_6.at[index, 'MENOR_E'] > self.MIN_EXATAS and df_data_6.at[index, 'MENOR_H'] < self.MIN_HUMANAS)) :
                    df_data_6.at[index, 'BAD'] = 2;#HUMANAS
                elif ((df_data_6.at[index, 'MENOR_E'] < self.MIN_EXATAS and df_data_6.at[index, 'MENOR_H'] < self.MIN_HUMANAS)) :
                    df_data_6.at[index, 'BAD'] = 3;#DIFICULDADE
                elif ((df_data_6.at[index, 'MENOR_E'] < self.MIN_EXCELENTE or df_data_6.at[index, 'MENOR_H'] < self.MIN_EXCELENTE)) :
                    df_data_6.at[index, 'BAD'] = 4;#MUITO_BOM
                elif ((df_data_6.at[index, 'MENOR_E'] > self.MIN_EXCELENTE and df_data_6.at[index, 'MENOR_H'] > self.MIN_EXCELENTE)) :
                    df_data_6.at[index, 'BAD'] = 5;#EXCELENTE
                else:
                    df_data_6.at[index, 'BAD'] = 0;

        return df_data_6;
