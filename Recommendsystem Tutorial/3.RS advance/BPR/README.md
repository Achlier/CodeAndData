# BPR vs SVD++
****

## 数据
- 数据均由ml-100k中的u.data提取，部分直接使用，部分由RSA分解
RSA会将u.data分解为5个csv文件，存放于RSA/data/cv之中,用于实现SVD++使用。

- u.data在RSA/data中被转换为u_ratings.txt从而进一步转换为csv文件

## 代码实现
- BPR的所有算法实现都在BPR.py中

- SVD++的算法实现主体都位于SVDpp.py当中，其中RSA中rs部分为对数据的处理

## notebook
- BPR_data 为对数据的具体介绍

- BPR_algorithm 为对BPR算法的具体介绍

- BPR_SVD_experiment 为BPR与SVD对比实验评测