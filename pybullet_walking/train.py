"""
训练脚本 / Training Script
使用简单的策略梯度方法训练行走机器人
Train walking robot using simple policy gradient method
"""

import os
import argparse
import pickle
import numpy as np
from environment import WalkingEnvironment
from policy import SimplePolicy


def train(episodes=1000, save_path='models/walking_model.pkl', render=False):
    """
    训练主函数
    Main training function
    
    Args:
        episodes: 训练回合数 / number of training episodes
        save_path: 模型保存路径 / model save path
        render: 是否显示图形 / whether to render
    """
    print("=" * 50)
    print("开始训练 PyBullet Walking 机器人")
    print("Starting PyBullet Walking Robot Training")
    print("=" * 50)
    print(f"训练回合数 / Episodes: {episodes}")
    print(f"保存路径 / Save path: {save_path}")
    print("=" * 50)
    
    # 创建环境
    # Create environment
    env = WalkingEnvironment(render=render)
    
    # 创建策略
    # Create policy
    policy = SimplePolicy(env.observation_dim, env.action_dim)
    
    # 训练统计
    # Training statistics
    episode_rewards = []
    best_reward = -float('inf')
    
    try:
        for episode in range(episodes):
            # 重置环境
            # Reset environment
            observation = env.reset()
            
            # 存储轨迹
            # Store trajectory
            observations = []
            actions = []
            rewards = []
            
            done = False
            episode_reward = 0
            
            # 运行一个回合
            # Run one episode
            while not done:
                # 选择动作
                # Select action
                action = policy.get_action(observation)
                
                # 执行动作
                # Execute action
                next_observation, reward, done, info = env.step(action)
                
                # 存储数据
                # Store data
                observations.append(observation)
                actions.append(action)
                rewards.append(reward)
                
                episode_reward += reward
                observation = next_observation
            
            # 更新策略
            # Update policy
            policy.update(observations, actions, rewards)
            
            # 记录奖励
            # Record reward
            episode_rewards.append(episode_reward)
            
            # 保存最佳模型
            # Save best model
            if episode_reward > best_reward:
                best_reward = episode_reward
                # 确保目录存在
                # Ensure directory exists
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                with open(save_path, 'wb') as f:
                    pickle.dump(policy, f)
                print(f"★ 新最佳模型已保存 / New best model saved! 奖励 / Reward: {best_reward:.2f}")
            
            # 打印进度
            # Print progress
            if (episode + 1) % 10 == 0:
                avg_reward = np.mean(episode_rewards[-10:])
                print(f"回合 / Episode {episode + 1}/{episodes} | "
                      f"平均奖励 / Avg Reward: {avg_reward:.2f} | "
                      f"最佳奖励 / Best: {best_reward:.2f}")
    
    except KeyboardInterrupt:
        print("\n训练被中断 / Training interrupted")
    
    finally:
        # 关闭环境
        # Close environment
        env.close()
        
        # 最终保存
        # Final save
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, 'wb') as f:
            pickle.dump(policy, f)
        
        print("\n" + "=" * 50)
        print("训练完成 / Training completed")
        print(f"最佳奖励 / Best reward: {best_reward:.2f}")
        print(f"模型已保存至 / Model saved to: {save_path}")
        print("=" * 50)
        
        # 打印使用说明
        # Print usage instructions
        print("\n如何使用训练好的模型 / How to use the trained model:")
        print(f"python run_model.py --model-path {save_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='训练 PyBullet Walking 机器人 / Train PyBullet Walking Robot')
    parser.add_argument('--episodes', type=int, default=1000,
                        help='训练回合数 / Number of training episodes (default: 1000)')
    parser.add_argument('--save-path', type=str, default='models/walking_model.pkl',
                        help='模型保存路径 / Model save path (default: models/walking_model.pkl)')
    parser.add_argument('--render', action='store_true',
                        help='是否显示图形界面 / Whether to render GUI (default: False for faster training)')
    
    args = parser.parse_args()
    
    train(episodes=args.episodes, save_path=args.save_path, render=args.render)
