# Sequences 

## 1. Lists：列表与索引

列表可以包含数字、字符串或其他列表。索引表示相对起点的偏移，从 0 开始。

```python
odds = [1, 3, 5, 7]
len(odds)                  # 4
odds[0]                    # 1
odds[3]                    # 7
odds[odds[3] - odds[2]]     # odds[2] → 5

[2, 7] + [1, 8]            # [2, 7, 1, 8]：拼接
[1, 8] * 2                 # [1, 8, 1, 8]：重复，不是逐项乘二
```

元素选择先求出方括号前的序列，再求出索引，最后取元素。非空列表最后一个非负索引为 `len(s) - 1`；越界不会得到空值，而会报错。

### 你的卡点：嵌套索引的括号

```python
data = [[8, 5], [3, 7]]
row = data[1]              # [3, 7]
number = row[0]            # 3

# 将 row 替换回 data[1]：
number = data[1][0]        # 3
```

每次索引各用一对方括号，开头必须有要操作的对象。

- `data[1][0]`：先取外层，再对结果取内层。
- `data[[1][0]]`：先计算 `[1][0]` 得到 1，实际只执行了 `data[1]`。
- `[1][1]`：对只有一个元素的列表 `[1]` 取索引 1，会越界。
- `data[[3, 7]]`：把列表内容当成索引，不是取出 `[3, 7]` 的写法。

另一个要点是运算所在的位置：

```python
a = [3, 4, 6]
boxes = [[4, 6], [9]]
a[len(boxes)] - 1          # a[2] - 1 → 5：取值后再减
a[len(boxes) - 1]          # a[1] → 4：先算索引
```

## 2. Membership：成员判断

对列表而言，`in` 判断当前层有没有与目标相等的直接元素；不返回索引、不查找连续片段、不自动进入内层。`not in` 是相反的判断。

```python
data = [[2, 5], [7, 2]]
data[0][0]                 # 2：取元素
2 in data                  # False
[2, 5] in data             # True
2 in data[0]               # True
9 not in data[0]           # True

digits = [1, 8, 2, 8]
8 in digits                # True，出现次数不影响判断
"1" in digits              # False，字符串不等于整数 1
[1, 8] in digits           # False，没有这个列表元素
```

**个人记录：**综合题中，你曾回答位置，后来说明以为题目在问下标，并正确更正为 `False / True`。这是题意理解偏差，不据此认定你不懂成员判断。做题时先辨别是在“取值”还是“判断存在”。

## 3. For Statements：遍历与解包

`for x in s` 依次将 `x` 绑定到序列中的元素，然后执行循环体，不需要手动更新索引。普通 `for` 不创建新的环境帧；函数内的循环名称绑定在该函数调用的局部帧中。

```python
def count(s, value):
    total = 0
    for x in s:
        if x == value:
            total += 1
    return total


def count_equal(pairs):
    total = 0
    for x, y in pairs:
        if x == y:
            total += 1
    return total
```

`for x, y in pairs` 每轮取出一组，再解包给两个名称；这里每组必须恰好包含两个元素。对整数计数，`total += 1` 相当于 `total = total + 1`。

### 你的卡点：题目条件、缩进与空列表

- 示例返回 `2` 表示符合条件的组数，不代表要寻找数字 2。
- `for` 和 `if` 行末需要冒号。条件成立才执行的更新必须缩进到 `if` 内。
- `return total` 放在循环外，才能处理完所有元素。
- 空列表只让循环体执行零次，不跳过初始化和循环后的返回。

```python
def check(items):
    total = 10
    for x in items:
        total += x
    return total

check([])                  # 10，不是 None
count([], 4)               # 0
```

函数执行到末尾而没有执行带值的 `return`，或执行单独的 `return`，才返回 `None`。

## 4. Ranges：连续整数范围

本讲讨论默认每次增加 1 的形式：`range(start, stop)` 包含起点，不包含终点；`range(stop)` 默认从 0 开始。`range` 是序列，但不是列表。

```python
r = range(-2, 2)
list(r)                    # [-2, -1, 0, 1]
len(r)                     # 4
r[3]                       # 1
list(range(4))             # [0, 1, 2, 3]
list(range(5, 2))          # []
```

默认步长下，长度为 `max(0, stop - start)`。有效非负索引对应的值为 `start + index`。`list(r)` 创建列表，不改变 `r` 的类型。

```python
def sum_through(n):
    """返回 0 到 n 的和；n 是非负整数。"""
    total = 0
    for s in range(n + 1):
        total += s
    return total


def cheer():
    for _ in range(3):
        print("Go Bears!")
```

**个人易错点：**`total += n` 每轮加固定参数；`total += s` 才累加当前元素。`sum_through(0)` 执行一次循环，加上 0，返回 0。

`_` 是合法名称，表示不打算使用它的值，不是可以留空的语法。`for x in range(4, 7)` 中的 `x` 依次是 4、5、6。

讲稿 `sum_below(5)` 的加数转写有误，正确为 `0 + 1 + 2 + 3 + 4 = 10`。

## 5. List Comprehensions：筛选与转换

```python
[结果表达式 for x in 序列 if 条件]
```

实际执行：取出一个 x → 检查条件 → 条件成立才计算结果表达式 → 放入新列表。

### 你的关键疑问：“既然先判断，能不能把计算写在后面？”

你的执行思路正确，但 Python 规定结果表达式写在最前面。**书写顺序不等于执行顺序。**不能用 `if 条件: 计算`，也不能用 `and` 表示“然后进行转换”。

```python
numbers = [1, 2, 3, 4]
a = [x + 1 for x in numbers if x % 2 == 0]
# 原始 x 为 2、4，最终结果为 [3, 5]

b = [x + 1 for x in numbers if (x + 1) % 2 == 0]
# 原始 x 为 1、3，最终结果为 [2, 4]
```

筛选通过的原始值，不一定是最终放进列表的值。

你在综合练习中独立写对的两种实现：

```python
def odd_squares_loop(n):
    result = []
    for x in range(1, n + 1):
        if x % 2 != 0:
            result += [x ** 2]
    return result


def odd_squares(n):
    return [x ** 2 for x in range(1, n + 1) if x % 2 != 0]
```

`x * 2` 是乘二；`x ** 2` 是平方。`n % x == 0` 表示 x 整除 n，不是 `n / x == 0`。

讲稿的因数函数还原如下（n 为正整数）：

```python
def divisors(n):
    return [1] + [x for x in range(2, n) if n % x == 0]
```

`divisors(12)` 返回 `[1, 2, 3, 4, 6]`。此实现对 n > 1 不包含 n 本身，并非全部正因数；n = 1 特殊返回 `[1]`。

## 6. Lists and Recursion：拆分列表与组合返回值

### 切片与递归求和

```python
s = [2, 4, 1]
s[0]                       # 2
s[1:]                      # [4, 1]，原来的 s 不变


def sum_list(s):
    if len(s) == 0:
        return 0
    return s[0] + sum_list(s[1:])
```

你的“拆整数”类比可以这样对应：

| 作用 | 拆整数 | 拆列表 |
|---|---|---|
| 取出一个部分 | `n % 10` | `s[0]` |
| 得到其余部分 | `n // 10` | `s[1:]` |

得到剩余部分的是 `s[1:]`，不是 `s[0]`。每次递归收到更短的列表，最终到达空列表。

```text
sum_list([2, 4]) 等待 2 + sum_list([4])
sum_list([4])    等待 4 + sum_list([])
sum_list([])    返回 0
回到上一层：4 + 0 → 返回 4
回到最外层：2 + 4 → 返回 6
```

每层有自己的 s。返回后继续完成等待中的表达式，不是从头重新执行整个函数。

### large：选与不选的树递归

输入正数列表 s 和非负额度 n，返回保持原顺序的一个选择列表，使总和不超过 n 且尽可能大。可以跳过元素，不要求连续，每个位置最多选择一次。

```python
def large(s, n):
    if len(s) == 0:
        return []

    first = s[0]
    rest = s[1:]

    if first > n:
        return large(rest, n)

    with_first = [first] + large(rest, n - first)
    without_first = large(rest, n)

    if sum_list(with_first) > sum_list(without_first):
        return with_first
    else:
        return without_first
```

- 选 first：已用掉 first 的额度，递归上限减为 n - first，并拼上 `[first]`。
- 不选 first：额度不变，不拼 first。
- first 超额：只能跳过。正数条件保证加入其他元素不会把超额的总和降下来。
- 空列表：返回 `[]`。
- 总和相等：这份代码选 without_first。

返回值始终是列表；用 sum_list 才得到用于比较的数字。这是教学实现，不是效率优化版本。

### 你的核心困惑：空列表也要逐层返回，为什么没有把数字都加回来？

以 `large([5, 3, 4], 7)` 的“选 5”分支为例：

```text
最外层等待：[5] + large([3, 4], 2)

large([3, 4], 2)：3 超额，return large([4], 2)
large([4], 2)：4 超额，return large([], 2)
large([], 2)：返回 []

向上返回：
处理 [4] 的层收到 []，原样返回 []
处理 [3, 4] 的层收到 []，原样返回 []
最外层完成 [5] + []，得到 [5]
```

空列表没有跳过中间层。中间层没有拼接操作，所以结果不变。递归参数是候选列表，不意味着它会原样返回。

对比两种代码：

```python
# 收到递归结果，直接返回给上一层：
return large(rest, n)

# 收到递归结果后拼接，并赋值；当前函数尚未返回：
with_first = [first] + large(rest, n - first)
```

两者都包含递归调用。后一种还要计算另一分支、比较方案，再执行 return。

同一例子的“不选 5”分支：

```text
large([3, 4], 7)
  选 3 的候选：[3] + large([4], 4) → [3] + [4] → [3, 4]
  不选 3 的候选：large([4], 7) → [4]
  比较后返回 [3, 4]

最外层比较 [5] 与 [3, 4]，返回 [3, 4]。
不会再拼 5，因为这个结果来自“不选 5”的分支。
```

你提出的“两条大路继续分小路”符合树递归结构，但不是每层都分两路：空列表停止，超额时只有跳过的一路。

### 你独立完成的递归练习

```python
def count_above(s, limit):
    if len(s) == 0:
        return 0
    if s[0] > limit:
        return 1 + count_above(s[1:], limit)
    else:
        return count_above(s[1:], limit)
```

你正确解释了：遇到不符合条件的元素不能直接返回 0，因为后面可能还有满足条件的元素。

## 7. 当前学习状态：依据实际表现

| 内容 | 本次表现 | 后续重点 |
|---|---|---|
| 列表与索引 | 多次提示后写对连续索引；综合题独立取出 7 | 较长表达式中保持括号结构准确 |
| 成员判断 | 小节判断题独立正确；综合题曾误读为问下标，澄清后正确 | 先区分取值与布尔判断 |
| for 与解包 | 初期需框架、冒号和缩进提示；综合循环独立正确 | 换任务继续检验完整函数书写 |
| range | 边界选择正确；曾混淆参数 n 与当前元素 | 注意空范围与包含终点 |
| 推导式 | 经讲解理解书写/执行顺序；迁移题及综合题独立正确 | 不把原始 x 当作最终结果 |
| 列表递归 | 独立完成递归计数；正确推演 large 的分支与平局 | large 的独立实现尚未检验 |

结论：六节核心思路已经比较理解，多项有独立应用证据；不据此认定所有复杂题都已掌握。递归的选择分支仍值得隔一段时间再练。

## 8. 自测题（先做题，再看答案）

### 题目

1. 给定 `a = [[1, 6], [4]]`，求 `6 in a`、`[4] in a`，并写出取 6 的表达式。
2. 写列表推导式，取 1 到 8（含 8）中所有偶数，并将每个数减 1。
3. 写函数 `product_list(s)`，递归计算数字列表的乘积，规定空列表乘积为 1。
4. 使用本笔记的 large，求 `large([4, 3, 2], 5)` 最外层两种候选及最终返回值。

### 答案与解释

1. 分别为 `False`、`True`；取值为 `a[0][1]`。成员判断只检查当前层。

2. 筛选原始 x，再计算 x - 1：

```python
[x - 1 for x in range(1, 9) if x % 2 == 0]
# [1, 3, 5, 7]
```

3. 空列表的 1 不改变乘积：

```python
def product_list(s):
    if len(s) == 0:
        return 1
    return s[0] * product_list(s[1:])
```

4. 选 4：`[4] + large([3, 2], 1)` 得到 `[4]`；不选 4：`large([3, 2], 5)` 得到 `[3, 2]`。最终返回 `[3, 2]`。

## 下次学习如何开始

先用一道未做过的简短新题复习本讲，优先检查递归返回或连续索引；根据结果局部补缺，不默认全部重学。自测答案已读过的题不作为新的独立掌握证据。
