import argparse
import json

from dl.anomaly_detector import DEFAULT_MODEL_PATH, train_and_save_model


def main() -> None:
    parser = argparse.ArgumentParser(description="Train the AegisOps LSTM telemetry anomaly detector.")
    parser.add_argument("--epochs", type=int, default=18)
    parser.add_argument("--windows", type=int, default=800)
    parser.add_argument("--output", default=str(DEFAULT_MODEL_PATH))
    args = parser.parse_args()
    if args.epochs < 1 or args.windows < 50:
        parser.error("Use at least 1 epoch and 50 training windows.")
    print(json.dumps(train_and_save_model(args.output, args.windows, args.epochs), indent=2))


if __name__ == "__main__":
    main()
