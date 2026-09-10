# Lecture Review Notes：函数、数字处理与装饰器

这次 lecture 学了三个小节。核心方法是：**按执行顺序追踪名字的绑定，区分调用、打印和返回。**

## 1. 函数调用、返回值与作用域

### 1.1 打印内容不等于返回值

```python
result = print(5)
```

屏幕打印 `5`，但 `print(5)` 返回 `None`，因此 `result = None`。注意 `None` 首字母大写。

交互式解释器通常自动显示表达式的值，但不会自动显示 `None`；赋值语句也不会自动显示赋给变量的值。普通 `.py` 文件中的独立表达式不会自动显示结果。

```python
value = square(3)  # 保存 9，不打印
print(value)      # 才打印 9
```

**你的易混点：算出一个值，不代表屏幕会打印它。**

### 1.2 嵌套调用：先计算参数，再调用外层函数

```python
print(print(1), print(2))
```

1. `print(1)` 打印 `1`，返回 `None`。
2. `print(2)` 打印 `2`，返回 `None`。
3. 外层执行 `print(None, None)`。

输出：

```text
1
2
None None
```

整个表达式的值是 `None`。多个参数默认用空格分隔，不会打印参数之间的逗号。

### 1.3 函数本身与函数调用

| 写法 | 含义 |
|---|---|
| `print` | 函数本身 |
| `print()` | 调用函数 |
| `return g` | 返回函数本身 |
| `return g()` | 调用 `g`，再返回调用结果 |

```python
def delay(arg):
    print('delayed')
    def g():
        return arg
    return g

f = delay(print)
x = f()
```

执行后，`f` 指向 `g`，`x` 指向 `print`。

**你的易混点：`x = f()` 不是 `x = print()`。** `f()` 返回 `print` 函数本身，没有调用它。之后执行 `x(6)` 才相当于 `print(6)`。

内部函数可以通过定义时的外层环境访问 `arg`，即使外层调用已经结束。这是这里的闭包行为。

### 1.4 连续括号不一定调用同一个函数

```python
def pirate(arggg):
    print('matey')
    def plunder(arggg):
        return arggg
    return plunder

result = pirate(3)(8)
```

等价地拆开：

```python
f = pirate(3)  # 打印 matey，返回 plunder
result = f(8)  # 调用 plunder，返回 8
```

只打印一次 `matey`，`result = 8`。内层 `plunder` 有自己的参数，所以返回自己收到的 `8`，不使用外层的 `3`。

**你的易混点：不能根据括号数量，直接判断 `pirate` 被调用几次。必须看每一步返回了什么。**

```python
pirate(pirate(pirate))(5)(7)
```

执行过程：

```text
内层 pirate(pirate) → 打印 matey，返回一个 plunder
外层 pirate(...)   → 打印 matey，返回另一个 plunder
接着调用 (5)       → 返回数字 5
最后调用 (7)       → 尝试执行 5(7)，报 TypeError
```

这不是死循环。把函数作为参数传入，不会自动反复调用它。

### 1.5 关键突破：def 也会重新绑定名字

```python
def horse(mask):
    horse = mask
    def mask(horse):
        return horse * 3
    return horse(mask)

mask = lambda horse: horse(4)

result = horse(mask)
```

**你最初漏掉的一步：执行内部 `def mask(...)` 后，局部名字 `mask` 改为指向新创建的函数。**

| 执行位置 | 局部 horse | 局部 mask |
|---|---|---|
| 执行 `horse = mask` 后 | lambda | lambda |
| 执行内部 `def mask` 后 | 仍是 lambda | 新创建的内部函数 |

名字没有变，变的是它指向的对象。重新绑定 `mask` 不会让 `horse` 跟着改变；全局的 `mask` 也仍然指向 lambda。

因此 `return horse(mask)` 表示：**调用 lambda，把内部的 mask 函数传进去。**

### 1.6 lambda 什么时候执行？里面的名字指谁？

```python
lambda horse: horse(4)
```

相当于定义这样的函数：

```python
def example(horse):
    return horse(4)
```

- 创建 lambda 时，不执行 `horse(4)`。
- 调用 lambda 时，参数 `horse` 绑定到传入的值。
- 然后调用该参数所指向的函数，传入 `4`。

原题的完整路线：

```text
调用外层 horse(mask)
→ lambda 被传入外层函数
→ 内部 def 创建新的 mask 函数
→ 调用 lambda，传入内部 mask
→ lambda 的参数 horse 指向内部 mask
→ horse(4) 就是内部 mask(4)
→ 返回 4 × 3 = 12
→ 逐层返回，result = 12
```

**你的疑问：horse 出现这么多次，到底是哪一个？**

先看当前调用环境里的绑定。lambda 的参数 `horse` 不会因为名字相同，就自动指向全局的 `horse`。数字 `4` 是内部参数的值，不是它的“地址”。

遇到同名嵌套，可以先换名理解，或在 Python Tutor 中观察每个调用框里的箭头。

## 2. 实现函数：删除整数中的指定数字

### 2.1 先明确题意

```python
remove(231, 3)     # 21
remove(243132, 2)  # 4313
remove(333, 3)     # 0
```

删除所有等于 `digit` 的数字，保留其他数字的原顺序，返回整数。

### 2.2 从右往左取数字

```python
last = n % 10
n = n // 10
```

`n = 231` 时，只执行一轮：`last = 1`，`n = 23`。

- `% 10`：取最后一位，不是计算有几位。
- `// 10`：对于这里的非负整数，去掉最后一位。

### 2.3 变量分别负责什么？

| 变量 | 含义 |
|---|---|
| `kept` | 已经拼出的结果 |
| `digits` | 已经保留的位数 |
| `digit` | 要删除的数字，整个过程中不变 |

每保留一位：

```python
kept = kept + last * 10 ** digits
digits = digits + 1
```

```text
digits = 0 → 倍率 1   → 放个位
digits = 1 → 倍率 10  → 放十位
digits = 2 → 倍率 100 → 放百位
```

**你的易混点：不是每循环一次倍率就增加。只有保留一位，digits 才增加。**

处理 `remove(231, 3)`：

```text
保留 1：kept = 1，digits = 1
删除 3：两者不变
保留 2：kept = 1 + 2 × 10 = 21，digits = 2
```

### 2.4 完整实现

```python
def remove(n, digit):
    kept = 0
    digits = 0

    while n > 0:
        last = n % 10
        n = n // 10

        if last != digit:
            kept = kept + last * 10 ** digits
            digits = digits + 1

    return kept
```

条件必须写成 `last != digit`，不能固定成 `last != 3`，因为 `3` 只是某个例子的输入。变量名是 `kept`，注意拼写。

### 2.5 保留 0，也必须计数

```python
remove(301, 1)  # 30
```

| 取出的数字 | 操作 | kept | digits |
|---|---|---:|---:|
| 1 | 删除 | 0 | 0 |
| 0 | 保留 | 0 | 1 |
| 3 | 保留 | 30 | 2 |

保留 `0` 没有改变 `kept` 的数值，但它占了一位。计数器必须增加，才能让 `3` 放在十位。

**digits 记录已保留的位数，不是当前 kept 显示出来有几位。**

你的疑问：“Python 会自动安排吗？”

```python
remove(301, 3)  # 剩下的数字顺序是 0、1，整数结果为 1
remove(301, 1)  # 结果为 30
```

- 整数结果不保留前导零，所以第一种结果是 `1`。
- 第二种结果中 `3` 在十位，是计数器和乘法安排的，不是 Python 自动判断的。

### 2.6 写函数的解题方法

1. 用例子核对题意。
2. 选一个简单例子，手动追踪变量。
3. 明确每个变量记录什么。
4. 写代码，检查是否得到目标结果。
5. 再检查没有匹配数字、全部删除、包含 `0` 等情况。

## 3. 装饰器：包装函数并重新绑定名字

### 3.1 先看包装函数

```python
def trace1(fn):
    def traced(x):
        print('开始计算')
        return fn(x)
    return traced

def square(x):
    return x * x

tracked_square = trace1(square)
result = tracked_square(3)
```

`trace1` 接收原函数，返回新函数。新函数先打印，再调用原函数。

这里打印“开始计算”，`result = 9`，其中 `fn` 指向原来的 `square`。

### 3.2 @ 的含义

```python
@trace1
def square(x):
    return x * x
```

等价于：

```python
def square(x):
    return x * x

square = trace1(square)
```

1. 创建原来的 `square` 函数。
2. 把它传给 `trace1`。
3. `trace1` 返回 `traced`。
4. 名字 `square` 改为指向 `traced`。

`traced` 中的 `fn` 仍然指向原平方函数，所以 `fn(x)` 不会因为这次重新绑定而无限调用包装函数。

### 3.3 你的关键易混点：定义时也可能执行代码

```python
def decorate(fn):
    print('装饰中')
    def wrapped(x):
        print('计算中')
        return fn(x)
    return wrapped

@decorate
def square(x):
    return x * x

print('准备好了')
result = square(3)
```

输出：

```text
装饰中
准备好了
计算中
```

`result = 9`，但不会自动打印。

| 时机 | 执行什么 |
|---|---|
| 执行带 `@decorate` 的函数定义时 | 调用 `decorate`，打印“装饰中”，返回包装函数 |
| 之后调用 `square(3)` 时 | 执行 `wrapped`，打印“计算中”，再调用原平方函数 |

**没有调用 square，不代表什么都不打印：装饰器本身已经在定义时被调用。**

### 3.4 包装函数可以改变返回值

```python
def decorate(fn):
    def wrapped(x):
        print('开始')
        value = fn(x)
        print('结束')
        return value + 1
    return wrapped

@decorate
def square(x):
    return x * x

result = square(3)
```

输出只有：

```text
开始
结束
```

原函数返回 `9`，包装函数再返回 `9 + 1`，因此 `result = 10`。

**中间算出的 9 不会自动打印，最终保存的 10 也不会自动打印。**

## 4. 做题时的四个检查问题

1. **这个名字现在指向什么？**
2. **这里是在传递函数，还是调用函数？**
3. **这一步打印什么，又返回什么？**
4. **有没有赋值或 def，改变当前环境中的名字绑定？**

你这次最重要的进步是理解了：**名字可以重新绑定；原来指向同一个对象的两个名字，不会因为其中一个重新绑定，就一起改变。** 这也是理解高阶函数和装饰器的基础。
