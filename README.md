# Auto-Song-Cutter (全自动歌回切片机) ✂️🎵

![Python](https://img.shields.io/badge/Python-3.10-blue.svg) ![FFmpeg](https://img.shields.io/badge/FFmpeg-Required-green.svg) ![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Auto-Song-Cutter** 是一个基于深度学习的全自动直播歌回切片工具。

它利用 [inaSpeechSegmenter](https://github.com/ina-foss/inaSpeechSegmenter) 神经网络模型，自动精准识别视频中的**歌唱部分 (Music)** 与**杂谈部分 (Speech)**，并调用 FFmpeg 进行**无损流拷贝**剪辑。

告别繁琐的手动拉轴和剪辑，一键提取直播中的所有歌曲！

## ✨ 核心特性

- 🧠 **AI 智能识别**：使用 CNN 模型精准区分人声与背景音乐，抗干扰能力强。
- ⚡ **无损极速剪辑**：底层调用 FFmpeg `-c copy`，不重编码，画质/音质 1:1 无损，速度极快。
- 🔗 **智能填缝**：自动忽略歌曲中间的简短停顿（间奏/过门），防止歌曲被切碎。
- ✂️ **精细化修剪**：支持自定义“跳过前奏说话”和“延长结尾伴奏”的时间。
- 🛠️ **高度可配置**：所有参数均可通过命令行调整。

## ⚙️ 环境依赖

由于依赖的深度学习库对环境要求严格，**强烈建议使用 Conda 创建 Python 3.10 虚拟环境**。

### 1. 前置准备
* **FFmpeg**: 请确保电脑已安装 FFmpeg 并配置到系统环境变量中。[下载地址](https://ffmpeg.org/download.html)
* **Anaconda/Miniconda**: 用于管理 Python 环境。

### 2. 安装步骤

```bash
# 1. 创建 Python 3.10 环境 (TensorFlow 兼容性最佳版本)
conda create -n singing python=3.10
conda activate singing

# 2. 安装项目依赖
# (会自动处理 numpy<2 和 tensorflow 的版本冲突)
pip install -r requirements.txt

```

## 🚀 快速开始

将你的直播录像文件（如 `input.mp4`）放入项目目录，然后在命令行运行：

```bash
python main.py input.mp4

```

程序将自动执行以下步骤：

1. 提取音频
2. AI 识别歌唱片段
3. 导出切片到 `Songs_Export` 文件夹

## 🎛️ 参数说明

你可以通过命令行参数微调切片逻辑，以适应不同的直播风格。

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `video_path` | (必填) | 输入视频文件的路径 |
| `--output` | `Songs_Export` | 输出文件夹名称 |
| `--trim_start` | `3.0` | **开头跳过秒数**。用于去除前奏中的说话声。设为 0 则保留全部。 |
| `--extend_end` | `5.0` | **结尾延长秒数**。用于防止切掉渐弱的尾奏或后半句。 |
| `--gap_tolerance` | `15.0` | **合并容忍度**。如果两段音乐间隔小于此值(秒)，将视为同一首歌。 |
| `--min_duration` | `60.0` | **最小歌曲时长**。小于此长度的片段会被视为误判（如BGM）并丢弃。 |

### 进阶用法示例

**场景：** 主播喜欢在前奏里说话（需要多跳过一点），且歌曲中间间奏很长（需要更强的合并能力）。

```bash
python main.py live_replay.mp4 --trim_start 5.0 --extend_end 8.0 --gap_tolerance 20.0

```

## ❓ 常见问题 (FAQ)

**Q1: 报错 `A module that was compiled using NumPy 1.x cannot be run in NumPy 2.x`?**

> A:这是因为 TensorFlow 尚不支持 Numpy 2.0。请确保你安装依赖时使用了本项目提供的 `requirements.txt`，它强制锁定了 `numpy<2`。

**Q2: 第一次运行非常慢？**

> A: 首次运行时，`inaSpeechSegmenter` 会自动下载神经网络模型文件（约几十MB），请保持网络通畅。下载完成后，之后的运行都会非常快。

**Q3: 为什么切出来的视频开头/结尾不太精准？**

> A: 本工具使用**无损剪辑** (`-c copy`)，这意味着剪辑点必须吸附到视频的**关键帧 (Keyframe)**。这是为了换取“秒级导出”和“无损画质”所必须的物理妥协。

## 🙏 致谢

* 核心算法基于 [inaSpeechSegmenter](https://github.com/ina-foss/inaSpeechSegmenter)
* 视频处理基于 [FFmpeg](https://ffmpeg.org/)

## 📄 License

MIT License

```

