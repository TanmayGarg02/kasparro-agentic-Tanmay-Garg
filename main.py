from core.orchestrator import run_orchestration
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default="data/product.json")
    args = parser.parse_args()

    run_orchestration(args.input)
    print("Generation completed. Check outputs folder.")

if __name__ == "__main__":
    main()
