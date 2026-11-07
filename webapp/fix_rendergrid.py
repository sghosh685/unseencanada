import re

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/app.js", "r") as f:
    js = f.read()

old_return = r"""        if \(!items \|\| items\.length === 0\) \{
            container\.parentElement\.style\.display = 'none';
            return 0;
        \}"""

new_return = """        if (!items || items.length === 0) {
            container.parentElement.style.display = 'none';
            return { total: 0, visited: 0 };
        }"""

js = re.sub(old_return, new_return, js)

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/app.js", "w") as f:
    f.write(js)
