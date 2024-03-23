#!/bin/bash

output_file="full_system_info_for_carbon_footprint_and_performance_analysis.csv"

echo "Category,Subcategory,Detail,Value" > "$output_file"

append_to_csv() {
    local category="$(echo "$1" | sed 's/"/""/g')"
    local subcategory="$(echo "$2" | sed 's/"/""/g')"
    local detail="$(echo "$3" | sed 's/"/""/g')"
    local value="$(echo "$4" | sed 's/"/""/g')"
    echo "\"$category\",\"$subcategory\",\"$detail\",\"$value\"" >> "$output_file"
}

process_cmd_output() {
    local category="$1"
    local subcategory="$2"
    local command="$3"
    local output
    if output=$(eval $command 2>/dev/null); then
        while IFS= read -r line; do
            local key="${line%%:*}"
            local value="${line#*: }"
            append_to_csv "$category" "$subcategory" "$key" "$value"
        done <<< "$output"
    else
        echo "Command failed or not found: $command"
        append_to_csv "$category" "$subcategory" "Error" "Command failed or not found: $command"
    fi
}

echo "Starting comprehensive system information gathering for carbon footprint and performance analysis..."

echo "Gathering detailed CPU information..."
process_cmd_output "CPU" "Details" "lscpu"
if command -v cpupower >/dev/null 2>&1; then
    process_cmd_output "CPU" "Power Efficiency" "cpupower frequency-info"
else
    echo "cpupower command not found, skipping CPU Power Efficiency."
fi

echo "Gathering detailed memory information..."
process_cmd_output "Memory" "Usage" "free -m"
process_cmd_output "Memory" "VMStat" "vmstat -s"
if command -v dmidecode >/dev/null 2>&1; then
    process_cmd_output "Memory" "Efficiency" "dmidecode -t memory | grep -E 'Type:|Speed:'"
else
    echo "dmidecode command not found, skipping Memory Efficiency."
fi

echo "Gathering detailed disk information..."
if command -v iostat >/dev/null 2>&1; then
    process_cmd_output "Disk" "IO" "iostat -dx"
else
    echo "iostat command not found, skipping Disk IO."
fi
process_cmd_output "Disk" "Usage" "df -hT | grep -v 'tmpfs\\|cdrom'"
process_cmd_output "Disk" "Type and Efficiency" "lsblk -d -o name,rota,type | grep disk"


echo "Gathering detailed network information..."
if command -v netstat >/dev/null 2>&1; then
    process_cmd_output "Network" "Interface Statistics" "netstat -i"
else
    echo "netstat command not found, using ss for Network Interface Statistics."
    process_cmd_output "Network" "Interface Statistics" "ss -i"
fi
process_cmd_output "Network" "Socket Connections" "ss -tuln"

echo "Gathering detailed GPU information..."
if command -v nvidia-smi >/dev/null 2>&1; then
    process_cmd_output "GPU" "NVIDIA" "nvidia-smi"
    process_cmd_output "GPU" "Power Efficiency" "nvidia-smi -q -d POWER"
elif command -v amdconfig >/dev/null 2>&1; then
    process_cmd_output "GPU" "AMD" "amdconfig --adapter=all --odgt"
elif lspci | grep -E "VGA|3D" | grep -i intel >/dev/null 2>&1 && command -v intel_gpu_top >/dev/null 2>&1; then
    echo "Gathering Intel GPU information..."
    gpu_output=$(timeout 10 intel_gpu_top -l -s 1000 2>/dev/null)
    avg_freq=$(echo "$gpu_output" | awk '{sum+=$2; count++} END {if(count > 0) print sum/count; else print "N/A"}')
    avg_power=$(echo "$gpu_output" | awk '{sum+=$5; count++} END {if(count > 0) print sum/count; else print "N/A"}')
    append_to_csv "GPU" "Intel" "Average Frequency (MHz)" "$avg_freq"
    append_to_csv "GPU" "Intel" "Average Power (W)" "$avg_power"
else
    echo "No supported GPU management tools found (nvidia-smi, amdconfig, intel_gpu_top) or not applicable. Skipping GPU information."
fi

echo "Gathering environmental variables..."
process_cmd_output "System" "Environmental Variables" "printenv"

echo "Gathering system uptime..."
uptime_info=$(uptime -p)
append_to_csv "System" "Uptime" "Uptime" "$uptime_info"

echo "Gathering power management settings..."
if command -v upower >/dev/null 2>&1; then
    process_cmd_output "Power" "Management" "upower -i /org/freedesktop/UPower/devices/battery_BAT0"
else
    echo "upower command not found, skipping Power Management."
fi

if command -v dmidecode >/dev/null 2>&1; then
    echo "Gathering system DMI information..."
    process_cmd_output "Hardware" "DMI" "dmidecode"
else
    echo "dmidecode command not found, skipping System DMI information."
fi

echo "Gathering kernel parameters..."
process_cmd_output "System" "Kernel Parameters" "sysctl -a"

echo "Gathering energy consumption data..."
process_cmd_output "Energy" "Consumption" "cat /sys/class/power_supply/*/energy_now"
process_cmd_output "Energy" "Battery Health" "cat /sys/class/power_supply/*/capacity"

echo "Gathering CPU and Memory usage data..."
cpu_memory_usage=$(ps -eo %cpu,%mem,comm --sort=-%cpu | head -n 10)
while IFS= read -r line; do
    IFS=',' read -ra ADDR <<< "$line"
    command=${ADDR[2]}
    cpu_usage=${ADDR[0]}
    mem_usage=${ADDR[1]}
    append_to_csv "Performance" "CPU Usage" "$command" "$cpu_usage%"
    append_to_csv "Performance" "Memory Usage" "$command" "$mem_usage%"
done <<< "$cpu_memory_usage"

if command -v iostat >/dev/null 2>&1; then
    echo "Gathering Disk I/O statistics..."
    disk_io=$(iostat -dx 1 2 | sed '1,3d' | sed '/^$/d' | tail -n +3)
    while IFS= read -r line; do
        device=$(echo $line | awk '{print $1}')
        tps=$(echo $line | awk '{print $2}')
        read_sec=$(echo $line | awk '{print $3}')
        write_sec=$(echo $line | awk '{print $4}')
        append_to_csv "Disk" "I/O TPS" "$device" "$tps"
        append_to_csv "Disk" "Read/sec" "$device" "$read_sec"
        append_to_csv "Disk" "Write/sec" "$device" "$write_sec"
    done <<< "$disk_io"
else
    echo "iostat command not found, skipping Disk I/O statistics."
fi

if command -v nstat >/dev/null 2>&1; then
    echo "Gathering Network usage data..."
    nstat -az > /dev/null 2>&1 
    sleep 10 
    network_usage=$(nstat | sed '1,2d')
    while IFS= read -r line; do
        metric=$(echo $line | awk '{print $1}')
        value=$(echo $line | awk '{print $2}')
        append_to_csv "Network" "Usage" "$metric" "$value"
    done <<< "$network_usage"
else
    echo "nstat command not found, skipping Network usage data."
fi

chmod 666 "$output_file"
echo "Comprehensive system information gathering complete. Data saved to $output_file"
