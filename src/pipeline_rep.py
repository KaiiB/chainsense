import argparse
import os
import subprocess
import sys


def run_cmd(args: list) -> None:
    result = subprocess.run(args, check=False)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int)
    parser.add_argument("--end", type=int)
    parser.add_argument("--window-size", type=int, default=10000)
    parser.add_argument("--raw-dir", default=os.path.join("data", "raw"))
    parser.add_argument("--bronze-dir", default=os.path.join("data", "bronze"))
    parser.add_argument("--silver-dir", default=os.path.join("data", "silver"))
    parser.add_argument("--gold-dir", default=os.path.join("data", "gold"))
    args = parser.parse_args()

    python = sys.executable

    if args.start is not None and args.end is not None:
        run_cmd(
            [
                python,
                "src/fetch_blocks.py",
                "--start",
                str(args.start),
                "--end",
                str(args.end),
                "--raw-dir",
                args.raw_dir,
            ]
        )

    run_cmd([python, "src/bronze_extract.py", "--raw-dir", args.raw_dir, "--out-dir", args.bronze_dir])
    run_cmd([python, "src/silver_decode.py", "--bronze-dir", args.bronze_dir, "--out-dir", args.silver_dir])
    run_cmd(
        [
            python,
            "src/gold_rep_a.py",
            "--bronze-dir",
            args.bronze_dir,
            "--out-dir",
            args.gold_dir,
            "--window-size",
            str(args.window_size),
        ]
    )
    run_cmd(
        [
            python,
            "src/gold_rep_b.py",
            "--bronze-dir",
            args.bronze_dir,
            "--silver-dir",
            args.silver_dir,
            "--out-dir",
            args.gold_dir,
            "--window-size",
            str(args.window_size),
        ]
    )
    run_cmd(
        [
            python,
            "src/gold_rep_c.py",
            "--bronze-dir",
            args.bronze_dir,
            "--out-dir",
            args.gold_dir,
            "--window-size",
            str(args.window_size),
        ]
    )


if __name__ == "__main__":
    main()
