import os
import numpy as np
import pandas as pd

def convert_npz_to_csv(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.npz'):
            npz_path = os.path.join(directory, filename)
            data = np.load(npz_path)
            
            # 複数の配列が含まれている可能性があるため、1つずつ処理
            for key in data.files:
                array = data[key]
                
                # DataFrameに変換（1次元/2次元配列対応）
                df = pd.DataFrame(array)
                
                # 出力ファイル名
                base_name = os.path.splitext(filename)[0]
                output_filename = f"{base_name}_{key}.csv"
                output_path = os.path.join(directory, output_filename)
                
                df.to_csv(output_path, index=False)
                print(f"Saved: {output_path}")

# 使用例（パスを適宜変更）
input_dir = input("Dir: ")
convert_npz_to_csv(input_dir)
