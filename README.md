# 点外卖提醒器

一个在工作日提醒你点外卖、并给出本地菜单推荐的小工具。

## 功能

- 自动判断今天是否是工作日
- 工作日发送系统通知提醒
- 支持本地 `dishes.json` 菜单库
- 每次随机推荐 2 个菜
- 支持创建自定义提醒时间的 Windows 计划任务
- 弹窗始终置顶，且不会自动关闭
- `换一换` 只影响当前会话，不会改写菜单文件

## 文件说明

- `reminder.py`：提醒入口，负责工作日判断、通知和推荐弹窗
- `menu_store.py`：读取 `dishes.json` 并随机抽取菜品
- `menu_window.py`：推荐弹窗和错误提示
- `dishes.json`：本地菜单库示例
- `setup_task.py`：创建 Windows 计划任务
- `remove_task.py`：删除 Windows 计划任务

## 环境要求

- Windows
- Python 3.12+
- `plyer`

## 安装

```bash
pip install -r requirements.txt
```

## 使用

直接运行提醒程序：

```bash
python reminder.py
```

创建计划任务并指定提醒时间：

```bash
python setup_task.py --time 08:30
```

时间格式固定为 `HH:MM`。如果不传 `--time`，默认仍然使用 `11:10`。

删除计划任务：

```bash
python remove_task.py
```

## 菜单维护

直接编辑 `dishes.json`：

```json
{
  "dishes": ["黄焖鸡", "牛肉面", "麻辣烫", "盖浇饭"]
}
```

## 说明

- `dishes.json` 只负责存储菜单，不记录历史排除项
- “换一换”会排除当前窗口已经展示过的菜，只在这一次弹窗会话里生效
- 如果菜单里的菜都已经看过了，弹窗会提示没有更多推荐
