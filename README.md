# pytoolkit

## installation

### pip

```shell
# 安装默认分支
pip install git+https://github.com/qsoyq/pytoolkit.git

# 安装指定分支
pip install git+https://github.com/qsoyq/pytoolkit.git@develop

# 安装指定 tag
pip install git+https://github.com/qsoyq/pytoolkit.git@v0.0.8
```

### poetry

```toml
[tool.poetry.dependencies]
pytoolkit = { git = "https://github.com/qsoyq/pytoolkit", branch = "develop" }
pytoolkit = { git = "https://github.com/pytoolkit/pytoolkit.git", tag = "v0.0.8" }
pytoolkit = { git = "https://github.com/ansible/pytoolkit.git", rev = "9abbecb" }
```
