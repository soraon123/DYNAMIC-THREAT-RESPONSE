document.addEventListener('DOMContentLoaded', function() {
    // DOM elements
    const processTable = document.getElementById('process-table').getElementsByTagName('tbody')[0];
    const threatsTable = document.getElementById('threats-table').getElementsByTagName('tbody')[0];
    const historyTable = document.getElementById('history-table').getElementsByTagName('tbody')[0];
    const cpuUsage = document.getElementById('cpu-usage');
    const memoryUsage = document.getElementById('memory-usage');
    const processCount = document.getElementById('process-count');
    const processSearch = document.getElementById('process-search');

    // Update system stats
    function updateSystemStats() {
        fetch('http://localhost:5000/api/stats')
            .then(response => response.json())
            .then(data => {
                cpuUsage.textContent = `${data.cpu_percent.toFixed(1)}%`;
                memoryUsage.textContent = `${data.memory_percent.toFixed(1)}%`;
                processCount.textContent = data.running_processes;
                
                // Color coding for high usage
                cpuUsage.className = 'stat-value';
                memoryUsage.className = 'stat-value';
                
                if (data.cpu_percent > 70) cpuUsage.classList.add('high-cpu');
                if (data.memory_percent > 70) memoryUsage.classList.add('high-memory');
            });
    }

    // Update processes table
    function updateProcesses() {
        fetch('http://localhost:5000/api/processes')
            .then(response => response.json())
            .then(processes => {
                processTable.innerHTML = '';
                processes.forEach(proc => {
                    const row = processTable.insertRow();
                    
                    row.insertCell(0).textContent = proc.pid;
                    row.insertCell(1).textContent = proc.name;
                    
                    const cpuCell = row.insertCell(2);
                    cpuCell.textContent = proc.cpu.toFixed(1);
                    if (proc.cpu > 50) cpuCell.classList.add('high-cpu');
                    
                    const memCell = row.insertCell(3);
                    memCell.textContent = proc.memory.toFixed(1);
                    if (proc.memory > 5) memCell.classList.add('high-memory');
                    
                    row.insertCell(4).textContent = proc.status;
                    
                    const actionCell = row.insertCell(5);
                    const button = document.createElement('button');
                    button.textContent = 'Terminate';
                    button.onclick = () => terminateProcess(proc.pid, proc.name);
                    actionCell.appendChild(button);
                });
            });
    }

    // Update threats table
    function updateThreats() {
        fetch('http://localhost:5000/api/threats')
            .then(response => response.json())
            .then(threats => {
                threatsTable.innerHTML = '';
                threats.forEach(threat => {
                    const row = threatsTable.insertRow();
                    
                    row.insertCell(0).textContent = threat.pid;
                    row.insertCell(1).textContent = threat.name;
                    
                    const cpuCell = row.insertCell(2);
                    cpuCell.textContent = threat.cpu.toFixed(1);
                    cpuCell.classList.add('high-cpu');
                    
                    row.insertCell(3).textContent = threat.timestamp;
                    
                    const actionCell = row.insertCell(4);
                    const button = document.createElement('button');
                    button.textContent = 'Terminate';
                    button.onclick = () => terminateProcess(threat.pid, threat.name);
                    actionCell.appendChild(button);
                });
            });
    }

    // Update history table
    function updateHistory() {
        fetch('http://localhost:5000/api/history')
            .then(response => response.json())
            .then(history => {
                historyTable.innerHTML = '';
                history.slice().reverse().forEach(item => {
                    const row = historyTable.insertRow();
                    
                    row.insertCell(0).textContent = item.name;
                    
                    const cpuCell = row.insertCell(1);
                    cpuCell.textContent = item.cpu.toFixed(1);
                    cpuCell.classList.add('high-cpu');
                    
                    row.insertCell(2).textContent = item.timestamp;
                });
            });
    }

    // Terminate process
    function terminateProcess(pid, name) {
        if (confirm(`Are you sure you want to terminate process ${name} (PID: ${pid})?`)) {
            fetch('http://localhost:5000/api/terminate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ pid: pid })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert(`Process ${name} (PID: ${pid}) terminated successfully.`);
                    updateAllData();
                } else {
                    alert(`Failed to terminate process ${name} (PID: ${pid}).`);
                }
            });
        }
    }

    // Process search functionality
    processSearch.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        const rows = processTable.getElementsByTagName('tr');
        
        for (let row of rows) {
            const name = row.cells[1].textContent.toLowerCase();
            const pid = row.cells[0].textContent.toLowerCase();
            
            if (name.includes(searchTerm) || pid.includes(searchTerm)) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        }
    });

    // Update all data
    function updateAllData() {
        updateSystemStats();
        updateProcesses();
        updateThreats();
        updateHistory();
    }

    // Initial load
    updateAllData();

    // Refresh data every 3 seconds
    setInterval(updateAllData, 3000);
});