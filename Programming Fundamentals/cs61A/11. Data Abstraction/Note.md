# CS61A Lecture Review：Data Abstraction

## 1. 核心知识

### 1.1 什么是 Data Abstraction？

Data abstraction 把程序分成两部分：

- **数据如何实现**：constructor 和 selectors 负责底层 representation。
- **数据如何使用**：上层函数只通过 constructor 和 selectors 操作数据。

以有理数为例，上层只需要知道：

```python
rational(n, d)  # 创建有理数 n/d
numer(x)        # 取得分子
denom(x)        # 取得分母
```

它不应该知道底层数据究竟是 list、tuple，还是 function/closure。

### 1.2 Constructor、Selector 与 ADT

- `rational` 是 **constructor**：构造抽象数据。
- `numer`、`denom` 是 **selectors**：取出抽象数据的组成部分。
- 三者共同提供一个有理数 **ADT（Abstract Data Type）** 的接口。

抽象的价值是降低 **coupling（耦合）**：底层 representation 改变时，上层运算代码不需要跟着改变。

## 2. 完整关键代码

### 2.1 List representation

```python
def rational(n, d):
    return [n, d]


def numer(x):
    return x[0]


def denom(x):
    return x[1]
```

这里 `[n, d]` 是底层实现细节。只有 constructor 和 selectors 应该直接使用下标。

### 2.2 Function/closure representation

```python
def rational(n, d):
    def select(name):
        if name == 'n':
            return n
        elif name == 'd':
            return d
    return select


def numer(x):
    return x('n')


def denom(x):
    return x('d')
```

`rational(n, d)` 返回内部函数 `select`。`select` 保留了它定义时的 parent environment，因此之后仍能找到 `n` 和 `d`；这就是 **closure（闭包）**。

### 2.3 两种 representation 的关系

这两种实现都属于底层 representation：

```text
List version      → 用 [n, d] 保存数据
Closure version   → 用 select 和它的 parent frame 保存数据
```

function/closure representation 并不是比 list 多出来的一层抽象。两者只是同一个 ADT 的不同实现。

## 3. Behavior condition

一种 representation 是否正确，不取决于它“长什么样”，而取决于 constructor 和 selectors 是否满足约定的行为：

```python
numer(rational(n, d)) == n
denom(rational(n, d)) == d
```

这就是本例的 **behavior condition（行为条件）**。

只要满足这个条件，上层代码就可以把两种 representation 当作同一种有理数 ADT 使用。例如：

```python
x = rational(3, 5)

numer(x)  # 3
denom(x)  # 5
```

上层程序无须知道 `x` 是 list 还是 function。

## 4. Abstraction barrier 的层级

```text
使用有理数的程序
    add_rational / sub_rational / mul_rational / div_rational
                         ↓
ADT 接口
                 rational / numer / denom
                         ↓
底层 representation
                    list 或 closure
```

每层只依赖下一层公开的接口。

正确：

```python
def mul_rational(x, y):
    return rational(
        numer(x) * numer(y),
        denom(x) * denom(y)
    )
```

违反 abstraction barrier：

```python
def mul_rational(x, y):
    return [x[0] * y[0], x[1] * y[1]]
```

错误版本直接依赖 list、下标 `0` 和下标 `1`。一旦底层改成 closure，它就不能工作。不要为了修补它再建立另一套上层“数据层”；应直接让它使用已有的 `rational`、`numer` 和 `denom` 接口。

## 5. Rational arithmetic

设：

```text
x = a/b
y = c/d
```

### 5.1 加法

```text
a/b + c/d = (a·d + c·b) / (b·d)
```

```python
def add_rational(x, y):
    return rational(
        numer(x) * denom(y) + numer(y) * denom(x),
        denom(x) * denom(y)
    )
```

### 5.2 减法

```text
a/b - c/d = (a·d - c·b) / (b·d)
```

```python
def sub_rational(x, y):
    return rational(
        numer(x) * denom(y) - numer(y) * denom(x),
        denom(x) * denom(y)
    )
```

**个人易错点：**之前 `sub_rational` 的分母公式写错。加法和减法的共同分母都是 `denom(x) * denom(y)`。

### 5.3 乘法

```text
a/b × c/d = (a·c) / (b·d)
```

```python
def mul_rational(x, y):
    return rational(
        numer(x) * numer(y),
        denom(x) * denom(y)
    )
```

### 5.4 除法

```text
(a/b) ÷ (c/d) = (a·d) / (b·c)
```

```python
def div_rational(x, y):
    return rational(
        numer(x) * denom(y),
        denom(x) * numer(y)
    )
```

这些函数全部通过 ADT 接口工作，因此换成 list 或 closure representation 都不需要修改。

## 6. 关键 environment / closure 推演

使用 closure representation：

```python
def rational(n, d):
    def select(name):
        if name == 'n':
            return n
        elif name == 'd':
            return d
    return select


def numer(x):
    return x('n')


r = rational(8, 13)
result = numer(r)
```

### 6.1 执行 `r = rational(8, 13)`

1. 调用 `rational(8, 13)`，创建一个调用 frame：

   ```text
   n = 8
   d = 13
   ```

2. 执行 `def select(name)`，创建函数 `select`。它的 parent 是这次 `rational` 调用的 frame。
3. `return select` 返回函数本身，没有调用它。
4. 全局名字 `r` 指向这个 `select` closure。

```text
Global frame
    r ───────────────→ select function
                           │
                           │ parent
                           ↓
                    rational frame
                       n = 8
                       d = 13
```

### 6.2 执行 `result = numer(r)`

1. 先计算参数 `r`，得到它指向的 `select`。
2. 调用 `numer`，所以 `numer` frame 中：

   ```text
   x → select
   ```

   `x` 不是字符串 `'n'`，也不是数字 `8`。

3. 执行：

   ```python
   return x('n')
   ```

   因为 `x` 指向 `select`，所以它等价于：

   ```python
   return select('n')
   ```

4. 调用 `select('n')` 时，新 frame 中：

   ```text
   name = 'n'
   ```

5. 条件 `name == 'n'` 为真，于是执行 `return n`。
6. 当前 `select` frame 没有局部变量 `n`，Python 沿 parent environment 找到 `rational` frame 中的 `n = 8`。
7. `select` 返回 `8`，`numer` 也返回 `8`，最终：

   ```text
   result = 8
   r 仍然指向 select
   ```

完整调用链：

```text
numer(r)
→ numer(select)
→ x 指向 select
→ x('n')
→ select('n')
→ name = 'n'
→ 从 parent frame 找到 n = 8
→ select 返回 8
→ numer 返回 8
→ result = 8
```

调用 `select` 没有改变 `r` 的绑定，也没有把 `r` 改成 `result`。

## 7. 个人易错点

### 7.1 `name = 'n'` 与 `n = 8` 不是一回事

```text
name = 'n'  → select 本次调用收到的字符串参数
n = 8       → rational 的 parent frame 中保存的变量
```

`name` 决定要选分子还是分母；`n` 保存真正的分子值。

### 7.2 `numer` 中的 `x` 指向 `select`

调用 `numer(r)` 时，实参 `r` 的值是 `select` closure，因此形参 `x` 也指向同一个 closure：

```text
r → select
x → select
```

参数传递不会自动调用函数，也不会让 `x` 指向字符串 `'n'`。

### 7.3 `numer` 返回调用结果，不是函数本身

```python
def numer(x):
    return x('n')
```

- `x` 是函数。
- `x('n')` 会调用这个函数。
- `numer` 返回该调用的结果，本例为数字 `8`。

对比：

```python
return x       # 返回函数本身
return x('n')  # 调用函数，返回调用结果
```

因此，“`numer` 接受一个函数”在当前 representation 下是对的，但“`numer` 返回这个函数并加入参数”不对。更准确地说：**`numer` 调用传入的函数，并返回调用结果。**

另外，`numer` 的接口意义是接收“有理数抽象数据”；只是 closure representation 恰好用函数表示这个数据。按“接收或返回函数”的定义，它在这个实现中技术上也可算 higher-order function，但这里更重要的角色是 **selector**。

### 7.4 不要把样例中的数字带到新题

若代码是 `rational(8, 13)`，则 parent frame 中 `n = 8`，结果是 `8`，不是之前例题里的 `5` 或 `6`。每次都从当前调用的实际参数重新绑定。

## 8. 当前掌握情况

### 已独立掌握

- Data abstraction 的目的
- constructor 与 selectors 的职责
- abstraction barrier 的基本原则
- 上层代码不应直接依赖 representation
- list 与 function/closure 都可以表示同一种 ADT
- 用 behavior condition 判断 representation 是否正确
- 使用 `rational`、`numer`、`denom` 实现运算
- `mul_rational` 与 `div_rational` 的公式和代码
- `r` 在 selector 调用后仍指向原来的 closure

### 仍需巩固

- 严格区分 `name = 'n'` 与 parent frame 中的 `n = 8`
- 稳定判断参数绑定：调用 `numer(r)` 后，`x → select`
- 区分返回函数本身 `return x` 与返回函数调用结果 `return x('n')`
- 按当前题目的实际参数推演，避免沿用上一题中的数字
- 记牢 `sub_rational` 的分母是两个分母的乘积
- 更准确地理解：closure representation 是一种底层实现，并不是新的 abstraction layer

## 9. 少量自测题

先独立作答，再查看答案。

### 题 1：Behavior condition

补全下面两个条件：

```python
numer(rational(n, d)) == ___
denom(rational(n, d)) == ___
```

### 题 2：执行过程

使用 closure representation：

```python
q = rational(4, 9)
answer = denom(q)
```

回答：

1. `q` 指向什么？
2. `denom` 中的 `x` 指向什么？
3. 调用 `select` 时，`name` 等于什么？
4. `select` 去哪个 frame 找到要返回的值？
5. `answer` 最终是多少？`q` 是否改变？

### 题 3：检查 abstraction barrier

下面的代码有什么问题？

```python
def double_rational(x):
    return [x[0] * 2, x[1]]
```

请改写成不依赖底层 representation 的版本。

### 题 4：实现减法

只使用 `rational`、`numer` 和 `denom`，实现 `sub_rational(x, y)`。

### 题 5：函数本身还是调用结果？

若 `x` 指向 `select`，分别说明下面两行返回什么：

```python
return x
return x('n')
```

## 10. 自测答案

### 答案 1

```python
numer(rational(n, d)) == n
denom(rational(n, d)) == d
```

### 答案 2

1. `q` 指向 `select` closure。
2. `x` 指向同一个 `select` closure。
3. `name = 'd'`。
4. 从 `select` 的 parent，也就是 `rational(4, 9)` 的调用 frame 中找到 `d = 9`。
5. `answer = 9`；`q` 不变，仍指向 `select`。

### 答案 3

它直接使用 list 和下标，违反 abstraction barrier。应改为：

```python
def double_rational(x):
    return rational(numer(x) * 2, denom(x))
```

### 答案 4

```python
def sub_rational(x, y):
    return rational(
        numer(x) * denom(y) - numer(y) * denom(x),
        denom(x) * denom(y)
    )
```

### 答案 5

```python
return x       # 返回 select 函数本身
return x('n')  # 调用 select，并返回分子的值
```

## 一句话总结

**上层代码依赖 constructor、selectors 和 behavior condition，不依赖底层 representation；读 closure 代码时，始终分清“函数本身”“函数调用”“当前调用的参数”和“parent frame 中保存的变量”。**
