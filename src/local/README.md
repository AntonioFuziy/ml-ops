# Local

Essa pasta utiliza funções muito semelhantes as funções lambda, porém esses scripts executam localmente. Vale lembrar que esses scripts precisam ser executados em uma ordem correta. Portanto, para executar o projeto localmente, seguem os passos abaixo:

No caminho de pastas raiz do projeto, instale as dependências do python.

```bash
pip install -r requirements.txt
```

Dentro da pasta `src/local` execute os scripts abaixo:

**OBS: TODAY-DATE format => year-month-day (yyyy-MM-DD)**

**Pre-processing:**

```bash
python3 proccess.py

#or

python proccess.py
```

**Train:**

```bash
python3 train.py ../../data/train-housing-{TODAY-DATE}.parquet

#or

python train.py ../../data/train-housing-{TODAY-DATE}.parquet
```

**Predict:**

```bash
python3 predict.py ../../data/train-housing-{TODAY-DATE}.parquet

#or

python predict.py ../../data/train-housing-{TODAY-DATE}.parquet
```