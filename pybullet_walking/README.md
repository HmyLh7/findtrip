# PyBullet Walking 使用说明 / PyBullet Walking Guide

## 介绍 / Introduction

这是一个使用 PyBullet 物理引擎实现的机器人行走模拟项目。支持训练和使用已训练模型进行推理。

This is a robot walking simulation project implemented with PyBullet physics engine. It supports both training and inference with trained models.

## 安装依赖 / Installation

```bash
pip install pybullet numpy gym
```

或使用项目的 requirements 文件：
Or use the project requirements file:

```bash
cd pybullet_walking
pip install -r requirements.txt
```

## 使用方法 / Usage

### 1. 训练模型 / Train a Model

运行训练脚本：
Run the training script:

```bash
python train.py
```

训练完成后，模型将保存在 `models/` 目录下，默认文件名为 `walking_model.pkl`

After training, the model will be saved in the `models/` directory with the default filename `walking_model.pkl`

可选参数 / Optional arguments:
- `--episodes`: 训练回合数 / Number of training episodes (default: 1000)
- `--save-path`: 模型保存路径 / Model save path (default: models/walking_model.pkl)

示例 / Example:
```bash
python train.py --episodes 2000 --save-path models/my_model.pkl
```

### 2. 使用训练后的模型 / Run with Trained Model

运行推理脚本使用已训练的模型：
Run the inference script with a trained model:

```bash
python run_model.py
```

可选参数 / Optional arguments:
- `--model-path`: 模型文件路径 / Path to the trained model (default: models/walking_model.pkl)
- `--episodes`: 运行回合数 / Number of episodes to run (default: 10)
- `--render`: 是否显示图形界面 / Whether to render GUI (default: True)

示例 / Examples:
```bash
# 使用默认模型运行
# Run with default model
python run_model.py

# 使用指定模型运行
# Run with specific model
python run_model.py --model-path models/my_model.pkl

# 运行20个回合，不显示图形界面
# Run 20 episodes without GUI
python run_model.py --episodes 20 --render False
```

### 3. 快速演示 / Quick Demo

如果没有训练好的模型，可以运行演示脚本查看随机行为：
If you don't have a trained model, you can run the demo script to see random behavior:

```bash
python demo.py
```

## 文件说明 / File Description

- `train.py` - 训练脚本 / Training script
- `run_model.py` - 推理脚本（使用训练好的模型）/ Inference script (run with trained model)
- `demo.py` - 演示脚本（随机动作）/ Demo script (random actions)
- `environment.py` - 环境定义 / Environment definition
- `models/` - 模型保存目录 / Directory for saved models
- `requirements.txt` - Python 依赖 / Python dependencies

## 注意事项 / Notes

1. 首次运行需要安装 PyBullet，这可能需要几分钟时间
   First-time setup requires PyBullet installation, which may take a few minutes

2. 如果遇到图形界面问题，可以使用 `--render False` 参数禁用渲染
   If you encounter GUI issues, use `--render False` to disable rendering

3. 训练可能需要较长时间，建议先运行几个回合测试环境是否正常
   Training may take a long time, it's recommended to test with a few episodes first

4. 模型文件使用 pickle 格式保存，请确保只加载可信来源的模型
   Model files are saved in pickle format, only load models from trusted sources

## 故障排查 / Troubleshooting

### 问题：ImportError: No module named 'pybullet'
**解决方案 / Solution:**
```bash
pip install pybullet
```

### 问题：图形界面无法显示
**解决方案 / Solution:**
使用无图形界面模式 / Use headless mode:
```bash
python run_model.py --render False
```

### 问题：找不到模型文件
**解决方案 / Solution:**
1. 确保先运行 `train.py` 训练并保存模型
   Make sure to run `train.py` first to train and save a model
2. 检查模型路径是否正确
   Check if the model path is correct
3. 使用 `--model-path` 参数指定正确的模型路径
   Use `--model-path` to specify the correct model path

## 进阶使用 / Advanced Usage

### 自定义环境参数
### Customizing Environment Parameters

编辑 `environment.py` 文件可以修改：
Edit `environment.py` to modify:
- 机器人模型 / Robot model
- 物理参数 / Physics parameters  
- 奖励函数 / Reward function
- 观测空间 / Observation space

### 使用不同的强化学习算法
### Using Different RL Algorithms

当前实现使用简单的策略梯度方法。要使用其他算法（如PPO、SAC等），可以集成如下库：
Current implementation uses simple policy gradient. To use other algorithms (PPO, SAC, etc.), integrate libraries like:
- Stable-Baselines3
- RLlib
- TensorFlow Agents

## 许可证 / License

MIT License

## 使用 motion_imitation 预训练模型 / Using motion_imitation Pretrained Models

本项目集成了对 [motion_imitation](https://github.com/erwincoumans/motion_imitation) 项目预训练模型的支持。

This project includes support for pretrained models from the [motion_imitation](https://github.com/erwincoumans/motion_imitation) project.

### 快速开始 / Quick Start

1. **查看完整使用说明 / View complete instructions:**

```bash
python use_motion_imitation.py --show-instructions
```

这将显示详细的中英文说明，包括：
This will display detailed bilingual instructions including:
- 如何克隆和安装 motion_imitation / How to clone and install motion_imitation
- 如何加载预训练模型 / How to load pretrained models
- 如何在不同地形环境中运行 / How to run in different terrain environments
- Python 代码示例 / Python code examples

2. **演示不同地形类型 / Demonstrate different terrain types:**

```bash
# 查看可用地形类型
# View available terrain types
python use_motion_imitation.py --terrain demo

# 平地环境
# Flat terrain
python use_motion_imitation.py --terrain flat

# 斜坡环境 (15度)
# Slope terrain (15 degrees)
python use_motion_imitation.py --terrain slope

# 楼梯环境
# Stairs terrain
python use_motion_imitation.py --terrain stairs
```

### 主要功能 / Main Features

1. **预训练模型支持 / Pretrained Model Support**
   - dog_pace.zip - 狗步态 / Dog pacing gait
   - dog_trot.zip - 狗小跑 / Dog trotting gait
   - dog_spin.zip - 狗旋转 / Dog spinning

2. **多种地形环境 / Multiple Terrain Environments**
   - 平地 / Flat terrain
   - 斜坡 / Slopes
   - 楼梯 / Stairs
   - 崎岖地形 / Rough terrain
   - 混合地形 / Mixed terrain

3. **环境自定义 / Environment Customization**
   - 调整摩擦系数 / Adjust friction coefficient
   - 修改重力参数 / Modify gravity parameters
   - 自定义地形复杂度 / Customize terrain complexity

### 使用 motion_imitation 预训练模型的步骤 / Steps to Use motion_imitation Pretrained Models

#### 1. 安装 motion_imitation

```bash
# 克隆仓库
git clone https://github.com/erwincoumans/motion_imitation.git
cd motion_imitation

# 安装依赖
pip install -r requirements.txt
pip install stable-baselines tensorflow
```

#### 2. 测试预训练模型

```bash
# 运行预训练的狗步态模型
python3 motion_imitation/run.py --mode test \
    --motion_file motion_imitation/data/motions/dog_pace.txt \
    --model_file motion_imitation/data/policies/dog_pace.zip \
    --visualize
```

#### 3. 在不同环境中运行

查看 `use_motion_imitation.py` 中的详细示例和代码。该文件包含：
See detailed examples and code in `use_motion_imitation.py`. The file includes:

- 创建不同地形的方法 / Methods to create different terrains
- 加载和运行预训练模型的示例 / Examples of loading and running pretrained models
- 环境参数调整指南 / Guide for environment parameter tuning
- 模型微调建议 / Suggestions for model fine-tuning

#### 4. 关键代码示例 / Key Code Examples

```python
from motion_imitation.envs import env_builder
from motion_imitation.learning import ppo_imitation
from motion_imitation.learning import imitation_policies

# 构建环境
env = env_builder.build_imitation_env(
    motion_files=["motion_imitation/data/motions/dog_pace.txt"],
    enable_randomizer=False,
    enable_rendering=True
)

# 加载预训练模型
model = ppo_imitation.PPOImitation(
    policy=imitation_policies.ImitationPolicy,
    env=env,
    gamma=0.95
)
model.load_parameters("motion_imitation/data/policies/dog_pace.zip")

# 运行模型
obs = env.reset()
for _ in range(1000):
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, done, info = env.step(action)
    if done:
        obs = env.reset()
```

### 应用到不同场地环境 / Applying to Different Terrain Environments

1. **平地到斜坡的过渡 / Transition from Flat to Slope:**
   - 逐步增加斜坡角度 (5°, 10°, 15°, 20°)
   - Gradually increase slope angle (5°, 10°, 15°, 20°)

2. **楼梯环境测试 / Stairs Environment Testing:**
   - 调整台阶高度和深度
   - Adjust step height and depth
   - 测试不同步态的适应性
   - Test adaptability of different gaits

3. **崎岖地形挑战 / Rough Terrain Challenge:**
   - 使用 heightfield 创建随机地形
   - Use heightfield to create random terrain
   - 评估模型的泛化能力
   - Evaluate model generalization capability

4. **混合环境 / Mixed Environments:**
   - 组合多种地形元素
   - Combine multiple terrain elements
   - 测试长距离导航能力
   - Test long-distance navigation capability

### 性能评估 / Performance Evaluation

运行不同地形环境中的模型并记录：
Run models in different terrain environments and record:

- 成功完成率 / Success completion rate
- 平均速度 / Average velocity
- 能量消耗 / Energy consumption
- 稳定性指标 / Stability metrics

### 故障排查 / Troubleshooting

**问题：找不到 motion_imitation 模块**
**Issue: Cannot find motion_imitation module**

解决方案 / Solution:
```bash
# 确保已克隆并安装 motion_imitation
git clone https://github.com/erwincoumans/motion_imitation.git
cd motion_imitation
pip install -e .
```

**问题：TensorFlow 版本兼容性**
**Issue: TensorFlow version compatibility**

解决方案 / Solution:
```bash
# motion_imitation 需要 TensorFlow 1.x
pip install tensorflow==1.15.0
# 或使用 TensorFlow 2.x 的兼容模式
pip install tensorflow==2.x
```

### 参考资源 / References

- [motion_imitation GitHub](https://github.com/erwincoumans/motion_imitation)
- [Project Page](https://xbpeng.github.io/projects/Robotic_Imitation/index.html)
- [Paper: Learning Agile Robotic Locomotion Skills by Imitating Animals](https://arxiv.org/abs/2004.00784)

