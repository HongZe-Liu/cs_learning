# Python 五部分精简复习笔记

## 1. Iteration Example：循环与斐波那契数列

斐波那契数列：

```text
索引：0 1 2 3 4 5 6
数值：0 1 1 2 3 5 8
```

```python
def fib(n):
    pred, curr = 1, 0
    k = 0

    while k < n:
        pred, curr = curr, pred + curr
        k += 1

    return curr
```

核心：

- `curr` 保存当前斐波那契数。
- `pred` 保存前一个斐波那契数。
- 每轮循环让两个数向前移动一位。
- `while` 条件为 `True` 时继续，条件为 `False` 时停止。
- `pred, curr = curr, pred + curr` 使用旧值同时完成赋值。

复杂度：时间 `O(n)`，额外空间 `O(1)`。

---

## 2. Control：控制语句与函数调用

`if` 只执行符合条件的分支：

```python
from math import sqrt

def real_sqrt(x):
    if x >= 0:
        return sqrt(x)
    else:
        return 0
```

当 `x < 0` 时，`sqrt(x)` 不会执行。

普通函数调用会先计算全部参数：

```python
def choose(condition, true_value, false_value):
    if condition:
        return true_value
    return false_value

# x = -16 时仍会先计算 sqrt(-16)，因此报错
result = choose(x >= 0, sqrt(x), 0)
```

核心：

> `if` 能跳过未选中的代码；普通函数在开始执行前，会先计算参数。

---

## 3. Control Expressions：短路求值

### `and`

- 左边是假值：返回左边，不计算右边。
- 左边是真值：计算并返回右边。

### `or`

- 左边是真值：返回左边，不计算右边。
- 左边是假值：计算并返回右边。

```python
x = 0

safe1 = (x != 0) and (10 / x > 1)  # False，不报错
safe2 = (x == 0) or (10 / x > 1)   # True，不报错
```

记忆：

> `and` 左假则停，`or` 左真则停。

`and` 和 `or` 返回的可能是原始值，不一定是布尔值：

```python
2 and 3  # 3
0 and 3  # 0
2 or 3   # 2
0 or 3   # 3
```

---

## 4. Higher-Order Functions：函数作为参数

高阶函数可以接收另一个函数作为参数。

```python
def identity(k):
    return k


def cube(k):
    return k ** 3


def double(k):
    return k * 2


def summation(n, term):
    total = 0
    k = 1

    while k <= n:
        total += term(k)
        k += 1

    return total
```

```python
summation(3, identity)  # 1 + 2 + 3 = 6
summation(3, cube)      # 1³ + 2³ + 3³ = 36
summation(3, double)    # 2 + 4 + 6 = 12
```

核心：

- `term` 绑定到传入的函数。
- `term(k)` 调用这个函数。
- 传函数本身时写 `cube`，不是 `cube()`。
- 高阶函数把不变的循环结构与可变化的计算规则分开。

---

## 5. Functions as Return Values：函数作为返回值

函数也可以创建并返回另一个函数：

```python
def make_adder(n):
    def adder(k):
        return k + n

    return adder
```

```python
add_two = make_adder(2)
add_five = make_adder(5)

add_two(3)   # 5
add_five(3)  # 8
```

返回的函数会记住创建它时外层函数中的变量：

- `add_two` 记住 `n = 2`。
- `add_five` 记住 `n = 5`。
- 这种结构称为闭包（closure）。

嵌套调用：

```python
make_adder(1)(2)  # 3
```

执行顺序：

1. `make_adder(1)` 返回一个记住 `n = 1` 的函数。
2. `(2)` 调用这个返回的函数，并令 `k = 2`。
3. 返回 `k + n`，即 `2 + 1 = 3`。

---

## 五句话总复习

1. `while` 在条件为真时重复执行，并持续更新状态。
2. `if` 只执行选中的分支，普通函数调用会先计算全部参数。
3. `and` 左假则停，`or` 左真则停。
4. 高阶函数可以把函数作为参数传入。
5. 闭包是一个能够记住外层变量的返回函数。

## 易错点

- `while` 条件为真时是继续循环，不是停止。
- `10 / 0` 不会得到 `False`，而是产生 `ZeroDivisionError`。
- `False and 右边` 不会计算右边。
- `True or 右边` 不会计算右边。
- `summation(3, cube)` 传入的是函数；`cube(3)` 得到的是数字。
- 不同函数中同名的局部变量互不影响。
- 过程式、函数式和面向对象是不同的编程范式；Python 同时支持它们。

