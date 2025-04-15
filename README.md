# Microsoft SpeechT5 TTS 服务

这是一个使用 Hugging Face Transformers 库中 `microsoft/speecht5_tts` 模型实现的简单文本转语音 (TTS) 服务。它通过 Flask 启动一个 Web 服务器，并提供一个 API 端点将文本转换为语音。

## 功能

* 接收包含文本的 POST 请求。
* 使用 SpeechT5 模型将文本合成为语音。
* 使用预定义的 CMU ARCTIC 说话人嵌入 (ID: 7306)。
* 将生成的语音保存为 `speech.wav` 文件。
* 在服务器端播放生成的语音文件 (使用 `playsound3`)。
* 返回操作成功或失败的 JSON 响应。

## 依赖项

* Python 3.12+
* transformers
* torch
* soundfile
* datasets
* flask
* playsound3
* numpy (<2.0.0)
* sentencepiece

## 安装

1. **克隆仓库:**

    ```bash
    git clone https://github.com/CaicoLeung/microsoft-speecht5-tts-service
    cd microsoft-speecht5-tts
    ```

2. **创建虚拟环境 (推荐):**

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Linux/macOS
    # .venv\Scripts\activate  # Windows
    ```

3. **安装依赖:**
    推荐使用 `uv` (如果已安装):

    ```bash
    uv pip install -r requirements.txt # 或者直接 uv pip install . 如果 pyproject.toml 配置完整
    # 如果没有 requirements.txt，可以根据 pyproject.toml 安装
    uv pip install transformers==4.37.2 torch==2.2.0 soundfile==0.12.1 datasets==2.17.1 flask==3.0.2 playsound3==3.2.3 "numpy<2.0.0" sentencepiece==0.2.0
    ```

    或者使用 `pip`:

    ```bash
    pip install -r requirements.txt # 或者直接 pip install . 如果 pyproject.toml 配置完整
    # 如果没有 requirements.txt，可以根据 pyproject.toml 安装
    pip install transformers==4.37.2 torch==2.2.0 soundfile==0.12.1 datasets==2.17.1 flask==3.0.2 playsound3==3.2.3 "numpy<2.0.0" sentencepiece==0.2.0
    ```

    *(注意: 你可能需要创建一个 `requirements.txt` 文件，或者可以直接从 `pyproject.toml` 安装)*

## 使用方法

1. **启动服务器:**

    ```bash
    python main.py
    ```

    服务器将在 `http://0.0.0.0:8000` 上运行。

2. **发送请求:**
    使用 `curl` 或其他 HTTP 客户端向 `/text-to-speech` 端点发送 POST 请求，请求体为包含 `text` 字段的 JSON 数据。

    ```bash
    curl -X POST http://localhost:8000/text-to-speech \
         -H "Content-Type: application/json" \
         -d '{"text": "Hello world, this is a test."}'
    ```

3. **响应:**
    * 成功时，服务器将返回 `{"success": true}`，并在服务器上播放生成的 `speech.wav` 文件。
    * 失败时，服务器将返回包含错误信息的 JSON，例如 `{"error": "No text provided"}` 或其他异常信息。

## Docker (可选)

项目包含一个 `Dockerfile`，你可以使用 Docker 来构建和运行此服务。

1. **构建镜像:**

    ```bash
    docker build -t speecht5-tts-service .
    ```

2. **运行容器:**

    ```bash
    docker run -p 8000:8000 speecht5-tts-service
    ```

    现在可以通过 `http://localhost:8000` 访问服务。

## 注意事项

* 每次请求都会覆盖之前的 `speech.wav` 文件。
* 语音播放是在服务器端进行的。
* 使用的说话人声音是固定的 (CMU ARCTIC 7306)。

## 未来改进 (可选)

* 允许通过 API 参数选择不同的说话人。
* 提供下载生成的 `.wav` 文件的选项，而不是仅在服务器端播放。
* 添加对语速、音调等参数的调整。
* 改进错误处理和日志记录。
