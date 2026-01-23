# Auto-Song-Cutter (全自动歌回切片机) ✂️🎵

基于深度学习 (`inaSpeechSegmenter`) 的全自动直播歌回切片工具。
无需人工干预，自动识别唱歌部分（Music）与杂谈部分（Speech），并调用 FFmpeg 进行**无损**剪辑。

## ✨ 特性

- **精准识别**：使用 CNN 神经网络区分人声与背景音乐。
- **无损画质**：使用 FFmpeg 流拷贝 (`-c copy`)，不重编码，画质无损且速度极快。
- **智能填缝**：自动忽略歌曲中间的简短停顿。
- **首尾修剪**：支持自动跳过前奏说话和延长结尾伴奏。

## 🛠️ 安装指南 (Windows/Linux)

**注意：由于依赖库兼容性问题，强烈建议使用 Conda 创建 Python 3.10 环境。**

1. **安装 FFmpeg**
   确保你的电脑已安装 `ffmpeg` 并配置了环境变量。

2. **创建环境**
   ```bash
   conda create -n singing python=3.10
   conda activate singing