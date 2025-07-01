import os
import sys
import argparse

# 対象とする拡張子（例: .py, .js など）
TARGET_EXTENSIONS = ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.h', '.cs', '.rb', '.go', '.php']

def is_code_file(filename):
    return any(filename.endswith(ext) for ext in TARGET_EXTENSIONS)

def count_loc_eloc(filepath):
    loc = 0
    eloc = 0
    in_block_comment = False
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            loc += 1
            stripped = line.strip()
            if not stripped:
                continue  # 空行
            # Python用のコメント判定（他言語は簡易対応）
            if stripped.startswith('#'):
                continue
            if stripped.startswith('//'):
                continue
            if stripped.startswith('/*'):
                in_block_comment = True
            if in_block_comment:
                if '*/' in stripped:
                    in_block_comment = False
                continue
            eloc += 1
    return loc, eloc

def scan_folder(folder):
    results = []
    for root, _, files in os.walk(folder):
        for file in files:
            if is_code_file(file):
                path = os.path.join(root, file)
                loc, eloc = count_loc_eloc(path)
                results.append((path, loc, eloc))
    return results

def scan_files(files):
    results = []
    for file in files:
        if is_code_file(file) and os.path.isfile(file):
            loc, eloc = count_loc_eloc(file)
            results.append((file, loc, eloc))
    return results

def main():
    parser = argparse.ArgumentParser(description='ソースコードのLOCとeLOCを計測するツール')
    parser.add_argument('targets', nargs='+', help='計測対象のフォルダまたはファイル（複数指定可）')
    args = parser.parse_args()
    results = []
    for target in args.targets:
        if os.path.isdir(target):
            results.extend(scan_folder(target))
        elif os.path.isfile(target):
            results.extend(scan_files([target]))
        else:
            print(f"警告: {target} は存在しません。", file=sys.stderr)
    total_loc = 0
    total_eloc = 0
    for path, loc, eloc in results:
        print(f'{path}: LOC={loc}, eLOC={eloc}')
        total_loc += loc
        total_eloc += eloc
    print(f'合計: LOC={total_loc}, eLOC={total_eloc}')

if __name__ == '__main__':
    main()
