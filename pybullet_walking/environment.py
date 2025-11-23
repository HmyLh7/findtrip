"""
PyBullet Walking Environment
简单的机器人行走环境 / Simple robot walking environment
"""

import pybullet as p
import pybullet_data
import numpy as np
import time


class WalkingEnvironment:
    """
    机器人行走环境类
    Robot walking environment class
    """
    
    def __init__(self, render=True):
        """
        初始化环境
        
        Args:
            render: 是否显示图形界面 / Whether to render GUI
        """
        self.render_mode = render
        self.physics_client = None
        self.robot_id = None
        self.plane_id = None
        self.time_step = 1.0 / 240.0
        self.max_steps = 1000
        self.current_step = 0
        
        # 动作和观测空间维度
        # Action and observation space dimensions
        self.action_dim = 4  # 4个关节 / 4 joints
        self.observation_dim = 12  # 位置、速度等 / position, velocity, etc.
        
    def connect(self):
        """连接到物理引擎 / Connect to physics engine"""
        if self.render_mode:
            self.physics_client = p.connect(p.GUI)
        else:
            self.physics_client = p.connect(p.DIRECT)
        
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.8)
        p.setTimeStep(self.time_step)
        
    def reset(self):
        """
        重置环境
        Reset environment
        
        Returns:
            observation: 初始观测 / Initial observation
        """
        if self.physics_client is None:
            self.connect()
        
        # 重置模拟器
        # Reset simulator
        p.resetSimulation()
        p.setGravity(0, 0, -9.8)
        
        # 加载地面
        # Load ground plane
        self.plane_id = p.loadURDF("plane.urdf")
        
        # 创建简单的机器人（使用球形关节的简化模型）
        # Create simple robot (simplified model with spherical joints)
        self._create_simple_robot()
        
        self.current_step = 0
        
        # 返回初始观测
        # Return initial observation
        return self._get_observation()
    
    def _create_simple_robot(self):
        """创建一个简单的双足机器人 / Create a simple biped robot"""
        # 机器人基座
        # Robot base
        base_collision = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.2, 0.1, 0.3])
        base_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.2, 0.1, 0.3], 
                                         rgbaColor=[0.8, 0.8, 0.8, 1])
        
        # 创建多体系统
        # Create multi-body system
        base_mass = 1.0
        base_position = [0, 0, 1.0]
        
        self.robot_id = p.createMultiBody(
            baseMass=base_mass,
            baseCollisionShapeIndex=base_collision,
            baseVisualShapeIndex=base_visual,
            basePosition=base_position
        )
        
        # 存储关节索引
        # Store joint indices
        self.joint_indices = []
        
    def _get_observation(self):
        """
        获取当前观测
        Get current observation
        
        Returns:
            observation: numpy数组，包含位置、方向、速度等信息
                        numpy array with position, orientation, velocity, etc.
        """
        if self.robot_id is None:
            return np.zeros(self.observation_dim)
        
        # 获取基座位置和方向
        # Get base position and orientation
        pos, orn = p.getBasePositionAndOrientation(self.robot_id)
        
        # 获取基座速度
        # Get base velocity
        vel, ang_vel = p.getBaseVelocity(self.robot_id)
        
        # 将四元数转换为欧拉角
        # Convert quaternion to Euler angles
        euler = p.getEulerFromQuaternion(orn)
        
        # 组合观测
        # Combine observation
        observation = np.concatenate([
            np.array(pos),      # 位置 (3) / position
            np.array(euler),    # 方向 (3) / orientation  
            np.array(vel),      # 线速度 (3) / linear velocity
            np.array(ang_vel)   # 角速度 (3) / angular velocity
        ])
        
        return observation
    
    def step(self, action):
        """
        执行一步动作
        Execute one step with action
        
        Args:
            action: numpy数组，机器人关节的目标位置或力
                   numpy array, target joint positions or forces
        
        Returns:
            observation: 新的观测 / new observation
            reward: 奖励值 / reward value
            done: 是否结束 / whether episode is done
            info: 额外信息字典 / additional info dict
        """
        # 应用动作（这里简化为对基座施加力）
        # Apply action (simplified as applying force to base)
        if len(action) >= 2:
            force = [action[0] * 10, action[1] * 10, 0]
            p.applyExternalForce(self.robot_id, -1, force, [0, 0, 0], p.LINK_FRAME)
        
        # 步进模拟
        # Step simulation
        p.stepSimulation()
        
        if self.render_mode:
            time.sleep(self.time_step)
        
        self.current_step += 1
        
        # 获取新的观测
        # Get new observation
        observation = self._get_observation()
        
        # 计算奖励
        # Calculate reward
        reward = self._compute_reward(observation)
        
        # 检查是否结束
        # Check if done
        done = self._is_done(observation)
        
        info = {
            'step': self.current_step,
            'position': observation[0]
        }
        
        return observation, reward, done, info
    
    def _compute_reward(self, observation):
        """
        计算奖励函数
        Compute reward function
        
        Args:
            observation: 当前观测 / current observation
        
        Returns:
            reward: 奖励值 / reward value
        """
        # 位置
        # Position
        x_pos = observation[0]
        y_pos = observation[1]
        z_pos = observation[2]
        
        # 方向（欧拉角）
        # Orientation (Euler angles)
        roll = observation[3]
        pitch = observation[4]
        
        # 前进奖励（沿x轴正方向）
        # Forward reward (along positive x-axis)
        forward_reward = x_pos
        
        # 保持直立的奖励（惩罚倾斜）
        # Upright reward (penalize tilting)
        upright_reward = -abs(roll) - abs(pitch)
        
        # 高度奖励（保持一定高度）
        # Height reward (maintain certain height)
        height_reward = -(z_pos - 1.0) ** 2
        
        # 侧向移动惩罚
        # Lateral movement penalty
        lateral_penalty = -abs(y_pos)
        
        # 组合奖励
        # Combined reward
        reward = forward_reward + 0.5 * upright_reward + 0.3 * height_reward + 0.2 * lateral_penalty
        
        return reward
    
    def _is_done(self, observation):
        """
        判断是否结束
        Check if episode is done
        
        Args:
            observation: 当前观测 / current observation
        
        Returns:
            done: 是否结束 / whether done
        """
        # 高度过低
        # Height too low
        if observation[2] < 0.3:
            return True
        
        # 倾斜过大
        # Tilted too much
        if abs(observation[3]) > 1.0 or abs(observation[4]) > 1.0:
            return True
        
        # 超过最大步数
        # Exceeded max steps
        if self.current_step >= self.max_steps:
            return True
        
        return False
    
    def close(self):
        """关闭环境 / Close environment"""
        if self.physics_client is not None:
            p.disconnect()
            self.physics_client = None
    
    def __del__(self):
        """析构函数 / Destructor"""
        self.close()
