import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_architecture_diagram(output_path):
    fig, ax = plt.subplots(figsize=(14, 10.5), dpi=300)
    ax.set_facecolor('#f8fafc')
    fig.patch.set_facecolor('#f8fafc')
    
    # Hide axes
    ax.axis('off')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    
    # Title & Subtitle
    ax.text(50, 97.5, "VIRTUALIZATION ARCHITECTURAL COMPARISON", 
            ha='center', va='center', fontsize=18, fontweight='bold', color='#0f172a', family='sans-serif')
    ax.text(50, 94.5, "Type-1 Bare-Metal Hypervisor (Proxmox VE / KVM) vs. Type-2 Hosted Hypervisor (VMware Workstation)", 
            ha='center', va='center', fontsize=11, color='#475569', family='sans-serif')
    
    # Helper to draw rounded rectangle box
    def draw_box(x, y, w, h, bg_color, border_color, title, subtitle="", title_color="white", sub_color="#e2e8f0"):
        rect = patches.FancyBboxPatch((x, y), w, h,
                                      boxstyle="round,pad=0.5,rounding_size=1.0",
                                      facecolor=bg_color, edgecolor=border_color, linewidth=1.8)
        ax.add_patch(rect)
        if subtitle:
            ax.text(x + w/2, y + h*0.62, title, ha='center', va='center', fontsize=11, fontweight='bold', color=title_color, family='sans-serif')
            ax.text(x + w/2, y + h*0.28, subtitle, ha='center', va='center', fontsize=8.5, color=sub_color, family='sans-serif')
        else:
            ax.text(x + w/2, y + h/2, title, ha='center', va='center', fontsize=11, fontweight='bold', color=title_color, family='sans-serif')

    # 1. PHYSICAL HARDWARE (TOP)
    draw_box(10, 83, 80, 8.5, '#1e293b', '#0f172a', 
             "PHYSICAL HARDWARE LAYER", 
             "Bare-Metal Server: Multi-Core CPU | RAM | Virtualization Extensions (Intel VT-x / AMD-V) | Storage | NIC")

    # Column Left Container: TYPE-1 VIRTUALIZATION
    type1_bg = patches.FancyBboxPatch((8, 6), 39, 67,
                                      boxstyle="round,pad=0.8,rounding_size=1.5",
                                      facecolor='#eff6ff', edgecolor='#93c5fd', linewidth=1.5, linestyle='--')
    ax.add_patch(type1_bg)
    # Header tag
    header1 = patches.FancyBboxPatch((13, 67.5), 29, 4.2, boxstyle="round,pad=0.3,rounding_size=0.6",
                                    facecolor='#dbeafe', edgecolor='#60a5fa', linewidth=1.2)
    ax.add_patch(header1)
    ax.text(27.5, 70.3, "TYPE-1: BARE-METAL VIRTUALIZATION", ha='center', va='center', fontsize=10.5, fontweight='bold', color='#1e40af')
    ax.text(27.5, 68.7, "Native Hypervisor Architecture", ha='center', va='center', fontsize=8, color='#2563eb')

    # Type-1 Hypervisor
    draw_box(12, 49, 31, 13.5, '#0284c7', '#0369a1',
             "PROXMOX VE / KVM",
             "Type-1 Bare-Metal Hypervisor\nDirect Hardware Execution & Kernel Scheduler")

    # Type-1 Guest OS
    draw_box(12, 29, 31, 13, '#2563eb', '#1d4ed8',
             "UBUNTU VIRTUAL MACHINE",
             "Guest OS Instance (KVM Guest)\n2 vCPU | 2 GB RAM | 20 GB Virtual Disk")

    # Type-1 Workload
    draw_box(12, 10, 31, 12, '#312e81', '#1e1b4b',
             "SYSBENCH CPU BENCHMARK",
             "Workload: 20,000 Primes Run\nDirect CPU Instructions Dispatch")

    # Column Right Container: TYPE-2 VIRTUALIZATION
    type2_bg = patches.FancyBboxPatch((53, 6), 39, 67,
                                      boxstyle="round,pad=0.8,rounding_size=1.5",
                                      facecolor='#fff7ed', edgecolor='#fdba74', linewidth=1.5, linestyle='--')
    ax.add_patch(type2_bg)
    # Header tag
    header2 = patches.FancyBboxPatch((58, 67.5), 29, 4.2, boxstyle="round,pad=0.3,rounding_size=0.6",
                                    facecolor='#ffedd5', edgecolor='#fb923c', linewidth=1.2)
    ax.add_patch(header2)
    ax.text(72.5, 70.3, "TYPE-2: HOSTED VIRTUALIZATION", ha='center', va='center', fontsize=10.5, fontweight='bold', color='#9a3412')
    ax.text(72.5, 68.7, "Host OS Arbitrated Architecture", ha='center', va='center', fontsize=8, color='#c2410c')

    # Type-2 Host OS
    draw_box(57, 54, 31, 10, '#475569', '#334155',
             "HOST OPERATING SYSTEM",
             "Base Operating System Kernel\nHost Drivers, Memory & Process Scheduler")

    # Type-2 Hypervisor
    draw_box(57, 39.5, 31, 10, '#ea580c', '#c2410c',
             "VMWARE WORKSTATION",
             "Type-2 Hosted Hypervisor Application\nTranslates & Manages Guest Virtual Hardware")

    # Type-2 Guest OS
    draw_box(57, 25, 31, 10, '#f59e0b', '#d97706',
             "UBUNTU VIRTUAL MACHINE",
             "Guest OS Instance (Hosted VM)\n2 vCPU | 2 GB RAM | 20 GB Virtual Disk")

    # Type-2 Workload
    draw_box(57, 10, 31, 10.5, '#701a75', '#4a044e',
             "SYSBENCH CPU BENCHMARK",
             "Workload: 20,000 Primes Run\nMediated through Host OS Scheduler")

    # Connector Lines from Physical Hardware down to columns
    # Split connector
    ax.plot([50, 50], [83, 77], color='#475569', linewidth=2.5)
    ax.plot([27.5, 72.5], [77, 77], color='#475569', linewidth=2.5)
    
    # Left arrow down to Proxmox
    ax.annotate('', xy=(27.5, 62.5), xytext=(27.5, 67.5),
                arrowprops=dict(facecolor='#0284c7', edgecolor='#0369a1', width=2.5, headwidth=8, headlength=8))
    # Line segment connecting across header
    ax.plot([27.5, 27.5], [77, 72], color='#0284c7', linewidth=2.5)

    # Right arrow down to Host OS
    ax.annotate('', xy=(72.5, 64), xytext=(72.5, 67.5),
                arrowprops=dict(facecolor='#475569', edgecolor='#334155', width=2.5, headwidth=8, headlength=8))
    ax.plot([72.5, 72.5], [77, 72], color='#475569', linewidth=2.5)

    # Left Column Arrows (Downwards)
    ax.annotate('', xy=(27.5, 42), xytext=(27.5, 49),
                arrowprops=dict(facecolor='#2563eb', edgecolor='#1d4ed8', width=2.5, headwidth=8, headlength=8))
    ax.annotate('', xy=(27.5, 22), xytext=(27.5, 29),
                arrowprops=dict(facecolor='#312e81', edgecolor='#1e1b4b', width=2.5, headwidth=8, headlength=8))

    # Right Column Arrows (Downwards)
    ax.annotate('', xy=(72.5, 49.5), xytext=(72.5, 54),
                arrowprops=dict(facecolor='#ea580c', edgecolor='#c2410c', width=2.5, headwidth=8, headlength=8))
    ax.annotate('', xy=(72.5, 35), xytext=(72.5, 39.5),
                arrowprops=dict(facecolor='#f59e0b', edgecolor='#d97706', width=2.5, headwidth=8, headlength=8))
    ax.annotate('', xy=(72.5, 20.5), xytext=(72.5, 25),
                arrowprops=dict(facecolor='#701a75', edgecolor='#4a044e', width=2.5, headwidth=8, headlength=8))

    # Bottom summary callout badges
    callout1 = patches.FancyBboxPatch((10, 1.5), 35, 3, boxstyle="round,pad=0.2,rounding_size=0.5",
                                      facecolor='#dbeafe', edgecolor='#93c5fd', linewidth=1)
    ax.add_patch(callout1)
    ax.text(27.5, 3, "Direct Hardware Virtualization (KVM Native Kernel Access)",
            ha='center', va='center', fontsize=8, fontweight='bold', color='#1e40af')

    callout2 = patches.FancyBboxPatch((55, 1.5), 35, 3, boxstyle="round,pad=0.2,rounding_size=0.5",
                                      facecolor='#ffedd5', edgecolor='#fed7aa', linewidth=1)
    ax.add_patch(callout2)
    ax.text(72.5, 3, "Two-Tier Scheduling Overhead (Host OS + VM Kernel)",
            ha='center', va='center', fontsize=8, fontweight='bold', color='#9a3412')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Architecture diagram saved to {output_path}")

if __name__ == '__main__':
    create_architecture_diagram(r"C:\Users\ariha\Documents\virtualization-performance-analysis\docs\architecture\virtualization-architecture.png")
