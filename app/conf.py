X_TEST_NAME = 'x_test.npy'
Y_TEST_NAME = 'y_test.npy'
MODEL_NAME = 'model.h5'

CLASSIFICATION_METRICS = [
    'accuracy_score',
    'f1_score',
    'fbeta_score',
    'hamming_loss',
    'jaccard_score',
    'precision_score',
    'recall_score',
    'roc_auc_score',
    'zero_one_loss',
]

REGRESSION_METRICS = [
    'explained_variance_score',
    'max_error',
    'mean_absolute_error',
    'mean_squared_error',
    'mean_squared_log_error',
    'median_absolute_error',
    'r2_score',
    'mean_poisson_deviance',
    'mean_gamma_deviance',
]