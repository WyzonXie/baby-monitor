# baby-monitor

  **English** | [中文](#中文说明)

  An AI-powered baby monitor that pings you only when it matters.

  Unlike ordinary camera apps that require you to keep watching a live stream,
  this system watches for you and reaches out proactively — the alert fires only
  when crying persists for 3 minutes **with no adult present in the frame**.
  The rest of the time, it stays silent.

  ## Core Idea

  Crying is not an anomaly. **Unattended crying is.**

  A baby crying for a minute while a caregiver is nearby is perfectly normal and
  should never trigger an alert. This single design decision cuts false alarms by
  an order of magnitude and shapes the entire architecture.

  ## How It Works

  Two-tier cascade:

  ```
  Camera (RTSP) ──┐
                  ├─→ Local screening (YAMNet audio + OpenCV vision, on a home PC)
  Microphone ─────┘         │
                            │  only suspicious moments (~1% of the time)
                            ▼
                     Claude API review
                            │  confirmed events only
                            ▼
                WeCom bot push → parent's phone (alert + single snapshot)
  ```

  - **Tier 1 (local):** filters out 99% of quiet time at zero cloud cost
  - **Tier 2 (Claude API):** double-checks suspicious moments to suppress false alarms
  - **Outbound-only networking:** no public IP, no port forwarding, no inbound
    exposure of the home network

  ## Current Status

  Early development. Six planned stages, currently in stage 2.

  | Stage | Scope | Status |
  |---|---|---|
  | 1 | Cry detection + WeCom push + heartbeat | Prototype done and tested; being
  migrated into this repo under proper engineering practices |
  | 2 | Camera access (RTSP), stream-loss recovery, adult detection | **In progress** —
  stream verified at 2880×1620 @ 15fps |
  | 3 | Infant posture (prone / face covered), bed-zone rules, snapshots | Planned |
  | 4 | Claude API second-opinion review | Planned |
  | 5 | One-week field tuning, target < 1 false alarm per night | Planned |
  | 6 | Foreign-object detection on the bed | Planned |

  ## Quick Start

  ```bash
  # 1. Clone
  git clone https://github.com/WyzonXie/baby-monitor.git
  cd baby-monitor

  # 2. Create and activate a virtual environment (Windows)
  py -m venv .venv
  .venv\Scripts\activate

  # 3. Install dependencies
  pip install -r requirements.txt
  ```

  **4. Create your own `config.py`.** It is deliberately absent from the repo —
  it holds secrets (camera credentials) and is excluded via `.gitignore`, so
  every user creates their own:

  ```python
  # config.py
  RTSP_URL = "rtsp://username:password@camera-ip/stream1"
  ```

  **5. Verify the camera connection:**

  ```bash
  python check_camera.py
  ```

  On success it prints the actual resolution and frame rate of the stream.

  ## Tech Stack

  See [tech.md](./tech.md) for the full selection rationale, including the
  options that were rejected and why.

  ## Privacy

  - No continuous recording. Only the single frame at the moment an alert
    triggers is saved.
  - Exactly two kinds of data ever leave the home network: alert snapshots
    (via WeCom) and suspicious-moment frames (sent to the Claude API for review).

  ## Known Limitations

  - WeCom push cannot break through the phone's Do-Not-Disturb / silent mode.
    The primary scenario is daytime, so this is accepted.
  - A white-noise machine in the room may lower cry-detection scores; thresholds
    will be tuned on-site in stage 5.
  - Some infant-specific vision models used here are licensed for
    **non-commercial use only**. This project is strictly for personal use;
    any commercial use would require rebuilding the entire vision pipeline.

  ## License

  TBD (will be decided before the first functional release).

  ---

  # 中文说明

  AI 婴儿监护系统：只在真正要紧的时刻打扰你。

  普通摄像头 App 需要你主动盯着直播画面看；本系统替你盯着，有事主动找你——
  只有当哭声持续满 3 分钟、且画面里全程没有成人出现时，才会推送告警。
  其余时间保持沉默。

  ## 核心判断

  哭不是异常，**哭了没人管才是异常。**

  看护人就在旁边时宝宝哭一分钟，是再正常不过的事，不应该触发任何告警。
  这一条判断把误报率降低了一个数量级，也决定了整个系统的架构。

  ## 工作原理

  两层级联：

  ```
  摄像头 (RTSP) ──┐
                  ├─→ 本地筛查（YAMNet 听声 + OpenCV 看画面，跑在家用 PC 上）
  麦克风 ─────────┘         │
                            │  只放行可疑时刻（约 1% 的时间）
                            ▼
                      Claude API 复核
                            │  只放行确认的事件
                            ▼
               企业微信机器人 → 家长手机（告警 + 单帧抓拍）
  ```

  - **第一层（本地）**：挡掉 99% 的平静时间，云端成本为零
  - **第二层（Claude API）**：对可疑时刻二次确认，压制误报
  - **纯出站网络**：不需要公网 IP、不做端口映射，家庭网络零暴露面

  ## 当前状态

  早期开发中。整体规划六个阶段，目前在阶段 2。

  | 阶段 | 内容 | 状态 |
  |---|---|---|
  | 1 | 哭声检测 + 微信推送 + 心跳 | 原型已完成并通过测试，正按工程规范迁入本仓库 |
  | 2 | 摄像头接入（RTSP）、断流重连、成人检测 | **进行中**——已实测取流 2880×1620 @
  15fps |
  | 3 | 婴儿姿态（俯卧/遮脸）、床区规则、抓拍 | 未开始 |
  | 4 | Claude API 二次复核 | 未开始 |
  | 5 | 一周实地调参，目标误报 < 1 次/晚 | 未开始 |
  | 6 | 床面异物检测 | 未开始 |

  ## 快速开始

  ```bash
  # 1. 下载代码
    (via WeCom) and suspicious-moment frames (sent to the Claude API for review).

  ## Known Limitations

  - WeCom push cannot break through the phone's Do-Not-Disturb / silent mode.
    The primary scenario is daytime, so this is accepted.
  - A white-noise machine in the room may lower cry-detection scores; thresholds
    will be tuned on-site in stage 5.
  - Some infant-specific vision models used here are licensed for
    **non-commercial use only**. This project is strictly for personal use;
    any commercial use would require rebuilding the entire vision pipeline.

  ## License

  TBD (will be decided before the first functional release).

  ---

  # 中文说明

  AI 婴儿监护系统：只在真正要紧的时刻打扰你。

  普通摄像头 App 需要你主动盯着直播画面看；本系统替你盯着，有事主动找你——
  只有当哭声持续满 3 分钟、且画面里全程没有成人出现时，才会推送告警。
  其余时间保持沉默。

  ## 核心判断

  哭不是异常，**哭了没人管才是异常。**

  看护人就在旁边时宝宝哭一分钟，是再正常不过的事，不应该触发任何告警。
  这一条判断把误报率降低了一个数量级，也决定了整个系统的架构。

  ## 工作原理

  两层级联：

  ```
  摄像头 (RTSP) ──┐
                  ├─→ 本地筛查（YAMNet 听声 + OpenCV 看画面，跑在家用 PC 上）
  麦克风 ─────────┘         │
                            │  只放行可疑时刻（约 1% 的时间）
                            ▼
                      Claude API 复核
                            │  只放行确认的事件
                            ▼
               企业微信机器人 → 家长手机（告警 + 单帧抓拍）
  ```

  - **第一层（本地）**：挡掉 99% 的平静时间，云端成本为零
  - **第二层（Claude API）**：对可疑时刻二次确认，压制误报
  - **纯出站网络**：不需要公网 IP、不做端口映射，家庭网络零暴露面

  ## 当前状态

  早期开发中。整体规划六个阶段，目前在阶段 2。

  | 阶段 | 内容 | 状态 |
  |---|---|---|
  | 1 | 哭声检测 + 微信推送 + 心跳 | 原型已完成并通过测试，正按工程规范迁入本仓库 |
  | 2 | 摄像头接入（RTSP）、断流重连、成人检测 | **进行中**——已实测取流 2880×1620 @
  15fps |
  | 3 | 婴儿姿态（俯卧/遮脸）、床区规则、抓拍 | 未开始 |
  | 4 | Claude API 二次复核 | 未开始 |
  | 5 | 一周实地调参，目标误报 < 1 次/晚 | 未开始 |
  | 6 | 床面异物检测 | 未开始 |

  ## 快速开始

  ```bash
  # 1. 下载代码
  git clone https://github.com/WyzonXie/baby-monitor.git
  cd baby-monitor

  # 2. 创建并激活虚拟环境（Windows）
  py -m venv .venv
  .venv\Scripts\activate

  # 3. 安装依赖
  pip install -r requirements.txt
  ```

  **第 4 步，创建你自己的 `config.py`。** 仓库里故意没有这个文件——它存放
  摄像头密码等敏感信息，被 `.gitignore` 排除在版本控制之外，每个使用者自建：

  ```python
  # config.py
  RTSP_URL = "rtsp://用户名:密码@摄像头IP/stream1"
  ```

  **第 5 步，验证摄像头连通：**

  ```bash
  python check_camera.py
  ```

  成功时会打印视频流的实际分辨率与帧率。

  ## 技术选型

  完整的选型理由（包括否决了哪些方案、为什么）见 [tech.md](./tech.md)。

  ## 隐私与数据

  - 不做连续录像，只保存告警触发瞬间的单帧画面
  - 会离开家庭网络的数据仅两类：告警抓拍（经企业微信）、可疑时刻画面
    （送 Claude API 复核）

  ## 已知限制

  - 微信推送穿不透手机的勿扰/静音模式。主场景为白天，此限制已接受
  - 房间白噪音机可能压低哭声识别分数，阈值需在阶段 5 实地调参
  - 本项目使用的部分婴儿专用视觉模型为**非商用许可**，仅限个人自用；
    任何商业化使用前，整条视觉链必须替换重做

  ## 许可证

  待定（首个正式功能版本发布前确定）。