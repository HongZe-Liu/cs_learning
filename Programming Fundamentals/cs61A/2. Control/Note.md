# Control 
## 1. Functions & Environments

```python
def square(x):
    return x * x
```

- `def`：创建函数，并把函数绑定到当前帧中的名称；**不会执行函数体**。
- 调用函数：计算 operator/operand → 创建局部帧 → 绑定参数 → 执行函数体 → 返回结果。
- 每次调用都会创建一个新的局部帧；同一函数可产生多个帧。
- environment（环境）是有顺序的 frames（帧）。
- 名称查找：从当前环境的第一个帧开始，沿父帧向外查找，找到即停止。

```python
square(square(3))  # 3 → 9 → 81；两次调用，两个局部帧
```

> 函数决定执行什么；帧保存一次调用的绑定；环境决定名称的含义。

## 2. Conditional Statements

```python
if condition_1:
    suite_1
elif condition_2:
    suite_2
else:
    suite_3
```

- clause（子句）= header（头部）+ suite（缩进语句组）。
- 按顺序检查条件；执行第一个真值对应的 suite，然后跳过其余子句。
- `elif`：零个或多个；`else`：零个或一个，且必须在最后。
- 常见假值：`False`、`0`、`""`、`None`。
- `"0"` 是非空字符串，因此是真值。

## 3. Iteration

```python
i = 0
total = 0

while i < 3:
    i = i + 1
    total = total + i
```

执行顺序：

1. 检查 header 条件。
2. 真：按顺序执行**完整的 suite**，再回到第 1 步。
3. 假：结束循环。

```text
(i, total): (0, 0) → (1, 1) → (2, 3) → (3, 6)
```

- suite 中变量改变后，不会立刻重新检查条件；必须先执行完整轮次。
- `if` 和 `while` 不会自动创建新帧。
- `i = i + 1`：先用旧 `i` 计算右侧，再把结果重新绑定给 `i`。

## 执行代码检查表

1. 当前在哪个环境/帧？
2. 表达式或条件的值是什么？
3. 应执行哪个分支或是否进入下一轮？
4. 哪些名称被重新绑定？
5. 是否遇到 `return`？

## 易错点

- 定义函数 ≠ 调用函数。
- 调用函数会创建帧；不是“调用帧”。
- `"0"` 为真，`0` 为假。
- `if` 最多选择一个分支；`while` 可以执行多轮。
- `while` 每轮执行完整 suite 后才重新检查条件。
