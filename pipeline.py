
import subprocess, sys, argparse, pathlib, os

BASE_DIR = pathlib.Path(__file__).parent

def run(cmd):
    print('>>',' '.join(cmd))
    subprocess.run(cmd, check=True)

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--mode', choices=['full','ingest','rewrite','publish'], default='full')
    args = p.parse_args()
    if args.mode in ('full','ingest'): run([sys.executable,'ingest.py'])
    if args.mode in ('full','rewrite'): run([sys.executable,'rewrite.py'])
    if args.mode in ('full','publish'): run([sys.executable,'publish.py'])

if __name__=='__main__':
    main()
