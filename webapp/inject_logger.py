import re

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/index.html", "r") as f:
    content = f.read()

logger_script = """
<script>
window.onerror = function(message, source, lineno, colno, error) {
    fetch('/log_error?msg=' + encodeURIComponent(message + ' at ' + lineno + ':' + colno + ' ' + (error && error.stack)));
};
window.addEventListener('unhandledrejection', function(event) {
    fetch('/log_error?msg=' + encodeURIComponent(event.reason));
});
</script>
</head>
"""

content = content.replace("</head>", logger_script)

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/index.html", "w") as f:
    f.write(content)
