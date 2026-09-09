# Python Lecture 复习笔记：Lambda、Return、抽象与错误

本 lecture 共 4 个部分：

1. Lambda Expressions and Environment Diagrams
2. Return、Search and Inverse Functions
3. Functional Abstraction and Naming
4. Errors and Tracebacks

---

## 第一部分：Lambda 与环境图

### 1. Lambda 表达式创建函数对象

```python
add_one = lambda x: x + 1
```

执行 lambda 表达式时：

- 创建一个函数对象；
- 确定这个函数的 parent；
- 不执行函数体；
- 不创建这个函数的调用帧；
- 此时参数 `x` 还没有绑定具体值。

只有调用函数时才会创建调用帧：

```python
result = add_one(5)
```

这时才会：

1. 创建调用帧；
2. 绑定 `x = 5`；
3. 执行 `x + 1`；
4. 返回 `6`。

记忆：

> 函数创建时确定 parent；函数调用时创建调用帧、绑定参数并执行函数体。

### 2. Parent 由创建环境决定

```python
a = 1

def f(g):
    a = 2
    return lambda y: a * g(y)

result = f(lambda y: a + y)(a)
```

给两个 lambda 起临时名字：

```text
L1 = lambda y: a + y
L2 = lambda y: a * g(y)
```

- L1 在 Global 中创建，所以 parent 是 Global。
- L2 在调用 `f` 产生的 f1 帧中创建，所以 parent 是 f1。
- 把 L1 传给 `f` 并绑定到名字 `g`，不会改变 L1 的 parent。
- 函数在哪里被调用，也不会改变它的 parent。

执行过程：

```text
全局 a = 1

调用 f(L1)
→ 创建 f1
→ g = L1
→ 局部 a = 2
→ 创建并返回 L2，L2 的 parent = f1

调用 L2(a)
→ 最外面的 a 在 Global 中求值，所以实参是 1
→ L2 的 y = 1
→ L2 中的 a 沿 parent 在 f1 找到 2
→ L2 中的 g 沿 parent 在 f1 找到 L1

调用 g(1)，也就是 L1(1)
→ L1 的 parent 是 Global
→ L1 中的 a 是全局 a = 1
→ g(1) = 1 + 1 = 2

最终：2 * 2 = 4
```

### 3. Parent 不是变量值的快照

函数记住的是父环境，不是创建时每个变量的固定值：

```python
a = 1

def f(g):
    a = 2
    return lambda y: a * g(y)

h = f(lambda y: a + y)
a = 10
result = h(a)
```

计算：

```text
h(a) → h(10)
g(10) → 全局 a + 10 → 10 + 10 = 20
h(10) → f1 中的 a * 20 → 2 * 20 = 40
```

### 4. 易错点

- Lambda 表达式的值是函数对象，不是函数体的计算结果。
- 创建函数时不创建该函数的调用帧。
- Parent 是创建函数时所在的环境帧。
- 调用位置不会改变函数的 parent。
- 函数、函数调用和调用帧是三个不同概念。
- `y` 这样的参数只有在函数被调用时才绑定具体值。

---

## 第二部分：Return、Search 与逆函数

### 1. Return 的作用

`return` 有两个作用：

1. 立即结束当前函数调用；
2. 把返回表达式的值作为整个函数调用的值。

```python
def test():
    print(1)
    return 2
    print(3)

r = test()
```

结果：

```text
打印：1
r = 2
```

执行 `return 2` 后，函数已经结束，因此 `print(3)` 不执行。

### 2. Print 与 Return

```text
print  → 在屏幕上显示内容
return → 结束函数，并决定函数调用的值
```

打印出来的数字不一定等于函数返回的数字。

### 3. Continue、Break 与 Return

```text
continue → 跳过当前一轮剩余代码，进入下一轮循环
break    → 结束当前循环，继续执行循环后面的代码
return   → 结束整个函数，并返回一个值
```

即使 `return` 写在 `if` 和 `while` 里面，它仍然属于包含它的函数。

### 4. While 本身没有返回值

```python
def count():
    x = 0

    while x < 3:
        x += 1

    return x
```

这里：

- `while` 负责重复执行并更新 `x`；
- 条件变为假时，循环停止；
- `return x` 让整个 `count()` 返回 `3`。

如果函数没有执行任何 `return`，执行到函数末尾时会默认返回 `None`。

### 5. Python 的真值与假值

在条件中：

```text
0        → 假
非零数字 → 真，包括负数
None     → 假
```

一个函数可以返回数字；数字放入 `if` 后，Python 才判断它是真值还是假值。

```python
def condition(x):
    return x - 2
```

```text
condition(0) 返回 -2
-2 是非零数字，在 if 中被判断为真
```

### 6. Search 函数

```python
def search(f):
    x = 0

    while True:
        if f(x):
            return x
        x += 1
```

它从 `0` 开始寻找第一个使 `f(x)` 为真值的 `x`。

```python
def condition(x):
    return x * x >= 9

result = search(condition)
```

```text
x = 0 → False
x = 1 → False
x = 2 → False
x = 3 → True
result = 3
```

需要区分两层返回值：

```text
f(x) 的返回值      → 用来判断是否找到
search(f) 的返回值 → 第一个满足条件的 x
```

例如：

```python
def condition(x):
    return x - 2

result = search(condition)
```

第一次检查：

```text
condition(0) = -2
-2 是真值
search 返回当前 x = 0
```

所以 `result = 0`，不是 `-2`。

### 7. 使用 Search 构造逆函数

```python
def search(f):
    x = 0

    while True:
        if f(x):
            return x
        x += 1


def square(x):
    return x * x


def inverse(f):
    return lambda y: search(lambda x: f(x) == y)


sqrt = inverse(square)
result = sqrt(256)
```

变量的作用：

```text
f = square       → 要反向寻找输入的函数
y = 256          → 已知输出，也就是目标值
x = 0, 1, 2...   → search 不断尝试的输入
```

执行过程：

```text
inverse(square)
→ f 绑定到 square
→ 创建并返回外层 lambda
→ sqrt 指向这个函数对象

sqrt(256)
→ y = 256
→ 创建判断函数 lambda x: square(x) == 256
→ search 从 x = 0 开始尝试
→ x = 16 时，16 * 16 == 256 为 True
→ search 返回 16
→ result = 16
```

环境关系：

```text
内部 lambda 调用帧：x = 当前尝试的数字
        ↓ parent
sqrt 调用帧：y = 256
        ↓ parent
inverse 调用帧：f = square
        ↓ parent
Global
```

限制：这个 `search` 只搜索非负整数。如果没有任何非负整数满足条件，`while True` 会一直运行。

---

## 第三部分：函数抽象与命名

### 1. 什么是函数抽象

函数抽象是：

> 给一个计算过程命名，以后把它当作一个整体使用，不必每次关心内部实现。

```python
def square(x):
    return x * x


def sum_squares(x, y):
    return square(x) + square(y)
```

`sum_squares` 需要知道：

- `square` 接受一个参数；
- `square(x)` 返回 `x` 的平方。

它不需要知道：

- `square` 内部如何计算；
- `square` 使用乘法还是 `pow`；
- `square` 是用户定义函数还是内置函数。

以下实现具有相同行为：

```python
def square(x):
    return x * x
```

```python
def square(x):
    return x ** 2
```

```python
def square(x):
    return pow(x, 2)
```

### 2. 名字与函数对象

```python
def double(x):
    return x * 2


square = double
```

此时名字 `square` 指向 `double` 的函数对象，所以：

```text
square(3) = 6
```

Python 根据名字当前绑定的对象执行，不会因为名字叫 `square` 就自动计算平方。

这也说明名字虽然通常不决定程序能否运行，但会影响人是否容易理解代码。

### 3. 好名字表达意义或用途

不清楚：

```python
def calculate_helper(n):
    return n * 3
```

更清楚：

```python
def triple(number):
    return number * 3
```

不要只用类型命名：

```python
my_int = 6
```

应该说明值代表什么：

```python
number_of_rolls = 6
```

布尔值的名字最好说明什么情况为真：

```python
rolled_one = True
```

Python 多单词名字通常使用 snake_case：

```python
total_price = price * quantity
```

### 4. 避免重复表达式

不推荐：

```python
if price * quantity > 100:
    print(price * quantity)
```

更清楚：

```python
total_price = price * quantity

if total_price > 100:
    print(total_price)
```

优点：

- 说明计算结果的含义；
- 避免重复计算；
- 修改计算方式时只需修改一处。

### 5. 拆分复杂表达式

```python
def larger_solution(a, b, c):
    discriminant = b * b - 4 * a * c
    square_root = discriminant ** 0.5
    solution = (-b + square_root) / (2 * a)
    return solution
```

把复杂表达式拆成有意义的步骤，可以让人更容易理解代码。

### 6. 普通函数与高阶函数

普通函数：

```python
def total_with_tax(price, quantity):
    subtotal = price * quantity
    tax = subtotal * 0.1
    total = subtotal + tax
    return total
```

高阶函数至少满足一种情况：

- 接受函数作为参数；
- 返回一个函数。

因此 `search(f)` 和 `inverse(f)` 是高阶函数，`total_with_tax` 不是。

---

## 第四部分：错误与 Traceback

### 1. 三种错误

#### 语法错误（Syntax Error）

代码形式不符合 Python 语法，通常在程序开始执行前被发现。

```python
result = (5 + 3
print(result)
```

这里缺少右括号。

#### 运行时错误（Runtime Error）

语法正确，但程序执行到某一步时发生错误。

```python
result = 10 / 0
```

会产生：

```text
ZeroDivisionError
```

#### 逻辑错误（Logical Error）

程序可以正常运行，但结果不符合设计目标。

```python
def double(x):
    return x * 3
```

Python 不知道我们想计算两倍，所以不会主动报错。逻辑错误通常通过测试发现。

### 2. Traceback 表示调用过程

```python
def f(x):
    return g(x - 1)


def g(y):
    return h(y) - h(1 / y)


def h(z):
    z * z


result = f(12)
```

调用过程：

```text
全局调用 f(12)
→ f 调用 g(11)
→ g 调用 h
→ g 尝试将两个 h 的结果相减
```

因为 `h` 没有写 `return`，所以默认返回 `None`：

```text
None - None
```

最终产生 `TypeError`。

这里需要区分：

```text
Python 检测到错误的位置：g 中执行减法的那一行
真正需要修改的位置：h 中缺少 return
```

正确代码：

```python
def h(z):
    return z * z
```

### 3. 参数会在调用函数前求值

```python
def g(y):
    return h(y) - h(1 / y)
```

如果 `y = 0`，Python 会先计算：

```python
1 / y
```

此时已经发生 `ZeroDivisionError`，第二个 `h` 还没有真正被调用。因此修改 `h` 无法解决除零错误。

### 4. 报错行不一定是真正写错的行

```python
def calculate(x):
    return abs(x


def square(y):
    return y * y
```

Python 可能把语法错误指向 `def square(y):`，因为它直到这里才确定前面的表达式无法继续解析。真正的问题是上一段代码中的 `abs(` 没有右括号。

记忆：

> Traceback 或错误位置是调查的起点；它表示 Python 在哪里发现问题，不一定表示根本原因就在那一行。

### 5. 运算优先级造成的逻辑错误

错误目标实现：

```python
def average(x, y):
    return x + y / 2
```

如果目标是计算平均数，应该写成：

```python
def average(x, y):
    return (x + y) / 2
```

前一种写法语法正确，也可以正常运行，因此 Python 不会报错；它属于逻辑错误。

---

## 四部分核心口诀

```text
Lambda：创建定 parent，调用建帧并绑定参数。
Return：结束整个函数，并把值交回调用处。
抽象：使用者关注输入与行为，不依赖内部实现。
错误：报错位置是发现问题的位置，根因可能在别处。
```

## 本次讨论中的重点易错项

1. `return` 写在 `while` 中，仍然属于整个函数。
2. `while` 本身没有返回值；函数没有执行 `return` 时默认返回 `None`。
3. `0` 是假值，负数和其他非零数字是真值。
4. `search` 返回满足条件的 `x`，不是判断函数 `f(x)` 的返回值。
5. Lambda 表达式求值时返回函数对象；调用后才得到函数体的运行结果。
6. `sqrt(256)` 中 `256` 绑定给 `y`，而 `x` 从 `0` 开始搜索。
7. 名字指向对象；名字叫 `square` 不保证函数真的计算平方。
8. 高阶函数接受函数或返回函数；使用中间变量不等于使用高阶函数。
9. Traceback 指出的错误行与真正需要修改的行可能不同。

## 自测题

### 题目 1：环境与 Lambda

```python
a = 2

def make(g):
    a = 5
    return lambda x: a + g(x)

h = make(lambda x: a * x)
a = 3
result = h(4)
```

思考：两个 lambda 的 parent 分别是谁？`result` 是多少？

### 题目 2：循环控制

```python
def test():
    x = 0

    while x < 5:
        x += 1
        if x == 2:
            continue
        if x == 4:
            break
        print(x)

    return x


r = test()
```

思考：打印哪些数字？`r` 是多少？

### 题目 3：Search

```python
def search(f):
    x = 0

    while True:
        if f(x):
            return x
        x += 1


def condition(x):
    return x * x - 9


result = search(condition)
```

思考：第一次 `condition(x)` 返回多少？它是真值还是假值？`result` 是多少？

### 题目 4：错误类型

```python
def half_sum(x, y):
    return x + y / 2
```

假设目标是返回 `x` 和 `y` 的平均数：这是什么类型的错误？应该怎样修改？

---

## 自测题答案

1. 外层返回 lambda 的 parent 是 `make` 的调用帧；传给 `make` 的 lambda 的 parent 是 Global。`result = 5 + 3 * 4 = 17`。
2. 打印 `1、3`，`r = 4`。
3. `condition(0) = -9`，非零数字是真值，所以 `result = 0`。
4. 逻辑错误。应改成 `return (x + y) / 2`。
