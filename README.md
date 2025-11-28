# DeepSeek Web Chat 部署指南

这是一个基于DeepSeek API的Web聊天应用，使用Docker容器化部署，支持流式响应和会话管理。

## 快速开始

### 1. 构建Docker镜像
```bash
docker build -t deepseek-chat:latest .
```

### 2. 运行容器（使用默认端口21048）
```bash
docker run -d \
  -p 21048:21048 \
  -e DEEPSEEK_API_KEY="sk-xxxxx" \  # 替换为您的API密钥
  --name deepseek-chat \
  deepseek-chat:latest
```

### 3. 访问应用
在浏览器中打开：`http://localhost:21048`

## 自定义端口设置

### 方法1：通过端口映射（推荐）
```bash
docker run -d \
  -p <宿主机端口>:21048 \  # 将21048替换为您想要的宿主机端口
  -e DEEPSEEK_API_KEY="sk-xxxxx" \
  --name deepseek-chat \
  deepseek-chat:latest
```

**示例**：使用8080端口
```bash
docker run -d \
  -p 8080:21048 \
  -e DEEPSEEK_API_KEY="sk-xxxxx" \
  --name deepseek-chat \
  deepseek-chat:latest
```

### 方法2：修改容器内部端口
```bash
docker run -d \
  -p <宿主机端口>:<容器端口> \  # 两个端口可以不同
  -e PORT=<容器端口> \          # 设置容器内部服务端口
  -e DEEPSEEK_API_KEY="sk-xxxxx" \
  --name deepseek-chat \
  deepseek-chat:latest
```

**示例**：容器内部使用3000端口，宿主机映射到4000端口
```bash
docker run -d \
  -p 4000:3000 \
  -e PORT=3000 \
  -e DEEPSEEK_API_KEY="sk-xxxxx" \
  --name deepseek-chat \
  deepseek-chat:latest
```

## 详细配置选项

### 必需参数
- **DEEPSEEK_API_KEY**: DeepSeek API密钥（必须提供）

### 可选参数
| 环境变量               | 默认值                         | 说明                                            |
| ------------------ | --------------------------- | --------------------------------------------- |
| `PORT`             | `21048`                     | 容器内部服务端口                                      |
| `DEEPSEEK_API_URL` | `https://api.deepseek.com/` | DeepSeek API地址                                |
| `DEEPSEEK_MODEL`   | `deepseek-chat`             | 使用的模型 (`deepseek-chat` 或 `deepseek-reasoner`) |
| `TZ`               | `Asia/Shanghai`             | 时区设置                                          |
| `FLASK_DEBUG`      | `0`                         | 调试模式 (1开启/0关闭)                                |
| `PYTHONUNBUFFERED` | 1                           | 禁用输出缓存                                        |
 **API_URL及MODEL 也可使用腾讯云地址具体如下：**
>DEEPSEEK_API_URL="https://api.lkeap.cloud.tencent.com/v1"
>DEEPSEEK_MODEL="支持的模型如下"
- DeepSeek-V3-0324（model 参数值为**deepseek-v3-0324**）
    - DeepSeek-V3-0324为671B参数MoE模型，在编程与技术能力、上下文理解与长文本处理等方面优势突出。
    - 支持128K上下文长度，最大输出16k（不含思维链）。
    - 注意：相比于DeepSeek-V3，DeepSeek-V3-0324仅更新了模型权重，未增加参数量。总模型大小为685B，其中包括671B的主模型权重和 14B 的多令牌预测（MTP）模块权重，后续均描述主模型参数量。
- DeepSeek-V3（model 参数值为**deepseek-v3**）
    - DeepSeek-V3为671B参数MoE模型，在百科知识、数学推理等多项任务上优势突出，评测成绩在主流榜单中位列开源模型榜首。
    - 支持64K上下文长度，最大输出16k。
- DeepSeek-R1（model 参数值为**deepseek-r1**）
    - DeepSeek-R1为671B模型，使用强化学习训练，推理过程包含大量反思和验证，思维链长度可达数万字。 该系列模型在数学、代码以及各种复杂逻辑推理任务上推理效果优异，并为用户展现了完整的思考过程。
    - 支持96K上下文长度，最大输入长度64k，最大输出16k（默认4k），最大思维链输出长度32k。
- DeepSeek-R1-0528（model 参数值为**deepseek-r1-0528**）
    - DeepSeek-R1-0528为671B 模型，架构优化与训练策略升级后，相比上一版本在代码生成、长文本处理和复杂推理领域提升明显。
    - 支持96K上下文长度，最大输入长度64k，最大输出16k（默认4k），最大思维链输出长度32k。
### 完整运行示例（自定义端口）
```bash
docker run -d \
  -p 8888:3000 \  # 宿主机8888端口映射到容器3000端口
  -e PORT=3000 \  # 容器内部使用3000端口
  -e DEEPSEEK_API_KEY="sk-xxxxx" \
  -e DEEPSEEK_MODEL="deepseek-reasoner" \
  -e TZ="Asia/Shanghai" \
  -e FLASK_DEBUG=1 \
  -e PYTHONUNBUFFERED=1 \
  --name deepseek-chat \
  deepseek-chat:latest
```

## 功能特性

1. **流式聊天体验**
   - 实时接收AI响应
   - 支持Markdown渲染
   - 代码块复制功能

2. **会话管理**
   - 多会话支持
   - 本地历史记录存储
   - 会话切换功能

3. **端口灵活性**
   - 支持任意宿主机端口映射
   - 可自定义容器内部端口
   - 无需修改代码即可更改端口

## 使用说明

1. 在输入框中输入消息，按Enter发送
2. 使用侧边栏管理会话：
   - 🆕 新建会话
   - 📚 查看历史
   - 🗑️ 清除历史
3. 代码块右上角有"Copy"按钮可复制代码

## 技术细节

- **后端**：Flask + Socket.IO
- **前端**：Markdown渲染 + 流式响应处理
- **部署**：Gunicorn + Eventlet
- **端口配置**：通过环境变量灵活设置

## 常见问题

**Q: 如何获取API密钥？**  
A: 访问DeepSeek官网创建账户并获取API密钥

**Q: 如何修改服务端口？**  
A: 使用`-p`参数进行端口映射，如`-p 8080:21048`将宿主机8080映射到容器21048端口

**Q: 容器内部端口可以修改吗？**  
A: 可以，通过`-e PORT=<自定义端口>`设置容器内部端口

**Q: 为什么响应速度慢？**  
A: 尝试设置 `-e FLASK_DEBUG=0` 关闭调试模式

**Q: 如何查看日志？**  
A: 使用命令 `docker logs deepseek-chat`

## 开发说明

如需修改代码，请安装依赖：
```bash
pip install -r scripts/requirements.txt
```

启动开发服务器：
```bash
cd scripts
python app.py
```

访问 `http://localhost:21048` 测试修改
