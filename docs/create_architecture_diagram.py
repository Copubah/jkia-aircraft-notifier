#!/usr/bin/env python3
"""
Script to create a visual architecture diagram for JKIA Aircraft Landing Notifier
Requires: pip install matplotlib pillow
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np

def create_architecture_diagram():
    # Create figure and axis
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Colors
    aws_orange = '#FF9900'
    aws_blue = '#232F3E'
    external_green = '#4CAF50'
    user_purple = '#9C27B0'
    
    # Title
    ax.text(7, 9.5, 'JKIA Aircraft Landing Notifier Architecture', 
            fontsize=18, fontweight='bold', ha='center')
    
    # AWS Cloud boundary
    aws_cloud = FancyBboxPatch((0.5, 2), 11, 6.5, 
                               boxstyle="round,pad=0.1", 
                               facecolor='lightblue', 
                               edgecolor=aws_blue, 
                               linewidth=2, 
                               alpha=0.3)
    ax.add_patch(aws_cloud)
    ax.text(1, 8.2, 'AWS Cloud', fontsize=12, fontweight='bold', color=aws_blue)
    
    # EventBridge
    eventbridge = FancyBboxPatch((1, 6.5), 2.5, 1.5, 
                                boxstyle="round,pad=0.1", 
                                facecolor=aws_orange, 
                                edgecolor='black', 
                                alpha=0.8)
    ax.add_patch(eventbridge)
    ax.text(2.25, 7.5, 'EventBridge', fontsize=10, fontweight='bold', ha='center', va='center')
    ax.text(2.25, 7.1, 'Schedule Rule', fontsize=8, ha='center', va='center')
    ax.text(2.25, 6.8, '(5 minutes)', fontsize=8, ha='center', va='center')
    
    # Lambda Function
    lambda_func = FancyBboxPatch((5, 6), 3.5, 2.5, 
                                boxstyle="round,pad=0.1", 
                                facecolor=aws_orange, 
                                edgecolor='black', 
                                alpha=0.8)
    ax.add_patch(lambda_func)
    ax.text(6.75, 7.7, 'AWS Lambda', fontsize=10, fontweight='bold', ha='center', va='center')
    ax.text(6.75, 7.4, 'jkia-landing-notifier', fontsize=9, ha='center', va='center')
    ax.text(6.75, 7.0, '• Fetch aircraft data', fontsize=7, ha='center', va='center')
    ax.text(6.75, 6.7, '• Detect landings', fontsize=7, ha='center', va='center')
    ax.text(6.75, 6.4, '• Send notifications', fontsize=7, ha='center', va='center')
    
    # SNS
    sns = FancyBboxPatch((10, 6.5), 2.5, 1.5, 
                        boxstyle="round,pad=0.1", 
                        facecolor=aws_orange, 
                        edgecolor='black', 
                        alpha=0.8)
    ax.add_patch(sns)
    ax.text(11.25, 7.5, 'Amazon SNS', fontsize=10, fontweight='bold', ha='center', va='center')
    ax.text(11.25, 7.1, 'Email Topic', fontsize=8, ha='center', va='center')
    ax.text(11.25, 6.8, 'Notifications', fontsize=8, ha='center', va='center')
    
    # CloudWatch Logs
    logs = FancyBboxPatch((1, 4), 2.5, 1.5, 
                         boxstyle="round,pad=0.1", 
                         facecolor=aws_orange, 
                         edgecolor='black', 
                         alpha=0.8)
    ax.add_patch(logs)
    ax.text(2.25, 4.9, 'CloudWatch', fontsize=10, fontweight='bold', ha='center', va='center')
    ax.text(2.25, 4.6, 'Logs', fontsize=9, ha='center', va='center')
    ax.text(2.25, 4.3, 'Monitoring', fontsize=8, ha='center', va='center')
    
    # OpenSky API (External)
    opensky = FancyBboxPatch((5, 3), 3.5, 1.5, 
                            boxstyle="round,pad=0.1", 
                            facecolor=external_green, 
                            edgecolor='black', 
                            alpha=0.8)
    ax.add_patch(opensky)
    ax.text(6.75, 4, 'OpenSky Network API', fontsize=10, fontweight='bold', ha='center', va='center', color='white')
    ax.text(6.75, 3.6, 'Aircraft Position Data', fontsize=8, ha='center', va='center', color='white')
    ax.text(6.75, 3.3, '(External Service)', fontsize=7, ha='center', va='center', color='white')
    
    # User
    user = FancyBboxPatch((10, 0.5), 2.5, 1.5, 
                         boxstyle="round,pad=0.1", 
                         facecolor=user_purple, 
                         edgecolor='black', 
                         alpha=0.8)
    ax.add_patch(user)
    ax.text(11.25, 1.4, 'End User', fontsize=10, fontweight='bold', ha='center', va='center', color='white')
    ax.text(11.25, 1.1, '📧 Email', fontsize=9, ha='center', va='center', color='white')
    ax.text(11.25, 0.8, 'Notifications', fontsize=8, ha='center', va='center', color='white')
    
    # Arrows and connections
    # EventBridge to Lambda
    arrow1 = ConnectionPatch((3.5, 7.25), (5, 7.25), "data", "data",
                            arrowstyle="->", shrinkA=5, shrinkB=5, 
                            mutation_scale=20, fc="black", lw=2)
    ax.add_patch(arrow1)
    ax.text(4.25, 7.5, 'Triggers', fontsize=8, ha='center', rotation=0)
    
    # Lambda to SNS
    arrow2 = ConnectionPatch((8.5, 7.25), (10, 7.25), "data", "data",
                            arrowstyle="->", shrinkA=5, shrinkB=5, 
                            mutation_scale=20, fc="black", lw=2)
    ax.add_patch(arrow2)
    ax.text(9.25, 7.5, 'Publishes', fontsize=8, ha='center', rotation=0)
    
    # Lambda to CloudWatch
    arrow3 = ConnectionPatch((5.5, 6), (3, 5.5), "data", "data",
                            arrowstyle="->", shrinkA=5, shrinkB=5, 
                            mutation_scale=20, fc="gray", lw=1.5)
    ax.add_patch(arrow3)
    ax.text(4, 5.5, 'Logs', fontsize=7, ha='center', rotation=-30, color='gray')
    
    # Lambda to OpenSky
    arrow4 = ConnectionPatch((6.75, 6), (6.75, 4.5), "data", "data",
                            arrowstyle="<->", shrinkA=5, shrinkB=5, 
                            mutation_scale=20, fc="blue", lw=2)
    ax.add_patch(arrow4)
    ax.text(7.5, 5.25, 'API Call', fontsize=8, ha='center', rotation=-90, color='blue')
    
    # SNS to User
    arrow5 = ConnectionPatch((11.25, 6.5), (11.25, 2), "data", "data",
                            arrowstyle="->", shrinkA=5, shrinkB=5, 
                            mutation_scale=20, fc="purple", lw=2)
    ax.add_patch(arrow5)
    ax.text(11.8, 4.25, 'Email', fontsize=8, ha='center', rotation=-90, color='purple')
    
    # Add timing annotations
    ax.text(0.5, 9, '⏰ Every 5 minutes', fontsize=10, fontweight='bold', color='red')
    ax.text(0.5, 0.5, '💰 Cost: ~$0.80/month', fontsize=10, fontweight='bold', color='green')
    
    # Add legend
    legend_elements = [
        patches.Patch(color=aws_orange, label='AWS Services'),
        patches.Patch(color=external_green, label='External API'),
        patches.Patch(color=user_purple, label='End User')
    ]
    ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.98, 0.98))
    
    plt.tight_layout()
    plt.savefig('docs/architecture.png', dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.savefig('docs/architecture.pdf', bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    
    print("Architecture diagram saved as:")
    print("- docs/architecture.png")
    print("- docs/architecture.pdf")
    
    # Show the plot
    plt.show()

if __name__ == "__main__":
    create_architecture_diagram()