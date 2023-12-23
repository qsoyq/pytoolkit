# pytoolkit

## installation

### pip

```shell
# 安装默认分支
pip install git+https://github.com/qsoyq/pytoolkit.git

# 安装指定分支
pip install git+https://github.com/qsoyq/pytoolkit.git@develop

# 安装指定 tag
pip install git+https://github.com/qsoyq/pytoolkit.git@v0.1.0
```

### poetry

```toml
[tool.poetry.dependencies]
pytoolkit = { git = "https://github.com/qsoyq/pytoolkit.git", branch = "develop" }
pytoolkit = { git = "https://github.com/qsoyq/pytoolkit.git", tag = "v0.1.0" }
pytoolkit = { git = "https://github.com/qsoyq/pytoolkit.git", rev = "eafdb2b" }
```

## test

performing multi-version Python testing

```shell
make tox
```
