# src

Nessa pasta estão scripts gerais para execução do projeto, como criação do bucket s3, upload de dados no bucket e verificação de arquivos do bucket S3. Portanto, segue abaixo um resumo sobre o que cada script dessa pasta faz:

- `create-container.py` -> Cria o container ECR do projeto na AWS;

- `create_bucket.py` -> Cria o bucket S3 do projeto na AWS;

- `upload_data.py` -> Faz upload do arquivo de dados sem pre-processamento no bucket S3;

- `read_s3_data.py` -> Lista todos os arquivos do bucket S3;

- `get_all_lambda_functions.py` -> Lista todas as funções lambda da conta da AWS.