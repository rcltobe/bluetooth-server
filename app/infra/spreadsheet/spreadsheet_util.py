from __future__ import annotations

import asyncio
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from typing import List, Any, Callable

import gspread_asyncio
from google.oauth2.service_account import Credentials
from gspread import Cell
from gspread_asyncio import AsyncioGspreadWorksheet


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
        """
        環境変数から、SpreadSheetのキーを取得(.envをファイルを参照)
        """
        return os.environ.get("SPREADSHEET_KEY")

    @classmethod
    def _get_credential_file_path(cls):
        """
        環境変数から、秘密鍵のファイルパスを取得(.envをファイルを参照)
        """
        return os.environ.get("CREDENTIAL_FILE_PATH")

    @classmethod
    def _get_credentials(cls):
        credentials = Credentials.from_service_account_file(SpreadSheetUtil._get_credential_file_path())
        scoped_credential = credentials.with_scopes([
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ])
        return scoped_credential

    async def _get_worksheet(self) -> AsyncioGspreadWorksheet:
        if self._client is None:
            client_manager = gspread_asyncio.AsyncioGspreadClientManager(SpreadSheetUtil._get_credentials)
            self._client = await client_manager.authorize()
        book = await self._client.open_by_key(self._get_spreadsheet_key())
        return await book.worksheet(self.book_name)

    async def get_values(self) -> List[List[str]]:
        """
        ワークシートにあるすべての値を取得。
        頻繁に呼び出してしまうと、一時的に停止させられる。
        """
        logging.info("get values")
        worksheet = await self._get_worksheet()
        return await worksheet.get_all_values()

    async def append_all_values(self, values: List[List[str]]):
        """
        複数行に渡る値を保存
        １行１行保存するよりも、リクエスト数を減らすことができる。
        """
        logging.info("append all values")

        row = len(await self.get_values()) + 1

        cells = []
        for row_i in range(len(values)):
            row_values = values[row_i]
            row_cells = [Cell(row_i + row, i + 1, row_values[i]) for i in range(0, len(row_values))]
            cells.extend(row_cells)

        worksheet = await self._get_worksheet()
        await worksheet.update_cells(cells)

    async def delete_rows(self, start_row: int, end_row: int):
        logging.info("delete rows")
        worksheet = await self._get_worksheet()
        await worksheet.delete_rows(start_row, end_row)
