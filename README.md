# Installation for windows

## Install UV

```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## Clone the project

```
git clone https://github.com/Yamiyorunoshura/project-part-B.git
```

## Start the programe

```Go to the project directory
cd ~/project-part-B
```

```Sync the dependencies
uv sync
```

```Or run the program directly
uv run main.py
```
