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
