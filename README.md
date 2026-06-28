# 授業内グループワーク制作物 Underbed Robot

ベッド下に落ちた物体をカメラで検知し、手元までモータで運ぶロボットです。  
Raspberry Pi + OpenCV + gpiozero を用いて実装しました。

## 概要

1. **動体検知**（背景差分法）で画角内の動く物体を検出
2. 検出した物体の色（HSV）を自動取得
3. 同じ色の物体をリアルタイムで追跡
4. X座標に応じてモータのスピードを調整しながら前進

赤色は誤検知が多いため対象外としています。

## ファイル構成

| ファイル | 内容 |
|---|---|
| `underbed_final.py` | メインスクリプト（動体検知・色追跡・モータ制御を統合） |
| `detect_object.py` | 背景差分による動体検知モジュール |
| `detect_color_position.py` | HSV色空間を用いた色検出・座標取得モジュール |
| `motor.py` | gpiozeroを用いたモータ制御モジュール |

## 動作環境

- Raspberry Pi（GPIOピン使用）
- Python 3
- OpenCV (`cv2`, `cv2.bgsegm`)
- gpiozero
- NumPy

## インストール

```bash
pip install opencv-contrib-python gpiozero numpy
```

## 使い方

```bash
python underbed_final.py
```

カメラ映像が表示されます。動く物体を映すと色を自動認識し、追跡を開始します。  
`q` キーで終了。

## モータ配線

| モータ | GPIOピン |
|---|---|
| 左モータ | 17, 18 |
| 右モータ | 19, 20 |

## 担当部分
- detect_object.py
- detect_color_position.py
