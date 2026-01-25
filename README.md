# Auto-Song-Cutter (全自动歌回切片机) ✂️🎵

![Python](https://img.shields.io/badge/Python-3.10-blue.svg) ![FFmpeg](https://img.shields.io/badge/FFmpeg-Required-green.svg) ![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Auto-Song-Cutter** 是一个基于深度学习的全自动直播歌回切片与识曲工具。

它利用 **inaSpeechSegmenter** 精准提取歌曲片段，使用 **FFmpeg** 进行无损剪辑，并集成了 **Shazam** 接口实现全自动听歌识曲与文件重命名。

## ✨ 核心特性

- 🧠 **AI 智能分段**：精准区分 Singing (歌唱) 与 Speech (杂谈)，自动剔除 BGM 干扰。
- 📝 **自动日志**：切片同时生成 `segments_log.txt`，记录包含原始时间戳的详细歌单。
- 🔍 **贪心识曲 (New)**：集成 Shazam 贪心算法，自动在 0s/60s/120s 多点采样，大幅提高识曲准确率。
- 🏷️ **自动重命名**：识别成功后自动将 `Song_01.mp4` 重命名为 `歌名 - 歌手.mp4`。
- 🛠️ **B站专用修复**：提供一键修复脚本，解决 B 站网页端无法播放的问题，或暴力开启 Hi-Res 图标。

## ⚙️ 安装依赖

建议使用 Python 3.10 环境（以获得最佳 TensorFlow 兼容性）。

```bash
# 安装核心依赖 (会自动锁定 numpy<2 以兼容 inaSpeechSegmenter)
pip install -r requirements.txt
注意：本项目依赖 FFmpeg，请确保电脑已安装 FFmpeg 并配置了环境变量。

🚀 使用指南 (Workflows)
本项目设计为拖拽式工作流，主要包含三个步骤：

第一步：全自动切片 (Auto Cut)
运行 main.py 或使用批处理脚本。

Bash

python main.py input.mp4 --trim_start 3.0 --min_duration 60
输出：默认生成 Songs_Export 文件夹。

日志：文件夹内包含 segments_log.txt，记录了切片的原始起止时间。

第二步：听歌识曲与改名 (Auto Recognize)
切片完成后，运行 recognize_greedy.py (或使用 一键识曲_贪心版.bat)。

它会自动扫描输出文件夹，对未命名的 Song_xx.mp4 进行多点位识别：

策略：尝试开头 0s -> 副歌 60s -> 尾奏 120s。

结果：一旦命中，自动重命名文件。

第三步：B站上传处理 (Post-Processing)
针对 Bilibili 上传优化，提供两个专用脚本：

hires_fix.bat (推荐)

功能：修复音频编码为 AAC-LC 320k，重写时间戳。

用途：解决上传后 B 站网页端黑屏、无法播放的问题。

画质：无损 Copy。

force_hires.bat (发烧友)

功能：强制转码为 FLAC 音频并封装为 MKV。

用途：暴力激活 B 站的 "Hi-Res" 无损音质图标。

📂 推荐目录结构
为了保证脚本正常运行，建议目录结构如下：

Plaintext

Auto-Song-Cutter/
├── .venv/                 # Python 虚拟环境
├── main.py                # 切片主程序
├── recognize_greedy.py    # 识曲主程序
├── requirements.txt       # 依赖清单
├── 一键切歌.bat           # 拖拽启动脚本
├── 一键识曲_贪心版.bat    # 点击启动脚本
└── README.md              # 说明文档
❓ 常见问题
Q: 识曲脚本报错 找不到文件夹？ A: 脚本默认查找 Songs_Export, hires, Bilibili_Ready 等文件夹。如果你修改了输出目录名，请在 recognize_greedy.py 的 POSSIBLE_FOLDERS 列表中添加你的文件夹名。

Q: 批处理脚本无法处理中文文件名？ A: 请确保你的 .bat 文件是以 ANSI (GB2312) 编码保存的，不要使用 UTF-8。

Q: 识别率突然下降？ A: 不同主播的混音风格不同。如果 BGM 太大导致误判，请在切片时尝试增大 --min_duration (如 90) 或减小 --gap_tolerance (如 5)。

📄 License
MIT License