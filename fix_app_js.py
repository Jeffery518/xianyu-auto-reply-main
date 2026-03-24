with open("static/js/app.js", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update loadRiskControlLogs signature
content = content.replace(
    "async function loadRiskControlLogs(offset = 0) {",
    "async function loadRiskControlLogs(offset = 0, isAutoRefresh = false) {"
)

# 2. Update loading visibility logic
old_loading_logic = """    const loadingDiv = document.getElementById('loadingRiskLogs');
    const logContainer = document.getElementById('riskLogContainer');
    const noLogsDiv = document.getElementById('noRiskLogs');

    loadingDiv.style.display = 'block';
    logContainer.style.display = 'none';
    noLogsDiv.style.display = 'none';"""

new_loading_logic = """    const loadingDiv = document.getElementById('loadingRiskLogs');
    const logContainer = document.getElementById('riskLogContainer');
    const noLogsDiv = document.getElementById('noRiskLogs');

    if (!isAutoRefresh) {
        loadingDiv.style.display = 'block';
        logContainer.style.display = 'none';
        noLogsDiv.style.display = 'none';
    }"""

content = content.replace(old_loading_logic, new_loading_logic)

# 3. Update loadingDiv hidden state in loadRiskControlLogs
old_loading_hide = """        const data = await response.json();
        loadingDiv.style.display = 'none';

        if (data.success && data.data && data.data.length > 0) {
            displayRiskControlLogs(data.data);
            updateRiskLogInfo(data);
            updateRiskLogPagination(data);
            logContainer.style.display = 'block';
        } else {
            noLogsDiv.style.display = 'block';
            updateRiskLogInfo({ total: 0, data: [] });
        }"""

new_loading_hide = """        const data = await response.json();
        if (!isAutoRefresh) {
            loadingDiv.style.display = 'none';
        }

        if (data.success && data.data && data.data.length > 0) {
            displayRiskControlLogs(data.data);
            updateRiskLogInfo(data);
            updateRiskLogPagination(data);
            logContainer.style.display = 'block';
            noLogsDiv.style.display = 'none';
        } else {
            noLogsDiv.style.display = 'block';
            logContainer.style.display = 'none';
            updateRiskLogInfo({ total: 0, data: [] });
        }"""

content = content.replace(old_loading_hide, new_loading_hide)

# 4. Update the toggleRiskLogAutoRefresh
old_toggle_interval = "riskLogAutoRefreshInterval = setInterval(() => loadRiskControlLogs(currentRiskLogOffset), 5000); // 每5秒刷新"
new_toggle_interval = "riskLogAutoRefreshInterval = setInterval(() => loadRiskControlLogs(currentRiskLogOffset, true), 5000); // 每5秒刷新"

content = content.replace(old_toggle_interval, new_toggle_interval)

# 5. Update showSection
old_show_section = """                    // 恢复自动刷新状态
                    const autoRefreshRiskLogs = document.getElementById('autoRefreshRiskLogs');
                    if (autoRefreshRiskLogs && autoRefreshRiskLogs.checked && !riskLogAutoRefreshInterval) {
                        riskLogAutoRefreshInterval = setInterval(() => loadRiskControlLogs(currentRiskLogOffset), 5000);
                    }"""

new_show_section = """                    // 恢复自动刷新状态
                    const autoRefreshRiskLogs = document.getElementById('autoRefreshRiskLogs');
                    if (autoRefreshRiskLogs && autoRefreshRiskLogs.checked && !riskLogAutoRefreshInterval) {
                        riskLogAutoRefreshInterval = setInterval(() => loadRiskControlLogs(currentRiskLogOffset, true), 5000);
                        const label = document.getElementById('autoRefreshRiskLogLabel');
                        const icon = document.getElementById('autoRefreshRiskLogIcon');
                        if (label) label.classList.add('text-primary', 'fw-bold');
                        if (icon) icon.classList.add('auto-refresh-indicator');
                    }"""

content = content.replace(old_show_section, new_show_section)

# Handle error catch block
old_error_block = """    } catch (error) {
        console.error('加载风控日志失败:', error);
        loadingDiv.style.display = 'none';
        noLogsDiv.style.display = 'block';
        showToast('加载风控日志失败', 'danger');
    }"""
new_error_block = """    } catch (error) {
        console.error('加载风控日志失败:', error);
        if (!isAutoRefresh) {
            loadingDiv.style.display = 'none';
            noLogsDiv.style.display = 'block';
            logContainer.style.display = 'none';
        }
        showToast('加载风控日志失败', 'danger');
    }"""

content = content.replace(old_error_block, new_error_block)

with open("static/js/app.js", "w", encoding="utf-8") as f:
    f.write(content)

print("Modifications written to app.js")
