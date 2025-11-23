# motion_imitation 故障排查指南 / Troubleshooting Guide

## 问题：运行 run.py 后没有出现机器人行走 / Issue: Robot Not Walking After Running run.py

### 症状 / Symptoms

运行 `motion_imitation/run.py` 后出现以下情况：
- 加载了 humanoid 模型
- 出现了多个 URDF 警告（关于 axis element）
- 输出在 "env=" 处停止
- 没有看到机器人行走

### 原因分析 / Root Cause Analysis

从你的错误输出来看，有几个可能的问题：

1. **缺少命令行参数** - run.py 需要特定的参数才能正确运行
2. **TensorFlow 版本问题** - motion_imitation 需要特定版本的 TensorFlow
3. **环境配置问题** - 可能缺少必要的依赖或配置

### 解决方案 / Solutions

#### 方案 1: 添加必要的命令行参数

运行 motion_imitation 需要指定模式和其他参数：

```bash
# 训练模式 (不推荐首次使用)
python motion_imitation/run.py --mode train --motion_file motion_imitation/data/motions/dog_pace.txt --visualize

# 测试模式 (推荐 - 使用预训练模型)
python motion_imitation/run.py --mode test \
    --motion_file motion_imitation/data/motions/dog_pace.txt \
    --model_file motion_imitation/data/policies/dog_pace.zip \
    --visualize
```

**重要参数说明：**
- `--mode` : 必须指定，可选 `train` 或 `test`
- `--motion_file` : 参考动作文件路径
- `--model_file` : 预训练模型路径（test 模式必需）
- `--visualize` : 启用可视化（可选，但推荐用于调试）

#### 方案 2: 检查 TensorFlow 版本

motion_imitation 需要 TensorFlow 1.x：

```bash
# 检查当前 TensorFlow 版本
python -c "import tensorflow as tf; print(tf.__version__)"

# 如果版本不对，安装正确版本
pip uninstall tensorflow
pip install tensorflow==1.15.0

# 或使用 TensorFlow 2.x 兼容模式
pip install tensorflow==2.3.0
```

#### 方案 3: 完整的环境设置步骤

```bash
# 1. 进入 motion_imitation 目录
cd D:\dogwalking\motion_imitation

# 2. 检查是否有预训练模型
dir motion_imitation\data\policies

# 应该看到:
# - dog_pace.zip
# - dog_trot.zip
# - dog_spin.zip

# 3. 运行测试（使用预训练模型）
python motion_imitation/run.py --mode test ^
    --motion_file motion_imitation/data/motions/dog_pace.txt ^
    --model_file motion_imitation/data/policies/dog_pace.zip ^
    --visualize

# 注意：Windows 使用 ^ 进行换行
```

#### 方案 4: 使用简化的示例

如果上述方法仍有问题，尝试使用 motion_imitation 提供的示例：

```bash
# 测试环境 GUI
python -m motion_imitation.examples.test_env_gui --robot_type=A1 --motor_control_mode=Position --on_rack=True

# MPC 示例
python -m motion_imitation.examples.whole_body_controller_example
```

### 常见错误修复 / Common Error Fixes

#### 错误 1: 缺少可视化窗口

**症状：** 程序运行但看不到窗口

**解决方案：**
```bash
# 确保添加了 --visualize 参数
python motion_imitation/run.py --mode test --motion_file ... --model_file ... --visualize
```

#### 错误 2: TensorFlow 相关错误

**症状：** 出现 TensorFlow 导入或版本错误

**解决方案：**
```bash
# 创建新的虚拟环境
conda create -n motion_tf1 python=3.7
conda activate motion_tf1

# 安装依赖
cd D:\dogwalking\motion_imitation
pip install -r requirements.txt
pip install tensorflow==1.15.0

# 重新运行
python motion_imitation/run.py --mode test --motion_file ... --model_file ... --visualize
```

#### 错误 3: MPI 相关问题

**症状：** 出现 MPI 错误

**解决方案：**
```bash
# Windows 上安装 Microsoft MPI
# 下载并安装: https://www.microsoft.com/en-us/download/details.aspx?id=100593

# 或者使用单进程模式（不使用 MPI）
# 直接运行 python 命令而不是 mpiexec
```

### 调试步骤 / Debugging Steps

#### 步骤 1: 验证安装

```python
# 创建测试脚本 test_installation.py
import sys
print(f"Python version: {sys.version}")

import pybullet
print(f"PyBullet version: {pybullet.__version__}")

import tensorflow as tf
print(f"TensorFlow version: {tf.__version__}")

import numpy as np
print(f"NumPy version: {np.__version__}")

print("\n所有依赖已正确安装！")
```

运行：
```bash
python test_installation.py
```

#### 步骤 2: 测试 PyBullet 可视化

```python
# 创建测试脚本 test_pybullet.py
import pybullet as p
import time

# 连接到 GUI
physics_client = p.connect(p.GUI)

# 加载地面
p.loadURDF("plane.urdf")

# 保持窗口打开
print("PyBullet GUI 已启动。按 Ctrl+C 退出...")
try:
    while True:
        p.stepSimulation()
        time.sleep(1./240.)
except KeyboardInterrupt:
    print("退出...")

p.disconnect()
```

运行：
```bash
python test_pybullet.py
```

如果看到一个窗口显示地面，说明 PyBullet 正常工作。

#### 步骤 3: 完整的测试命令

```bash
# Windows PowerShell
cd D:\dogwalking\motion_imitation

# 确保在正确的虚拟环境中
conda activate motion_tf1

# 运行完整的测试命令
python motion_imitation/run.py `
    --mode test `
    --motion_file motion_imitation/data/motions/dog_pace.txt `
    --model_file motion_imitation/data/policies/dog_pace.zip `
    --visualize

# 或者 Windows CMD
python motion_imitation/run.py ^
    --mode test ^
    --motion_file motion_imitation/data/motions/dog_pace.txt ^
    --model_file motion_imitation/data/policies/dog_pace.zip ^
    --visualize
```

### 预期的正确输出 / Expected Correct Output

运行成功时，你应该看到：

```
pybullet build time: ...
===========================================================
Loading motion file: ...
Building environment...
Loading model: ...
Running simulation...
```

然后会出现一个 PyBullet 窗口，显示机器人在行走。

### 在不同地形中运行 / Running in Different Terrains

如果基本测试成功，你可以使用我们提供的工具在不同地形中测试：

```bash
# 进入我们的项目目录
cd D:\dogwalking\findtrip\pybullet_walking

# 查看地形创建示例
python use_motion_imitation.py --show-instructions

# 创建不同地形
python use_motion_imitation.py --terrain slope --render True
```

### 如何修改 env_builder.py 添加地形 / How to Modify env_builder.py to Add Terrain

如果你想直接在 motion_imitation 中添加自定义地形：

#### 1. 打开文件

```
D:\dogwalking\motion_imitation\motion_imitation\envs\env_builder.py
```

#### 2. 找到环境构建函数

在 `build_imitation_env` 函数中，找到创建地面的部分，通常是：

```python
def build_imitation_env(motion_files, ...):
    # ... 其他代码 ...
    
    # 创建地面
    plane = pybullet_client.loadURDF("plane.urdf")
    
    # 在这里添加自定义地形！
    # 例如，添加斜坡：
    slope_shape = pybullet_client.createCollisionShape(
        shapeType=pybullet_client.GEOM_BOX,
        halfExtents=[5, 5, 0.1]
    )
    slope_orientation = pybullet_client.getQuaternionFromEuler([0.1, 0, 0])  # 10度斜坡
    slope = pybullet_client.createMultiBody(
        baseMass=0,
        baseCollisionShapeIndex=slope_shape,
        basePosition=[5, 0, 0],
        baseOrientation=slope_orientation
    )
    
    # ... 继续其他代码 ...
```

#### 3. 使用我们提供的 TerrainEnvironment 类

更简单的方法是复制我们的 `TerrainEnvironment` 类到你的代码中：

```python
# 在 env_builder.py 开头添加
import sys
sys.path.append('D:/dogwalking/findtrip/pybullet_walking')
from use_motion_imitation import TerrainEnvironment

# 在 build_imitation_env 函数中使用
def build_imitation_env(motion_files, ...):
    # ... 其他代码 ...
    
    # 使用我们的工具创建地形
    TerrainEnvironment.create_slope_terrain(pybullet_client, slope_angle=15)
    
    # ... 继续其他代码 ...
```

### 获取更多帮助 / Getting More Help

如果问题仍然存在：

1. **检查 motion_imitation GitHub Issues:**
   https://github.com/erwincoumans/motion_imitation/issues

2. **查看我们的详细文档:**
   ```bash
   # 在我们的项目中
   cat MODIFICATION_GUIDE.md
   cat FILE_STRUCTURE.txt
   ```

3. **运行诊断脚本:**
   ```bash
   cd D:\dogwalking\findtrip\pybullet_walking
   python use_motion_imitation.py --show-instructions
   ```

### 快速参考 / Quick Reference

| 问题 | 解决方案 |
|------|---------|
| 没有可视化窗口 | 添加 `--visualize` 参数 |
| TensorFlow 错误 | 安装 TensorFlow 1.15.0 |
| 缺少模型 | 使用 `--mode test` 和 `--model_file` |
| MPI 错误 | 安装 Microsoft MPI 或使用单进程 |
| URDF 警告 | 可以忽略，这是正常的警告信息 |

### 完整的工作示例 / Complete Working Example

```bash
# 1. 激活环境
conda activate motion_tf1

# 2. 进入目录
cd D:\dogwalking\motion_imitation

# 3. 运行测试
python motion_imitation/run.py --mode test --motion_file motion_imitation/data/motions/dog_pace.txt --model_file motion_imitation/data/policies/dog_pace.zip --visualize

# 4. 如果成功，尝试其他动作
python motion_imitation/run.py --mode test --motion_file motion_imitation/data/motions/dog_trot.txt --model_file motion_imitation/data/policies/dog_trot.zip --visualize

python motion_imitation/run.py --mode test --motion_file motion_imitation/data/motions/dog_spin.txt --model_file motion_imitation/data/policies/dog_spin.zip --visualize
```
