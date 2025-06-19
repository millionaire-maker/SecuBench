# SecuBench 开源安全评测社区

### 专注于安全AI模型的开源评测平台

[🚀快速开始](#-快速开始) |
[📚知识库管理](#-知识库管理) |
[🧪评测框架](#-评测框架) |
[📊结果展示](#-结果展示) |
[🐛常见问题](#-常见问题)

## 📁 项目结构

```bash
SecuBench/
├── README.md                       # 项目说明文档
├── data/                           # 标准化安全数据集
│   ├── cissp/                      # CISSP认证题库
│   ├── cisco/                      # 思科威胁情报数据
│   └── cseval/                     # CS-Eval计算机安全
├── evaluation/                     # 评测脚本与工具
│   └── scripts/                    # 标准化评测脚本
├── models/                         # 模型配置模板
│   └── configs/                    # OpenCompass兼容配置
│       ├── api_models/             # API模型配置
│       └── local_models/           # 本地模型配置
├── tools/                          # 辅助工具
└── results/                        # 评测结果与分析
```

## 🌟 项目简介

**SecuBench** 是一个专注于安全领域的开源模型评测平台，致力于为安全AI模型的评估提供全面的解决方案。通过标准化评测框架和丰富的安全知识库体系，SecuBench能够：

- 🎯 **深度评估模型安全能力**：针对漏洞识别、合规分析、威胁预测等专业领域提供专项评测
- 📚 **集成多维知识库**：构建网络安全、行业合规、漏洞数据库等专业安全知识体系
- 🔧 **提供标准化评测工具**：开箱即用的评测脚本与可视化分析工具
- 📈 **驱动模型迭代优化**：通过量化指标与案例对比展示模型能力演进
- 🤝 **社区驱动发展**：开放的知识库贡献机制，共建安全AI评测生态

> 🎯 **平台使命**: 建立安全AI模型评测的行业标准，推动安全领域人工智能技术的发展与应用

### ✨ 核心特性

- **🏆 标准化评测**：基于OpenCompass框架的专业评测体系
- **📊 多维度分析**：从技术能力到实战应用的全方位评估
- **🔄 持续更新**：社区驱动的知识库动态扩展机制
- **🎯 领域专精**：专注安全领域的深度评测与分析
- **🌐 开放生态**：完全开源，支持自定义扩展与贡献

## 📚 知识库管理

SecuBench 提供多层次的安全知识库体系，涵盖从基础概念到前沿威胁的全方位内容：

### 🔒 安全专业知识库

| 知识库类型 | 数据集名称 | 描述 | 题目数量 | 更新时间 |
|------------|------------|------|----------|----------|
| **网络安全基础** | CS-Eval | 网络安全综合评测 | 4000+ | 2024/12/18 |
| **安全认证** | CISSP | 信息安全综合评测 | 2000+ | 2024/12/18 |
| **漏洞分析** | CTI-MCQ | 威胁情报选择题 | 2000+ | 2024/12/18 |
| **威胁响应** | CTI-RCM | 威胁响应分析题 | 1000+ | 2024/12/18 |

### 🌐 通用能力基准

| 知识库类型 | 数据集名称 | 描述 | 评测目的 |
|------------|------------|------|----------|
| **数学推理** | GSM8K | 小学数学问题 | 基础逻辑能力 |
| **综合知识** | MMLU | 多领域知识评测 | 知识广度测试 |
| **复杂推理** | BBH | 大模型困难任务 | 推理能力极限 |
| **中文理解** | C-Eval | 中文综合能力 | 中文处理能力 |

### 🚀 即将推出

- **🛡️ 恶意软件分析**：恶意代码识别与分析评测
- **🔐 密码学应用**：密码算法与协议安全评测  
- **🌐 Web安全**：Web应用安全漏洞检测评测
- **☁️ 云安全**：云环境安全配置与防护评测
- **📱 移动安全**：移动应用安全分析评测

> 💡 **数据集扩展**: 我们将持续与安全行业专家合作，定期更新和扩展知识库内容

## 🚀 快速开始

### 📋 环境要求

- **操作系统**: Linux / macOS / Windows
- **Python**: 3.10 或更高版本
- **CUDA**: 11.8+ (如需 GPU 加速)
- **内存**: 建议 16GB 以上
- **存储**: 至少 10GB 可用空间

### 🛠️ 部署步骤

#### 1. 克隆项目仓库

```bash
# 克隆SecuBench项目到本地
git clone https://github.com/millionaire-maker/SecuBench.git
cd SecuBench
```

#### 2. 创建虚拟环境

```bash
# 使用 Conda 创建环境 (推荐)
conda create --name SecuBench python=3.10 -y
conda activate SecuBench

# 或使用 virtualenv
python -m venv SecuBench
source SecuBench/bin/activate  # Linux/macOS
# SecuBench\Scripts\activate   # Windows
```

#### 3. 安装 OpenCompass 评测框架

```bash
# 克隆 OpenCompass 官方仓库
git clone https://github.com/open-compass/opencompass.git
cd opencompass

# 安装核心依赖
pip install -e .

# 安装扩展功能 (根据需要选择)
pip install -e ".[api]"      # API 模型支持
pip install -e ".[lmdeploy]" # LMDeploy 推理后端
pip install -e ".[vllm]"     # vLLM 推理后端
```

#### 4. 下载 OpenCompass 数据集

```bash
# 下载核心数据集包
wget https://github.com/open-compass/opencompass/releases/download/0.2.2.rc1/OpenCompassData-core-20240207.zip

# 解压核心数据集包
unzip OpenCompassData-core-20240207.zip
```

#### 5. 配置 SecuBench 集成

```bash
# 回到项目根目录
cd ..

# 创建配置目录
mkdir -p opencompass/opencompass/configs/models/clouditera

# 复制配置文件到 OpenCompass
cp -r models/configs/api_models/* opencompass/opencompass/configs/models/clouditera/
cp -r models/configs/local_models/* opencompass/opencompass/configs/models/clouditera/

# 复制数据集文件
cp -r data/* opencompass/data/

# 复制评测脚本
cp -r evaluation/scripts/* opencompass/configs/

# 复制工具脚本
cp -r tools/* opencompass/tools/
```

### ⚙️ 模型配置

#### API模型配置示例

编辑 `opencompass/opencompass/configs/models/clouditera/SecGPT_7B.py`:

```python
"""SecGPT-7B 模型配置文件

使用前请修改以下配置：
1. internlm_url: 替换为您的 API 服务地址
2. api_key: 替换为您的 API 密钥
3. 根据您的服务性能调整 query_per_second 和 batch_size
"""

import os
from opencompass.models import OpenAISDK

# 🔧 配置区域 - 请根据您的环境修改
internlm_url = 'http://your-api-server:port/v1'  # 替换为您的 API 地址
api_key = '0'  # 替换为您的 API Key

models = [
    dict(
        abbr='SecGPT-7B',               # 模型简称
        type=OpenAISDK,                 # 使用 OpenAI SDK
        path='SecGPT-7B',               # 请求服务时的模型名称
        key=api_key,                    # API 密钥
        openai_api_base=internlm_url,   # 服务地址
        rpm_verbose=True,               # 显示请求速率
        query_per_second=6,             # 请求频率限制
        max_out_len=2048,              # 最大输出长度
        max_seq_len=2048,              # 最大输入长度
        temperature=0.01,               # 生成温度
        batch_size=15,                 # 批处理大小
        retry=3,                       # 重试次数
    )
]
```

#### 本地模型配置示例

编辑 `opencompass/opencompass/configs/models/clouditera/Foundation-Sec-8B.py`:

```python
"""
Foundation-Sec-8B 本地模型配置文件

本配置文件用于在OpenCompass框架中部署Foundation-Sec-8B模型进行本地推理评测。

使用前请修改以下配置：
1. path: 替换为您的模型本地路径
2. run_cfg: 根据您的GPU配置调整GPU数量
3. engine_config: 根据您的硬件性能调整批处理大小和会话长度
4. gen_config: 根据评测需求调整生成参数

"""
from opencompass.models import TurboMindModel

models = [
    dict(
        type=TurboMindModel,
        abbr='Foundation-Sec-8B',
        path='/root/.xinference/models/Foundation-Sec-8B/',  # 🔧 替换为您的模型路径
        engine_config=dict(session_len=16384, max_batch_size=16, tp=1),
        gen_config=dict(top_k=1, temperature=1e-6, top_p=0.9, max_new_tokens=4096),
        max_seq_len=16384,
        max_out_len=4096,
        batch_size=16,
        run_cfg=dict(num_gpus=1),  # 🔧 根据您的GPU数量调整
    )
]
```

## 🧪 评测框架

### 🔄 标准化评测流程

SecuBench 提供完整的评测流水线，从数据集选择到结果分析的全自动化处理：

1. **📂 选择知识库**: 从安全专业知识库中选择评测维度
2. **⚙️ 配置评测参数**: 设置模型参数、评测指标和输出格式
3. **🤖 选择评测模型**: 配置待评测的AI模型接口
4. **▶️ 运行评测脚本**: 执行标准化评测流程
5. **📊 生成分析报告**: 自动生成详细的评测报告
6. **💾 结果对比存储**: 保存结果并支持历史对比

> ⚠️ **重要提示**: 在评测前，请确保已按照[部署步骤](#🛠️-部署步骤)完成配置文件部署，并激活相应的conda环境

### 📋 评测示例

#### 🔒 安全专业知识库评测

##### 1. 网络安全综合能力评测 (CS-Eval)

> 📝 **特别说明**: CS-Eval数据集没有提供参考答案，需要先获取模型预测结果，然后前往CS-Eval官网提交获取最终评分。

**第一步：生成模型预测结果**

```bash
# 进入OpenCompass目录
cd opencompass

# 激活环境
conda activate SecuBench

# 运行CS-Eval评测 (API模型示例)
opencompass \
    --models configs/models/clouditera/SecGPT_7B.py \
    --custom-dataset-path /root/opencompass/data/cseval/cs-eval-questions.jsonl \
    --custom-dataset-data-type qa \
    --custom-dataset-infer-method gen \
    -w results/SecGPT-7B \
    --debug

# 本地模型评测示例 (指定GPU)
CUDA_VISIBLE_DEVICES=0,1 opencompass \
    --models configs/models/clouditera/Foundation-Sec-8B.py \
    --custom-dataset-path /root/opencompass/data/cseval/cs-eval-questions.jsonl \
    --custom-dataset-data-type qa \
    --custom-dataset-infer-method gen \
    -w results/Foundation-Sec-8B \
    --debug
```

**第二步：提取预测结果**

```bash
# 使用工具脚本提取模型预测答案
python tools/process_cseval_predictions.py \
    --input results/SecGPT-7B/predictions/cs-eval-questions.jsonl \
    --output results/SecGPT-7B/cs_eval_submission.json
```

**第三步：提交评测**

前往 [CS-Eval官网](https://cs-eval.com/#/app/submission) 提交 `cs_eval_submission.json` 文件获取最终评分。

##### 2. 安全认证评测 (CISSP)

```bash
# 进入OpenCompass目录
cd opencompass

# 运行CISSP评测
python configs/eval_cissp.py

# 本地模型指定GPU评测
CUDA_VISIBLE_DEVICES=0,1 python configs/eval_cissp.py
```

##### 3. 威胁情报分析 (CTI-MCQ)

```bash
# 运行CTI多选题评测
python configs/eval_cti_mcq.py

# 本地模型指定GPU评测
CUDA_VISIBLE_DEVICES=0,1 python configs/eval_cti_mcq.py
```

##### 4. 威胁响应案例 (CTI-RCM)

```bash
# 运行CTI响应案例评测
python configs/eval_cti_rcm.py

# 本地模型指定GPU评测
CUDA_VISIBLE_DEVICES=0,1 python configs/eval_cti_rcm.py
```

#### 🌐 通用能力基准评测

##### API模型评测示例

```bash
# 数学推理能力 (GSM8K)
opencompass \
    --models configs/models/clouditera/SecGPT_7B.py \
    --datasets gsm8k_gen \
    --max-num-workers 8 \
    -w results/SecGPT-7B \
    --debug

# 多领域知识 (MMLU)
opencompass \
    --models configs/models/clouditera/SecGPT_7B.py \
    --datasets mmlu_gen \
    --max-num-workers 8 \
    -w results/SecGPT-7B \
    --debug

# 复杂推理 (BBH)
opencompass \
    --models configs/models/clouditera/SecGPT_7B.py \
    --datasets bbh_gen \
    --max-num-workers 8 \
    -w results/SecGPT-7B \
    --debug

# 中文理解 (C-Eval)
opencompass \
    --models configs/models/clouditera/SecGPT_7B.py \
    --datasets ceval_gen \
    --max-num-workers 8 \
    -w results/SecGPT-7B \
    --debug
```

##### 本地模型评测示例

```bash
# 数学推理能力 (GSM8K) - 指定GPU
CUDA_VISIBLE_DEVICES=0,1 opencompass \
    --models configs/models/clouditera/Foundation-Sec-8B.py \
    --datasets gsm8k_gen \
    --max-num-workers 8 \
    -w results/Foundation-Sec-8B \
    --debug

# 多领域知识 (MMLU) - 指定GPU
CUDA_VISIBLE_DEVICES=0,1 opencompass \
    --models configs/models/clouditera/Foundation-Sec-8B.py \
    --datasets mmlu_gen \
    --max-num-workers 8 \
    -w results/Foundation-Sec-8B \
    --debug
```


## 📊 结果展示

### 📁 结果文件结构

评测完成后，结果将保存在 `results/` 目录下（以CISSP数据集为例）：

```bash
results/cissp/
├── Foundation-Sec-8B/
│   ├── prediction/
│   │   └── foundation_sec_8b_cissp.json     # 模型预测结果
│   └── summary/
│       └── foundation_sec_8b_cissp.csv      # 评测结果汇总
└── SecGPT-7B/
    ├── prediction/
    │   └── secgpt_7b_cissp.json             # 模型预测结果
    └── summary/
        └── secgpt_7b_cissp.csv              # 评测结果汇总
```

### 📊 模型性能对比

以下是Foundation-Sec-8B模型和SecGPT-7B模型在各个数据集上的评测结果对比：

| 模型 | CS-Eval | CISSP | BBH | C-Eval | GSM8K | MMLU | CTI-MCQ | CTI-RCM |
|------|---------|-------|-----|--------|-------|------|---------|---------|
| **Foundation-Sec-8B** | 55.02 | 39.19 | 58.72 | 42.70 | 54.73 | 47.36 | 41.36 | 67.30 |
| **SecGPT-7B** | 85.03 | 77.00 | 61.51 | 70.40 | 82.94 | 70.94 | 77.60 | 70.00 |

> 📋 **评测说明**: 以上所有评测得分均使用本项目提供的评测脚本和 OpenCompass 官方评测框架运行得出，确保结果的一致性和可重现性。

### 📝 典型案例分析

以下是从各个数据集中选取的典型案例，展示了两个模型在不同安全场景下的表现对比：

#### 🔍 案例一：威胁响应分析 (CTI-RCM)

**📋 输入提示词 (题目ID: 981)**
```
Analyze the following CVE description and map it to the appropriate CWE. Provide a brief justification for your choice. Ensure the last line of your response contains only the CWE ID.  CVE Description: A heap-based buffer overflow was found in the __vsyslog_internal function of the glibc library. This function is called by the syslog and vsyslog functions. This issue occurs when the openlog function was not called, or called with the ident argument set to NULL, and the program name (the basename of argv[0]) is bigger than 1024 bytes, resulting in an application crash or local privilege escalation. This issue affects glibc 2.36 and newer. 
Remember to put your final answer within \boxed{}.
```

**🤖 模型回答对比**

| 模型 | 预测结果 | 答案正确性 |
|------|----------|------------|
| **SecGPT-7B** | `CWE-787` ✅ | **正确** |
| **Foundation-Sec-8B** | `CWE-122` ❌ | **错误** |
| **标准答案** | `CWE-787` | - |

**SecGPT-7B 完整回答:**
```
The vulnerability described in the CVE is a **heap-based buffer overflow**, which falls under the **CWE-787** category. Let's break this down to understand why this mapping is appropriate.

### Understanding the Vulnerability

A **buffer overflow** occurs when more data is written to a buffer (a fixed-size block of memory) than it can hold, causing the excess data to overwrite adjacent memory locations. In this case, the overflow happens on the **heap**, which is a region of memory used for dynamic memory allocation during program execution.

The specific issue arises in the `__vsyslog_internal` function of the **glibc (GNU C Library)**. This function is part of the system's logging mechanism and is called by `syslog` and `vsyslog`. The problem occurs when:

- The `openlog` function is **not called**, or
- It is called with the `ident` argument set to **NULL**, and
- The program name (obtained from `argv[0]`) is **larger than 1024 bytes**.

In such cases, the function does not properly validate the length of the program name before copying it into a fixed-size buffer on the heap. If the program name exceeds the buffer's capacity, it overflows into adjacent memory, potentially corrupting data or even allowing an attacker to execute arbitrary code.

This type of overflow can lead to **application crashes** or, in some cases, **local privilege escalation**, depending on how the overflowed memory is accessed or modified.

### Why CWE-787 is the Correct Mapping

**CWE-787** is defined as:

> *"Out-of-bounds Write: The software writes data past the end, or before the beginning, of the intended buffer."*

This directly matches the scenario described in the CVE. The overflow occurs because the program writes more data into a heap-allocated buffer than it can safely hold, without proper bounds checking.

### Summary

- **Vulnerability Type**: Heap-based buffer overflow.
- **Impact**: Application crash or local privilege escalation.
- **Root Cause**: Improper validation of input size before writing to a heap-allocated buffer.
- **CWE Mapping**: CWE-787.

This is a classic example of a buffer overflow that exploits improper memory handling, making **CWE-787** the correct identifier.

CWE-787
```

**Foundation-Sec-8B 完整回答:**
```
CWE-122: Heap-based Buffer Overflow

Justification: The description mentions a heap-based buffer overflow in the __vsyslog_internal function of the glibc library. This aligns with CWE-122, which is about heap-based buffer overflows.
```


#### 🔍 案例二：威胁情报选择题 (CTI-MCQ)

**📋 输入提示词 (题目ID: 2386)**
```
Which of the following best describes the weakness categorized as CWE-794?
A. The product processes data from an upstream component but fails to handle all instances of a special element before it moves downstream.
B. The product has a vulnerability due to improper handling of user authentication, leading to unauthorized access.
C. The product does not encrypt all critical data before transmission, making it vulnerable to interception.
D. The product allows unauthorized users to access administrative functionality due to improper session management.
请你只回答正确答案选项，不要额外的文字描述。
```

**🤖 模型回答对比**

| 模型 | 预测结果 | 答案正确性 |
|------|----------|------------|
| **SecGPT-7B** | `A` ✅ | **正确** |
| **Foundation-Sec-8B** | `Answer: D` ❌ | **错误** |
| **标准答案** | `A` | - |

**SecGPT-7B 完整回答:**
```
A
```

**Foundation-Sec-8B 完整回答:**
```
Answer: D
```
#### 🔍 案例三：安全认证 (CISSP) - WPA2协议

**📋 输入提示词 (题目ID: 2403)**
```
Wi-Fi Protected Access 2 (WPA2) is a security protocol designed with which of the following security feature?
A. Encryption control
B. Malware attack protection
C. Data availability
D. Replay attack protection
请你只回答正确答案选项，不要额外的文字描述。
```

**🤖 模型回答对比**

| 模型 | 预测结果 | 答案正确性 |
|------|----------|------------|
| **SecGPT-7B** | `A` ✅ | **正确** |
| **Foundation-Sec-8B** | `A.\nB.\nC.\nD.` ❌ | **格式错误** |
| **标准答案** | `A` | - |

**SecGPT-7B 完整回答:**
```
A
```

**Foundation-Sec-8B 完整回答:**
```
A.
B.
C.
D.
```


## 🐛 常见问题

### ❓ 安装问题

**Q: 安装过程中出现依赖冲突怎么办？**

A: 建议使用独立的虚拟环境，并按顺序安装依赖：
```bash
conda create --name SecuBench python=3.10 -y
conda activate SecuBench
cd opencompass && pip install -e .
```

**Q: 下载数据集失败怎么解决？**

A: 尝试使用国内镜像源或手动下载：
```bash
# 使用ModelScope镜像
pip install modelscope
export DATASET_SOURCE=ModelScope

# 或者手动下载数据集
wget -c https://github.com/open-compass/opencompass/releases/download/0.2.2.rc1/OpenCompassData-core-20240207.zip
```

### 🔧 配置问题

**Q: API模型连接失败怎么办？**

A: 请检查以下配置项：
- ✅ API地址格式正确 (`http://host:port/v1`)
- ✅ API Key有效且有权限
- ✅ 网络连接正常，防火墙允许访问
- ✅ 模型服务正在运行并可正常响应

**Q: 本地模型加载失败怎么办？**

A: 请检查以下配置：
```python
# 确认模型路径正确
path='/correct/path/to/your/model/',

# 确认GPU配置合理
run_cfg=dict(num_gpus=1),  # 根据实际GPU数量调整

# 确认内存配置足够
engine_config=dict(session_len=16384, max_batch_size=16, tp=1),
```


**Q: 评测结果异常怎么分析？**

A: 检查以下方面：
- 📋 查看 `work_dir/logs/` 目录下相应的日志文件了解详细错误信息
- 🔍 检查 `work_dir/predictions/` 目录下的预测结果格式
- ⚙️ 验证模型配置参数是否合理
- 📊 确认数据集路径和格式正确性


## 🙏 致谢

感谢以下项目和团队的支持：
- [SecGPT](https://github.com/Clouditera/SecGPT) - 全球首个网络安全开源大模型
- [OpenCompass](https://github.com/open-compass/opencompass) - 强大的大模型评测框架
- [OpenAI](https://openai.com/) - API标准设计参考
- [HuggingFace](https://huggingface.co/) - 模型生态支持
- 安全社区的专家们 - 提供专业知识库内容和宝贵建议
---

<div align="center">
如果这个项目对您有帮助，请给我们一个 ⭐ Star!
</div>
