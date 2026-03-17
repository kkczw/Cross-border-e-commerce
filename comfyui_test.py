import websocket
import uuid
import json
import urllib.request
import urllib.parse
import os
import random
# ================= 配置区 =================
SERVER_ADDRESS = "127.0.0.1:8188"
CLIENT_ID = str(uuid.uuid4())
JSON_FILE = "mix_controlnet_api.json" # 你刚才导出的 API JSON 文件名
SAVE_DIR = "./output_images"          # 图片保存目录
# ==========================================

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def queue_prompt(prompt):
    """发送任务到 ComfyUI"""
    p = {"prompt": prompt, "client_id": CLIENT_ID}
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request(f"http://{SERVER_ADDRESS}/prompt", data=data)
    return json.loads(urllib.request.urlopen(req).read())

def get_image(filename, subfolder, folder_type):
    """从服务器获取二进制图片数据"""
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    with urllib.request.urlopen(f"http://{SERVER_ADDRESS}/view?{url_values}") as response:
        return response.read()

def get_history(prompt_id):
    """获取任务历史记录（包含输出的文件名）"""
    with urllib.request.urlopen(f"http://{SERVER_ADDRESS}/history/{prompt_id}") as response:
        return json.loads(response.read())

def run_workflow():
    # 1. 加载你的工作流 JSON
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        prompt_workflow = json.load(f)

    # (可选) 在这里修改参数，例如修改提示词
    # prompt_workflow["6"]["inputs"]["text"] = "a beautiful sunset"
    seed_modified=False
    for node_id,node_info in prompt_workflow.items():
        if node_info.get("class_type") in ["KSampler", "KSamplerAdvanced"]:
            new_seed=random.randint(1,1125899906842624)
            node_info["inputs"]["seed"]=new_seed
            print(f"检测到 {node_info['class_type']} 节点 (ID: {node_id})，已随机修改种子为: {new_seed}")
            seed_modified = True
            # 如果你有多个采样器，通常修改第一个即可，或者去掉 break 修改全部
            break 
    if not seed_modified:
        print("警告：在工作流中未找到 KSampler 节点，图片可能不会发生变化。")
    # 2. 连接 WebSocket (用于监听进度)
    ws = websocket.WebSocket()
    ws.connect(f"ws://{SERVER_ADDRESS}/ws?clientId={CLIENT_ID}")
    print(f"已连接到 ComfyUI，正在发送任务...")

    # 3. 发送任务
    prompt_response = queue_prompt(prompt_workflow)
    prompt_id = prompt_response['prompt_id']
    print(f"任务已入队，ID: {prompt_id}")

    # 4. 监听 WebSocket 消息
    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message['type'] == 'executing':
                data = message['data']
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    print("\n任务执行完毕！")
                    break # 任务完成
                else:
                    print(f"正在执行节点: {data['node']}", end="\r")
        else:
            continue # 二进制预览图忽略

    # 5. 任务完成后，提取图片并下载
    history_res = get_history(prompt_id)
    if prompt_id not in history_res:
        print(f"未找到任务 {prompt_id} 的历史记录")
        return

    history = history_res[prompt_id]
    
    # 遍历所有节点的输出，不再指定 ID 为 "3"
    for node_id, node_output in history.get('outputs', {}).items():
        if 'images' in node_output:
            for image in node_output['images']:
                image_data = get_image(image['filename'], image['subfolder'], image['type'])
                
                # 为了防止文件名冲突，建议加上 node_id
                save_filename = f"result_{node_id}_{image['filename']}"
                file_path = os.path.join(SAVE_DIR, save_filename)
                
                with open(file_path, "wb") as f:
                    f.write(image_data)
                print(f"成功！来自节点 {node_id} 的图片已保存: {file_path}")

    ws.close()

if __name__ == "__main__":
    try:
        run_workflow()
    except Exception as e:
        print(f"\n运行出错: {e}")