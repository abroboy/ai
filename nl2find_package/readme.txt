========================================================
 NL2Find - 内网部署包使用说明
========================================================

本压缩包包含了 NL2Find 应用及其所有依赖，可在无法连接外网的环境中部署和运行。

## 部署与启动

请严格按照以下两个步骤操作。

**第一步：环境安装 (只需执行一次)**

1.  将本压缩包解压到任意位置。
2.  进入解压后的 `nl2find_package` 文件夹。
3.  **双击运行 `setup.bat` 脚本。**
4.  脚本会自动完成以下工作：
    *   检查您的电脑是否已安装 Python。
    *   在当前目录下创建一个名为 `venv` 的独立 Python 虚拟环境。
    *   从 `libs` 文件夹中安装所有必需的依赖库。
5.  安装完成后，按任意键关闭窗口。

**注意：** 如果脚本提示未找到 Python，请先安装 Python 3 并确保已将其添加到系统的 PATH 环境变量中。

**第二步：启动服务**

1.  环境安装成功后，在 `nl2find_package` 文件夹中，**双击运行 `start_server.bat` 脚本。**
2.  服务将在 `http://127.0.0.1:5001` 上启动并等待请求。
3.  请保持此命令行窗口开启，关闭窗口即代表关闭服务。

---
## 服务使用说明

服务启动后，您可以通过发送 HTTP 请求到 `http://127.0.0.1:5001/mcp` 端点来使用此服务。

以下示例使用 PowerShell 中的 `Invoke-RestMethod`。

**1. 创建计划**

*   功能：根据自然语言指令搜索文件，并创建一个计划文件。
*   请求体 (保存为 `request.json`):
    ```json
    {
        "query": "在 D:\\your\\directory 目录下查找所有和 'your_keyword' 相关的文件，并把结果保存到 my_plan.txt"
    }
    ```
*   发送请求:
    ```powershell
    Invoke-RestMethod -Uri http://127.0.0.1:5001/mcp -Method Post -Body (Get-Content request.json -Raw) -ContentType 'application/json'
    ```
*   成功后，系统会在 `nl2find_package/files/` 目录下创建一个名为 `my_plan.txt` 的文件。

**2. 为计划追加指令**

*   功能：为计划文件中列出的每个文件追加一个处理指令。
*   请求体 (保存为 `request.json`):
    ```json
    {
        "plan_id": "my_plan.txt",
        "instruction": "打印这个文件的行数"
    }
    ```
*   发送请求:
    ```powershell
    Invoke-RestMethod -Uri http://127.0.0.1:5001/mcp -Method Post -Body (Get-Content request.json -Raw) -ContentType 'application/json'
    ```

**3. 执行计划的下一步**

*   功能：执行计划中的下一个任务。
*   请求体 (保存为 `request.json`):
    ```json
    {
        "plan_id": "my_plan.txt"
    }
    ```
*   发送请求 (可重复执行以处理所有步骤):
    ```powershell
    Invoke-RestMethod -Uri http://127.0.0.1:5001/mcp -Method Post -Body (Get-Content request.json -Raw) -ContentType 'application/json'
    ``` 