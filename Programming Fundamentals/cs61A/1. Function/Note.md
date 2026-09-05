# CS61A Lecture 1 — Review Notes

> 目标：快速恢复概念，不重复课堂讲解。  
> 复习时优先看 **Core Rules + Examples**。

---

# 1. Assignment and Names

## Core Rules

- Python 中 **name 会绑定到 value**。
- Assignment：**先 evaluate 右边，再 bind 左边**。
- Reassignment：让 name 重新绑定到新的 value。
- 一个 function 也是 value，因此可以被多个 names 绑定。
- 普通 assignment 保存的是**当时计算出的 value**，不会记住公式。

```python
radius = 10
area = 3.14 * radius * radius

radius = 20
```

此时：

```text
radius -> 20
area   -> 314.0
```

如果要更新 `area`，必须重新计算：

```python
area = 3.14 * radius * radius
```

## Multiple Assignment

```python
a = 1
b = 2

b, a = a + b, b
```

先计算右边：

```text
a + b -> 3
b     -> 2
```

再绑定：

```text
b -> 3
a -> 2
```

### Key Rule

> **Evaluate right, then bind left.**

---

# 2. Name Binding Example

```python
f = min
f = max
g, h = min, max
max = g
```

最终：

```text
f   -> max function
g   -> min function
h   -> max function
max -> min function
```

所以：

```python
max(f(2, g(h(1, 5), 3)), 4)
```

等价于：

```python
min(max(2, min(max(1, 5), 3)), 4)
```

最终结果：

```text
3
```

### Key Idea

```python
max = g
```

不是让 `max` 永远跟着 `g`。

而是：

> 把 `max` 绑定到 **g 当时绑定的 value**。

---

# 3. Environment and Frame

## Environment

Environment 用来记录：

```text
name -> value
```

之间的 binding。

更准确地说：

> **Environment 是有顺序的一系列 frames。**

例如 function call 时：

```text
Local Frame
    ↓
Global Frame
```

## Frame

Frame 保存一组 name-value bindings。

在同一个 frame 中：

> **一个 name 同一时刻最多绑定一个 value。**

但：

> **同一个 value 可以被多个 names 绑定。**

例如：

```python
f = max
h = max
```

```text
f --\
     -> max function
h --/
```

---

# 4. Defining Functions

基本语法：

```python
def square(x):
    return x * x
```

结构：

```text
def             -> 定义函数
square          -> function name
x               -> formal parameter
return x * x    -> function body
```

```python
def square(x):
```

叫做 **function signature**。

---

# 5. What `def` Does

执行：

```python
def square(x):
    return x * x
```

Python 会：

1. 创建一个 function
2. 保存 function signature
3. 保存 function body
4. 把 function name 绑定到这个 function

```text
square -> square function
```

重要：

> **执行 `def` 时不会执行 function body。**

函数体只会在 function 被调用时执行。

### Key Rule

> **Define now, execute when called.**

---

# 6. Function Call

调用：

```python
square(-2)
```

Python 会：

1. 创建一个新的 local frame
2. 把 formal parameter 绑定到 argument value
3. 在新的 environment 中执行 function body

```text
x -> -2
```

然后：

```python
return x * x
```

得到：

```text
4
```

---

# 7. Formal Parameter vs Argument

定义：

```python
def square(x):
```

```text
x -> formal parameter
```

调用：

```python
square(-2)
```

```text
-2 -> argument value
```

调用时：

```text
x -> -2
```

---

# 8. Name Lookup

Python 查找 name 时：

```text
Local Frame
    ↓
找不到
    ↓
Global Frame
```

找到以后就停止。

例如：

```python
from operator import mul

def square(x):
    return mul(x, x)
```

调用：

```python
square(-2)
```

查找 `x`：

```text
Local Frame
x -> -2
```

查找 `mul`：

```text
Local Frame -> 没有
Global Frame -> mul function
```

---

# 9. Same Name in Different Frames

```python
def square(square):
    return square * square
```

调用：

```python
square(-2)
```

此时：

```text
Global Frame:
square -> square function

Local Frame:
square -> -2
```

函数体中的：

```python
square * square
```

先在 local frame 找到：

```text
square -> -2
```

因此结果：

```text
4
```

### Key Rule

> **Name lookup: local first, then global.**

---

# 10. Expression Evaluation vs `print`

在 REPL 中：

```python
>>> -2
-2
```

这是：

```text
expression
-> evaluate
-> value
-> REPL 自动显示
```

而：

```python
>>> print(-2)
-2
```

显示 `-2` 是 `print` 的 **side effect**。

所以：

> **Evaluate expression 和 print 不是一回事。**

---

# 11. `None`

`None` 是一个特殊 value。

如果 function 没有显式 return value：

```python
def does_not_square(x):
    x * x
```

调用：

```python
does_not_square(4)
```

实际返回：

```text
None
```

而不是 `16`。

### Key Rule

> **计算出一个值，不等于 return 这个值。**

---

# 12. `print()` and Side Effect

```python
x = print(1)
```

发生：

```text
side effect -> 显示 1
return value -> None
```

所以：

```text
x -> None
```

因此：

```python
print(x)
```

会显示：

```text
None
```

---

# 13. Pure vs Non-pure Function

## Pure Function

主要通过：

```text
arguments
-> function
-> return value
```

例如：

```python
abs(-2)   # 2
pow(2, 3) # 8
```

## Non-pure Function

除了 return value，还会产生 side effect。

例如：

```python
print(-2)
```

```text
side effect -> 显示 -2
return value -> None
```

### Key Rule

> **Function 显示了什么，和 function 返回了什么，是两件不同的事情。**

---

# 14. Nested `print`

```python
print(print(1), print(2))
```

从内部开始：

```python
print(1)
```

```text
显示 1
return None
```

```python
print(2)
```

```text
显示 2
return None
```

所以外层变成：

```python
print(None, None)
```

最终显示：

```text
1
2
None None
```

---

# 15. Operators

可以先把常见运算符理解成 built-in function call 的简写。

```python
from operator import add, mul
```

例如：

```python
2 + 3 * 4 + 5
```

可以理解为类似：

```python
add(add(2, mul(3, 4)), 5)
```

注意 precedence：

```text
* 高于 +
```

括号可以改变默认优先级。

---

# 16. Division

```python
2013 / 10
# 201.3
```

```text
/ -> true division
```

```python
2013 // 10
# 201
```

```text
// -> floor division
```

```python
2013 % 10
# 3
```

```text
% -> remainder / mod
```

---

# 17. Returning Multiple Values

```python
def divide_exact(n, d):
    return n // d, n % d
```

调用：

```python
q, r = divide_exact(2013, 10)
```

得到：

```text
q -> 201
r -> 3
```

---

# 18. Python File vs REPL

REPL：

```python
>>> 2 + 3
5
```

`.py` 文件：

```python
2 + 3
```

不会自动显示结果。

需要：

```python
print(2 + 3)
```

执行文件：

```bash
python3 file.py
```

执行文件后进入交互模式：

```bash
python3 -i file.py
```

---

# 19. Docstring and Doctest

## Docstring

```python
def divide_exact(n, d):
    """Return the quotient and remainder of dividing N by D."""
    return n // d, n % d
```

Docstring 用来说明 function 的用途。

## Doctest

```python
def divide_exact(n, d):
    """
    >>> q, r = divide_exact(2013, 10)
    >>> q
    201
    >>> r
    3
    """
    return n // d, n % d
```

运行：

```bash
python3 -m doctest file.py
```

详细模式：

```bash
python3 -m doctest -v file.py
```

---

# 20. Default Argument

```python
def divide_exact(n, d=10):
    return n // d, n % d
```

调用：

```python
divide_exact(2013)
```

等价于：

```python
divide_exact(2013, 10)
```

注意：

```python
d=10
```

这里表示 parameter 的 **default value**，不是普通 assignment statement。

---

# Final Review

## Five Most Important Rules

1. **Names are bound to values.**
2. **Evaluate right, then bind left.**
3. **Define now, execute when called.**
4. **Name lookup: local first, then global.**
5. **Display and return are different.**

## Quick Mental Model

```text
Assignment
-> evaluate expression
-> bind value to name
```

```text
def
-> create function
-> save body
-> bind function to name
```

```text
function call
-> create local frame
-> bind arguments to parameters
-> execute body
-> return value
```

```text
name lookup
-> local
-> global
```

```text
print
-> side effect: display
-> return: None
```
