"""Generate JSON artifacts consumed by the Astro web app.

Writes three files to web/public/data/:
    predictions.json  — per-ticker latest signal, price history, features
    backtest.json     — pre-computed backtest grid over the holdout period
    methodology.json  — model split metadata, metrics, feature importance

All data comes from the offline parquet + trained models. No live API calls —
that keeps the daily GitHub Actions job deterministic and credential-free.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import polars as pl

TICKERS = ["AAPL", "MSFT", "AMZN", "TSLA", "NVDA"]
BUY_THRESHOLDS = [0.52, 0.55, 0.58, 0.60]
SELL_THRESHOLDS = [0.40, 0.42, 0.45, 0.48]
HISTORY_DAYS = 250

OUTPUT_DIR = Path("web/public/data")


def load_artifacts():
    clf = joblib.load("models/classifier.joblib")
    reg = joblib.load("models/regressor.joblib")
    features = joblib.load("models/features_list.joblib")
    meta = joblib.load("models/split_meta.joblib")
    df = pl.read_parquet("data/processed/features.parquet")
    return clf, reg, features, meta, df


def build_predictions(clf, reg, features, meta, df):
    cutoff = pl.lit(meta["cutoff_date"]).str.strptime(pl.Date, "%Y-%m-%d")
    out = []
    for ticker in TICKERS:
        t_df = df.filter(pl.col("Ticker") == ticker).sort("Date")
        if len(t_df) == 0:
            continue

        X_latest = t_df.select(features).tail(1).to_pandas().values
        prob_up = float(clf.predict_proba(X_latest)[0][1])
        pred_log_return = float(reg.predict(X_latest)[0])

        latest = t_df.tail(1)
        current_price = float(latest["Close"].item())
        target_price = current_price * float(np.exp(pred_log_return))

        if prob_up > 0.55:
            signal = "BUY"
        elif prob_up < 0.45:
            signal = "SELL"
        else:
            signal = "HOLD"

        history = t_df.tail(HISTORY_DAYS).select(["Date", "Close", "Volume"])
        history_rows = [
            {
                "date": d.isoformat(),
                "close": float(c),
                "volume": float(v),
            }
            for d, c, v in zip(
                history["Date"].to_list(),
                history["Close"].to_list(),
                history["Volume"].to_list(),
            )
        ]

        out.append(
            {
                "ticker": ticker,
                "current_price": current_price,
                "target_price": target_price,
                "prob_up": prob_up,
                "pred_log_return": pred_log_return,
                "signal": signal,
                "change_pct": (
                    float(np.exp(t_df["Log_Return_1d"].tail(1).item())) - 1
                ) * 100,
                "last_date": latest["Date"].item().isoformat(),
                "history": history_rows,
                "in_holdout": latest["Date"].item().isoformat() >= meta["cutoff_date"],
            }
        )
    return out


def run_backtest(clf, features, meta, df, ticker, buy_th, sell_th):
    cutoff = pl.lit(meta["cutoff_date"]).str.strptime(pl.Date, "%Y-%m-%d")
    t_df = (
        df.filter(pl.col("Ticker") == ticker)
        .filter(pl.col("Date") >= cutoff)
        .sort("Date")
    )
    if len(t_df) == 0:
        return None

    X = t_df.select(features).to_pandas().values
    probs = clf.predict_proba(X)[:, 1]
    returns = np.exp(t_df["Target_Log_Return"].to_numpy()) - 1
    signals = np.where(probs > buy_th, 1, np.where(probs < sell_th, -1, 0))

    strat_ret = signals * returns
    equity = (1 + strat_ret).cumprod()
    bench = (1 + returns).cumprod()

    running_max = np.maximum.accumulate(equity)
    drawdown = (equity - running_max) / running_max
    active = signals != 0

    return {
        "dates": [d.isoformat() for d in t_df["Date"].to_list()],
        "equity": equity.tolist(),
        "benchmark": bench.tolist(),
        "drawdown": (drawdown * 100).tolist(),
        "probs": probs.tolist(),
        "signals": signals.tolist(),
        "metrics": {
            "strategy_return_pct": float((equity[-1] - 1) * 100),
            "benchmark_return_pct": float((bench[-1] - 1) * 100),
            "max_drawdown_pct": float(drawdown.min() * 100),
            "win_rate_pct": (
                float((strat_ret[active] > 0).sum() / active.sum() * 100)
                if active.sum() > 0
                else 0.0
            ),
            "num_trades": int(active.sum()),
        },
    }


def build_backtest(clf, features, meta, df):
    grid = {}
    for ticker in TICKERS:
        grid[ticker] = {}
        for buy_th in BUY_THRESHOLDS:
            for sell_th in SELL_THRESHOLDS:
                key = f"{buy_th:.2f}_{sell_th:.2f}"
                result = run_backtest(clf, features, meta, df, ticker, buy_th, sell_th)
                if result is not None:
                    grid[ticker][key] = result
    return {
        "tickers": TICKERS,
        "buy_thresholds": BUY_THRESHOLDS,
        "sell_thresholds": SELL_THRESHOLDS,
        "grid": grid,
        "cutoff_date": meta["cutoff_date"],
    }


def build_methodology(clf, reg, features, meta):
    fi_clf = sorted(
        zip(features, clf.feature_importances_.tolist()),
        key=lambda x: x[1],
        reverse=True,
    )
    fi_reg = sorted(
        zip(features, reg.feature_importances_.tolist()),
        key=lambda x: x[1],
        reverse=True,
    )
    return {
        "split": {
            "cutoff_date": meta["cutoff_date"],
            "holdout_fraction": meta["holdout_fraction"],
            "train_rows": meta["train_rows"],
            "holdout_rows": meta["holdout_rows"],
        },
        "metrics": {
            "cv_precision": meta["cv_precision"],
            "cv_rmse": meta["cv_rmse"],
            "holdout_precision": meta["holdout_precision"],
            "holdout_rmse": meta["holdout_rmse"],
        },
        "feature_count": len(features),
        "top_features_classifier": [
            {"feature": f, "importance": int(i)} for f, i in fi_clf[:15]
        ],
        "top_features_regressor": [
            {"feature": f, "importance": int(i)} for f, i in fi_reg[:15]
        ],
    }


def main():
    clf, reg, features, meta, df = load_artifacts()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "cutoff_date": meta["cutoff_date"],
    }

    predictions = build_predictions(clf, reg, features, meta, df)
    backtest = build_backtest(clf, features, meta, df)
    methodology = build_methodology(clf, reg, features, meta)

    (OUTPUT_DIR / "predictions.json").write_text(
        json.dumps({**payload, "predictions": predictions}, indent=2)
    )
    (OUTPUT_DIR / "backtest.json").write_text(
        json.dumps({**payload, **backtest}, indent=2)
    )
    (OUTPUT_DIR / "methodology.json").write_text(
        json.dumps({**payload, **methodology}, indent=2)
    )

    print(f"Wrote {len(predictions)} predictions to {OUTPUT_DIR}/predictions.json")
    print(f"Wrote backtest grid to {OUTPUT_DIR}/backtest.json")
    print(f"Wrote methodology to {OUTPUT_DIR}/methodology.json")


if __name__ == "__main__":
    main()
