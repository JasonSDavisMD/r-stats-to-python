"""Search regression tests for the broader catalog: the phrasing (or R name) a
user would type must surface the intended entry first. Search does not import
any library, so these run even when optional add-ons are not installed."""

import pytest

from statsbench.finder import Index

CASES = {
    # hypothesis tests and agreement
    "wilcox.test": "mann-whitney",
    "paired wilcox.test": "wilcoxon-signed-rank",
    "chi square test": "chi2-contingency",
    "TukeyHSD": "tukey-hsd",
    "p.adjust": "multipletests",
    "pwr.t.test": "power-analysis",
    "bland altman": "bland-altman",
    "cohen kappa": "cohen-kappa",
    "kappam.fleiss": "fleiss-kappa",
    "icc": "intraclass-corr",
    "mcnemar test": "mcnemar",
    "sensitivity specificity confidence interval": "diagnostic-accuracy-ci",
    "auc confidence interval": "auc-bootstrap-ci",
    "concordance correlation coefficient": "lin-ccc",
    # advanced regression and time series
    "lmer": "mixedlm",
    "mixed effects model": "mixedlm",
    "robust standard errors": "ols-robust-se",
    "clustered standard errors": "ols-cluster-se",
    "glm.nb": "negbin-glm",
    "polr": "ordinal-logit",
    "multinomial logistic regression": "mnlogit",
    "gam": "glm-gam",
    "arima forecast": "arima",
    "adf test": "stationarity-tests",
    "ljung box": "ljung-box",
    "holt winters": "ets-holt-winters",
    "time series cross validation": "time-series-split",
    # unsupervised and ML models
    "prcomp": "pca",
    "PCA": "pca",
    "kmeans": "kmeans",
    "hclust": "hierarchical-clustering",
    "support vector machine": "svm",
    "naive bayes": "naive-bayes",
    "mice": "missing-value-imputation",
    "f1 score": "classification-report",
    "calibration curve": "probability-calibration",
    "permutation importance": "permutation-importance",
    # numerics and survival
    "nls": "curve-fit",
    "fitdistr": "dist-fit-mle",
    "chol": "np-cholesky",
    "kaplan meier": "kaplan-meier",
    "lifelines kaplan meier": "kaplan-meier-lifelines",
    "coxph": "cox-ph",
    "survreg": "weibull-aft",
    # deep learning, Bayesian, boosting (optional add-ons)
    "pytorch linear regression": "torch-linear-regression",
    "autograd": "torch-autograd",
    "bayesian regression": "pymc-linear-regression",
    "beta binomial": "beta-binomial-posterior",
    "posterior predictive check": "pymc-posterior-predictive",
    "xgboost": "xgboost-early-stopping",
    "lightgbm": "lightgbm-early-stopping",
}


@pytest.fixture(scope="module")
def index(catalog):
    return Index(catalog)


@pytest.mark.parametrize("query, expected", CASES.items(), ids=list(CASES))
def test_topic_query_first_hit(index, query, expected):
    assert index.search(query, limit=1)[0].entry.id == expected
