from __future__ import annotations

import asyncio
import os
from concurrent.futures import ThreadPoolExecutor
from typing import List, Any, Callable

import gspread_asyncio
from google.oauth2.service_account import Credentials
from gspread import Cell
from gspread_asyncio import AsyncioGspreadWorksheet


def _get_credentials():
    credentials = Credentials.from_service_account_file(SpreadSheetUtil._get_credential_file_path())
    scoped_credential = credentials.with_scopes([
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ])
    return scoped_credential


async def _create_async(runnable: Callable[[], Any]) -> Any:
    """
    ブロッキングコールをノンブロッキングコールに変換する
    """
    loop = asyncio.get_running_loop()
    executor = ThreadPoolExecutor()
    future = loop.run_in_executor(executor, runnable)
    results = await asyncio.gather(future)
    executor.shutdown(wait=True)
    return results[0]


class SpreadSheetUtil:
    def __init__(self, num_columns: int, book_name: str):
        """
        :param num_columns: 扱うデータの行数
        :param book_name: SpreadSheetのブックの名前
        """
        self.data_range = f"A:{chr(ord('A') + num_columns - 1)}"
        self.num_columns = num_columns
        self.book_name = book_name
        self._client = None

    @classmethod
    def _get_spreadsheet_key(cls):
        return os.environ.get("SPREADSHEET_KEY")

    @classmethod
    def _get_credential_file_path(cls):
        return os.environ.get("CREDENTIAL_FILE_PATH")

    async def _get_worksheet(self) -> AsyncioGspreadWorksheet:
        if self._client is None:
            client_manager = gspread_asyncio.AsyncioGspreadClientManager(_get_credentials)
            self._client = await client_manager.authorize()
        book = await self._client.open_by_key(self._get_spreadsheet_key())
        return await book.worksheet(self.book_name)

    async def find_all(self, value: str, column: int) -> List[Cell]:
        """
        column の値が valueであるすべてのセルを取得
        """
        worksheet = await self._get_worksheet()
        result = await _create_async(lambda: worksheet.ws.findall(value, in_column=column))
        return result

    async def batch_get(self, ranges: List[str]) -> List[List[List[str]]]:
        worksheet = await self._get_worksheet()
        results = await _create_async(lambda: worksheet.ws.batch_get(ranges))
        return results

    async def get_values(self) -> List[List[str]]:
        """
        ワークシートにあるすべての値を取得
        """
        worksheet = await self._get_worksheet()
        return await worksheet.get_all_values()

    async def append_values(self, values: List[str]):
        """
        SpreadSheetに値を書き込む
        :param values: 書き込む値
        """
        worksheet = await self._get_worksheet()
        row = len(await self.get_values()) + 1
        cells = [Cell(row, i + 1, values[i]) for i in range(0, len(values))]
        await worksheet.update_cells(cells)

    async def get_row(self, row) -> List[str]:
        """
        値がvalueと一致する行を取得する
        @:param value 検索する値
        @:param column 添削する列番号
        """
        worksheet = await self._get_worksheet()
        values = await worksheet.row_values(row)
        return values

    async def get_row_number_of(self, value: str, column: int) -> int:
        """
        値がvalueと一致するセルの行数を取得する
        @:param value 検索する値
        @:param column 添削する列番号
        @:return 行数、見つからなかった場合は-1
        """
        worksheet = await self._get_worksheet()
        column_values = await worksheet.col_values(column)
        row = -1
        for i, v in enumerate(column_values):
            if v is not None and v == value:
                row = i + 1

        return row

    async def clear_values(self, row: int):
        worksheet = await self._get_worksheet()
        await worksheet.delete_row(row)
