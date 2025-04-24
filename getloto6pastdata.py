import requests
import pandas as pd
from io import StringIO
from collections import Counter
import os

# CSVデータのURL
url = "https://loto6.thekyo.jp/data/loto6.csv"

# ローカルに保存するファイル名
local_file = "loto6_data.csv"

def fetch_data_from_url(url):
    """URLからデータを取得する"""
    try:
        response = requests.get(url)
        response.raise_for_status()  # HTTPエラーをチェック
        csv_data = response.content.decode("shift_jis")
        print("データをURLから取得しました。")
        return csv_data
    except requests.exceptions.RequestException as e:
        print("データを取得できませんでした:", e)
        return None

def load_data_from_file(file_path):
    """ローカルファイルからデータを読み込む"""
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            print("ローカルファイルからデータを読み込みました。")
            return f.read()
    else:
        print("ローカルファイルが見つかりません。")
        return None

def save_data(data, file_path):
    """データをローカルに保存する"""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(data)
    print("データをローカルに保存しました。")

def calculate_occurrence_rates(df, start_idx, end_idx, columns):
    """指定範囲で数字の出現率を計算する"""
    selected_rows = df.iloc[start_idx:end_idx]
    selected_dates = selected_rows["日付"].tolist()
    
    # 数字をすべて収集してカウント
    all_numbers = []
    for col in columns:
        all_numbers.extend(selected_rows[col])
    
    # 出現回数をカウント
    count = Counter(all_numbers)
    total_numbers = sum(count.values())
    
    # 出現率を計算
    rates = {number: (freq / total_numbers) * 100 for number, freq in count.items()}
    sorted_rates = sorted(rates.items(), key=lambda x: x[1], reverse=True)
    
    return sorted_rates, selected_dates

def compare_and_get_top_numbers(data1, data2, top_n=6):
    """2つの出現率データを比較し、出現率の高い共通または特定の数字を抽出"""
    combined = Counter()
    for number, rate in data1:
        combined[number] += rate
    for number, rate in data2:
        combined[number] += rate
    
    # 出現率の高い順に並べて上位N件を取得
    top_numbers = sorted(combined.items(), key=lambda x: x[1], reverse=True)[:top_n]
    return top_numbers

def calculate_top_numbers_with_rates(df, start_idx, end_idx, columns):
    """
    指定範囲で出現回数が多い数字と出現率を取得
    """
    selected_rows = df.iloc[start_idx:end_idx]
    
    # 数字をすべて収集してカウント
    all_numbers = []
    for col in columns:
        all_numbers.extend(selected_rows[col])
    
    # 出現回数をカウント
    count = Counter(all_numbers)
    total_numbers = sum(count.values())
    
    # 出現回数と出現率を計算
    rates = {number: (freq / total_numbers) * 100 for number, freq in count.items()}
    sorted_rates = sorted(rates.items(), key=lambda x: x[1], reverse=True)
    
    return sorted_rates

def main():
    # URLからデータを取得
    csv_data = fetch_data_from_url(url)
    if csv_data is None:
        csv_data = load_data_from_file(local_file)
    else:
        save_data(csv_data, local_file)

    if csv_data:
        df = pd.read_csv(StringIO(csv_data))
        
        # 出現率を計算する列
        columns = ["第1数字", "第2数字", "第3数字", "第4数字", "第5数字", "第6数字"]
        
        total_rows = len(df)
        
        # 範囲を設定
        ranges = {
            "A": (total_rows - 4, total_rows),
            "B": (total_rows - 8, total_rows - 4),
            "C": (total_rows - 12, total_rows - 8)
        }
        
        # 各範囲の出現率を計算
        results = {}
        for key, (start_idx, end_idx) in ranges.items():
            results[key], dates = calculate_occurrence_rates(df, start_idx, end_idx, columns)
            print(f"\n【範囲 {key}】")
            print(f"日付: {dates}")
            for number, rate in results[key]:
                print(f"{number}: {rate:.2f}%")
        
        # 範囲CとBの比較
        print("\n【範囲 C と B の比較】")
        top_c_b = compare_and_get_top_numbers(results["C"], results["B"])
        for number, combined_rate in top_c_b:
            print(f"{number}: {combined_rate:.2f}%")
        
        # 範囲BとAの比較
        print("\n【範囲 B と A の比較】")
        top_b_a = compare_and_get_top_numbers(results["B"], results["A"])
        for number, combined_rate in top_b_a:
            print(f"{number}: {combined_rate:.2f}%")
        
        # 最後から12回分の結果を取得
        print("\n【最後から12回分の結果】")
        top_numbers_with_rates = calculate_top_numbers_with_rates(df, total_rows - 12, total_rows, columns)
        print("出現回数の多い数字とその出現率:")
        for num, rate in top_numbers_with_rates:
            print(f"{num}: 出現率 {rate:.2f}%")
    else:
        print("データが取得できませんでした。")

if __name__ == "__main__":
    main()
