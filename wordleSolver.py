import re
from typing import Dict, List

WORDLE_WORD_LIST_FILE_PATH = './WORDLE'


def read_file(path: str) -> List[str]:
    """ファイルの読み込みを行い、行ごとのリストにして返却する

    Args:
        path (str): 読み込みたいファイルのパス(絶対|相対)

    Returns:
        List[str]: 行ごとのリスト
    """
    with open(path) as f:
        l_strip = [s.strip() for s in f.readlines()]
    return l_strip


def get_word_list() -> List[str]:
    """WORDLEの単語候補リストを取得する

    Returns:
        List[str]: 単語候補リスト
    """
    wordle_list = read_file(WORDLE_WORD_LIST_FILE_PATH)
    return wordle_list


def get_green_guess_list(
        word_list: List[str],
        green_list: Dict[int, str]) -> List[str]:
    """完全にHitした文字に対応する推測を返却する

    Args:
        word_list (List[str]): 単語候補リスト
        green_list (Dict[int, str]): 完全にHitした文字の辞書リスト

    Returns:
        List[str]: 抽出した候補リスト
    """
    for k, v in green_list.items():
        if k == 1:
            word_list = [s for s in word_list if re.match(f'{v}....', s)]
        elif k == 2:
            word_list = [s for s in word_list if re.match(f'.{v}...', s)]
        elif k == 3:
            word_list = [s for s in word_list if re.match(f'..{v}..', s)]
        elif k == 4:
            word_list = [s for s in word_list if re.match(f'...{v}.', s)]
        elif k == 5:
            word_list = [s for s in word_list if re.match(f'....{v}', s)]
        else:
            word_list = word_list
    return word_list


def get_yellow_guess_list(
        word_list: List[str],
        yellow_list: Dict[int, str]) -> List[str]:
    """一部Hitした文字に対応する推測を返却する

    Args:
        word_list (List[str]): 単語候補リスト
        yellow_list (Dict[int, str]): 一部Hitした文字の辞書リスト

    Returns:
        List[str]: 抽出した候補リスト
    """
    for k, v in yellow_list.items():
        if k == 1:
            word_list = [s for s in word_list if re.match(f'[^{v}]....', s)]
        elif k == 2:
            word_list = [s for s in word_list if re.match(f'.[^{v}]...', s)]
        elif k == 3:
            word_list = [s for s in word_list if re.match(f'..[^{v}]..', s)]
        elif k == 4:
            word_list = [s for s in word_list if re.match(f'...[^{v}].', s)]
        elif k == 5:
            word_list = [s for s in word_list if re.match(f'....[^{v}]', s)]
        else:
            word_list = word_list
        word_list = [s for s in word_list if v in s]
    return word_list


def get_black_guess_list(
        word_list: List[str],
        black_list: List[str]) -> List[str]:
    """Hitしなかった文字に対応する推測を返却する

    Args:
        word_list (List[str]): 単語候補リスト
        black_list (List[str]): Hitしなかった文字のリスト

    Returns:
        List[str]: 抽出した候補リスト
    """
    for black in black_list:
        word_list = [s for s in word_list if black not in s]
    return word_list


def main():
    # 単語候補リスト
    word_list = get_word_list()

    # 完全一致した文字の辞書リスト {key: 何文字目か, value: 文字[a-z]}
    green_list = {2: 'i', 3: 'g', 4: 'h', 5: 't'}
    word_list = get_green_guess_list(word_list, green_list)

    # 部分一致した文字の辞書リスト {key: 何文字目か, value: 文字[a-z]}
    yellow_list = {3: 'i', 4: 'i'}
    word_list = get_yellow_guess_list(word_list, yellow_list)

    # 一致しなかった文字のリスト ['a', 'b', ...]
    black_list = []
    word_list = get_black_guess_list(word_list, black_list)

    print(word_list)
    print(len(word_list))


if __name__ == "__main__":
    main()
