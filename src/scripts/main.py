"""Projeto Netflix dataset"""

#importes  necessárias para o projeto
import pandas as pd
import os
import glob

# definir caminho para ler os arquivos
folder_path = 'src\\data\\raw'

# definir caminho para saida 
output_path = os.path.join('src', 'data', 'ready', 'clean.xlsx')

# listar todos os arquivos excel
excel_files = glob.glob(os.path.join(folder_path, "*.xlsx"))


# Tratamento 
if not excel_files:
    print("Nenhum arquivo foi encontrado")
else:
  # dataframe  = tabela na memória para guardar os conteúdos dos arquivos
  dfs = []
     
  # percorre os arquivos
  for excel_file in excel_files:
        
    try:
        # ler arquivo
        dfs_temp = pd.read_excel(excel_file)
            
        # ler nome do arquivo excel
        file_name = os.path.basename(excel_file)
            
        # criar column com nome do arquivo de origem
        dfs_temp['Origin_File']= file_name
            
        # criar column Location para manter a rastreabilidade
        if 'brasil' or 'brazil' in file_name.lower():
            dfs_temp['Location'] = 'BR'
        elif 'italian' in file_name.lower():
            dfs_temp['Location'] = 'IT'
        elif 'France' in file_name.lower():
            dfs_temp['Location'] = 'FR'  
                
        # criar column Campaing para identificar as campanhas para analise 
        dfs_temp['campaing'] = dfs_temp['utm_link'].str.extract(r'utm_campaign=(.*)')
            
        # guardar os dados tratados dentro do dataframe
        dfs.append(dfs_temp)
            
    except Exception as e:
        print(f"Erro ao ler arquivo {file_name}: {e}")
            
    
    # Se o  dataframe não estiver vazio
    if dfs:
        #concatena todas as tabelas salvas no dfs em uma unica tabela
        result = pd.concat(dfs, ignore_index=True)
        #caminho de saída
        output_file = output_path

        #configurou o motor de escrita
        writer = pd.ExcelWriter(output_file, engine='xlsxwriter')

        # leva os dados do resultado a serem escritos no motor de excel configurado
        result.to_excel(writer, index=False)

        #salva o arquivo de excel
        writer._save()

    else:
        print("nenhum dado for processado")