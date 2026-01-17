# TimeExpandedGraph

このリポジトリは、Pythonと NetworkX を使用して、格子状マップ（Grid Map）をベースにした Time-Expanded Graph (TEG) を作成し、Matplotlib で可視化するスクリプトを提供します。

## 概要

Time-Expanded Graph (TEG) は、空間と時間を組み合わせたグラフ構造です。このスクリプトでは、3×3 の格子マップを T=5 のタイムステップで展開し、各ノードを (x, y, t) の形式で表現します。

## 機能

- **グラフ構造**: 
  - 格子サイズ: m=3, n=3
  - 最大タイムステップ: T=5
  - ノード形式: (x, y, t) - x, y は座標、t は時間

- **エッジの定義**:
  - **移動エッジ**: 時刻 t の地点 (x, y) から、時刻 t+1 の隣接する地点 (nx, ny) への有向エッジ（4近傍）
  - **待機エッジ**: 時刻 t の地点 (x, y) から、時刻 t+1 の同じ地点 (x, y) への有向エッジ

- **可視化**:
  - **2D可視化**:
    - 横軸: 時間 (t)
    - 縦軸: 空間（格子内の位置を1列に並べたもの）
    - ノードラベル: (x, y, t) 形式
    - 有向グラフとして描画
  - **3D可視化**:
    - X軸: x座標
    - Y軸: y座標
    - Z軸: 時間 (t)
    - ノードは時間ステップで色分け
    - 青い線: 待機エッジ（同じ位置に留まる）
    - 赤い線: 移動エッジ（隣接する位置への移動）

## インストール

必要なパッケージをインストールします：

```bash
pip install -r requirements.txt
```

## 使用方法

スクリプトを実行して、Time-Expanded Graph を生成・可視化します：

```bash
python time_expanded_graph.py
```

実行すると、`time_expanded_graph.png` というファイルが生成され、グラフが保存されます。

## 出力ファイル

スクリプトは以下の2つのファイルを生成します：

1. **time_expanded_graph.png**: 2D可視化（時間を横軸、空間位置を縦軸としたレイアウト）
2. **time_expanded_graph_3d.png**: 3D可視化（X-Y平面が空間座標、Z軸が時間）

## 出力例

スクリプトを実行すると、以下のような出力が表示されます：

```
Creating Time-Expanded Graph for 3×3 grid with T=5...
Graph created with 54 nodes and 165 edges.
Visualizing the graph in 2D...
Graph saved as 'time_expanded_graph.png'
Visualizing the graph in 3D...
3D Graph saved as 'time_expanded_graph_3d.png'
Done!
```

## グラフの詳細

- **ノード数**: 54 個 (3 × 3 × 6 = 54、t は 0 から 5 まで)
- **エッジ数**: 165 個
  - 各ノードから最大 5 つのエッジ（待機エッジ 1 つ + 移動エッジ最大 4 つ）
  - 境界のノードは移動先が少ないため、エッジ数が減る

## ファイル構成

- `time_expanded_graph.py`: メインスクリプト
- `requirements.txt`: 必要なパッケージ
- `README.md`: このファイル
- `time_expanded_graph.png`: 生成される2D可視化画像
- `time_expanded_graph_3d.png`: 生成される3D可視化画像

## 要件

- Python 3.7 以上
- NetworkX 3.0 以上
- Matplotlib 3.5.0 以上

## ライセンス

MIT License
