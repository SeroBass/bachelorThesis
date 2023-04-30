import collect_data
import graham_strategy
import trader
from ml import randomForestClassifier, ml_preprocessor
from ml import decisionTreeClassifier, hyperParamTuning


def main():
    collect_data.download_data()

    graham_strategy.search_for_possibilities()
    trader.trade_graham_50()

    ml_preprocessor.set_target()
    ml_preprocessor.merge_all_companies()  # Not necessary, if master.csv already existing
    ml_preprocessor.clean_table()  # Not necessary, if master.csv already existing

    hyperParamTuning.tune_dtc()  # High CPU and RAM load. Can take a while until finished
    #hyperParamTuning.tune_rfc()  # High CPU and RAM load. Can take a while until finished

    decisionTreeClassifier.dtc()  # Not necessary, if conditions in trader.trade_ml_50() satisfied
    #randomForestClassifier.rfc()  # Ready to be used. But not used for Bachelor Thesis

    trader.trade_ml_50()


if __name__ == "__main__":
    main()

