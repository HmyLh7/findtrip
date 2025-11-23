"""
演示脚本 / Demo Script
使用随机动作演示环境
Demonstrate environment with random actions
"""

import argparse
import numpy as np
from environment import WalkingEnvironment


def run_demo(episodes=5, render=True):
    """
    运行演示
    Run demonstration
    
    Args:
        episodes: 演示回合数 / number of demo episodes
        render: 是否显示图形 / whether to render
    """
    print("=" * 50)
    print("PyBullet Walking 环境演示")
    print("PyBullet Walking Environment Demo")
    print("=" * 50)
    print("使用随机动作演示环境 / Demonstrating with random actions")
    print(f"回合数 / Episodes: {episodes}")
    print("=" * 50)
    
    # 创建环境
    # Create environment
    env = WalkingEnvironment(render=render)
    
    try:
        for episode in range(episodes):
            print(f"\n{'='*50}")
            print(f"回合 / Episode {episode + 1}/{episodes}")
            print(f"{'='*50}")
            
            # 重置环境
            # Reset environment
            observation = env.reset()
            print(f"初始观测 / Initial observation: {observation}")
            
            done = False
            episode_reward = 0
            step_count = 0
            
            # 运行一个回合
            # Run one episode
            while not done:
                # 生成随机动作
                # Generate random action
                action = np.random.randn(env.action_dim) * 0.5
                
                # 执行动作
                # Execute action
                observation, reward, done, info = env.step(action)
                
                episode_reward += reward
                step_count += 1
                
                # 打印步骤信息
                # Print step info
                if step_count % 50 == 0:
                    print(f"  步数 / Step {step_count}: "
                          f"位置 / Position: ({observation[0]:.2f}, {observation[1]:.2f}, {observation[2]:.2f}), "
                          f"奖励 / Reward: {reward:.2f}")
            
            # 打印回合总结
            # Print episode summary
            print(f"\n回合总结 / Episode Summary:")
            print(f"  总奖励 / Total Reward: {episode_reward:.2f}")
            print(f"  步数 / Steps: {step_count}")
            print(f"  最终位置 / Final position: ({observation[0]:.2f}, {observation[1]:.2f}, {observation[2]:.2f})")
    
    except KeyboardInterrupt:
        print("\n\n演示被中断 / Demo interrupted")
    
    finally:
        # 关闭环境
        # Close environment
        env.close()
        
        print("\n" + "=" * 50)
        print("演示完成 / Demo completed")
        print("=" * 50)
        print("\n提示 / Hint:")
        print("  这只是随机动作演示，机器人行为不会很好")
        print("  This is just a random action demo, robot behavior won't be good")
        print("\n要看到更好的效果，请:")
        print("To see better results, please:")
        print("  1. 训练模型 / Train a model:")
        print("     python train.py --episodes 100")
        print("  2. 运行训练好的模型 / Run the trained model:")
        print("     python run_model.py")


def main():
    """主函数 / Main function"""
    parser = argparse.ArgumentParser(
        description='PyBullet Walking 环境演示 / PyBullet Walking Environment Demo'
    )
    parser.add_argument('--episodes', type=int, default=5,
                        help='演示回合数 / Number of demo episodes (default: 5)')
    parser.add_argument('--render', type=str, default='True',
                        help='是否显示图形界面 / Whether to render GUI (default: True)')
    
    args = parser.parse_args()
    
    # 解析 render 参数
    # Parse render argument
    render = args.render.lower() in ['true', '1', 'yes', 'y']
    
    run_demo(episodes=args.episodes, render=render)


if __name__ == "__main__":
    main()
