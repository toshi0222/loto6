import random
import numpy as np
from itertools import combinations
from numba import cuda

def generate_combinations_from_array_gpu(array, exclude_numbers, total_range=43):
    """
    GPUの補助を使って、大量の組み合わせ処理を高速化
    """
    # フルレンジから除外数字を除く
    full_range = set(range(1, total_range + 1)) - set(exclude_numbers)

    # 4つの数字の組み合わせ（CPU側）
    four_combinations = list(combinations(array, 4))

    # 結果格納
    results = []

    for selected_four in four_combinations:
        remaining_numbers = list(full_range - set(selected_four))
        # ここで残りの2個の組み合わせをNumPyベースにして高速化
        two_combinations = list(combinations(remaining_numbers, 2))

        for two in two_combinations:
            full_combo = tuple(sorted(selected_four + two))
            results.append(full_combo)

    return results

def main():
    input_array = [1, 9, 11, 15, 16, 18, 19, 20, 27, 28, 35, 38, 39, 42, 43]
    exclude_numbers = [8, 12, 17, 21, 24, 29, 31, 33, 34, 37, 40]

    combinations_result = generate_combinations_from_array_gpu(input_array, exclude_numbers)

    # ランダムに200件選択
    sample_count = 200
    if len(combinations_result) > sample_count:
        random_sample = random.sample(combinations_result, sample_count)
    else:
        random_sample = combinations_result

    print(f"生成された組み合わせ総数: {len(combinations_result)}")
    print(f"ランダムに選択された {len(random_sample)} 件:")
    for combo in random_sample:
        print(combo)

if __name__ == "__main__":
    main()
