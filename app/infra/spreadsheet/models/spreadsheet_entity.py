from typing import List


class SpreadSheetEntity:
    @classmethod
    def validate(cls, attr_size: int, values: List[str], require_filled: bool = True) -> bool:
        """
        SpreadSheetの行データに対して、値の検証を行う。

        @:param attr_size 列の数
        @:param require_filled 全てのセルが埋まっている必要があるか
        """
        # セルの数は十分か
        if len(values) < attr_size:
            return False

        # 全てのセルに値が入っているか
        if not require_filled:
            return True

        for i, value in enumerate(values):
            if i >= attr_size:
                break
            if len(value) == 0:
                return False

        return True
