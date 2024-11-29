# Machine Learning Ops Project - California Housing Price Prediction

### Project Video:

- [https://youtu.be/EcIu8k7QSig](https://youtu.be/EcIu8k7QSig) 

**Alunos:** Antonio Fuziy e André Tavernaro

Este projeto consiste basicamente em prever os preços de casas localizadas na Califórnia com base em algumas características, como o número de domicílios, a renda média, o número de quartos na casa e muito mais. A ideia do projeto é construir um pipeline de automação para implantar em um projeto de Aprendizado de Máquina. Neste caso, temos um projeto concluído usando apenas um notebook e abstraímos esse notebook para deixar o projeto com boas práticas do que se espera de um projeto de machine learning. Dessa forma, separamos o notebook em arquivos de código responsáveis por treino, predição e pré-processamento, deixando o notebook apenas com análise exploratória do projeto.

Para a construção desse projeto usamos dois projetos como base para automatização, dentre eles estão:

- [https://www.kaggle.com/code/shtrausslearning/bayesian-regression-house-price-prediction](https://www.kaggle.com/code/shtrausslearning/bayesian-regression-house-price-prediction) from (Andrey Shtrauss)

- [https://www.kaggle.com/code/unsatisfiable/california-housing-svm](https://www.kaggle.com/code/unsatisfiable/california-housing-svm) from (HamidrezaSh)

## Estrutura do projeto

Para esse projeto separou-se os arquivos em várias pastas, suas especificações se encontram abaixo:

- `models` armazena localmente os modelos, porém as funções lambda armazenam esses modelos no bucket S3 também;

- `notebooks` onde está a análise exploratória do projeto;

- `src` onde estão os scripts do projeto, ou seja, os arquivos `.py`, vale lembrar que a pasta `src/lambdas` armazena as funções lambda de `pre-processing`, `train` e `predict` reponsáveis por gerar os arquivos do projeto;

- `data` armazena os dados do projeto rodando localmente

- `.github/workflows` armazena os arquivos `.yml` para deploy automático das lambda functions através do github actions;

- `docs` armazena documentações do projeto, por enquanto apenas a documentação do modelo;

- `images` armazena imagens do utilizadas no projeto;

## Pipeline do projeto

![](/images/mlops_project_pipeline.jpg)

A proposta desse projeto consiste na automação de um sistema de machine learning, especificamente adotando o modelo de *batch prediction*. Nesse cenário, o modelo é retreinado periodicamente através de um *schedule*, ou seja, conforme um tempo determinado, geralmente durante períodos de menor demanda computacional. Essa abordagem se justifica pela natureza do modelo de previsão de preços de imóveis destinado a aplicativos ou websites. Dessa forma, é comum optar por horários nos quais a maioria dos clientes não está ativamente utilizando o app/website. Isso porque, o *schedule* em horários de baixa demanda minimiza o impacto nas operações normais do aplicativo ou website.

Dessa maneira, a fim de alinhar o projeto com as melhores práticas de *batch prediction*, decidiu-se utilizar funções lambda, buckets S3 e o AWS ECR como serviços de nuvem para executar o projeto, em conjunto com o GitHub Actions para CI/CD. Agora, abordaremos mais detalhadamente o funcionamento do pipeline do projeto.

Incialmente, criamos um bucket S3 que desempenha a função de repositório para uma variedade de arquivos, incluindo dados *raw*, dados pré-processados, dados de predição, e os arquivos associados aos modelos pré-treinados. Esse bucket é a forma de ativação ou *trigger* da lambda de `pre-processing`, portanto ao realizar o upload de um arquivo no formato `.csv` no path `data/raw` do bucket, a função lambda de pré-processamento é automaticamente acionada, iniciando o tratamento dos dados submetidos.  Após a limpeza dos dados, a função Lambda salva um novo arquivo .csv no path `data/process`, onde são armazenados os dados pré-processados. 

Dessa forma, a etapa de pré processamento dos dados está concluída. Com os dados devidamente pré-processados, a próxima fase envolve o treinamento do modelo. Para isso, criou-se um *schedule event*  configurado para ocorrer semanalmente aos sábados às 3:00AM, uma vez que nos baseamos em um modelo de *batch prediction*. Ao realizar o treinamento, são gerados os arquivos correspondentes ao modelo, sendo estes salvos no path `models/`. Esses arquivos modelares serão posteriormente empregados no processo de predição do modelo.   

Por fim, temos uma lambda de predição dos dados, a qual utiliza os arquivos dos modelos pré treinados e os dados pré processados para realizar predições e fazer uma análise de como está a performance do modelo. Como resultado desse processo, a função lambda gera um arquivo no formato `.csv` e armazena-o no path `data/predict`, consolidando os resultados das predições.

## CI/CD

Vale lembrar que o projeto possui um workflow no github actions para deploy automático do código, dessa forma o fluxo de trabalho do desenvolvedor se torna muito mais simples, de forma que ele apenas precisa escrever código em uma branch específica dele e abrir um pull request para a branch de `development`. Assim que o pull request for aprovado e o merge for feito na branch `development`, basta agora abrir um pull request da branch `development` para a branch `main`. Por fim, assim que o pull request for fechado e o merge for feito na branch `main`, o github actions realiza um deploy da função lambda na AWS.

## Estratégia do modelo de predição

Este projeto, voltado para a automação de um sistema de machine learning, direciona seu foco predominantemente à implementação de práticas de MLOps, sem ênfase na construção de uma arquitetura modelar sofisticada. A estrutura do modelo de previsão de preços, portanto, foi realizada de maneira simplificada. Inicialmente, foi adquirido um conjunto de dados contendo diversas características, conforme delineado abaixo:

|          |  longitude 	| latitude 	| housing_median_age 	| total_rooms 	| total_bedrooms 	| population |	households 	| median_income 	| median_house_value 	| ocean_proximity |
|----------|--------------|-----------|---------------------|---------------|-----------------|------------|--------------|-----------------|---------------------|---------------- |      
| 0 	     | -122.23 	    | 37.88 	  | 41.0 	              | 880.0 	      | 129.0 	        | 322.0 	   | 126.0 	      | 8.3252 	        | 452600.0 	          | NEAR BAY        |
| 1 	     | -122.22 	    | 37.86 	  | 21.0 	              | 7099.0 	      | 1106.0 	        | 2401.0 	   | 1138.0 	    | 8.3014 	        | 358500.0 	          | NEAR BAY        |
| 2 	     | -122.24 	    | 37.85 	  | 52.0 	              | 1467.0 	      | 190.0 	        | 496.0 	   | 177.0 	      | 7.2574 	        | 352100.0 	          | NEAR BAY        |
| 3 	     | -122.25 	    | 37.85 	  | 52.0 	              | 1274.0 	      | 235.0 	        | 558.0 	   | 219.0 	      | 5.6431 	        | 341300.0 	          | NEAR BAY        |
| 4 	     | -122.25 	    | 37.85 	  | 52.0 	              | 1627.0 	      | 280.0 	        | 565.0 	   | 259.0 	      | 3.8462 	        | 342200.0 	          | NEAR BAY        |
|... 	     |... 	        |... 	      |... 	                |... 	          |... 	            |... 	       |... 	        |... 	            |... 	                |...              |
| 20635 	 | -121.09 	    | 39.48 	  | 25.0 	              | 1665.0 	      | 374.0 	        | 845.0 	   | 330.0 	      | 1.5603 	        | 78100.0 	          | INLAND          |
| 20636 	 | -121.21 	    | 39.49 	  | 18.0 	              | 697.0 	      | 150.0 	        | 356.0 	   | 114.0 	      | 2.5568 	        | 77100.0 	          | INLAND          |
| 20637 	 | -121.22 	    | 39.43 	  | 17.0 	              | 2254.0 	      | 485.0 	        | 1007.0     | 433.0 	      | 1.7000 	        | 92300.0 	          | INLAND          |
| 20638 	 | -121.32 	    | 39.43 	  | 18.0 	              | 1860.0 	      | 409.0 	        | 741.0 	   | 349.0 	      | 1.8672 	        | 84700.0 	          | INLAND          |
| 20639 	 | -121.24 	    | 39.37 	  | 16.0 	              | 2785.0 	      | 616.0 	        | 1387.0     | 530.0 	      | 2.3886 	        | 89400.0 	          | INLAND          |

O modelo utilizado na arquitetura do projeto foi o `SVR` do `Scikit Learn` com kernels `linear`, `polynomial` e `RBF`, através desses três kernels, gerou-se três modelos e comparou-se os resultados de cada um, segue abaixo os porquês de termos optado por utilizar os três kernels e o `SVR`.

  - Não Linearidade nos Dados:
      O conjunto de dados pode exibir relacionamentos não lineares entre as características de entrada e a variável alvo `median_house_value`. Nesses casos, o uso de kernels não lineares, como `RBF` e polinomial, pode capturar padrões complexos nos dados que os modelos mais simples poderiam não perceber.

  - Interações entre Características:
      Kernels polinomiais são úteis quando existem interações entre características. O kernel polinomial pode modelar interações de grau superior, permitindo que o modelo leve em consideração dependências não lineares entre características.

  - Robustez a Outliers:
      O `SVR` é conhecido por sua robustez a outliers, e o kernel `RBF`, em particular, é menos sensível a outliers em comparação com um kernel linear. Isso pode ser importante em conjuntos de dados do mundo real, nos quais outliers são comuns.

  - Escalabilidade:
      O `SVR` com um kernel linear geralmente é mais escalável para conjuntos de dados grandes, enquanto os kernels `RBF` e polinomial podem ser computacionalmente caros. No entanto, o tamanho e a complexidade do conjunto de dados devem ser avaliados para determinar se o custo computacional adicional é justificado.

  - Avaliação de Desempenho:
      O script registra o R quadrado para cada modelo no conjunto de teste. A métrica R quadrado indica a proporção da variância na variável alvo que é previsível a partir das características. Comparar o desempenho de modelos com diferentes kernels ajuda a avaliar qual kernel é mais adequado para os dados fornecidos.

  - Experimentação:
      Tentar vários kernels permite experimentação e seleção com base em resultados empíricos. Diferentes kernels podem se sair de maneira diferente em conjuntos de dados distintos, e é uma prática comum explorar várias opções antes de escolher um modelo final.

  - Compreensão do Negócio:
      Deve-se considerar o contexto de negócios e a interpretabilidade dos modelos. Alguns kernels podem fornecer resultados mais fáceis de interpretar do que outros, e a escolha deve se alinhar aos requisitos do projeto.