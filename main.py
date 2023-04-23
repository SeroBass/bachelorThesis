import collect_data
import graham_strategy
import trader
from ml import randomForestClassifier, ml_preprocessor
from ml import decisionTreeClassifier, hyperParamTuning

#collect_data.download_data()
#graham_strategy.search_for_possibilities()
#trader.trade_graham_50()
#ml_preprocessor.set_target()
#ml_preprocessor.merge_all_companies()
#ml_preprocessor.clean_table()
#randomForestClassifier.rfc()
#hyperParamTuning.tune_dtc()
decisionTreeClassifier.dtc()
#trader.trade_ml_50()
