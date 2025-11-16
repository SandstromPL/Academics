"""
Main Entry Point for Warehouse Robot Simulator
"""

import argparse
import sys

from src.simulator import Simulator, run_simulation


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Multi-Agent Warehouse Robot Simulator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with default settings
  python main.py
  
  # Run with custom warehouse size
  python main.py --width 30 --height 30
  
  # Run with more robots and packages
  python main.py --robots 5 --packages 10
  
  # Run with simple terminal visualization
  python main.py --visualization simple
  
  # Run without visualization (faster)
  python main.py --visualization none --delay 0
  
  # Run batch simulations for statistics
  python main.py --batch 10
        """
    )
    
    # Warehouse parameters
    parser.add_argument('--width', type=int, default=20,
                       help='Warehouse width (default: 20)')
    parser.add_argument('--height', type=int, default=20,
                       help='Warehouse height (default: 20)')
    parser.add_argument('--obstacles', type=int, default=30,
                       help='Number of obstacles (default: 30)')
    parser.add_argument('--drop-zones', type=int, default=2,
                       help='Number of drop zones (default: 2)')
    
    # Simulation parameters
    parser.add_argument('--robots', type=int, default=3,
                       help='Number of robots (default: 3)')
    parser.add_argument('--packages', type=int, default=5,
                       help='Number of packages (default: 5)')
    parser.add_argument('--max-steps', type=int, default=1000,
                       help='Maximum simulation steps (default: 1000)')
    
    # Visualization
    parser.add_argument('--visualization', choices=['matplotlib', 'simple', 'none'],
                       default='matplotlib',
                       help='Visualization mode (default: matplotlib)')
    parser.add_argument('--delay', type=float, default=0.1,
                       help='Delay between steps in seconds (default: 0.1)')
    
    # Batch mode
    parser.add_argument('--batch', type=int, metavar='N',
                       help='Run N simulations and show aggregate statistics')
    
    args = parser.parse_args()
    
    # Print header
    print("\n" + "=" * 80)
    print(" " * 15 + "🤖 MULTI-AGENT WAREHOUSE ROBOT SIMULATOR 🤖")
    print(" " * 20 + "IIT Bhilai - CSL304 AI Project")
    print("=" * 80)
    
    try:
        if args.batch:
            # Batch mode
            print(f"\n🔄 Running {args.batch} simulations...")
            
            sim = Simulator(
                width=args.width,
                height=args.height,
                num_robots=args.robots,
                num_packages=args.packages,
                num_obstacles=args.obstacles,
                num_drop_zones=args.drop_zones,
                max_steps=args.max_steps,
                visualization='none'
            )
            
            results = sim.run_batch(args.batch)
            
            # Print aggregate statistics
            print("\n" + "=" * 80)
            print("📊 AGGREGATE STATISTICS")
            print("=" * 80)
            print(f"Completed Runs: {results['completed']}/{args.batch}")
            print(f"Completion Rate: {100 * results['completed'] / args.batch:.1f}%")
            
            if results['total_steps']:
                print(f"\nSteps:")
                print(f"   • Average: {sum(results['total_steps']) / len(results['total_steps']):.1f}")
                print(f"   • Min: {min(results['total_steps'])}")
                print(f"   • Max: {max(results['total_steps'])}")
            
            if results['total_distances']:
                print(f"\nTotal Distance:")
                print(f"   • Average: {sum(results['total_distances']) / len(results['total_distances']):.1f}")
                print(f"   • Min: {min(results['total_distances'])}")
                print(f"   • Max: {max(results['total_distances'])}")
            
            print("=" * 80 + "\n")
        
        else:
            # Single simulation mode
            sim = Simulator(
                width=args.width,
                height=args.height,
                num_robots=args.robots,
                num_packages=args.packages,
                num_obstacles=args.obstacles,
                num_drop_zones=args.drop_zones,
                max_steps=args.max_steps,
                visualization=args.visualization
            )
            
            sim.run(step_delay=args.delay, interactive=True)
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Simulation terminated by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
