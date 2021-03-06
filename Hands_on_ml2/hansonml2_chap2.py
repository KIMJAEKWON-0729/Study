#!/usr/bin/env python
# coding: utf-8



#데이터 다운로드 

#데이터를 다운로드 하는 함수를 준비하면 특히 데이터가 정기적으로 바뀌는 경우에 유용하다 

import os 
import tarfile
import urllib

import pandas as pd

os.getcwd()
os.chdir("/Users/data_analysis/Desktop/Study/Hands_on_ml2")
download_root = "https://raw.githubusercontent.com/ageron/handson-ml2/master/"
HOUSING_PATH = os.path.join("datasets","housing")
HOUSING_URL = download_root +"datasets/housing/housing.tgz"

def fetch_housing_data(housing_url = HOUSING_URL, housing_path = HOUSING_PATH):
    os.makedirs(housing_path,exist_ok=True)
    tgz_path = os.path.join(housing_path,"housing.tgz")
    urllib.request.urlretrieve(housing_url,tgz_path)
    housing_tgz = tarfile.open(tgz_path)
    housing_tgz.extractall(path = housing_path)
    housing_tgz.close()
#fetch_housing_data 를 호출하면 현재 작업공간에 datasets/housing 디렉터리르 만들고 
#housing.tgz 파일을 내려받고 같은 디렉터리에 압축을 풀어 housing.csv 파일을 만듭니다




import pandas as pd

#def load_housing_data(housing_path = HOUSING_PATH):
 #   csv_path = os.path.join(housing_path,"housing.csv")
  #  return pd.read_csv(csv_path)

#데이터 구조 훑어보기
housing = pd.read_csv("datasets/housing.csv")

housing.head()

#info 메서드는 데이터에 대한 간략한 설명과 전채 행수 데이터 타입 확인 
housing.info()
#RangeIndex: 20640 entries, 0 to 20639
#머신러닝 프로젝트치고는 작은사이즈
#total_bedrooms 특성은 20433 개만 널값이 아니다 207개는 특성을 가지고 있지 않다 
#ocean_proximity 필드만 배고 모든 틀성이 숫자형 
#ocean_proximity 변수 특성 확인 




housing["ocean_proximity"].value_counts( )




#describe()메서드는 숫자형 특성의 요약정보를 보여준다 
#summary
housing.describe()




#데이터의 형태를 빠르게 검토하는 다른방법은 각 숫자형 틀성을 히스토그램으로 그려보는것 
#주피터 노트북의 매직 명령

import matplotlib.pyplot as plt

housing.hist(bins=50,figsize=(20,15))

#plt.show()




#housing_median_age 와 median_house_value의 최대값들이 크다 한정해야 한다 

#테스트 세트 만들기 
import numpy as np 

def split_train_test(data,test_ratio):
    shuffled_indices = np.random.permutation(len(data))
    #permutation은 array를 복사하여 리턴 
    test_set_size = int(len(data) * test_ratio)
    test_indices = shuffled_indices[:test_set_size]
    train_indices = shuffled_indices[test_set_size:]
    return data.iloc[train_indices],data.iloc[test_indices]
#20프로 테스트 셋
train_set, test_set = split_train_test(housing , 0.2)
print(len(train_set)
)
print(len(test_set))




#위 코드를 쓸경우 다시 불러올떄 새롭게 섞인다 난수값이 필요 그리고 두 경우 데이터셋이 업데이트 될경우 샘플링이 이상해 진다 

from zlib import crc32

def test_set_check(identifier, test_ratio):
    return crc32(np.int64(identifier)) & 0xffffffff <test_ratio * 2 * 32
#비트 연산을 하는 이유는 파이썬2와 호환성 유지를 위해 

def split_train_test_by_id(data, test_ratio,id_column):
    ids = data[id_column]
    in_test_set = ids.apply(lambda id_ : test_set_check(id_,test_ratio))
    return data.loc[~in_test_set],data.loc[in_test_set]




# 주택 데이터 셋에는 식별자 컬럼이 없다 대신 행의 인덱스를 ID로 사용 

housing.reset_index()
#index 열이추가된 데이터 프레임이 반환 된다 

housing_with_id = housing.reset_index()

train_set, test_set = split_train_test_by_id(housing_with_id,0.2,"index")


#

housing_with_id["id"] =  housing["longitude"] * 1000 + housing["latitude"]

train_set, test_set = split_train_test_by_id(housing_with_id,0.2,"id")




#train_test_split  난수 초깃값을지정할수 있다 행의 개수가 같은 여러개의 데이터셋을 넘겨서 같은 인덱스를 기반으로 나눌수 있다 




from sklearn.model_selection import train_test_split

train_set, test_set = train_test_split(housing, test_size = 0.2, random_state = 42)




#테스트 세트 안 변수 하나가 중요하다 는 가정  이 테스트 세트가 전체 데이터 셋 에 있는 여러 소득 카테고리를 잘 대표 해야 한다 
# 이 셋안에서는 median_income 이 중요하다고 한다  

#위 히스토 그램 확인후 계급 설정 

housing["income_cat"] = pd.cut(housing["median_income"],
                              bins = [0,1.5,3.0,4.5,6,np.inf],
                              labels = [1,2,3,4,5])

housing["income_cat"].hist()



from sklearn.model_selection import StratifiedShuffleSplit

#StratifiedShuffleSplit 층위 무작위 추출을 통한 train test

split = StratifiedShuffleSplit(n_splits = 1, test_size= 0.2, random_state= 42)

for train_index, test_index in split.split(housing, housing["income_cat"]):
                                    strat_train_set = housing.loc[train_index]
                                    strat_test_set = housing.loc[test_index]



#소득 카테고리의 비율확인 
strat_test_set["income_cat"].value_counts()/len(strat_test_set)



#파생 변수를 만드는 목적이 아니기에 카테고리에 따라 비율을 나눠준뒤 INCOME_CAT 특성 삭제 

for set_ in (strat_train_set,strat_test_set):
    set_.drop("income_cat",axis=1,inplace = True)



# 데이터 이해를 위한 탐색과 시각화

#훈련세트를 손상시키지 않기 위해 복사본을 만들어 사용 

housing =  strat_test_set.copy()

#지리적 데이터 시각화 

housing.plot(kind = "scatter", x ="longitude",y = "latitude")
#kind 그래프 종류 # x y 는  y

#캘리포니아 지역의 위경도를 잘 나타 내지만 패턴을 찾아보기는 힘들다 

#alpha 옵션 조정 

housing.plot(kind = "scatter",x = "longitude", y = "latitude",alpha = 0.1)

#매개 변수 를 넣어 보기 s(scale) 는 인구 c(color) 색상은 가격 

housing.plot(kind = 'scatter', x = 'longitude', y = 'latitude', alpha = 0.4,
            s = housing['population']/100, c = 'median_house_value',cmap = plt.get_cmap('jet'),colorbar = True, 
            figsize = (10,7))

#상관관계 조사 

#데이터의 셋이 너무 크지 않으므로 모든 특성가느이 표준 상관계수(피어슨)를  corr()메서드를 이용해 쉽계 계산할수 있다

corr_matrix = housing.corr()

print(corr_matrix['median_house_value'].sort_values(ascending = False))

#데이터 정제 

housing = strat_train_set.drop("median_house_value",axis = 1)
print(housing)

housing_labels = strat_train_set["median_house_value"].copy()

print(housing_labels)

#total_bedrooms na 값 
#해당구역 제거 

print(housing.dropna(subset= ["total_bedrooms"])) 

#전체 특성을 삭제 

print(housing.drop("total_bedrooms",axis = 1))
#중간값으로 대체 

median = housing["total_bedrooms"].median()

print(housing["total_bedrooms"].fillna(median,inplace = True))

#sklearn 의 simpleimputer는 누락된 값을 손쇱게 다루도록 해준다 

from sklearn.impute import SimpleImputer

imputer = SimpleImputer(strategy = "median")

#수치형 특성에서만 계산될수 있다 텍스트 특성 ocean_proximity 제외

# 텍스트 특성 제외 복사 

housing_num = housing.drop("ocean_proximity",axis = 1)

imputer.fit(housing_num)

#중간값을 계싼해서 저장 

print(imputer.statistics_)

x = imputer.transform(housing_num)

print(x)
#변형된 특성들이 들어 있는 평범한 numpy 배열 판다스로 되돌릴수도 있음
 
 #텍스트와 범주형 특성다루기 
housing_cat = housing[["ocean_proximity"]]

print(housing_cat.head(10))


#숫자로 변형 

from sklearn.preprocessing import OrdinalEncoder

ordinal_encoder = OrdinalEncoder()

housing_cat_encoded = ordinal_encoder.fit_transform(housing_cat)

print(housing_cat_encoded[:10])

#categories 인스턴스 변수를 사용해 카테고리 목록을 얻을수 있다 

ordinal_encoder.categories

#더미로 인코딩을 하는게 낫다 

from sklearn.preprocessing import OneHotEncoder

cat_encoder = OneHotEncoder()
housing_cat_1hot = cat_encoder.fit_transform(housing_cat)

print(housing_cat_1hot)

#넘파이 배열이 아니라 희소행렬 수천개의 카테고리가 있는 범주형 특성일경우매우 효율적 

print(housing_cat_1hot.toarray())
#카테고리 5개 

#나만의 변환기 만들기 
from sklearn.base import BaseEstimator, TransformerMixin

rooms_ix, bedrooms_ix, population_ix, households_ix = 3,4,5,6

class CombinedAttributesAdder(BaseEstimator,TransformerMixin):
    def __init__(self,add_bedrooms_per_room = True):
        self.add_bedrooms_per_room = add_bedrooms_per_room
    def fit(self, X,y=None):
        return self
    def transform(self,X):
        rooms_per_household = X[:, rooms_ix]/X[:, households_ix]
        population_per_household = X[:, population_ix]/ X[:,households_ix]
        if self.add_bedrooms_per_room:
            bedrooms_per_room = X[:,bedrooms_ix]/ X[:,rooms_ix]
            return np.c_[X,rooms_per_household,population_per_household,
            bedrooms_per_room]
        else :
            return np.c_[X,rooms_per_household,population_per_household]

attr_adder = CombinedAttributesAdder(add_bedrooms_per_room=False)
housing_extra_attribs = attr_adder.transform(housing.values)

#특성 스케일링 

#데이터에 적용할 가장 중요한 변환중 하나가 특성스케일링 

#머신러닝 알고리즘은 입력 숫자 특성들의 스케일이 많이 다르면 잘 작동하지 않는다 

# 모든 특성의 범위를 같도록 만들어주는 방법으로 min-man 스케일릴과 표준화 가 널리 사용된다 

#변환 파이프 라인 
#변환이 많아질때 사용

#Pipeline은 단계를 나타내는 이름 과 추정기를 입력받는다

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

num_pipeline = Pipeline([
  ('imputer', SimpleImputer(strategy= "median")),
  ('attribs_adder', CombinedAttributesAdder()),
  ('std_scaler', StandardScaler()),  
])
#끝에도 쉼표 

housing_num_tr  = num_pipeline.fit_transform(housing_num)

#
from sklearn.compose import ColumnTransformer

num_attribs = list(housing_num)

cat_attribs = ['ocean_proximity']

full_pipeline = ColumnTransformer([
    ("num", num_pipeline, num_attribs),
    ("cat", OneHotEncoder(),cat_attribs),

])

housing_prepared = full_pipeline.fit_transform(housing)

print(housing_prepared)

#모델 선택과 훈련
#훈련 세트에서훈련하고 평가하기 

from sklearn.linear_model import LinearRegression

lin_reg = LinearRegression()

lin_reg.fit(housing_prepared,housing_labels)
#x값 , y값

some_data = housing.iloc[:5]
print(some_data)

some_labels = housing_labels.iloc[:5]
print(some_labels)

some_data_prepared = full_pipeline.transform(some_data)
print("예측:",lin_reg.predict(some_data_prepared))

print("레이블:",list(some_labels))

#벗어난 모습 
#MSE함수를 이용해 전체 훈련 세트에 대한 이 회귀 모델의 RMSE를 측정 

from sklearn.metrics import mean_squared_error
housing_predictions = lin_reg.predict(housing_prepared)

lin_mse = mean_squared_error(housing_labels,housing_predictions)

lin_rmse = np.sqrt(lin_mse)

print(lin_rmse) #68626 
#없는것 보다는 낫지만 확실히좋은 점수는 아니다  대부분 중간 주택 가격은 120000에서 265000사이  이는 모델이 훈련 데이터에 과소적합된 상태 
#과소적합을 해결하는 주요 방법은 더 강력한 모델을 선택
# 훈련 알고리즘에 더 좋은 특성을 주입
# 모델의 규제를 감소시키는것 

#먼저 더 복잡한 모델 사용해 보기 

from sklearn.tree import DecisionTreeRegressor

tree_reg = DecisionTreeRegressor()

tree_reg.fit(housing_prepared,housing_labels)

housing_predictions = tree_reg.predict(housing_prepared)

tree_mse = mean_squared_error(housing_labels,housing_predictions)

tree_rmse  = np.sqrt(tree_mse)
print(tree_rmse)

#rmse 가 0 과대적합된것으로 보인다 

#K-fold cross-vallidation
#훈련세트를 10개의 서브셋으로 무작위로 분할 그다음 결정트리 모델을 10번 훈련하고 평가 

from sklearn.model_selection import cross_val_score

scores = cross_val_score(tree_reg,housing_prepared,housing_labels, scoring="neg_mean_squared_error",cv=10)
#scoring 매개 변수에 비용함수가 아니라 효용함수를 기대 그래서 반댓값을 계산하는 neg ~
tree_rmse_scores = np.sqrt(-scores)

#결과 확인 

def display_scores(scores):
    print("점수:",scores)
    print("평균",scores.mean())
    print("표준편차",scores.std())

display_scores(tree_rmse_scores)
#교차 검증으로 모델의 성능을 추정하는것 뿐만 아니라 이 추정이 얼마나 정확한지 측정할수 있다  
#평균 71031.11567721912
#표준편차 2842.614812532021
#결정트리 점수가 대략 평균 71407에서 2439사이 
#모델을 여러번 훈련시켜야 해서 비용이 비싸기에 언제나 쓸수 있는 것은 아니다 


#선형회귀모델 점수 비교 ----------------------------------------------------------------------------

lin_scores = cross_val_score(lin_reg,housing_prepared,housing_labels,scoring = "neg_mean_squared_error",cv=10)

lin_rmse_scores  = np.sqrt(-lin_scores)

display_scores(lin_rmse_scores)


#앙상블 , RandomForestRegressor--------------------------------------

from sklearn.ensemble import RandomForestRegressor

forest_reg = RandomForestRegressor()

forest_reg.fit(housing_prepared,housing_labels)

housing_predictions = forest_reg.predict(housing_prepared)

forset_mse = mean_squared_error(housing_labels,housing_predictions)

forest_rmse = np.sqrt(forset_mse)
print(forest_rmse)

forest_scores = cross_val_score(forest_reg,housing_prepared,housing_labels,scoring = "neg_mean_squared_error",cv=10)

forest_rmse_scores  = np.sqrt(-forest_scores)

display_scores(forest_rmse_scores)

#실험한 모델 저장 

import joblib
#joblib.dump(my_model,"my_model.pkl")
#load my_model_loaded = joblib.load("my_model.pkl")

#그리드탐색 GridSearchCV ------------------------------------------------------------
#가능성 있는 모델 추렸다고 가정 -> 모델을 세부튜닝
#가장 단순한 방법은 만족할 만한 하이퍼 파라미터 조합을 찾을 때까지 수동으로 하이퍼파라미터를 조정하는것 이는 매우 지루한 작업이며 많은 경우를 탐색하기에는 시간이 부족 할수도 있다 
#GridSearchCV는 탐색하고자 하는 하이퍼파라미터와 시도해볼 값을 지정하기만 하면 된다 
from sklearn.model_selection import GridSearchCV

#RandomForestRegressor 에 대한 최적의 하이퍼 파라미터조합을 탐색
param_grid = [
    {'n_estimators': [3,10,30],'max_features':[2,4,6,8]},
    {'bootstrap':[False],'n_estimators':[3,10],'max_features':[2,3,4]},
]
grid_search = GridSearchCV(forest_reg,param_grid,cv=5,
scoring="neg_mean_squared_error",return_train_score=True)

grid_search.fit(housing_prepared,housing_labels)

#첫번째 dict 에 있는 n_estimator와 max_features 하이퍼 파라미터의 조합인 3*4 =12개를 평가 그다음 두번째 dict에 있는 하이퍼 파라미터 조합인 2*3=6
#6개를 시도 총 12+6= 18개의 조합을 탐색하고 5번 훈련 전체훈련 횟수는 90 

print("best_paranms",grid_search.best_params_)

#최적의 추정기에 직접 접근

print("best_estimator",grid_search.best_estimator_)
#평가점수 확인 

cvres = grid_search.cv_results_

for mean_score, params in zip(cvres["mean_test_score"],cvres["params"]):
    print(np.sqrt(-mean_score),params)

#max_feature가 하이퍼 파라미터 8 n_estimatr 30  rmse : 50099