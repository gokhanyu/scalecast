# 🌄 Scalecast: The practitioner's time series forecasting library

<p align="center">
  <img src="assets/logo2.png" />
</p>

## About

Scalecast is a light-weight modeling procedure, wrapper, and results container meant for those who are looking for the fastest way possible to apply, tune, and validate many different model classes for forecasting applications. In the Data Science industry, it is often asked of practitioners to deliver predictions and ranges of predictions for several lines of businesses or data slices, 100s or even 1000s. In such situations, it is common to see a simple linear regression or some other quick procedure applied to all lines due to the complexity of the task. This works well enough for people who need to deliver *something*, but more can be achieved.  

The scalecast package was designed to address this situation and offer advanced machine learning models that can be applied, optimized, and validated quickly. Unlike many libraries, the predictions produced by scalecast are always dynamic by default, not averages of one-step forecasts, so you don't run into the situation where the estimator looks great on the test-set but can't generalize to real data. What you see is what you get, with no attempt to oversell results. If you download a library that looks like it's able to predict the COVID pandemic in your test-set, you probably have a one-step forecast happening under-the-hood. You can't predict the unpredictable, and you won't see such things with scalecast.  

The library provides the `Forecaster` (for one series) and `MVForecaster` (for multiple series) wrappers around the following estimators: 

- Any regression model from [Sklearn](https://scikit-learn.org/stable/), including Sklearn APIs (like [Xgboost](https://xgboost.readthedocs.io/en/stable/) and [LightGBM](https://lightgbm.readthedocs.io/en/latest/))
- Recurrent neural nets from [Keras TensorFlow](https://keras.io/)
- Classic econometric models from [statsmodels](https://www.statsmodels.org/stable/): Holt-Winters Exponential Smoothing and ARIMA
- [Facebook Prophet](https://facebook.github.io/prophet)
- [LinkedIn Silverkite](https://engineering.linkedin.com/blog/2021/greykite--a-flexible--intuitive--and-fast-forecasting-library)
- Average, weighted average, and spliced models

## Installation
- Only the base package is needed to get started:  
`pip install scalecast`  
- Optional add-ons:  
`pip install fbprophet` (prophet model--see [here](https://stackoverflow.com/questions/49889404/fbprophet-installation-error-failed-building-wheel-for-fbprophet) to resolve a common installation issue if using Anaconda)  
`pip install greykite` (silverkite model)  
`pip install tqdm` (progress bar with notebook)  
`pip install ipython` (widgets with notebook)  
`pip install ipywidgets` (widgets with notebook)  
`jupyter nbextension enable --py widgetsnbextension` (widgets with notebook)  
`jupyter labextension install @jupyter-widgets/jupyterlab-manager` (widgets with Lab)  

## Links
### Official Docs
  - [Read the Docs](https://scalecast.readthedocs.io/en/latest/)
  - [Change Log](https://scalecast.readthedocs.io/en/latest/change_log.html)

### Forecasting with Different Model Types
- Sklearn Univariate
  - [Expand your Time Series Arsenal with These Models](https://towardsdatascience.com/expand-your-time-series-arsenal-with-these-models-10c807d37558)
  - [Notebook](https://scalecast-examples.readthedocs.io/en/latest/sklearn/sklearn.html)
- Sklearn Multivariate
  - [Multiple Series? Forecast Them together with any Sklearn Model](https://towardsdatascience.com/multiple-series-forecast-them-together-with-any-sklearn-model-96319d46269)
  - [Notebook](https://scalecast-examples.readthedocs.io/en/latest/multivariate/multivariate.html)
- RNN 
  - [Exploring the LSTM Neural Network Model for Time Series](https://towardsdatascience.com/exploring-the-lstm-neural-network-model-for-time-series-8b7685aa8cf)
  - [LSTM Notebook](https://scalecast-examples.readthedocs.io/en/latest/lstm/lstm.html)
  - [RNN Notebook](https://scalecast-examples.readthedocs.io/en/latest/rnn/rnn.html)
- ARIMA
  - [Forecast with ARIMA in Python More Easily with Scalecast](https://towardsdatascience.com/forecast-with-arima-in-python-more-easily-with-scalecast-35125fc7dc2e)
  - [Notebook](https://scalecast-examples.readthedocs.io/en/latest/arima/arima.html)
- Other Notebooks
  - [Prophet](https://scalecast-examples.readthedocs.io/en/latest/prophet/prophet.html)
  - [Combo](https://scalecast-examples.readthedocs.io/en/latest/combo/combo.html)
  - [Holt-Winters Exponential Smoothing](https://scalecast-examples.readthedocs.io/en/latest/hwes/hwes.html)
  - [Silverkite](https://scalecast-examples.readthedocs.io/en/latest/silverkite/silverkite.html)
  
### The importance of dynamic validation
- [How Not to be Fooled by Time Series Models](https://towardsdatascience.com/how-not-to-be-fooled-by-time-series-forecasting-8044f5838de3)
- [Model Validation Techniques for Time Series](https://towardsdatascience.com/model-validation-techniques-for-time-series-3518269bd5b3)
- [Notebook](https://scalecast-examples.readthedocs.io/en/latest/misc/validation/validation.html)

### Model Input Selection
  - [Variable Reduction Techniques for Time Series](https://medium.com/towards-data-science/variable-reduction-techniques-for-time-series-646743f726d4)
  - [Notebook](https://scalecast-examples.readthedocs.io/en/latest/misc/feature-selection/feature_selection.html)

### Scaled Forecasting on Many Series
  - [May the Forecasts Be with You](https://towardsdatascience.com/may-the-forecasts-be-with-you-introducing-scalecast-pt-2-692f3f7f0be5)
  - [Notebook](https://scalecast-examples.readthedocs.io/en/latest/misc/multi-series/multi-series.html)

## Example

Let's say we wanted to forecast each of the 1-year, 5-year, 10-year, 20-year, and 30-year corporate bond rates through the next 12 months. There are two ways we could do this with scalecast:  
1. Forecast each series individually (univariate): they will only have their own histories and any exogenous regressors we add to make forecasts. One series is predicted forward dynamically at a time.  
2. Forecast all series together (multivariate): they will have their own histories, exogenous regressors, and each other's histories to make forecasts. All series will be predicted forward dynamically at the same time.    


```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scalecast.Forecaster import Forecaster
from scalecast.MVForecaster import MVForecaster
from scalecast import GridGenerator
from scalecast.multiseries import export_model_summaries
import pandas_datareader as pdr

sns.set(rc={'figure.figsize':(14,7)})

df = pdr.get_data_fred(
    ['HQMCB1YR','HQMCB5YR','HQMCB10YR','HQMCB20YR','HQMCB30YR'],
    start='2000-01-01',
    end='2022-03-01'
)

f_dict = {c: Forecaster(y=df[c],current_dates=df.index) for c in df}
```

### Option 1 - Univariate

#### Select Models


```python
models = (
    'arima',       # linear time series model
    'elasticnet',  # linear model with regularization
    'knn',         # nearest neighbor model
    'xgboost',     # boosted tree model
)
```

#### Create Grids
These grids will be used to tune each model. To get example grids, you can use:  

```python
GridGenerator.get_example_grids()
```

This saves a Grids.py file to your working directory by default, which scalecast knows how to read. In this example, we create our own grids:  


```python
arima_grid = dict(
    order = [(1,1,1),(0,1,1),(0,1,0)],
    seasonal_order = [(1,1,1,12),(0,1,1,12),(0,1,0,12)],
    Xvars = [None,'all']
)

elasticnet_grid = dict(
    l1_ratio = [0.25,0.5,0.75,1],
    alpha = np.linspace(0,1,100),
)

knn_grid = dict(
    n_neighbors = np.arange(2,100,2)
)

xgboost_grid = dict(
     n_estimators=[150,200,250],
     scale_pos_weight=[5,10],
     learning_rate=[0.1,0.2],
     gamma=[0,3,5],
     subsample=[0.8,0.9],
)

grid_list = [arima_grid,elasticnet_grid,knn_grid,xgboost_grid]
grids = dict(zip(models,grid_list))
```

#### Select test length, validation length, and forecast horizon


```python
def prepare_fcst(f):
    f.set_test_length(0.2)
    f.set_validation_length(12)
    f.generate_future_dates(12)
```

#### Add seasonal regressors
These are regressors like month, quarter, dayofweek, dayofyear, minute, hour, etc. Raw integer values, dummy variables, or fourier transformed variables. They are determined by the series' own histories.  


```python
def add_seasonal_regressors(f):
    f.add_seasonal_regressors('month',raw=False,sincos=True)
    f.add_seasonal_regressors('year')
    f.add_seasonal_regressors('quarter',raw=False,dummy=True,drop_first=True)
```

#### Choose Autoregressive Terms
A better way to do this would be to examine each series individually for autocorrelation. This example uses three lags for each series and one seasonal seasonal lag (assuming 12-month seasonality).


```python
def add_ar_terms(f):
    f.add_ar_terms(3)       # lags
    f.add_AR_terms((1,12))  # seasonal lags
```

#### Write the forecast procedure


```python
def tune_test_forecast(k,f,models):
    for m in models:
        print(f'forecasting {m} for {k}')
        f.set_estimator(m)
        f.ingest_grid(grids[m])
        f.tune()
        f.auto_forecast()
```

#### Run a forecast loop


```python
for k, f in f_dict.items():
    prepare_fcst(f)
    add_seasonal_regressors(f)
    add_ar_terms(f)
    f.integrate(critical_pval=0.01) # takes differences in series until they are stationary using the adf test
    tune_test_forecast(k,f,models)
```

    forecasting arima for HQMCB1YR
    forecasting elasticnet for HQMCB1YR
    forecasting knn for HQMCB1YR
    forecasting xgboost for HQMCB1YR
    forecasting arima for HQMCB5YR
    forecasting elasticnet for HQMCB5YR
    forecasting knn for HQMCB5YR
    forecasting xgboost for HQMCB5YR
    forecasting arima for HQMCB10YR
    forecasting elasticnet for HQMCB10YR
    forecasting knn for HQMCB10YR
    forecasting xgboost for HQMCB10YR
    forecasting arima for HQMCB20YR
    forecasting elasticnet for HQMCB20YR
    forecasting knn for HQMCB20YR
    forecasting xgboost for HQMCB20YR
    forecasting arima for HQMCB30YR
    forecasting elasticnet for HQMCB30YR
    forecasting knn for HQMCB30YR
    forecasting xgboost for HQMCB30YR
    

#### Visualize results
Since there are 5 series to visualize, it might be undesirable to write a plot function for each one. Instead, scalecast lets you leverage Jupyter widgets by using this function:

```python
from scalecast.notebook import results_vis
results_vis(f_dict)
```

Because we aren't able to show widgets through markdown, this readme shows a visualization for the 30-year rate only:

##### Integrated Results


```python
f.plot_test_set(ci=True,order_by='LevelTestSetMAPE')
plt.title(f'{k} test-set results',size=16)
plt.show()
```


    
![png](README_files/README_17_0.png)
    


##### Level Results


```python
f.plot_test_set(level=True,order_by='LevelTestSetMAPE')
plt.title(f'{k} test-set results',size=16)
plt.show()
```


    
![png](README_files/README_19_0.png)
    


Comparing level test-set MAPE values, the K-nearest Neighbor model performed best, although, as we can see, predicting bond rates accurately is difficult if not impossible. To make the forecasts look better, we can set `dynamic_testing=False` in the `manual_forecast()` or `auto_forecast()` methods when calling forecasts. This will make test-set predictions an average on one-step forecasts. By default, everything is dynamic with scalecast to give a more realistic sense of how the models perform. To see our future predictions:


```python
f.plot(level=True,models='knn')
plt.title(f'{k} forecast',size=16)
plt.show()
```


    
![png](README_files/README_21_0.png)
    


### View Results
We can print a dataframe that shows how each model performed on each series.


```python
results = export_model_summaries(f_dict,determine_best_by='LevelTestSetMAPE')
results.columns
```




    Index(['ModelNickname', 'Estimator', 'Xvars', 'HyperParams', 'Scaler',
           'Observations', 'Tuned', 'CrossValidated', 'DynamicallyTested',
           'Integration', 'TestSetLength', 'TestSetRMSE', 'TestSetMAPE',
           'TestSetMAE', 'TestSetR2', 'LastTestSetPrediction', 'LastTestSetActual',
           'CILevel', 'CIPlusMinus', 'InSampleRMSE', 'InSampleMAPE', 'InSampleMAE',
           'InSampleR2', 'ValidationSetLength', 'ValidationMetric',
           'ValidationMetricValue', 'models', 'weights', 'LevelTestSetRMSE',
           'LevelTestSetMAPE', 'LevelTestSetMAE', 'LevelTestSetR2', 'best_model',
           'Series'],
          dtype='object')




```python
results[['ModelNickname','Series','LevelTestSetMAPE','LevelTestSetR2','HyperParams']]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>ModelNickname</th>
      <th>Series</th>
      <th>LevelTestSetMAPE</th>
      <th>LevelTestSetR2</th>
      <th>HyperParams</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>elasticnet</td>
      <td>HQMCB1YR</td>
      <td>3.178337</td>
      <td>-1.156049</td>
      <td>{'l1_ratio': 0.25, 'alpha': 0}</td>
    </tr>
    <tr>
      <th>1</th>
      <td>knn</td>
      <td>HQMCB1YR</td>
      <td>3.526606</td>
      <td>-1.609881</td>
      <td>{'n_neighbors': 6}</td>
    </tr>
    <tr>
      <th>2</th>
      <td>arima</td>
      <td>HQMCB1YR</td>
      <td>5.052915</td>
      <td>-4.458788</td>
      <td>{'order': (1, 1, 1), 'seasonal_order': (0, 1, ...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>xgboost</td>
      <td>HQMCB1YR</td>
      <td>5.881190</td>
      <td>-6.700988</td>
      <td>{'n_estimators': 150, 'scale_pos_weight': 5, '...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>xgboost</td>
      <td>HQMCB5YR</td>
      <td>0.372265</td>
      <td>0.328466</td>
      <td>{'n_estimators': 250, 'scale_pos_weight': 5, '...</td>
    </tr>
    <tr>
      <th>5</th>
      <td>knn</td>
      <td>HQMCB5YR</td>
      <td>0.521959</td>
      <td>0.119923</td>
      <td>{'n_neighbors': 26}</td>
    </tr>
    <tr>
      <th>6</th>
      <td>elasticnet</td>
      <td>HQMCB5YR</td>
      <td>0.664711</td>
      <td>-0.263214</td>
      <td>{'l1_ratio': 0.25, 'alpha': 0}</td>
    </tr>
    <tr>
      <th>7</th>
      <td>arima</td>
      <td>HQMCB5YR</td>
      <td>1.693632</td>
      <td>-7.335685</td>
      <td>{'order': (1, 1, 1), 'seasonal_order': (0, 1, ...</td>
    </tr>
    <tr>
      <th>8</th>
      <td>elasticnet</td>
      <td>HQMCB10YR</td>
      <td>0.145834</td>
      <td>0.390825</td>
      <td>{'l1_ratio': 0.25, 'alpha': 0.010101010101010102}</td>
    </tr>
    <tr>
      <th>9</th>
      <td>knn</td>
      <td>HQMCB10YR</td>
      <td>0.175513</td>
      <td>0.341443</td>
      <td>{'n_neighbors': 26}</td>
    </tr>
    <tr>
      <th>10</th>
      <td>xgboost</td>
      <td>HQMCB10YR</td>
      <td>0.465610</td>
      <td>-2.875923</td>
      <td>{'n_estimators': 150, 'scale_pos_weight': 5, '...</td>
    </tr>
    <tr>
      <th>11</th>
      <td>arima</td>
      <td>HQMCB10YR</td>
      <td>0.569411</td>
      <td>-4.968624</td>
      <td>{'order': (1, 1, 1), 'seasonal_order': (0, 1, ...</td>
    </tr>
    <tr>
      <th>12</th>
      <td>elasticnet</td>
      <td>HQMCB20YR</td>
      <td>0.096262</td>
      <td>0.475912</td>
      <td>{'l1_ratio': 0.25, 'alpha': 0.030303030303030304}</td>
    </tr>
    <tr>
      <th>13</th>
      <td>knn</td>
      <td>HQMCB20YR</td>
      <td>0.103565</td>
      <td>0.486593</td>
      <td>{'n_neighbors': 26}</td>
    </tr>
    <tr>
      <th>14</th>
      <td>xgboost</td>
      <td>HQMCB20YR</td>
      <td>0.105995</td>
      <td>0.441079</td>
      <td>{'n_estimators': 200, 'scale_pos_weight': 5, '...</td>
    </tr>
    <tr>
      <th>15</th>
      <td>arima</td>
      <td>HQMCB20YR</td>
      <td>0.118033</td>
      <td>0.378309</td>
      <td>{'order': (1, 1, 1), 'seasonal_order': (0, 1, ...</td>
    </tr>
    <tr>
      <th>16</th>
      <td>knn</td>
      <td>HQMCB30YR</td>
      <td>0.075318</td>
      <td>0.560975</td>
      <td>{'n_neighbors': 22}</td>
    </tr>
    <tr>
      <th>17</th>
      <td>elasticnet</td>
      <td>HQMCB30YR</td>
      <td>0.089038</td>
      <td>0.538360</td>
      <td>{'l1_ratio': 0.25, 'alpha': 0.030303030303030304}</td>
    </tr>
    <tr>
      <th>18</th>
      <td>xgboost</td>
      <td>HQMCB30YR</td>
      <td>0.098148</td>
      <td>0.495318</td>
      <td>{'n_estimators': 200, 'scale_pos_weight': 5, '...</td>
    </tr>
    <tr>
      <th>19</th>
      <td>arima</td>
      <td>HQMCB30YR</td>
      <td>0.099816</td>
      <td>0.498638</td>
      <td>{'order': (1, 1, 1), 'seasonal_order': (0, 1, ...</td>
    </tr>
  </tbody>
</table>
</div>



### Option 2: Multivariate

#### Select Models
Only sklearn models are available with multivariate forecasting, so we can replace ARIMA with mlr.


```python
mv_models = (
    'mlr',
    'elasticnet',
    'knn',
    'xgboost',
)
```

#### Create Grids
We can use three of the same grids as we did in univariate forecasting and create a new MLR grid, with a modification to also search the optimal lag numbers. The `lags` argument can be an `int`, `list`, or `dict` type and all series will use the other series' lags (as well as their own lags) in each model that is called, unless we tell the models to not use a certain series' lags for whatever reason. Again, for mv forecasting, we can save default grids:  

```python
GridGenerator.get_mv_grids()
```

This creates the MVGrids.py file in our working directory by default, which scalecast knows how to read.  


```python
mlr_grid = dict(lags = np.arange(1,13,1))
elasticnet_grid['lags'] = np.arange(1,13,1)
knn_grid['lags'] = np.arange(1,13,1)
xgboost_grid['lags'] = np.arange(1,13,1)

mv_grid_list = [mlr_grid,elasticnet_grid,knn_grid,xgboost_grid]
mv_grids = dict(zip(mv_models,mv_grid_list))
```

### Create multivariate forecasting object
- Need to change test and validation length
- Regressors are already carried forward from the underlying `Forecaster` objects
- Integrated levels are also carried forward from the underlying `Forecaster` objects


```python
mvf = MVForecaster(
    *f_dict.values(),
    names = f_dict.keys(),
)

mvf.set_test_length(.2)
mvf.set_validation_length(12)
mvf
```




    MVForecaster(
        DateStartActuals=2000-02-01T00:00:00.000000000
        DateEndActuals=2022-03-01T00:00:00.000000000
        Freq=MS
        N_actuals=266
        N_series=5
        SeriesNames=['HQMCB1YR', 'HQMCB5YR', 'HQMCB10YR', 'HQMCB20YR', 'HQMCB30YR']
        ForecastLength=12
        Xvars=['monthsin', 'monthcos', 'year', 'quarter_2', 'quarter_3', 'quarter_4']
        TestLength=53
        ValidationLength=12
        ValidationMetric=rmse
        ForecastsEvaluated=[]
        CILevel=0.95
        BootstrapSamples=100
        CurrentEstimator=mlr
        OptimizeOn=mean
    )



### Choose how to optimize the models when tuning hyperparameters
Default behavior is use the mean performance of each model on all series. We don't have to run the line below to keep this behavior, but we also have the option to use this code to optimize on the min/max error across all series, a weighted average of the error across the series, or to only consider one series' error over all others. See the [docs](https://scalecast.readthedocs.io/en/latest/Forecaster/MVForecaster.html#src.scalecast.MVForecaster.MVForecaster.add_optimizer_func) for more info.


```python
mvf.set_optimize_on('mean')
```

#### Write Forecasting Procedure
- Instead of grid search, we will use randomized grid search to speed up evaluation times


```python
for m in mv_models:
    print(f'forecasting {m}')
    mvf.set_estimator(m)
    mvf.ingest_grid(mv_grids[m])
    mvf.limit_grid_size(100,random_seed=20) # do this because now grids are larger and this speeds it up
    mvf.tune()
    mvf.auto_forecast()
```

    forecasting mlr
    forecasting elasticnet
    forecasting knn
    forecasting xgboost
    

### Set best model


```python
mvf.set_best_model(determine_best_by='LevelTestSetMAPE')
mvf.best_model
```




    'knn'



The elasticnet model was chosen based on its average test-set MAPE performance on all series.

#### Visualize results
Multivariate forecasting allows us to view all series and all models together. This could get jumbled, so let's just see the mlr and elasticnet results, knowing we can see the others if we want later.

##### Integrated Results


```python
mvf.plot_test_set(ci=True,models=['mlr','elasticnet'])
plt.title(f'test-set results',size=16)
plt.show()
```


    
![png](README_files/README_39_0.png)
    


##### Level Results


```python
mvf.plot_test_set(level=True,models=['mlr','elasticnet'])
plt.title(f'test-set results',size=16)
plt.show()
```


    
![png](README_files/README_41_0.png)
    


Once again, in this object, we can also set `dynamic_testing=False` in the `manual_forecast()` or `auto_forecast()` methods when calling forecasts. This would make our plots and metrics look better, but not be realistic in the sense it wouldn't show how well our forecasts could predict more than one period in the future. Let's see model forecasts into the future using the elasticent model only:


```python
mvf.plot(level=True,models='elasticnet')
plt.title(f'forecasts',size=16)
plt.show()
```


    
![png](README_files/README_43_0.png)
    


### View Results
We can print a dataframe that shows how each model did on each series.


```python
mvresults = mvf.export_model_summaries()
mvresults.columns
```




    Index(['Series', 'ModelNickname', 'Estimator', 'Xvars', 'HyperParams', 'Lags',
           'Scaler', 'Observations', 'Tuned', 'CrossValidated',
           'DynamicallyTested', 'Integration', 'TestSetLength', 'TestSetRMSE',
           'TestSetMAPE', 'TestSetMAE', 'TestSetR2', 'LastTestSetPrediction',
           'LastTestSetActual', 'CILevel', 'CIPlusMinus', 'InSampleRMSE',
           'InSampleMAPE', 'InSampleMAE', 'InSampleR2', 'ValidationSetLength',
           'ValidationMetric', 'ValidationMetricValue', 'LevelTestSetRMSE',
           'LevelTestSetMAPE', 'LevelTestSetMAE', 'LevelTestSetR2', 'OptimizedOn',
           'MetricOptimized', 'best_model'],
          dtype='object')




```python
mvresults[['ModelNickname','Series','LevelTestSetMAPE','LevelTestSetR2','HyperParams','Lags']]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>ModelNickname</th>
      <th>Series</th>
      <th>LevelTestSetMAPE</th>
      <th>LevelTestSetR2</th>
      <th>HyperParams</th>
      <th>Lags</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>knn</td>
      <td>HQMCB1YR</td>
      <td>1.571109</td>
      <td>0.144064</td>
      <td>{'n_neighbors': 30}</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>mlr</td>
      <td>HQMCB1YR</td>
      <td>3.793842</td>
      <td>-2.039209</td>
      <td>{}</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>elasticnet</td>
      <td>HQMCB1YR</td>
      <td>1.846718</td>
      <td>0.029598</td>
      <td>{'l1_ratio': 0.5, 'alpha': 0.010101010101010102}</td>
      <td>7</td>
    </tr>
    <tr>
      <th>3</th>
      <td>xgboost</td>
      <td>HQMCB1YR</td>
      <td>3.045742</td>
      <td>-0.892055</td>
      <td>{'n_estimators': 150, 'scale_pos_weight': 5, '...</td>
      <td>4</td>
    </tr>
    <tr>
      <th>4</th>
      <td>knn</td>
      <td>HQMCB5YR</td>
      <td>0.407562</td>
      <td>0.299347</td>
      <td>{'n_neighbors': 30}</td>
      <td>1</td>
    </tr>
    <tr>
      <th>5</th>
      <td>mlr</td>
      <td>HQMCB5YR</td>
      <td>0.824692</td>
      <td>-0.856614</td>
      <td>{}</td>
      <td>1</td>
    </tr>
    <tr>
      <th>6</th>
      <td>elasticnet</td>
      <td>HQMCB5YR</td>
      <td>0.339546</td>
      <td>0.329795</td>
      <td>{'l1_ratio': 0.5, 'alpha': 0.010101010101010102}</td>
      <td>7</td>
    </tr>
    <tr>
      <th>7</th>
      <td>xgboost</td>
      <td>HQMCB5YR</td>
      <td>0.341928</td>
      <td>0.491882</td>
      <td>{'n_estimators': 150, 'scale_pos_weight': 5, '...</td>
      <td>4</td>
    </tr>
    <tr>
      <th>8</th>
      <td>knn</td>
      <td>HQMCB10YR</td>
      <td>0.143230</td>
      <td>0.392050</td>
      <td>{'n_neighbors': 30}</td>
      <td>1</td>
    </tr>
    <tr>
      <th>9</th>
      <td>mlr</td>
      <td>HQMCB10YR</td>
      <td>0.243091</td>
      <td>-0.063537</td>
      <td>{}</td>
      <td>1</td>
    </tr>
    <tr>
      <th>10</th>
      <td>elasticnet</td>
      <td>HQMCB10YR</td>
      <td>0.141094</td>
      <td>0.369078</td>
      <td>{'l1_ratio': 0.5, 'alpha': 0.010101010101010102}</td>
      <td>7</td>
    </tr>
    <tr>
      <th>11</th>
      <td>xgboost</td>
      <td>HQMCB10YR</td>
      <td>0.314682</td>
      <td>-1.480335</td>
      <td>{'n_estimators': 150, 'scale_pos_weight': 5, '...</td>
      <td>4</td>
    </tr>
    <tr>
      <th>12</th>
      <td>knn</td>
      <td>HQMCB20YR</td>
      <td>0.088009</td>
      <td>0.508611</td>
      <td>{'n_neighbors': 30}</td>
      <td>1</td>
    </tr>
    <tr>
      <th>13</th>
      <td>mlr</td>
      <td>HQMCB20YR</td>
      <td>0.107826</td>
      <td>0.438056</td>
      <td>{}</td>
      <td>1</td>
    </tr>
    <tr>
      <th>14</th>
      <td>elasticnet</td>
      <td>HQMCB20YR</td>
      <td>0.094137</td>
      <td>0.478033</td>
      <td>{'l1_ratio': 0.5, 'alpha': 0.010101010101010102}</td>
      <td>7</td>
    </tr>
    <tr>
      <th>15</th>
      <td>xgboost</td>
      <td>HQMCB20YR</td>
      <td>0.194508</td>
      <td>-1.189377</td>
      <td>{'n_estimators': 150, 'scale_pos_weight': 5, '...</td>
      <td>4</td>
    </tr>
    <tr>
      <th>16</th>
      <td>knn</td>
      <td>HQMCB30YR</td>
      <td>0.077223</td>
      <td>0.578823</td>
      <td>{'n_neighbors': 30}</td>
      <td>1</td>
    </tr>
    <tr>
      <th>17</th>
      <td>mlr</td>
      <td>HQMCB30YR</td>
      <td>0.084045</td>
      <td>0.558262</td>
      <td>{}</td>
      <td>1</td>
    </tr>
    <tr>
      <th>18</th>
      <td>elasticnet</td>
      <td>HQMCB30YR</td>
      <td>0.088357</td>
      <td>0.532725</td>
      <td>{'l1_ratio': 0.5, 'alpha': 0.010101010101010102}</td>
      <td>7</td>
    </tr>
    <tr>
      <th>19</th>
      <td>xgboost</td>
      <td>HQMCB30YR</td>
      <td>0.122523</td>
      <td>-0.021191</td>
      <td>{'n_estimators': 150, 'scale_pos_weight': 5, '...</td>
      <td>4</td>
    </tr>
  </tbody>
</table>
</div>



## Backtest results
To test how well, on average, our models would have done across the last-10 12-month forecast horizons, we can use the `backtest()` method. It works for both the `Forecaster` and `MVForecaster` objects.


```python
mvf.backtest('elasticnet')
mvf.export_backtest_metrics('elasticnet')
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th>iter1</th>
      <th>iter2</th>
      <th>iter3</th>
      <th>iter4</th>
      <th>iter5</th>
      <th>iter6</th>
      <th>iter7</th>
      <th>iter8</th>
      <th>iter9</th>
      <th>iter10</th>
      <th>mean</th>
    </tr>
    <tr>
      <th>series</th>
      <th>metric</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="4" valign="top">HQMCB1YR</th>
      <th>RMSE</th>
      <td>0.703448</td>
      <td>0.529606</td>
      <td>0.394162</td>
      <td>0.326016</td>
      <td>0.253461</td>
      <td>0.189774</td>
      <td>0.154667</td>
      <td>0.145592</td>
      <td>0.098435</td>
      <td>0.065001</td>
      <td>0.286016</td>
    </tr>
    <tr>
      <th>MAE</th>
      <td>0.455746</td>
      <td>0.387781</td>
      <td>0.309262</td>
      <td>0.260086</td>
      <td>0.195941</td>
      <td>0.14293</td>
      <td>0.112216</td>
      <td>0.109277</td>
      <td>0.065746</td>
      <td>0.06156</td>
      <td>0.210055</td>
    </tr>
    <tr>
      <th>R2</th>
      <td>-1.23385</td>
      <td>-2.30855</td>
      <td>-4.457327</td>
      <td>-7.213157</td>
      <td>-12.598314</td>
      <td>-30.564624</td>
      <td>-59.223251</td>
      <td>-44.422297</td>
      <td>-13.780367</td>
      <td>-1.501688</td>
      <td>-17.730343</td>
    </tr>
    <tr>
      <th>MAPE</th>
      <td>0.619615</td>
      <td>0.7905</td>
      <td>0.806487</td>
      <td>0.792692</td>
      <td>0.669248</td>
      <td>0.540401</td>
      <td>0.456609</td>
      <td>0.450764</td>
      <td>0.277333</td>
      <td>0.237213</td>
      <td>0.564086</td>
    </tr>
    <tr>
      <th rowspan="4" valign="top">HQMCB5YR</th>
      <th>RMSE</th>
      <td>0.734249</td>
      <td>0.816982</td>
      <td>0.761748</td>
      <td>0.713451</td>
      <td>0.624121</td>
      <td>0.538565</td>
      <td>0.517054</td>
      <td>0.507586</td>
      <td>0.420291</td>
      <td>0.308957</td>
      <td>0.594301</td>
    </tr>
    <tr>
      <th>MAE</th>
      <td>0.472792</td>
      <td>0.696664</td>
      <td>0.681502</td>
      <td>0.643641</td>
      <td>0.541247</td>
      <td>0.449949</td>
      <td>0.435904</td>
      <td>0.423632</td>
      <td>0.317672</td>
      <td>0.235491</td>
      <td>0.489849</td>
    </tr>
    <tr>
      <th>R2</th>
      <td>-0.994349</td>
      <td>-4.100226</td>
      <td>-7.078805</td>
      <td>-9.115769</td>
      <td>-7.122668</td>
      <td>-6.150019</td>
      <td>-6.744144</td>
      <td>-5.812594</td>
      <td>-3.259064</td>
      <td>-1.302456</td>
      <td>-5.168009</td>
    </tr>
    <tr>
      <th>MAPE</th>
      <td>0.226192</td>
      <td>0.432627</td>
      <td>0.468919</td>
      <td>0.474502</td>
      <td>0.412414</td>
      <td>0.355956</td>
      <td>0.364298</td>
      <td>0.364892</td>
      <td>0.269983</td>
      <td>0.20938</td>
      <td>0.357916</td>
    </tr>
    <tr>
      <th rowspan="4" valign="top">HQMCB10YR</th>
      <th>RMSE</th>
      <td>0.421758</td>
      <td>0.551241</td>
      <td>0.58273</td>
      <td>0.638543</td>
      <td>0.566173</td>
      <td>0.50082</td>
      <td>0.529147</td>
      <td>0.579911</td>
      <td>0.542271</td>
      <td>0.351532</td>
      <td>0.526413</td>
    </tr>
    <tr>
      <th>MAE</th>
      <td>0.277111</td>
      <td>0.476382</td>
      <td>0.54243</td>
      <td>0.602894</td>
      <td>0.509764</td>
      <td>0.430215</td>
      <td>0.450412</td>
      <td>0.497538</td>
      <td>0.436258</td>
      <td>0.295126</td>
      <td>0.451813</td>
    </tr>
    <tr>
      <th>R2</th>
      <td>-0.408145</td>
      <td>-4.420615</td>
      <td>-9.994648</td>
      <td>-12.686294</td>
      <td>-6.253784</td>
      <td>-3.926973</td>
      <td>-4.366555</td>
      <td>-4.704238</td>
      <td>-3.31398</td>
      <td>-0.672898</td>
      <td>-5.074813</td>
    </tr>
    <tr>
      <th>MAPE</th>
      <td>0.093003</td>
      <td>0.172464</td>
      <td>0.206174</td>
      <td>0.235258</td>
      <td>0.199348</td>
      <td>0.169049</td>
      <td>0.179578</td>
      <td>0.200682</td>
      <td>0.174637</td>
      <td>0.12241</td>
      <td>0.175260</td>
    </tr>
    <tr>
      <th rowspan="4" valign="top">HQMCB20YR</th>
      <th>RMSE</th>
      <td>0.348891</td>
      <td>0.279699</td>
      <td>0.370068</td>
      <td>0.485955</td>
      <td>0.411693</td>
      <td>0.308747</td>
      <td>0.37619</td>
      <td>0.48552</td>
      <td>0.497345</td>
      <td>0.292792</td>
      <td>0.385690</td>
    </tr>
    <tr>
      <th>MAE</th>
      <td>0.300601</td>
      <td>0.205061</td>
      <td>0.336667</td>
      <td>0.460362</td>
      <td>0.369534</td>
      <td>0.260833</td>
      <td>0.309405</td>
      <td>0.420104</td>
      <td>0.417615</td>
      <td>0.257115</td>
      <td>0.333730</td>
    </tr>
    <tr>
      <th>R2</th>
      <td>-0.381451</td>
      <td>-0.603745</td>
      <td>-3.657283</td>
      <td>-6.926987</td>
      <td>-3.519094</td>
      <td>-1.317033</td>
      <td>-2.396007</td>
      <td>-4.52852</td>
      <td>-4.165721</td>
      <td>-0.611186</td>
      <td>-2.810703</td>
    </tr>
    <tr>
      <th>MAPE</th>
      <td>0.091612</td>
      <td>0.060179</td>
      <td>0.103287</td>
      <td>0.143462</td>
      <td>0.114549</td>
      <td>0.080542</td>
      <td>0.095243</td>
      <td>0.130241</td>
      <td>0.129078</td>
      <td>0.08163</td>
      <td>0.102982</td>
    </tr>
    <tr>
      <th rowspan="4" valign="top">HQMCB30YR</th>
      <th>RMSE</th>
      <td>0.364866</td>
      <td>0.222895</td>
      <td>0.318102</td>
      <td>0.446323</td>
      <td>0.382051</td>
      <td>0.25885</td>
      <td>0.346402</td>
      <td>0.45607</td>
      <td>0.478374</td>
      <td>0.286101</td>
      <td>0.356003</td>
    </tr>
    <tr>
      <th>MAE</th>
      <td>0.334947</td>
      <td>0.181975</td>
      <td>0.276637</td>
      <td>0.416693</td>
      <td>0.336769</td>
      <td>0.210484</td>
      <td>0.283833</td>
      <td>0.392222</td>
      <td>0.403274</td>
      <td>0.243648</td>
      <td>0.308048</td>
    </tr>
    <tr>
      <th>R2</th>
      <td>-0.747284</td>
      <td>0.021359</td>
      <td>-1.740434</td>
      <td>-4.31338</td>
      <td>-2.465227</td>
      <td>-0.548616</td>
      <td>-1.800884</td>
      <td>-4.013138</td>
      <td>-4.068474</td>
      <td>-0.670227</td>
      <td>-2.034631</td>
    </tr>
    <tr>
      <th>MAPE</th>
      <td>0.103043</td>
      <td>0.054387</td>
      <td>0.082671</td>
      <td>0.126624</td>
      <td>0.101576</td>
      <td>0.063127</td>
      <td>0.084734</td>
      <td>0.117698</td>
      <td>0.120757</td>
      <td>0.074304</td>
      <td>0.092892</td>
    </tr>
  </tbody>
</table>
</div>



## Correlation Matrices
- If you want to see how correlated the series are in your `MVForecaster` object, you can use these correlation matrices  

### All Series, no lags


```python
heatmap_kwargs = dict(
    disp='heatmap',
    vmin=-1,
    vmax=1,
    annot=True,
    cmap = "Spectral",
)
mvf.corr(**heatmap_kwargs)
plt.show()
```


    
![png](README_files/README_50_0.png)
    


### Two series, with lags


```python
mvf.corr_lags(y='HQMCB1YR',x='HQMCB30YR',lags=12,**heatmap_kwargs)
plt.show()
```


    
![png](README_files/README_52_0.png)
    


There is much more than can be done with this package! Be sure to [read the docs](https://scalecast.readthedocs.io/en/latest/) and see the [examples](https://scalecast-examples.readthedocs.io/en/latest/)!


```python

```
