import os
import shutil
from pathlib import Path

def collect_first_frames(source_folder, output_folder):
    """
    从源文件夹中的每个camx文件夹收集frame_00001.jpg到新文件夹
    
    Args:
        source_folder: 包含camx文件夹的源目录
        output_folder: 输出目录
    """
    source_path = Path(source_folder)
    output_path = Path(output_folder)
    
    # 创建输出文件夹
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 查找所有camx文件夹
    cam_folders = [f for f in source_path.iterdir() 
                   if f.is_dir() and f.name.startswith('cam')]
    
    print(f"找到 {len(cam_folders)} 个cam文件夹")
    
    successful_copies = 0
    
    for cam_folder in sorted(cam_folders):
        frame_file = cam_folder / "frame_00001.jpg"
        
        if frame_file.exists():
            # 新文件名：cam文件夹名_frame_00001.jpg
            new_filename = f"{cam_folder.name}_frame_00001.jpg"
            destination = output_path / new_filename
            
            try:
                shutil.copy2(frame_file, destination)
                print(f"复制: {frame_file} -> {destination}")
                successful_copies += 1
            except Exception as e:
                print(f"复制失败 {frame_file}: {e}")
        else:
            print(f"文件不存在: {frame_file}")
    
    print(f"\n完成！成功复制了 {successful_copies} 个文件到 {output_folder}")

# 使用示例
if __name__ == "__main__":
    # 修改这两个路径
    source_folder = "./zju_mocap_dataset"
    output_folder = "./collected_frames"
    
    collect_first_frames(source_folder, output_folder)