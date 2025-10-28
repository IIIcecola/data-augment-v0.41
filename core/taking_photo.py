from gradio_client import Client, handle_file
import shutil
import os
from tqdm import tqdm

client = Client("http://10.59.67.2:5012/")

def find_image_files(root_dir):
  image_extensions = (".jpg", ".jepg", ".png", ".gif", ".bmp", ".tiff", ".webp")
  image_files = []

  for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
      if filename.lower().endwith(image_extensions):
        file_path = os.path.join(dirpath, filename)
        image_files.append(file_path)

  return image_files

def edit_one_image(client, image_path, prompt, output_path):
  print(image_path)
  result = client.predict(
    image1=handle_file(image_path),
    image2=None,
    image3=None,
    prompt=prompt,
    seed=0,
    randomize_seed=True,
    true_guidance_scale=1,
    num_inference_steps=4,
    rewrite_prompt=False,
    height=720,
    width=1280,
    api_name="/infer"
  )
  src_path = result[0]

  os.makedirs(output_path, exist_ok=True)
  base_name = os.path.join(output_path, base_name[:-4]+'_'+prompt+base_name[-4:])

  try:
    shutil.move(src_path, dst_path)
    # shutil.copy2(src_path, dst_path)
  except FileNotFoundError:
    print(f"源文件不存在: {src_path}")
  except Exception as e:
    print(f"操作失败: {e}")

prompt_list = [
  '',
  '',
  '',
  ''
]

for image_path in tqdm(all_image_path):
  for prompt in prompt_list:
    edit_onr_image(client, image_path, prompt, "path/to/dir")


