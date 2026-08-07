import argparse

def main():
    p=argparse.ArgumentParser(description="Professional AI Book Image Enhancement Suite")
    p.add_argument("--config",default="config.yaml")
    a=p.parse_args()
    print("Using config:",a.config)
