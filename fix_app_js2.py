with open("static/js/app.js", "r", encoding="utf-8") as f:
    content = f.read()

# Fix loading hide
old_hide = """    try {
        const response = await fetch(url, {
            headers: {
                'Authorization': `Bearer ${token}`
            },
            cache: 'no-store'
        });

        const data = await response.json();
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

new_hide = """    try {
        const response = await fetch(url, {
            headers: {
                'Authorization': `Bearer ${token}`
            },
            cache: 'no-store'
        });

        const data = await response.json();
        if (!isAutoRefresh) {
            loadingDiv.style.display = 'none';
        }

        if (data.success && data.data && data.data.length > 0) {
            displayRiskControlLogs(data.data);
            updateRiskLogInfo(data);
            updateRiskLogPagination(data);
            if (!isAutoRefresh) {
                logContainer.style.display = 'block';
            }
        } else {
            if (!isAutoRefresh) {
                noLogsDiv.style.display = 'block';
            }
            updateRiskLogInfo({ total: 0, data: [] });
        }"""

content = content.replace(old_hide, new_hide)

with open("static/js/app.js", "w", encoding="utf-8") as f:
    f.write(content)
