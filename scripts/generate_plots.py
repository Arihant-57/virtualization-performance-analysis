#!/usr/bin/env python3
"""
Performance Visualization Script
Cloud Computing Experiment: Performance Analysis of Type-1 and Type-2 Hypervisors

Generates academic publication-quality charts from recorded benchmark data:
1. Throughput Comparison (Events per Second)
2. Latency Metrics Comparison (Min, Avg, 95th Percentile, Max)
3. Total Processed Events Comparison
4. Comprehensive 4-Panel Performance Dashboard
"""

import os
import shutil
import csv
import matplotlib.pyplot as plt
import numpy as np

def load_data(csv_path):
    data = {}
    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data[row['hypervisor']] = {
                'type': row['type'],
                'total_time_s': float(row['total_time_s']),
                'total_events': int(row['total_events']),
                'events_per_sec': float(row['events_per_sec']),
                'avg_latency_ms': float(row['avg_latency_ms'])
            }
    return data

def generate_all_plots(base_dir):
    csv_path = os.path.join(base_dir, 'results', 'raw', 'sysbench_results.csv')
    figures_dir = os.path.join(base_dir, 'results', 'figures')
    comparison_dir = os.path.join(base_dir, 'docs', 'screenshots', 'comparison')
    
    os.makedirs(figures_dir, exist_ok=True)
    os.makedirs(comparison_dir, exist_ok=True)
    
    data = load_data(csv_path)
    proxmox = data['Proxmox VE']
    vmware = data['VMware Workstation']
    
    # Latency percentiles extracted from verified benchmark terminal logs
    latency_data = {
        'Proxmox VE (Type-1)': {'min': 0.57, 'avg': 0.69, 'p95': 0.74, 'max': 1.24},
        'VMware Workstation (Type-2)': {'min': 0.94, 'avg': 0.96, 'p95': 1.03, 'max': 3.30}
    }
    
    labels = ['Proxmox VE\n(Type-1 Bare-Metal)', 'VMware Workstation\n(Type-2 Hosted)']
    colors = ['#0284c7', '#ea580c'] # Proxmox blue, VMware orange
    edge_colors = ['#0369a1', '#c2410c']
    
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    fig_dpi = 300
    
    # -------------------------------------------------------------
    # 1. Events Per Second (Throughput)
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8, 6), dpi=fig_dpi)
    eps_vals = [proxmox['events_per_sec'], vmware['events_per_sec']]
    bars = ax.bar(labels, eps_vals, color=colors, edgecolor=edge_colors, width=0.45, linewidth=1.5)
    
    ax.set_ylabel('Throughput (Events per Second)', fontsize=12, fontweight='bold', color='#1e293b')
    ax.set_title('Sysbench CPU Throughput Comparison\n(Higher is Better)', fontsize=14, fontweight='bold', pad=15, color='#0f172a')
    ax.set_ylim(0, 1850)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    for bar in bars:
        h = bar.get_height()
        ax.annotate(f'{h:,.2f} eps',
                    xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 6), textcoords="offset points",
                    ha='center', va='bottom', fontsize=11, fontweight='bold', color='#0f172a')
        
    eps_diff_pct = ((proxmox['events_per_sec'] - vmware['events_per_sec']) / vmware['events_per_sec']) * 100
    ax.text(0.5, 0.88, f'Proxmox VE demonstrates +{eps_diff_pct:.2f}% higher throughput\n(+{proxmox["events_per_sec"] - vmware["events_per_sec"]:.2f} events/sec)',
            transform=ax.transAxes, fontsize=10.5, fontweight='bold', ha='center',
            bbox=dict(boxstyle="round,pad=0.5", facecolor='#f0f9ff', edgecolor='#0284c7', alpha=0.9))
    
    plt.tight_layout()
    eps_img = os.path.join(figures_dir, 'events-per-second-comparison.png')
    plt.savefig(eps_img)
    plt.close()
    
    # -------------------------------------------------------------
    # 2. Average Latency Comparison
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8, 6), dpi=fig_dpi)
    lat_vals = [proxmox['avg_latency_ms'], vmware['avg_latency_ms']]
    bars = ax.bar(labels, lat_vals, color=colors, edgecolor=edge_colors, width=0.45, linewidth=1.5)
    
    ax.set_ylabel('Average Latency (milliseconds ms)', fontsize=12, fontweight='bold', color='#1e293b')
    ax.set_title('Sysbench CPU Average Latency Comparison\n(Lower is Better)', fontsize=14, fontweight='bold', pad=15, color='#0f172a')
    ax.set_ylim(0, 1.35)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    for bar in bars:
        h = bar.get_height()
        ax.annotate(f'{h:.2f} ms',
                    xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 6), textcoords="offset points",
                    ha='center', va='bottom', fontsize=11, fontweight='bold', color='#0f172a')
        
    lat_reduction_pct = ((vmware['avg_latency_ms'] - proxmox['avg_latency_ms']) / vmware['avg_latency_ms']) * 100
    ax.text(0.5, 0.88, f'Proxmox VE reduces average latency by {lat_reduction_pct:.2f}%\n({vmware["avg_latency_ms"] - proxmox["avg_latency_ms"]:.2f} ms lower response time)',
            transform=ax.transAxes, fontsize=10.5, fontweight='bold', ha='center',
            bbox=dict(boxstyle="round,pad=0.5", facecolor='#f0fdf4', edgecolor='#16a34a', alpha=0.9))
    
    plt.tight_layout()
    lat_img = os.path.join(figures_dir, 'latency-comparison.png')
    plt.savefig(lat_img)
    plt.close()
    
    # -------------------------------------------------------------
    # 3. Total Events Comparison
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8, 6), dpi=fig_dpi)
    event_vals = [proxmox['total_events'], vmware['total_events']]
    bars = ax.bar(labels, event_vals, color=colors, edgecolor=edge_colors, width=0.45, linewidth=1.5)
    
    ax.set_ylabel('Total Events Processed (~10 Seconds)', fontsize=12, fontweight='bold', color='#1e293b')
    ax.set_title('Total Sysbench Events Processed\n(Higher is Better)', fontsize=14, fontweight='bold', pad=15, color='#0f172a')
    ax.set_ylim(0, 18000)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    for bar in bars:
        h = bar.get_height()
        ax.annotate(f'{h:,} events',
                    xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 6), textcoords="offset points",
                    ha='center', va='bottom', fontsize=11, fontweight='bold', color='#0f172a')
        
    events_delta = proxmox['total_events'] - vmware['total_events']
    ax.text(0.5, 0.88, f'Proxmox VE processed +{events_delta:,} additional events\n(+{eps_diff_pct:.2f}% event capacity)',
            transform=ax.transAxes, fontsize=10.5, fontweight='bold', ha='center',
            bbox=dict(boxstyle="round,pad=0.5", facecolor='#f0f9ff', edgecolor='#0284c7', alpha=0.9))
    
    plt.tight_layout()
    events_img = os.path.join(figures_dir, 'total-events-comparison.png')
    plt.savefig(events_img)
    plt.close()
    
    # -------------------------------------------------------------
    # 4. Comprehensive 4-Panel Performance Dashboard
    # -------------------------------------------------------------
    fig, axs = plt.subplots(2, 2, figsize=(14, 10.5), dpi=fig_dpi)
    fig.suptitle('Performance Analysis Dashboard: Proxmox VE (Type-1) vs VMware Workstation (Type-2)',
                 fontsize=15, fontweight='bold', color='#0f172a', y=0.98)
    
    # Panel 1: Throughput (EPS)
    bars1 = axs[0, 0].bar(labels, eps_vals, color=colors, edgecolor=edge_colors, width=0.4, linewidth=1.2)
    axs[0, 0].set_title('Throughput: Events per Second (Higher is Better)', fontsize=12, fontweight='bold', color='#1e293b')
    axs[0, 0].set_ylabel('Events / Second', fontsize=10, fontweight='bold')
    axs[0, 0].set_ylim(0, 1850)
    axs[0, 0].grid(axis='y', linestyle='--', alpha=0.6)
    for b in bars1:
        axs[0, 0].annotate(f'{b.get_height():,.2f}', (b.get_x() + b.get_width()/2, b.get_height()),
                           xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # Panel 2: Total Events
    bars2 = axs[0, 1].bar(labels, event_vals, color=colors, edgecolor=edge_colors, width=0.4, linewidth=1.2)
    axs[0, 1].set_title('Total Completed Events (Higher is Better)', fontsize=12, fontweight='bold', color='#1e293b')
    axs[0, 1].set_ylabel('Total Events Count', fontsize=10, fontweight='bold')
    axs[0, 1].set_ylim(0, 18000)
    axs[0, 1].grid(axis='y', linestyle='--', alpha=0.6)
    for b in bars2:
        axs[0, 1].annotate(f'{int(b.get_height()):,}', (b.get_x() + b.get_width()/2, b.get_height()),
                           xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # Panel 3: Average Latency
    bars3 = axs[1, 0].bar(labels, lat_vals, color=colors, edgecolor=edge_colors, width=0.4, linewidth=1.2)
    axs[1, 0].set_title('Average Latency (Lower is Better)', fontsize=12, fontweight='bold', color='#1e293b')
    axs[1, 0].set_ylabel('Latency (ms)', fontsize=10, fontweight='bold')
    axs[1, 0].set_ylim(0, 1.35)
    axs[1, 0].grid(axis='y', linestyle='--', alpha=0.6)
    for b in bars3:
        axs[1, 0].annotate(f'{b.get_height():.2f} ms', (b.get_x() + b.get_width()/2, b.get_height()),
                           xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # Panel 4: Latency Percentiles Distribution (Min, Avg, 95th, Max)
    categories = ['Min Latency', 'Avg Latency', '95th Percentile', 'Max Latency']
    p_lats = [latency_data['Proxmox VE (Type-1)']['min'], latency_data['Proxmox VE (Type-1)']['avg'],
              latency_data['Proxmox VE (Type-1)']['p95'], latency_data['Proxmox VE (Type-1)']['max']]
    v_lats = [latency_data['VMware Workstation (Type-2)']['min'], latency_data['VMware Workstation (Type-2)']['avg'],
              latency_data['VMware Workstation (Type-2)']['p95'], latency_data['VMware Workstation (Type-2)']['max']]
    
    x = np.arange(len(categories))
    w = 0.35
    r1 = axs[1, 1].bar(x - w/2, p_lats, w, label='Proxmox VE (Type-1)', color='#0284c7', edgecolor='#0369a1')
    r2 = axs[1, 1].bar(x + w/2, v_lats, w, label='VMware Workstation (Type-2)', color='#ea580c', edgecolor='#c2410c')
    axs[1, 1].set_title('Latency Distribution Profile (Lower is Better)', fontsize=12, fontweight='bold', color='#1e293b')
    axs[1, 1].set_ylabel('Latency (ms)', fontsize=10, fontweight='bold')
    axs[1, 1].set_xticks(x)
    axs[1, 1].set_xticklabels(categories, fontsize=9.5, fontweight='bold')
    axs[1, 1].legend(loc='upper left', fontsize=9.5)
    axs[1, 1].set_ylim(0, 4.0)
    axs[1, 1].grid(axis='y', linestyle='--', alpha=0.6)
    
    for r in r1:
        axs[1, 1].annotate(f'{r.get_height():.2f}', (r.get_x() + r.get_width()/2, r.get_height()),
                           xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#0369a1')
    for r in r2:
        axs[1, 1].annotate(f'{r.get_height():.2f}', (r.get_x() + r.get_width()/2, r.get_height()),
                           xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#c2410c')
        
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    dash_img = os.path.join(figures_dir, 'hypervisor-performance-comparison.png')
    plt.savefig(dash_img)
    plt.close()
    
    # Mirror generated charts to docs/screenshots/comparison/
    for img_name in ['events-per-second-comparison.png', 'latency-comparison.png',
                     'total-events-comparison.png', 'hypervisor-performance-comparison.png']:
        src = os.path.join(figures_dir, img_name)
        dst = os.path.join(comparison_dir, img_name)
        shutil.copy2(src, dst)
        
    print(f"[OK] Generated 4 performance figures in {figures_dir}")
    print(f"[OK] Copied figures to {comparison_dir}")

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    generate_all_plots(project_root)
