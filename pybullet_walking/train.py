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


class SimplePolicy:
    """
    简单的策略网络（线性策略）
    Simple policy network (linear policy)
    """
    
    def __init__(self, observation_dim, action_dim):
        """
        初始化策略
        
        Args:
            observation_dim: 观测维度 / observation dimension
            action_dim: 动作维度 / action dimension
        """
        self.observation_dim = observation_dim
        self.action_dim = action_dim
        
        # 初始化权重和偏置
        # Initialize weights and bias
        self.weights = np.random.randn(action_dim, observation_dim) * 0.1
        self.bias = np.zeros(action_dim)
        
    def get_action(self, observation, deterministic=False):
        """
        根据观测选择动作
        Select action based on observation
        
        Args:
            observation: 当前观测 / current observation
            deterministic: 是否使用确定性策略 / whether to use deterministic policy
        
        Returns:
            action: 选择的动作 / selected action
        """
        # 线性映射
        # Linear mapping
        mean_action = np.dot(self.weights, observation) + self.bias
        
        if deterministic:
            return np.tanh(mean_action)
        else:
            # 添加噪声探索
            # Add noise for exploration
            noise = np.random.randn(self.action_dim) * 0.1
            action = mean_action + noise
            return np.tanh(action)
    
    def update(self, observations, actions, rewards, learning_rate=0.01):
        """
        更新策略参数
        Update policy parameters
        
        Args:
            observations: 观测列表 / list of observations
            actions: 动作列表 / list of actions
            rewards: 奖励列表 / list of rewards
            learning_rate: 学习率 / learning rate
        """
        # 计算累积奖励
        # Compute cumulative rewards
        discounted_rewards = self._discount_rewards(rewards)
        
        # 标准化奖励
        # Normalize rewards
        discounted_rewards = (discounted_rewards - np.mean(discounted_rewards)) / (np.std(discounted_rewards) + 1e-8)
        
        # 简单的策略梯度更新
        # Simple policy gradient update
        for obs, action, reward in zip(observations, actions, discounted_rewards):
            # 计算梯度
            # Compute gradient
            gradient_w = np.outer(action * reward, obs)
            gradient_b = action * reward
            
            # 更新参数
            # Update parameters
            self.weights += learning_rate * gradient_w
            self.bias += learning_rate * gradient_b
    
    def _discount_rewards(self, rewards, gamma=0.99):
        """
        计算折扣累积奖励
        Compute discounted cumulative rewards
        
        Args:
            rewards: 奖励列表 / reward list
            gamma: 折扣因子 / discount factor
        
        Returns:
            discounted_rewards: 折扣累积奖励 / discounted cumulative rewards
        """
        discounted = np.zeros_like(rewards)
        cumulative = 0
        for i in reversed(range(len(rewards))):
            cumulative = rewards[i] + gamma * cumulative
            discounted[i] = cumulative
        return discounted


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
