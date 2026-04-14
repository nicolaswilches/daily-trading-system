import fs from "node:fs";
import path from "node:path";

const dataDir = path.resolve("public/data");

function read<T>(name: string): T {
  return JSON.parse(fs.readFileSync(path.join(dataDir, name), "utf-8"));
}

export interface Prediction {
  ticker: string;
  current_price: number;
  target_price: number;
  prob_up: number;
  pred_log_return: number;
  signal: "BUY" | "SELL" | "HOLD";
  change_pct: number;
  last_date: string;
  history: { date: string; close: number; volume: number }[];
  in_holdout: boolean;
}

export interface BacktestRun {
  dates: string[];
  equity: number[];
  benchmark: number[];
  drawdown: number[];
  probs: number[];
  signals: number[];
  metrics: {
    strategy_return_pct: number;
    benchmark_return_pct: number;
    max_drawdown_pct: number;
    win_rate_pct: number;
    num_trades: number;
  };
}

export interface BacktestData {
  generated_at: string;
  cutoff_date: string;
  tickers: string[];
  buy_thresholds: number[];
  sell_thresholds: number[];
  grid: Record<string, Record<string, BacktestRun>>;
}

export interface MethodologyData {
  generated_at: string;
  split: {
    cutoff_date: string;
    holdout_fraction: number;
    train_rows: number;
    holdout_rows: number;
  };
  metrics: {
    cv_precision: number;
    cv_rmse: number;
    holdout_precision: number;
    holdout_rmse: number;
  };
  feature_count: number;
  top_features_classifier: { feature: string; importance: number }[];
  top_features_regressor: { feature: string; importance: number }[];
}

export function loadPredictions() {
  return read<{ generated_at: string; cutoff_date: string; predictions: Prediction[] }>(
    "predictions.json"
  );
}
export function loadBacktest() {
  return read<BacktestData>("backtest.json");
}
export function loadMethodology() {
  return read<MethodologyData>("methodology.json");
}
