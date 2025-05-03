import os
import sys
import argparse

def main():
    """Main entry point for the Driver Safety Monitoring System"""
    parser = argparse.ArgumentParser(description='Driver Safety Monitoring System')
    parser.add_argument('--mode', type=str, choices=['ui', 'train', 'collect_data'],
                        default='ui', help='Mode to run the application in')
    parser.add_argument('--data_class', type=str, choices=['focused', 'distracted',
                        'eyes_open', 'eyes_half_closed', 'eyes_closed',
                        'head_forward', 'head_tilted', 'head_sideways',
                        'hands_on_wheel', 'hands_off_wheel', 'holding_object'],
                        help='Class of data to collect (required for collect_data mode)')
    parser.add_argument('--samples', type=int, default=200,
                        help='Number of samples to collect in collect_data mode')
    
    args = parser.parse_args()
    
    # Add project root to path
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(project_root)
    
    if args.mode == 'ui':
        # Run the UI application
        from ui.monitoring_app import main as run_ui
        run_ui()
    
    elif args.mode == 'train':
        # Run the simplified training script that doesn't rely on TensorFlow
        from training.simple_train import train_model
        train_model()
    
    elif args.mode == 'collect_data':
        # Run the data collection script
        if not args.data_class:
            print("Error: --data_class is required for collect_data mode")
            parser.print_help()
            return
        
        from data.collect_data import collect_data, create_directory_structure
        
        data_dir = os.path.join(project_root, 'data')
        create_directory_structure(data_dir)
        
        # Use detailed collection by default
        detailed = True
        collect_data(data_dir, args.data_class, args.samples, 0.2, detailed)

if __name__ == "__main__":
    main()