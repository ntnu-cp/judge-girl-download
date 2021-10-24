from pathlib import Path
from typing import List
import os
import sys
import shutil
import requests as rq

testcase_root = Path('testcase')
zip_root = Path('zip')

# Ensure directories exists
if not testcase_root.exists():
    testcase_root.mkdir()
if not zip_root.exists():
    zip_root.mkdir()


def problem_dir(pid: int):
    d = testcase_root / str(pid)
    if not d.exists():
        d.mkdir()
    return d


def re_orgnize(pid, case_counts: List[int]):
    src = 0
    base_dir = problem_dir(pid)
    for i, c in enumerate(case_counts):
        for j in range(c):
            for suffix in ['.in', '.out']:
                os.system(
                    f'mv {base_dir}/{src}{suffix} {base_dir}/{i:02d}{j:02d}{suffix}'
                )
            src += 1
    shutil.make_archive(zip_root / str(pid), 'zip', base_dir)


def re_orgnize_with_single_testcase(pid: int):
    base_dir = problem_dir(pid)
    files = [*base_dir.iterdir()]
    assert len(files) % 2 == 0
    case_count = [1] * (len(files) // 2)
    re_orgnize(pid, case_count)


def download_testdata(pid: int):
    base_url = f'https://judgegirl.csie.org/downloads/testdata/{pid}/'
    i = 0
    d = problem_dir(pid)
    if d.exists():
        shutil.rmtree(d)
    d.mkdir()
    while 1:
        resp = rq.get(base_url + f'{i}.in')
        if not resp.ok:
            break
        open(d / f'{i}.in', 'wb').write(resp.content)
        resp = rq.get(base_url + f'{i}.out')
        open(d / f'{i}.out', 'wb').write(resp.content)
        i += 1


if __name__ == '__main__':
    '''
    usage: python rename.py PID CASES
    e.g., python 14 2 2 3
    '''
    pid = int(sys.argv[1])
    download_testdata(pid)
    if len(sys.argv) == 2:
        re_orgnize_with_single_testcase(pid)
    else:
        case_counts = [*map(int, sys.argv[2:])]
        re_orgnize(pid, case_counts)
