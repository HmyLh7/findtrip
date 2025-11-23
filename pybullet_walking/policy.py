"""
策略模块 / Policy Module
定义策略网络类 / Define policy network class
"""

import numpy as np


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
