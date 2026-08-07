import argparse


def main():
    parser = argparse.ArgumentParser(description="Professional AI Book Image Enhancement Suite")
    parser.add_argument("--config", default="config.yaml")
    args = parser.parse_args()
    print("Using config:", args.config)


if __name__ == "__main__":
    main()
