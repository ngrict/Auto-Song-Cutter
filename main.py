import argparse
import os
import subprocess
from inaSpeechSegmenter import Segmenter
from tqdm import tqdm

def format_timestamp(seconds):
    """将秒数转换为 HH:MM:SS.mmm 格式"""
    if seconds < 0: seconds = 0
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return f"{int(h):02d}:{int(m):02d}:{s:06.3f}"

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

    # 获取绝对路径，方便记录
    abs_video_path = os.path.abspath(input_video)

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

    # 5. 导出与记录
    if not merged_segments:
        print("❌ 未检测到歌曲。")
        return

    print(f"\n>>> 识别到 {len(merged_segments)} 首歌曲，准备导出...")
    if not os.path.exists(output_dir): os.makedirs(output_dir)

    # === 准备 Log 文件 ===
    log_file_path = os.path.join(output_dir, "segments_log.txt")
    
    with open(log_file_path, "w", encoding="utf-8") as f_log:
        # 写入头部信息
        f_log.write(f"Source Video: {abs_video_path}\n")
        f_log.write(f"Total Songs: {len(merged_segments)}\n")
        f_log.write("--------------------------------------------------------------------------------------\n")
        # 调整表头，增加 Duration 和 Size
        f_log.write(f"{'Filename':<15} | {'Start Time':<15} | {'End Time':<15} | {'Duration':<15} | {'Size (MB)':<10}\n")
        f_log.write("--------------------------------------------------------------------------------------\n")

        for i, (s, e) in enumerate(tqdm(merged_segments, unit="file")):
            # 计算最终时间 (应用偏移量)
            new_s = s + args.trim_start
            new_e = e + args.extend_end
            
            if new_s >= new_e: continue
            
            filename = f"Song_{i+1:02d}.mp4"
            out_name = os.path.join(output_dir, filename)

            # === 1. 先执行切片 (必须先生成文件才能获取大小) ===
            subprocess.run([
                'ffmpeg', '-y', '-ss', f"{new_s:.2f}", '-to', f"{new_e:.2f}",
                '-i', input_video, '-c', 'copy', '-avoid_negative_ts', '1',
                '-loglevel', 'error', out_name
            ])

            # === 2. 获取文件信息 ===
            # 计算时长
            duration_sec = new_e - new_s
            
            # 获取文件大小 (单位: MB)
            file_size_mb = 0.0
            if os.path.exists(out_name):
                file_size_mb = os.path.getsize(out_name) / (1024 * 1024)

            # === 3. 格式化字符串 ===
            time_start_str = format_timestamp(new_s)
            time_end_str = format_timestamp(new_e)
            time_dur_str = format_timestamp(duration_sec)

            # === 4. 写入日志 ===
            # 使用 <15 对齐列，MB 保留两位小数
            f_log.write(f"{filename:<15} | {time_start_str:<15} | {time_end_str:<15} | {time_dur_str:<15} | {file_size_mb:.2f} MB\n")
            
            # 实时刷新缓冲区
            f_log.flush() 

    print(f"\n✅ 全部完成！输出目录: {output_dir}")
    print(f"📄 详细日志(含时长/大小)已保存至: {log_file_path}")

if __name__ == "__main__":
    main()