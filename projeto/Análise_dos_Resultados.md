# Análise dos Resultados 

Após algumas semanas de treinamentos dos modelos de machine learning anteriormente apresentados, incluimos novas análises e percepções sobre eles. Assim disponibilizamos o material coletado da última execução de cada modelo nosso, também acrescentamos ao código a possibilidade do usúario ver a avaliação do modelos de ML visualmente e dados em .csv na pasta:  

**eixo5_grupo6_20241\projeto\Etapa 5**


# Análise dos Resultados do Modelo de Floresta Aleatória  - ML Analise satisfação cruzada produto e serviços

Como equipe, desenvolvemos um modelo de floresta aleatória para prever os valores de pagamentos com base em dados de um salão de beleza. Após treinar nosso modelo com um conjunto de dados cuidadosamente preparado, avaliamos seu desempenho usando várias métricas.

## Métricas de Avaliação

- **RMSE (Erro Quadrático Médio Raiz)**: Nosso modelo alcançou um RMSE de $$0.4442$$, o que significa que, em média, as previsões do modelo estão a essa distância dos valores reais. Dado que os valores foram normalizados, estamos satisfeitos com esse resultado, pois indica que o modelo está fazendo previsões precisas.

- **MAE (Erro Absoluto Médio)**: O MAE foi de $$0.1207$$. Esse número nos informa que, em média, o modelo erra por essa quantidade, sem considerar a direção do erro. É uma boa métrica para entender a magnitude dos erros, e estamos contentes que esteja baixo.

- **R² (Coeficiente de Determinação)**: O R² foi de $$0.8217$$. Isso é excelente, pois mostra que nosso modelo pode explicar cerca de 82.17% da variância dos dados. Quanto mais próximo de 1, melhor o modelo é em prever os valores reais, então esse resultado nos dá muita confiança na qualidade das previsões do modelo.

## Importância das Variáveis

Analisamos a importância das variáveis, que nos ajuda a entender quais características dos dados têm mais impacto nas previsões. A variável mais importante teve um valor de aproximadamente 0.1645, o que é bastante significativo. Isso nos permite focar nessas características importantes para refinar o modelo ou coletar dados mais precisos no futuro.

## Conclusão

Com base nesses resultados, podemos concluir que o modelo que criamos como equipe está performando bem e fazendo previsões confiáveis. No entanto, sempre há espaço para melhorias, e poderíamos experimentar ajustar os parâmetros do modelo ou testar diferentes algoritmos para buscar resultados ainda melhores. Como grupo, estamos comprometidos em continuar aprimorando nosso trabalho para alcançar a excelência em modelagem preditiva.



# Análise de Resultados do Modelo de Classificação - ML previsão de cancelamento agenda

Como equipe, desenvolvemos um modelo de Gradient Boosting Classifier para classificar dados de um salão de beleza. Após treinar nosso modelo com um conjunto de dados cuidadosamente preparado, avaliamos seu desempenho usando o conjunto de teste.

## Métricas de Avaliação

- **Acurácia**: Nosso modelo alcançou uma acurácia de 73%, o que significa que ele foi capaz de fazer previsões corretas em 73% dos casos no conjunto de teste.

- **Relatório de Classificação**: O relatório mostrou uma média ponderada de acurácia de 73%, com uma média macro de 30% para precisão, recall e pontuação F1.

- **Matriz de Confusão**: A matriz de confusão revelou que muitas classes têm poucas ou nenhuma previsão correta, o que pode indicar um desequilíbrio de classe ou dificuldades do modelo em diferenciar entre certas classes.

## Conclusão

Com base nesses resultados, podemos concluir que, embora o modelo tenha uma acurácia geral razoável, há espaço para melhorias, especialmente na classificação de algumas classes. Poderíamos explorar técnicas de balanceamento de classes, ajustar os parâmetros do modelo ou experimentar diferentes algoritmos para melhorar a precisão das previsões.

Como equipe, estamos comprometidos em continuar aprimorando nosso trabalho para alcançar a excelência em modelagem preditiva.


# Análise de Resultados do Modelo de Regressão - ML previsão de demanda serviço

Como equipe, desenvolvemos um modelo de RandomForestRegressor para prever os valores de pagamentos com base em dados de um salão de beleza. Após treinar nosso modelo com um conjunto de dados cuidadosamente preparado, avaliamos seu desempenho usando o conjunto de teste.

## Métricas de Avaliação

- **RMSE**: O RMSE obtido foi de $$ 26.3073 $$, o que indica que, em média, as previsões do modelo estão a essa distância dos valores reais. Um valor baixo de RMSE indica um bom ajuste do modelo aos dados.

- **MAE**: O MAE foi de $$ 7.3662 $$, mostrando que, em média, o modelo erra por essa quantidade, sem considerar a direção do erro. É uma boa métrica para entender a magnitude dos erros.

- **R²**: O R² de $$ 0.7765 $$ é excelente, pois mostra que nosso modelo pode explicar cerca de 77.65% da variância dos dados. Quanto mais próximo de 1, melhor o modelo é em prever os valores reais.

## Conclusão

Com base nesses resultados, podemos concluir que o modelo que criamos como equipe está performando bem e fazendo previsões confiáveis. No entanto, sempre há espaço para melhorias, e poderíamos experimentar ajustar os parâmetros do modelo ou testar diferentes algoritmos para buscar resultados ainda melhores. Como equipe, estamos comprometidos em continuar aprimorando nosso trabalho para alcançar a excelência em modelagem preditiva.

# Análise de Resultados do Modelo de Classificação

## Contexto
Como equipe, desenvolvemos um modelo de KNeighborsClassifier para prever os serviços mais frequentes dos clientes com base em dados de um salão de beleza. Após treinar nosso modelo com um conjunto de dados cuidadosamente preparado, avaliamos seu desempenho usando o conjunto de teste.

## Conjunto de Dados
Os dados foram extraídos de um banco de dados MySQL, contendo informações sobre os clientes, serviços prestados e valores pagos. Após a extração, os dados passaram por um processo de normalização e agregação para prepará-los para a modelagem.

## Modelo KNN
O modelo KNN foi treinado com os dados processados para classificar os clientes com base em seus serviços mais frequentes. O modelo foi avaliado usando uma divisão de treino-teste de 80-20.

## Métricas de Avaliação
A avaliação do modelo foi realizada utilizando as seguintes métricas:

- **Acurácia**: $$ 0.6578947368421053 $$
  - Indica que o modelo previu corretamente aproximadamente 65.79% das vezes.

- **Matriz de Confusão**:
  - Revela onde o modelo fez previsões corretas e onde errou, fornecendo uma visão detalhada do desempenho do modelo para cada classe.

- **Relatório de Classificação**:
  - **Precisão**: Mede a proporção de identificações positivas que foram realmente corretas.
  - **Recall**: Mede a proporção de positivos reais que foram identificados corretamente.
  - **F1-Score**: Combina precisão e recall em uma única métrica que pondera ambos igualmente.

## Conclusão
Com base nesses resultados, podemos concluir que o modelo está performando de maneira satisfatória, mas há espaço para melhorias. A acurácia pode ser melhorada, e a análise da matriz de confusão e do relatório de classificação pode nos ajudar a entender onde o modelo está errando mais e ajustar nossas estratégias de modelagem. Como equipe, estamos comprometidos em continuar aprimorando nosso trabalho para alcançar a excelência em modelagem preditiva.

---

Para mais detalhes sobre a implementação e os resultados, consulte o código-fonte e os arquivos CSV gerados na pasta etapa 5.
