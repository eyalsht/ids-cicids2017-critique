"""Unit tests for ids_critique.evaluate and ids_critique.critique (no dataset required)."""

import numpy as np
from sklearn.metrics import f1_score

from ids_critique.critique import (
    flaw1_inflation,
    flaw2_drop,
    novel_attack_share,
    total_honest_gap,
)
from ids_critique.evaluate import always_benign_accuracy, binary_metrics, macro_f1


def test_macro_f1_matches_sklearn():
    y_true = [0, 0, 1, 1, 0, 1]
    y_pred = [0, 1, 1, 1, 0, 0]
    assert np.isclose(macro_f1(y_true, y_pred), f1_score(y_true, y_pred, average="macro"))


def test_binary_metrics_perfect_prediction():
    y = [0, 1, 0, 1]
    m = binary_metrics(y, y, y_score=[0.1, 0.9, 0.2, 0.8])
    assert m["accuracy"] == 1.0
    assert m["recall"] == 1.0
    assert m["mcc"] == 1.0
    assert m["roc_auc"] == 1.0
    assert set(m) == {"accuracy", "precision", "recall", "f1", "fbeta2", "mcc", "roc_auc"}


def test_binary_metrics_roc_auc_nan_without_scores():
    m = binary_metrics([0, 1], [0, 1])
    assert np.isnan(m["roc_auc"])


def test_always_benign_accuracy():
    # 3 benign (0) out of 4 -> 0.75
    assert always_benign_accuracy([0, 0, 0, 1]) == 0.75


def test_flaw_deltas():
    assert np.isclose(flaw1_inflation(0.9987, 0.9984), 0.0003)
    assert np.isclose(flaw2_drop(0.9984, 0.4883), 0.5101)
    assert np.isclose(total_honest_gap(0.9987, 0.4883), 0.5104)


def test_novel_attack_share_full_novelty():
    # train attacks: only DoS; test attacks: DDoS/PortScan/Bot -> all novel
    train = ["BENIGN", "DoS", "BENIGN"]
    test = ["BENIGN", "DDoS", "PortScan", "Bot"]
    assert novel_attack_share(train, test) == 1.0


def test_novel_attack_share_partial_and_empty():
    train = ["BENIGN", "DoS"]
    test = ["BENIGN", "DoS", "Bot"]  # one seen, one novel
    assert np.isclose(novel_attack_share(train, test), 0.5)
    assert np.isnan(novel_attack_share(["BENIGN"], ["BENIGN"]))  # no test attacks
