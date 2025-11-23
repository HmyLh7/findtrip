"""
使用 motion_imitation 预训练模型的示例
Example for using motion_imitation pretrained models

此脚本演示如何加载 motion_imitation 项目的预训练模型并在不同地形环境中运行
This script demonstrates how to load pretrained models from the motion_imitation project
and run them in different terrain environments.

GitHub: https://github.com/erwincoumans/motion_imitation
"""

import os
import sys
import argparse
import numpy as np
import pybullet as p
import pybullet_data

# motion_imitation 的预训练模型使用说明
# Instructions for using motion_imitation pretrained models

INSTRUCTIONS_CN = """
=============================================================================
如何使用 motion_imitation 预训练模型
=============================================================================

1. 克隆 motion_imitation 仓库:
   git clone https://github.com/erwincoumans/motion_imitation.git
   cd motion_imitation

2. 安装依赖:
   pip install -r requirements.txt
   pip install stable-baselines tensorflow

3. 预训练模型位置:
   motion_imitation/data/policies/
   - dog_pace.zip  (狗步态)
   - dog_trot.zip  (狗小跑)
   - dog_spin.zip  (狗旋转)

4. 测试预训练模型:
   python3 motion_imitation/run.py --mode test \\
       --motion_file motion_imitation/data/motions/dog_pace.txt \\
       --model_file motion_imitation/data/policies/dog_pace.zip \\
       --visualize

5. 在不同地形环境中运行:
   
   a) 修改环境构建器 (motion_imitation/envs/env_builder.py)
      可以添加不同的地形:
      - 斜坡 (slopes)
      - 楼梯 (stairs)
      - 崎岖地形 (rough terrain)
      - 障碍物 (obstacles)
   
   b) 使用环境随机化:
      env = build_imitation_env(
          motion_files=[motion_file],
          enable_randomizer=True,  # 启用环境随机化
          enable_rendering=True
      )
   
   c) 自定义地形环境示例:
      # 在 PyBullet 中创建地形
      terrain_shape = p.createCollisionShape(
          shapeType=p.GEOM_HEIGHTFIELD,
          meshScale=[.05, .05, 1],
          heightfieldTextureScaling=128,
          heightfieldData=height_data,
          numHeightfieldRows=rows,
          numHeightfieldColumns=cols
      )
      terrain = p.createMultiBody(0, terrain_shape)

6. 加载和使用模型的 Python 代码示例:
   
   from motion_imitation.envs import env_builder
   from motion_imitation.learning import ppo_imitation
   from motion_imitation.learning import imitation_policies
   
   # 构建环境
   env = env_builder.build_imitation_env(
       motion_files=["motion_imitation/data/motions/dog_pace.txt"],
       enable_randomizer=False,
       enable_rendering=True
   )
   
   # 创建模型
   policy_kwargs = {
       "net_arch": [{"pi": [512, 256], "vf": [512, 256]}],
       "act_fun": tf.nn.relu
   }
   
   model = ppo_imitation.PPOImitation(
       policy=imitation_policies.ImitationPolicy,
       env=env,
       gamma=0.95,
       policy_kwargs=policy_kwargs
   )
   
   # 加载预训练模型
   model.load_parameters("motion_imitation/data/policies/dog_pace.zip")
   
   # 运行模型
   obs = env.reset()
   for _ in range(1000):
       action, _ = model.predict(obs, deterministic=True)
       obs, reward, done, info = env.step(action)
       if done:
           obs = env.reset()

7. 应用到不同场地环境的关键步骤:
   
   a) 地形类型:
      - 平地: 默认环境
      - 斜坡: 添加倾斜的地面
      - 楼梯: 使用 box 创建台阶
      - 崎岖地形: 使用 heightfield
      - 混合地形: 组合多种地形元素
   
   b) 环境参数调整:
      - 摩擦系数 (friction)
      - 重力 (gravity)
      - 机器人初始位置 (initial position)
      - 地形复杂度 (terrain complexity)
   
   c) 测试模型泛化能力:
      - 逐步增加地形难度
      - 记录成功率和性能指标
      - 对比不同预训练模型的表现

8. 高级用法 - 微调模型:
   
   # 加载预训练模型
   model.load_parameters("pretrained_model.zip")
   
   # 在新环境中继续训练
   model.learn(total_timesteps=1000000, save_path="finetuned_model.zip")

=============================================================================
"""

INSTRUCTIONS_EN = """
=============================================================================
How to Use motion_imitation Pretrained Models
=============================================================================

1. Clone the motion_imitation repository:
   git clone https://github.com/erwincoumans/motion_imitation.git
   cd motion_imitation

2. Install dependencies:
   pip install -r requirements.txt
   pip install stable-baselines tensorflow

3. Pretrained model locations:
   motion_imitation/data/policies/
   - dog_pace.zip  (dog pacing gait)
   - dog_trot.zip  (dog trotting gait)
   - dog_spin.zip  (dog spinning)

4. Test pretrained models:
   python3 motion_imitation/run.py --mode test \\
       --motion_file motion_imitation/data/motions/dog_pace.txt \\
       --model_file motion_imitation/data/policies/dog_pace.zip \\
       --visualize

5. Run in different terrain environments:
   
   a) Modify environment builder (motion_imitation/envs/env_builder.py)
      You can add different terrains:
      - Slopes
      - Stairs
      - Rough terrain
      - Obstacles
   
   b) Use environment randomization:
      env = build_imitation_env(
          motion_files=[motion_file],
          enable_randomizer=True,  # Enable environment randomization
          enable_rendering=True
      )
   
   c) Custom terrain environment example:
      # Create terrain in PyBullet
      terrain_shape = p.createCollisionShape(
          shapeType=p.GEOM_HEIGHTFIELD,
          meshScale=[.05, .05, 1],
          heightfieldTextureScaling=128,
          heightfieldData=height_data,
          numHeightfieldRows=rows,
          numHeightfieldColumns=cols
      )
      terrain = p.createMultiBody(0, terrain_shape)

6. Python code example for loading and using models:
   
   from motion_imitation.envs import env_builder
   from motion_imitation.learning import ppo_imitation
   from motion_imitation.learning import imitation_policies
   
   # Build environment
   env = env_builder.build_imitation_env(
       motion_files=["motion_imitation/data/motions/dog_pace.txt"],
       enable_randomizer=False,
       enable_rendering=True
   )
   
   # Create model
   policy_kwargs = {
       "net_arch": [{"pi": [512, 256], "vf": [512, 256]}],
       "act_fun": tf.nn.relu
   }
   
   model = ppo_imitation.PPOImitation(
       policy=imitation_policies.ImitationPolicy,
       env=env,
       gamma=0.95,
       policy_kwargs=policy_kwargs
   )
   
   # Load pretrained model
   model.load_parameters("motion_imitation/data/policies/dog_pace.zip")
   
   # Run model
   obs = env.reset()
   for _ in range(1000):
       action, _ = model.predict(obs, deterministic=True)
       obs, reward, done, info = env.step(action)
       if done:
           obs = env.reset()

7. Key steps for applying to different terrain environments:
   
   a) Terrain types:
      - Flat: Default environment
      - Slopes: Add inclined ground
      - Stairs: Create steps using boxes
      - Rough terrain: Use heightfield
      - Mixed terrain: Combine multiple terrain elements
   
   b) Environment parameter tuning:
      - Friction coefficient
      - Gravity
      - Robot initial position
      - Terrain complexity
   
   c) Test model generalization:
      - Gradually increase terrain difficulty
      - Record success rate and performance metrics
      - Compare performance of different pretrained models

8. Advanced usage - Fine-tuning models:
   
   # Load pretrained model
   model.load_parameters("pretrained_model.zip")
   
   # Continue training in new environment
   model.learn(total_timesteps=1000000, save_path="finetuned_model.zip")

=============================================================================
"""


class TerrainEnvironment:
    """
    不同地形环境的示例
    Example terrain environments
    """
    
    @staticmethod
    def create_flat_terrain(physics_client):
        """创建平地 / Create flat terrain"""
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        plane_id = p.loadURDF("plane.urdf", physicsClientId=physics_client)
        return plane_id
    
    @staticmethod
    def create_slope_terrain(physics_client, slope_angle=10):
        """
        创建斜坡地形 / Create slope terrain
        
        Args:
            slope_angle: 斜坡角度(度) / Slope angle in degrees
        """
        slope_angle_rad = np.deg2rad(slope_angle)
        
        # 创建斜坡碰撞形状
        # Create slope collision shape
        collision_shape = p.createCollisionShape(
            shapeType=p.GEOM_BOX,
            halfExtents=[5, 5, 0.1],
            physicsClientId=physics_client
        )
        
        visual_shape = p.createVisualShape(
            shapeType=p.GEOM_BOX,
            halfExtents=[5, 5, 0.1],
            rgbaColor=[0.6, 0.6, 0.6, 1],
            physicsClientId=physics_client
        )
        
        # 创建带旋转的斜坡
        # Create slope with rotation
        orientation = p.getQuaternionFromEuler([slope_angle_rad, 0, 0])
        terrain_id = p.createMultiBody(
            baseMass=0,
            baseCollisionShapeIndex=collision_shape,
            baseVisualShapeIndex=visual_shape,
            basePosition=[0, 0, 0],
            baseOrientation=orientation,
            physicsClientId=physics_client
        )
        
        return terrain_id
    
    @staticmethod
    def create_stairs_terrain(physics_client, num_steps=10, step_height=0.1, step_depth=0.3):
        """
        创建楼梯地形 / Create stairs terrain
        
        Args:
            num_steps: 台阶数量 / Number of steps
            step_height: 台阶高度 / Step height
            step_depth: 台阶深度 / Step depth
        """
        step_ids = []
        
        for i in range(num_steps):
            collision_shape = p.createCollisionShape(
                shapeType=p.GEOM_BOX,
                halfExtents=[1, step_depth/2, step_height/2],
                physicsClientId=physics_client
            )
            
            visual_shape = p.createVisualShape(
                shapeType=p.GEOM_BOX,
                halfExtents=[1, step_depth/2, step_height/2],
                rgbaColor=[0.5, 0.5, 0.5, 1],
                physicsClientId=physics_client
            )
            
            position = [0, i * step_depth, (i + 0.5) * step_height]
            
            step_id = p.createMultiBody(
                baseMass=0,
                baseCollisionShapeIndex=collision_shape,
                baseVisualShapeIndex=visual_shape,
                basePosition=position,
                physicsClientId=physics_client
            )
            
            step_ids.append(step_id)
        
        return step_ids
    
    @staticmethod
    def create_rough_terrain(physics_client, size=50, max_height=0.5):
        """
        创建崎岖地形 / Create rough terrain using heightfield
        
        Args:
            size: 地形大小 / Terrain size
            max_height: 最大高度变化 / Maximum height variation
        """
        try:
            # 平滑处理需要 scipy
            # Smoothing requires scipy
            from scipy import ndimage
            
            # 生成随机高度数据
            # Generate random height data
            height_data = np.random.uniform(0, max_height, (size, size))
            
            # 平滑处理
            # Smoothing
            height_data = ndimage.gaussian_filter(height_data, sigma=2)
        except ImportError:
            # 如果没有 scipy，使用简单的随机地形
            # If scipy is not available, use simple random terrain
            print("Warning: scipy not installed, using simple random terrain")
            print("For better terrain, install: pip install scipy")
            height_data = np.random.uniform(0, max_height, (size, size))
        
        terrain_shape = p.createCollisionShape(
            shapeType=p.GEOM_HEIGHTFIELD,
            meshScale=[0.1, 0.1, 1],
            heightfieldTextureScaling=size/2,
            heightfieldData=height_data.flatten(),
            numHeightfieldRows=size,
            numHeightfieldColumns=size,
            physicsClientId=physics_client
        )
        
        terrain_id = p.createMultiBody(
            baseMass=0,
            baseCollisionShapeIndex=terrain_shape,
            basePosition=[0, 0, 0],
            physicsClientId=physics_client
        )
        
        # 设置颜色
        # Set color
        p.changeVisualShape(
            terrain_id, -1,
            rgbaColor=[0.5, 0.7, 0.5, 1],
            physicsClientId=physics_client
        )
        
        return terrain_id


def demonstrate_terrain_types(render=True):
    """
    演示不同的地形类型
    Demonstrate different terrain types
    """
    print("=" * 70)
    print("地形类型演示 / Terrain Types Demonstration")
    print("=" * 70)
    
    terrains = [
        ("flat", "平地 / Flat"),
        ("slope", "斜坡 / Slope"),
        ("stairs", "楼梯 / Stairs"),
    ]
    
    for terrain_type, terrain_name in terrains:
        print(f"\n{terrain_name}:")
        print(f"  要查看 {terrain_name}，请运行:")
        print(f"  To view {terrain_name}, run:")
        print(f"  python use_motion_imitation.py --terrain {terrain_type}")


def main():
    """主函数 / Main function"""
    parser = argparse.ArgumentParser(
        description='使用 motion_imitation 预训练模型示例 / Example for using motion_imitation pretrained models'
    )
    
    parser.add_argument('--show-instructions', action='store_true',
                        help='显示详细使用说明 / Show detailed instructions')
    parser.add_argument('--terrain', type=str, default='demo',
                        choices=['demo', 'flat', 'slope', 'stairs', 'rough'],
                        help='地形类型 / Terrain type')
    parser.add_argument('--render', type=str, default='True',
                        help='是否显示图形 / Whether to render')
    
    args = parser.parse_args()
    
    if args.show_instructions:
        print(INSTRUCTIONS_CN)
        print(INSTRUCTIONS_EN)
        return
    
    if args.terrain == 'demo':
        demonstrate_terrain_types()
        print("\n" + "=" * 70)
        print("要查看完整使用说明，请运行:")
        print("To view complete instructions, run:")
        print("python use_motion_imitation.py --show-instructions")
        print("=" * 70)
        return
    
    # 解析渲染参数
    # Parse render argument
    render = args.render.lower() in ['true', '1', 'yes', 'y']
    
    # 创建物理引擎客户端
    # Create physics client
    if render:
        physics_client = p.connect(p.GUI)
    else:
        physics_client = p.connect(p.DIRECT)
    
    p.setGravity(0, 0, -9.8)
    
    # 创建地形
    # Create terrain
    print(f"\n创建地形: {args.terrain}")
    print(f"Creating terrain: {args.terrain}")
    
    if args.terrain == 'flat':
        TerrainEnvironment.create_flat_terrain(physics_client)
    elif args.terrain == 'slope':
        TerrainEnvironment.create_slope_terrain(physics_client, slope_angle=15)
    elif args.terrain == 'stairs':
        TerrainEnvironment.create_stairs_terrain(physics_client)
    elif args.terrain == 'rough':
        TerrainEnvironment.create_rough_terrain(physics_client)
    
    print("\n地形创建完成 / Terrain created")
    print("按 Ctrl+C 退出 / Press Ctrl+C to exit")
    
    # 保持窗口打开
    # Keep window open
    try:
        while True:
            p.stepSimulation()
            if render:
                import time
                time.sleep(1./240.)
    except KeyboardInterrupt:
        print("\n退出 / Exiting")
    
    p.disconnect()


if __name__ == "__main__":
    main()
