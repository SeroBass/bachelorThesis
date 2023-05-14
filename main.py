import collect_data
import graham_strategy
import trader
from ml import ml_preprocessor
from ml import decisionTreeClassifier, hyperParamTuning



def main():
    collect_data.download_data()

    graham_strategy.search_for_possibilities()
    trader.trade_graham_20()
    trader.trade_graham_10()

    ml_preprocessor.set_target()
    ml_preprocessor.merge_all_companies()  # Not necessary, if master.csv already existing
    ml_preprocessor.clean_table()  # Not necessary, if master.csv already existing

    #hyperParamTuning.tune_dtc()  # High CPU and RAM load. Can take a while until finished

    decisionTreeClassifier.dtc()  # Not necessary, if conditions in trader.trade_ml() satisfied

    trader.trade_ml()


if __name__ == "__main__":
    main()

