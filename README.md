# 🤖 JMComic QQ Bot

基于 NoneBot2 + NapCat 的禁漫天堂 QQ 机器人，支持自动下载漫画并转换为 PDF 发送。

> 作者：浮浮酱 ฅ'ω'ฅ
> 适用场景：私密小群（3-5人）

[![GitHub stars](https://img.shields.io/github/stars/socialzoe/jmcomic_qq_bot?style=social)](https://github.com/socialzoe/jmcomic_qq_bot)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

---

## 📋 功能特性

- ✅ 命令式下载：`/jm <本子ID>`
- ✅ 智能识别：`@机器人 123456`
- ✅ 自动转PDF：下载完成自动转换
- ✅ 文件发送：自动发送到群聊
- ✅ 自动清理：发送后删除本地文件
- ✅ 队列管理：防止并发过高

---

## 🚀 快速开始

### 前置要求

- Windows 10/11
- Python 3.9+ ([下载地址](https://www.python.org/downloads/))
- Git ([下载地址](https://git-scm.com/downloads))

### 第零步：下载项目

```bash
git clone https://github.com/socialzoe/jmcomic_qq_bot.git
cd jmcomic_qq_bot
```

或直接下载 ZIP 并解压。

### 第一步：安装OneBot实现

推荐使用 **NapCat**（最稳定）：

1. 下载：https://github.com/NapNeko/NapCatQQ/releases
2. 解压并运行 `NapCat.exe`
3. 扫码登录QQ账号
4. 配置WebSocket连接

**NapCat 配置示例：**
```json
{
  "http": {
    "enable": true,
    "host": "127.0.0.1",
    "port": 3000
  },
  "ws": {
    "enable": true,
    "host": "127.0.0.1",
    "port": 3001
  }
}
```

### 第二步：配置机器人

**⚠️ 重要：复制示例配置文件**

```bash
copy config.example.yml config.yml
copy .env.example .env.prod
```

**然后编辑 `config.yml`：**

```yaml
auth:
  admins:
    - 你的QQ号  # 改成你的QQ号

jmcomic:
  download_dir: "E:\\JMDownload"  # 改成你想要的下载目录
```

**编辑 `.env.prod`：**

```env
# 把 "你的机器人QQ号" 替换为实际的机器人QQ号
ONEBOT_API_ROOTS={"你的机器人QQ号": "http://127.0.0.1:3000"}
ONEBOT_ACCESS_TOKEN=jmbot2024
```

### 第三步：安装依赖

```bash
pip install -r requirements.txt
```

或使用国内镜像加速（推荐）：

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 第四步：启动 NapCat 并登录 QQ

1. 运行 NapCat
2. 扫码登录机器人QQ账号
3. 确认看到 "WebSocket server listening" 等提示

### 第五步：启动机器人

**方法一：使用启动脚本（推荐）**
```bash
start.bat
```

**方法二：手动启动**
```bash
python bot.py
```

看到 "JMComic QQ Bot 启动成功" 即表示启动成功！

---

## 📖 使用方法

### 命令列表

| 命令 | 说明 | 示例 |
|------|------|------|
| `/jm <ID>` | 下载本子 | `/jm 123456` |
| `/jm status` | 查看状态 | `/jm status` |
| `@机器人 <ID>` | 智能识别 | `@机器人 123456` |

### 使用示例

**场景1：普通下载**
```
你: /jm 123456
机器人: ✅ 已加入队列喵～
      本子ID: 123456
      队列位置: 1

机器人: 📥 开始下载喵～
      ID: 123456
      请耐心等待...

机器人: ✅ 完成喵～共3个章节
      开始发送...

机器人: [发送文件: 第1话.pdf]
机器人: 📄 [1/3] 第1话.pdf
...
机器人: 🎉 全部完成喵～
```

**场景2：智能识别**
```
你: @机器人 123456
机器人: ✅ 检测到本子ID: 123456
      已自动加入队列喵～
      队列: 1/5
```

**场景3：查看状态**
```
你: /jm status
机器人: 📊 浮浮酱状态

      队列: 0/5
      处理中: 否
      下载目录: C:\Users\...\jmcomic_temp
```

---

## ⚙️ 配置说明

### config.yml 配置项

```yaml
# 权限配置
auth:
  enable_whitelist: false  # 小群关闭白名单
  admins: [123456789]      # 管理员QQ号

# 下载配置
jmcomic:
  download_dir: "临时下载目录"
  client_impl: "api"       # api=移动端, html=网页端
  # proxy: "代理地址"      # 如需代理取消注释

  threading:
    album: 1  # 同时下载的本子数
    photo: 3  # 同时下载的章节数
    image: 8  # 同时下载的图片数

# 机器人配置
max_queue_size: 5           # 最大队列长度
task_interval: 3            # 任务间隔（秒）
max_file_size_mb: 200       # 最大文件大小
delete_after_send: true     # 发送后删除
```

---

## 🔧 故障排查

### 问题1：机器人无响应

**检查清单：**
- [ ] NapCat是否正常运行？
- [ ] 机器人是否在群里？
- [ ] WebSocket连接是否正常？
- [ ] 是否@了机器人或使用了正确的命令？

**解决方法：**
```bash
# 查看日志
python bot.py
# 检查是否有错误信息
```

### 问题2：下载失败

**可能原因：**
- 网络问题（需要代理）
- 本子ID错误
- JMComic网站故障

**解决方法：**
1. 检查本子ID是否正确
2. 配置代理：
   ```yaml
   jmcomic:
     proxy: "http://127.0.0.1:7890"
   ```

### 问题3：文件发送失败

**可能原因：**
- 文件过大
- QQ限制
- 网络问题

**解决方法：**
1. 检查文件大小
2. 调整配置：
   ```yaml
   max_file_size_mb: 100  # 降低限制
   ```

### 问题4：依赖安装失败

**解决方法：**
```bash
# 使用清华源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 或使用阿里云源
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
```

---

## 📁 项目结构

```
jmcomic_qq_bot/
├── bot.py                # 主程序
├── config.yml            # 配置文件
├── .env.prod            # 环境变量
├── requirements.txt      # 依赖列表
├── start.bat            # 启动脚本
├── plugins/             # 插件目录
│   └── jm_plugin.py     # JM插件
└── core/                # 核心模块
    ├── downloader.py    # 下载管理器
    └── converter.py     # PDF转换器
```

---

## ⚠️ 注意事项

1. **仅供个人学习使用**，不得用于商业用途
2. **遵守当地法律法规**，风险自负
3. **不要公开部署**，仅限私密小群
4. **注意版权问题**，不要传播受版权保护的内容
5. **定期清理文件**，避免占用过多磁盘空间

---

## 🎨 进阶功能

### 自定义下载路径

编辑 `config.yml`：
```yaml
jmcomic:
  download_dir: "D:\\MyDownloads\\jmcomic"
```

### 使用代理

编辑 `config.yml`：
```yaml
jmcomic:
  proxy: "http://127.0.0.1:7890"
```

### 调整并发

编辑 `config.yml`：
```yaml
jmcomic:
  threading:
    photo: 5   # 章节并发调高
    image: 10  # 图片并发调高
```

---

## 📞 支持

有问题？
- 查看日志文件
- 检查配置文件
- 确认网络连接

---

## 📚 相关链接

- [NoneBot2 文档](https://nonebot.dev/)
- [NapCat 项目](https://github.com/NapNeko/NapCatQQ)
- [JMComic 爬虫库](https://github.com/hect0x7/JMComic-Crawler-Python)

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

如果这个项目对你有帮助，请给个 ⭐ Star 支持一下喵～

---

## 📄 开源协议

[MIT License](LICENSE)

本项目仅供学习交流使用，请勿用于非法用途。使用本项目产生的一切后果由使用者自行承担。

---

**Made with ❤️ by 浮浮酱 ฅ'ω'ฅ**
