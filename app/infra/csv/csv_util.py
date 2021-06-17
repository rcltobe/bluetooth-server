import csv
import os
from typing import Callable
from typing import List


def save_row(file_name: str, data: List[str]):
    mode = 'a' if os.path.exists(file_name) else 'w'
    with open(file_name, mode) as file:
        writer = csv.writer(file)
        writer.writerow(data)


def delete_row(file_name: str, check: Callable[[List[str]], bool]):
    """
    対象の行のデータを削除
    :param file_name: 編集するファイル名
    :param check: 対応する項目を検索するコールバック
    """
    if not os.path.exists(file_name):
        return

    with open(file_name, 'r') as f:
        reader = csv.reader(f)
        rows = [
            row
            for row in reader
            if not check(row)
        ]
    with open(file_name, 'w') as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row)


def update_row(file_name: str, check: Callable[[List[str]], bool], on_update: Callable[[List[str]], List[str]]):
    """
    対象の行のデータを更新
    :param file_name: 編集するファイル名
    :param check: 対応する項目を検索するコールバック
    :param on_update: 対応する項目を更新するコールバック
    """
    if not os.path.exists(file_name):
        return

    with open(file_name, 'r') as f:
        reader = csv.reader(f)
        rows = [
            on_update(row) if check(row) else row
            for row in reader
        ]

    with open(file_name, 'w') as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row)
