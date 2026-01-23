import argparse
import os
import subprocess
from inaSpeechSegmenter import Segmenter
from tqdm import tqdm

def main():
    # 1. 设置命令行参数
    parser = argparse.ArgumentParser(description="基于 AI (inaSpeechSegmenter) 的全自动歌回切片工具")
    parser.add_argument("video_path", help="输入的视频文件路径 (例如: input.mp4)")
    parser.add_argument("--output", default="Songs_Export", help="输出文件夹名称 (默认: Songs_Export)")
    parser.add_argument("--trim_start", type=float, default=3.0, help="开头跳过秒数 (默认: 3.0)")
    parser.add_argument("--extend_end", type=float, default=5.0, help="结尾延长秒数 (默认: 5.0)")
    parser.add_argument("--min_duration", type=float, default=60.0, help="最短歌曲时长 (默认: 60.0)")
    parser.add_argument("--gap_tolerance", type=float, default=15.0, help="合并间隙容忍度 (默认: 15.0)")
    
    args = parser.parse_args()

    input_video = args.video_path
    output_dir = args.output

    if not os.path.exists(input_video):
        print(f"❌ 错误：找不到文件 {input_video}")
        return

    print(f">>> 正在处理: {input_video}")
    print(f">>> 参数配置: 开头+{args.trim_start}s | 结尾+{args.extend_end}s | 最小{args.min_duration}s")

    # 2. 提取音频
    print("\n>>> [1/3] 提取临时音频...")
    temp_audio = "temp_process.wav"
    subprocess.run([
        'ffmpeg', '-y', '-i', input_video, 
        '-vn', '-ac', '1', '-ar', '16000', temp_audio
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 3. AI 识别
    print(">>> [2/3] 神经网络识别中 (请稍候)...")
    seg = Segmenter(detect_gender=False)
    segmentation = seg(temp_audio)

    # 4. 逻辑处理
    music_segments = []
    for label, start, end in segmentation:
        if label == 'music':
            music_segments.append((start, end))

    merged_segments = []
    if music_segments:
        curr_start, curr_end = music_segments[0]
        for i in range(1, len(music_segments)):
            next_start, next_end = music_segments[i]
            if (next_start - curr_end) < args.gap_tolerance:
                curr_end = next_end
            else:
                if (curr_end - curr_start) >= args.min_duration:
                    merged_segments.append((curr_start, curr_end))
                curr_start, curr_end = next_start, next_end
        if (curr_end - curr_start) >= args.min_duration:
            merged_segments.append((curr_start, curr_end))

    if os.path.exists(temp_audio):
        os.remove(temp_audio)

    # 5. 导出
    if not merged_segments:
        print("❌ 未检测到歌曲。")
        return

    print(f"\n>>> 识别到 {len(merged_segments)} 首歌曲，准备导出...")
    if not os.path.exists(output_dir): os.makedirs(output_dir)

    for i, (s, e) in enumerate(tqdm(merged_segments, unit="file")):
        new_s = s + args.trim_start
        new_e = e + args.extend_end
        
        if new_s >= new_e: continue
        
        out_name = os.path.join(output_dir, f"Song_{i+1:02d}.mp4")
        subprocess.run([
            'ffmpeg', '-y', '-ss', f"{new_s:.2f}", '-to', f"{new_e:.2f}",
            '-i', input_video, '-c', 'copy', '-avoid_negative_ts', '1',
            '-loglevel', 'error', out_name
        ])

    print(f"\n✅ 全部完成！输出目录: {output_dir}")

if __name__ == "__main__":
    main()