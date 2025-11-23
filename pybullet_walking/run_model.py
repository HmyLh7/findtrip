"""
运行已训练模型脚本 / Run Trained Model Script
使用训练好的模型在环境中运行
Run trained model in the environment
"""

import os
import argparse
import pickle
import numpy as np
from environment import WalkingEnvironment


def run_model(model_path='models/walking_model.pkl', episodes=10, render=True):
    """
    使用训练好的模型运行
    Run with trained model
    
    Args:
        model_path: 模型文件路径 / path to model file
        episodes: 运行回合数 / number of episodes to run
        render: 是否显示图形 / whether to render
    """
    print("=" * 50)
    print("运行 PyBullet Walking 训练模型")
    print("Running PyBullet Walking Trained Model")
    print("=" * 50)
    print(f"模型路径 / Model path: {model_path}")
    print(f"运行回合数 / Episodes: {episodes}")
    print(f"图形显示 / Render: {render}")
    print("=" * 50)
    
    # 检查模型文件是否存在
    # Check if model file exists
    if not os.path.exists(model_path):
        print(f"\n错误 / Error: 模型文件不存在 / Model file not found: {model_path}")
        print("\n请先训练模型 / Please train a model first:")
        print("  python train.py")
        print("\n或指定正确的模型路径 / Or specify correct model path:")
        print(f"  python run_model.py --model-path <your_model_path>")
        return
    
    # 加载模型
    # Load model
    try:
        with open(model_path, 'rb') as f:
            policy = pickle.load(f)
        print(f"\n✓ 模型加载成功 / Model loaded successfully")
        print(f"  观测维度 / Observation dim: {policy.observation_dim}")
        print(f"  动作维度 / Action dim: {policy.action_dim}")
    except Exception as e:
        print(f"\n错误 / Error: 加载模型失败 / Failed to load model: {e}")
        return
    
    # 创建环境
    # Create environment
    env = WalkingEnvironment(render=render)
    
    # 统计信息
    # Statistics
    episode_rewards = []
    episode_lengths = []
    
    try:
        for episode in range(episodes):
            print(f"\n{'='*50}")
            print(f"回合 / Episode {episode + 1}/{episodes}")
            print(f"{'='*50}")
            
            # 重置环境
            # Reset environment
            observation = env.reset()
            
            done = False
            episode_reward = 0
            step_count = 0
            
            # 运行一个回合
            # Run one episode
            while not done:
                # 使用确定性策略选择动作
                # Select action using deterministic policy
                action = policy.get_action(observation, deterministic=True)
                
                # 执行动作
                # Execute action
                observation, reward, done, info = env.step(action)
                
                episode_reward += reward
                step_count += 1
                
                # 打印步骤信息
                # Print step info
                if step_count % 100 == 0:
                    print(f"  步数 / Step {step_count}: "
                          f"位置 / Position: {observation[0]:.2f}, "
                          f"奖励 / Reward: {reward:.2f}")
            
            # 记录统计
            # Record statistics
            episode_rewards.append(episode_reward)
            episode_lengths.append(step_count)
            
            # 打印回合总结
            # Print episode summary
            print(f"\n回合总结 / Episode Summary:")
            print(f"  总奖励 / Total Reward: {episode_reward:.2f}")
            print(f"  步数 / Steps: {step_count}")
            print(f"  平均奖励 / Avg Reward per step: {episode_reward/step_count:.4f}")
    
    except KeyboardInterrupt:
        print("\n\n运行被中断 / Run interrupted")
    
    finally:
        # 关闭环境
        # Close environment
        env.close()
        
        # 打印总体统计
        # Print overall statistics
        if episode_rewards:
            print("\n" + "=" * 50)
            print("总体统计 / Overall Statistics")
            print("=" * 50)
            print(f"运行回合数 / Episodes run: {len(episode_rewards)}")
            print(f"平均奖励 / Average reward: {np.mean(episode_rewards):.2f}")
            print(f"最佳奖励 / Best reward: {np.max(episode_rewards):.2f}")
            print(f"最差奖励 / Worst reward: {np.min(episode_rewards):.2f}")
            print(f"奖励标准差 / Reward std: {np.std(episode_rewards):.2f}")
            print(f"平均步数 / Average steps: {np.mean(episode_lengths):.2f}")
            print("=" * 50)
            
            # 打印每个回合的详细结果
            # Print detailed results for each episode
            print("\n详细结果 / Detailed Results:")
            for i, (reward, length) in enumerate(zip(episode_rewards, episode_lengths), 1):
                print(f"  回合 / Episode {i}: 奖励 / Reward = {reward:.2f}, 步数 / Steps = {length}")


def main():
    """主函数 / Main function"""
    parser = argparse.ArgumentParser(
        description='使用训练好的模型运行 PyBullet Walking / Run PyBullet Walking with trained model'
    )
    parser.add_argument('--model-path', type=str, default='models/walking_model.pkl',
                        help='模型文件路径 / Path to trained model (default: models/walking_model.pkl)')
    parser.add_argument('--episodes', type=int, default=10,
                        help='运行回合数 / Number of episodes to run (default: 10)')
    parser.add_argument('--render', type=str, default='True',
                        help='是否显示图形界面 / Whether to render GUI (default: True)')
    
    args = parser.parse_args()
    
    # 解析 render 参数
    # Parse render argument
    render = args.render.lower() in ['true', '1', 'yes', 'y']
    
    run_model(model_path=args.model_path, episodes=args.episodes, render=render)


if __name__ == "__main__":
    main()
