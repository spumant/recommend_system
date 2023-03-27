import pandas as pd
import numpy as np
from catboost import CatBoostClassifier
from sklearn import preprocessing
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import train_test_split
# 数据读取
train_df = pd.read_csv("./data/train.csv")
test_df = pd.read_csv("./data/test.csv")

# 特征处理
train_df.fillna("-1", inplace=True)
test_df.fillna("-1", inplace=True)

for feature in train_df.columns:
    if train_df[feature].dtype == "object":
        le = preprocessing.LabelEncoder()
        le.fit(list(train_df[feature]) + list(test_df[feature]))
        train_df[feature] = le.transform(train_df[feature])
        test_df[feature] = le.transform(test_df[feature])

cols = ['pkgname', 'ver', 'slotid', 'mediaid', 'material']

X_train = train_df.drop(['label'], axis=1)
Y_train = train_df['label']
test_data = test_df.copy()

model = CatBoostClassifier(loss_function="Logloss",
                           eval_metric="AUC",
                           task_type="CPU",
                           learning_rate=0.05,
                           iterations=500,
                           random_seed=2022,
                           od_type="Iter",
                           depth=10)

answers = []
mean_score = 0
n_folds = 5
skf = StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=2022)

# 训练模型，使用交叉验证评估结果
for fold, (train_idx, val_idx) in enumerate(skf.split(X_train, Y_train)):
    print(f"====== Fold {fold + 1} of {n_folds} ======")
    x_train, x_val = X_train.iloc[train_idx, :], X_train.iloc[val_idx, :]
    y_train, y_val = Y_train.iloc[train_idx], Y_train.iloc[val_idx]
    clf = model.fit(x_train, y_train,
                    eval_set=(x_val, y_val),
                    verbose=500,
                    cat_features=cols)

    # 在验证集计算AUC
    predictions = clf.predict_proba(x_val)[:, 1]
    auc = roc_auc_score(y_val, predictions)
    mean_score += auc / n_folds
    print(f"Fold {fold + 1} AUC: {auc:.6f}\n")

print(f"\nMean AUC: {mean_score:.6f}")

# 使用全量数据训练一个模型
model.fit(X_train, Y_train, cat_features=cols)

# 预测测试集结果并输出提交文件
predictions = clf.predict_proba(test_data)[:, 1]

submission = pd.read_csv('./dataset/提交示例.csv')
submission['predict'] = predictions
submission.to_csv('./results/catboost_predictions.csv', index=None)
