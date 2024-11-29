# Lambdas

Aqui estão localizados os scripts das funções lambda que devem ser publicadas no aws para funcionamento. Portanto, é necessário executar os scrips em uma ordem específica para que o pipeline funcione, segue abaixo a ordem citada:

**Pre-processing**

On `src/lambdas/proccess`

```bash
docker build --platform linux/amd64 -t preprocessing_antoniovf_andretv1_project:v1 .
```

```bash
docker tag preprocessing_antoniovf_andretv1_project:v1 ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-2.amazonaws.com/mlops-project-antoniovf-andretv1:preprocessing
```

```bash
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-2.amazonaws.com/mlops-project-antoniovf-andretv1:preprocessing
```

```bash
python3 create_proccess_lambda.py
```

On `src/lambdas/train`

**Train:**

```bash
docker build --platform linux/amd64 -t train_antoniovf_andretv1_project:v1 .
```

```bash
docker tag train_antoniovf_andretv1_project:v1 ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-2.amazonaws.com/mlops-project-antoniovf-andretv1:train
```

```bash
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-2.amazonaws.com/mlops-project-antoniovf-andretv1:train
```

```bash
python3 create_train_lambda.py
```

On `src/lambdas/predict`

**Predict:**

```bash
docker build --platform linux/amd64 -t predict_antoniovf_andretv1_project:v1 .
```

```bash
docker tag predict_antoniovf_andretv1_project:v1 ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-2.amazonaws.com/mlops-project-antoniovf-andretv1:predict
```

```bash
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-2.amazonaws.com/mlops-project-antoniovf-andretv1:predict
```

```bash
python3 create_predict_lambda.py
```

### Outros scripts

Os outros scripts servem para testes, portanto os arquivos `invoke_lambda.py` são responsáveis por executar as funções lambda em núvem e observar seus resultados, enquanto os scripts com  `read_${function_name}_logs.py` servem para checagem de logs na AWS.