
from gradio_client import Client, file

client = Client("http://api-base")

client.predict(
  local_high_LoRA_paths="path/to/LoRA",
  local_low_LoRA_paths="",
  api_name="/update_local_LoRA_path"
)

def generate_video(client, img_path, video_prompt, output_dir):
    """调用API生成单个视频并保存"""
    try:
        # 调用图生视频API（沿用已测试的参数）
        result = client.predict(
            prompt=video_prompt,
            negative_prompt='',
            seed=-1,
            steps=4,
            input_image=handle_file(img_path),
            end_image=None,
            mode_selector="图生视频", 
            fps_slider=24,
            input_video=None,
            prompt_refiner=False,
            lora_selector=["上传本地LoRA"],
            height=832,
            width=480,
            frame_num=75,
            api_name="/generate_video"
        )

        # 解析API返回的视频路径
        video_temp_path = result.get("video")
        if not video_temp_path or not os.path.exists(video_temp_path):
            print(f"警告：API未返回有效视频路径 {img_path}")
            return False

        # 构建输出视频路径
        img_dir, img_name = os.path.split(img_path)
        img_base_name, img_ext = os.path.splitext(img_name)
        output_video_name = f"{img_base_name}.mp4"
        output_video_path = os.path.join(output_dir, output_video_name)

        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)

        # 复制临时视频到输出目录（避免临时文件被清理）
        with open(video_temp_path, "rb") as f_in, open(output_video_path, "wb") as f_out:
            f_out.write(f_in.read())

        print(f"成功生成视频：{output_video_path}")
        return True

    except Exception as e:
        print(f"\n错误：生成视频失败 {img_path}")
        print(f"错误详情：{str(e)}")
        traceback.print_exc()
        return False
