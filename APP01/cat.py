import pandas as pd
import numpy as np
from catboost import CatBoostClassifier
from sklearn import preprocessing
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import train_test_split

clf = None


def cat_prepare():
    global clf
    train_df = pd.read_csv(
        "APP01/data/log.csv",
        low_memory=True,
        usecols=['user', 'itemid', 'tagid', 'time', 'love', 'col'],
        names=['user', 'itemid', 'tagid', 'time', 'love', 'col'],
        nrows=None,
        dtype={
            'user': "category",
            'itemid': "category",
            'tagid': "category",
            'time': "category",
            'love': "category",
            'col': "category",
        },
    )
    train_data = np.loadtxt(
        "APP01/data/log.csv",
        dtype=np.float32,
        delimiter=",",
        usecols=list(range(0, 6)),
        skiprows=1,
    )

    # train_df.to_parquet('APP01/temp_data/train_df.parquet')
    # np.save('APP01/temp_data/train_data.npy', train_data)
    #
    # train_df = pd.read_parquet("APP01/temp_data/train_df.parquet")
    #
    # train_data = np.load("APP01/temp_data/train_data.npy")

    train_data = pd.DataFrame(data=train_data)

    for col in ['user', 'itemid', 'tagid', 'time', 'love']:
        train_df[col] = train_df[col].str.replace("b'", "").str.replace("'", "")

    del train_df['col'][0]

    train_df['col'] = train_df['col'].astype('str').astype('int')
    # train_df = train_df.drop(0)
    train_df = train_df.iloc[1:]
    train_df.index = range(len(train_df))
    # print(train_df)

    train = pd.merge(train_df, train_data, left_index=True, right_index=True)

    # print("train:\n")
    # print(train)
    train = train.drop([5], axis=1)
    X_train = train[train['col'].notnull()].drop(['col'], axis=1)
    Y_train = train[train['col'].notnull()]['col']

    # print("X_train\n", X_train)
    # print("Y_train\n", Y_train)

    cols = ['user', 'itemid', 'tagid', 'time', 'love']
    model = CatBoostClassifier(
        loss_function="Logloss",
        eval_metric="AUC",
        task_type="CPU",
        learning_rate=0.05,
        iterations=500,
        random_seed=2022,
        od_type="Iter",
        depth=10)

    answers = []
    mean_score = 0
    mean_f1 = 0
    # --------------------------------
    n_folds = 2  # 后期需要换成5折交叉验证
    # --------------------------------
    sk = StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=2022)

    for fold_, (train, test) in enumerate(sk.split(X_train, Y_train)):
        # print("fold n°{}".format(fold_))
        # print('trn_idx:', train)
        # print('val_idx:', test)
        x_train = X_train.iloc[train]
        y_train = Y_train.iloc[train]
        x_test = X_train.iloc[test]
        y_test = Y_train.iloc[test]

        clf = model.fit(x_train, y_train, eval_set=(x_test, y_test), verbose=500, cat_features=cols)
        # yy_pred_valid=clf.predict(x_test)            #输出直接为标签
        yy_pred_valid = clf.predict_proba(x_test)[:, 1]  # 输出预测为1的概率
        # 验证集的AUC
        print('cat验证的auc:{}'.format(roc_auc_score(y_test, yy_pred_valid)))
        mean_score += roc_auc_score(y_test, yy_pred_valid) / n_folds

    print('mean_score:{}'.format(mean_score))

    print('over!')


def boost1():
    test_df = pd.read_csv(
        "APP01/data/test.csv",
        low_memory=True,
        usecols=['user', 'itemid', 'tagid', 'time', 'love'],
        names=['user', 'itemid', 'tagid', 'time', 'love'],
        nrows=None,
        dtype={
            'user': "category",
            'itemid': "category",
            'tagid': "category",
            'time': "category",
            'love': "category",
        },
    )

    test_data = np.loadtxt(
        "APP01/data/test.csv",
        dtype=np.float32,
        delimiter=",",
        usecols=list(range(0, 6)),
        skiprows=1,
    )
    #
    # test_df.to_parquet('APP01/temp_data/test_df.parquet')
    #
    # np.save('APP01/temp_data/test_data.npy', test_data)
    #
    # test_df = pd.read_parquet("APP01/temp_data/test_df.parquet")
    #
    # test_data = np.load("APP01/temp_data/test_data.npy")
    #
    test_data = pd.DataFrame(data=test_data)

    for col in ['user', 'itemid', 'tagid', 'time', 'love']:
        test_df[col] = test_df[col].str.replace("b'", "").str.replace("'", "")
    test_df = test_df.drop(0)
    test_df.index = range(len(test_df))

    test = pd.merge(test_df, test_data, left_index=True, right_index=True)
    test = test.drop([5], axis=1)
    test_data = test
    # print("test_data\n", test_data)

    test = clf.predict(test_data)
    # print("test:\n")
    # print(test)

    return test


def boost2():
    test_df = pd.read_csv(
        "APP01/data/test2.csv",
        low_memory=True,
        usecols=['user', 'itemid', 'tagid', 'time', 'love'],
        names=['user', 'itemid', 'tagid', 'time', 'love'],
        nrows=None,
        dtype={
            'user': "category",
            'itemid': "category",
            'tagid': "category",
            'time': "category",
            'love': "category",
        },
    )

    test_data = np.loadtxt(
        "APP01/data/test2.csv",
        dtype=np.float32,
        delimiter=",",
        usecols=list(range(0, 6)),
        skiprows=1,
    )

    # test_df.to_parquet('APP01/temp_data/test_df2.parquet')
    #
    # np.save('APP01/temp_data/test_data2.npy', test_data)
    #
    # test_df = pd.read_parquet("APP01/temp_data/test_df2.parquet")
    #
    # test_data = np.load("APP01/temp_data/test_data2.npy")
    #
    test_data = pd.DataFrame(data=test_data)

    for col in ['user', 'itemid', 'tagid', 'time', 'love']:
        test_df[col] = test_df[col].str.replace("b'", "").str.replace("'", "")

    test_df = test_df.drop(0)
    test_df.index = range(len(test_df))

    test = pd.merge(test_df, test_data, left_index=True, right_index=True)
    test = test.drop([5], axis=1)
    # test_data = test
    # print("test:\n")
    # print(test)

    return clf.predict(test)
