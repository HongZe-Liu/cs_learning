# 高阶函数、环境、闭包与 Currying：完整复习笔记

这份笔记总结以下内容：

1. 函数作为值与高阶函数
2. name、value 与 binding
3. frame 与 environment
4. 局部作用域与名称查找
5. 嵌套函数与闭包
6. 函数组合
7. lambda 表达式
8. Currying（柯里化）

这些内容共同回答一个核心问题：Python 如何把函数当作值，并通过多层 environment 分阶段保存和使用参数？

---

## 1. 最重要的整体模型

到目前为止，课程真正想建立的不是几个 Python 语法点，而是一套观察程序运行的方法：

> 名称绑定到值；函数也是值；调用函数会创建 frame；函数体在一个由 frame 组成的 environment 中执行。

可以先记住下面这张总表：

| 概念 | 含义 |
|---|---|
| name | 名称，例如 `x`、`square`、`f` |
| value | 值，例如 `5`、一个函数对象 |
| binding | 名称和值之间的绑定，例如 `x → 5` |
| function | 一份可以被调用的操作说明，同时也是一种值 |
| frame | 一次函数调用使用的局部“记事本” |
| environment | 当前 frame 与 parent frames 组成的名称查找链 |
| closure | 函数代码与其定义环境引用的组合 |

---

## 2. Name、value 与 binding

Python 中的名称像标签，可以绑定到不同类型的值：

```python
x = 10
```

表示：

```text
x → 10
```

函数也是一种值：

```python
def square(x):
    return x * x
```

执行 `def` 后：

```text
square → square function
```

还可以让另一个名称绑定到同一个函数：

```python
another_name = square
```

此时：

```text
square       ─┐
              ├→ 同一个 function
another_name ─┘
```

这不是调用函数，只是传递或保存函数值。

必须区分：

```python
square       # 查找名称，得到函数值
square(4)    # 调用函数，得到数字 16
```

---

## 3. 定义、传递、返回和调用函数

这四个动作不能混在一起：

```text
定义函数 → 创建函数值，并记录其定义环境
传递函数 → 把函数值作为参数传递，不调用
返回函数 → 把函数值返回，不调用
调用函数 → 执行函数体，并创建新的调用 frame
```

例子：

```python
def add_one(x):
    return x + 1


f = add_one
result = f(5)
```

执行：

```python
f = add_one
```

不会调用 `add_one`，只会建立绑定：

```text
f → add_one function
```

执行：

```python
f(5)
```

才会调用该函数并创建 frame。

---

## 4. 高阶函数

高阶函数满足以下至少一个条件：

- 接收函数作为参数；
- 返回函数作为返回值。

### 4.1 接收函数的高阶函数

```python
def apply_twice(f, x):
    return f(f(x))


def add_one(x):
    return x + 1


result = apply_twice(add_one, 5)
```

调用 `apply_twice(add_one, 5)` 时：

```text
apply_twice frame
├── f → add_one function
└── x → 5
```

然后计算：

```python
f(f(x))
```

由内向外：

```text
f(5) → add_one(5) → 6
f(6) → add_one(6) → 7
```

所以：

```python
result == 7
```

每次调用 `add_one` 都会创建一个独立的 frame：

```text
第一次 add_one frame：x → 5
第二次 add_one frame：x → 6
```

`apply_twice` frame 中原来的 `f` 和 `x` 没有不断变化：

```text
f 始终绑定到 add_one function
x 始终绑定到 5
```

变化来自新的函数调用创建了新的 frame。

### 4.2 高阶函数的抽象意义

下面几个表达式具有相同结构：

```python
square(square(x))
double(double(x))
add_one(add_one(x))
```

共同结构是：

```text
某个操作(某个操作(x))
```

于是可以把具体操作抽象成参数 `f`：

```python
def apply_twice(f, x):
    return f(f(x))
```

这里：

```text
apply_twice → 控制执行流程
f           → 提供具体行为
x           → 被处理的数据
```

高阶函数把固定流程与可变行为分开。这与接口、多态、策略等设计思想具有共同的抽象目标，但实现机制不同。

---

## 5. Frame：一次函数调用的局部记事本

每调用一次用户定义函数，Python 都会为这次调用创建一个新的 frame。

```python
def add_one(x):
    y = x + 1
    return y


add_one(5)
```

对应的 frame：

```text
add_one frame
├── x → 5
├── y → 6
└── parent → Global frame
```

再次调用：

```python
add_one(20)
```

会创建另一个独立的 frame：

```text
add_one frame
├── x → 20
├── y → 21
└── parent → Global frame
```

frame 主要记录：

- 形参与实参的绑定；
- 局部名称和值的绑定；
- parent 指向哪个 frame。

frame 不是程序执行历史的完整日志。它不会记录每一行代码先后怎样执行。

可以记成：

> 函数是操作说明；frame 是某一次执行这份说明时使用的记事本。

---

## 6. Environment：用于名称查找的 frame 链

Environment 不是程序中所有 frame 的集合。它是：

> 当前 frame 加上沿 parent 可以到达的所有外层 frame，按照查找顺序组成的链。

例如：

```text
当前局部 frame → parent frame → Global frame
```

Python 查找名称时：

1. 先查当前 frame；
2. 找不到就沿 parent 查找；
3. 一直查到 Global frame；
4. 仍然找不到就报 `NameError`。

Global environment 是最简单的 environment，因为它只有 Global frame。

---

## 7. 调用关系不等于 parent 关系

这是前面最容易混淆、也最重要的细节。

完整代码：

```python
def f(x, y):
    return g(x)


def g(a):
    return a + y


result = f(1, 2)
```

调用 `f(1, 2)` 时：

```text
f frame
├── x → 1
├── y → 2
└── parent → Global
```

`f` 调用 `g(x)`，因此调用 `g(1)`：

```text
g frame
├── a → 1
└── parent → Global
```

执行：

```python
return a + y
```

查找 `y` 的路径是：

```text
g frame → Global frame
```

`f` frame 虽然仍然存在并且有 `y = 2`，但它不在 `g` 的 environment 中，因此不能访问。

程序会出现：

```text
NameError: name 'y' is not defined
```

必须分清：

```text
调用关系：f 调用了 g
parent 关系：g 定义在 Global，所以 g 的 parent 是 Global
```

关键规则：

> 函数的 parent 取决于函数在哪里定义，不取决于谁调用了它。

另外，执行：

```python
return g(x)
```

时，`f` 必须先计算 `g(x)`，获得结果后才能返回。如果 `g(x)` 报错，`f` 就没有成功返回。

---

## 8. 嵌套定义与闭包

完整代码：

```python
def make_adder(n):
    def adder(k):
        return k + n

    return adder


add_ten = make_adder(10)
result = add_ten(7)
```

第一次调用：

```python
make_adder(10)
```

创建：

```text
f1：make_adder frame
└── n → 10
```

随后在 `f1` 中定义 `adder`：

```text
adder function
├── 代码：return k + n
└── parent → f1
```

`make_adder` 返回的是 `adder` 函数本身：

```text
add_ten → adder function
```

这里还没有给 `k` 传值。`k` 来自第二次调用：

```python
add_ten(7)
```

这相当于调用：

```python
adder(7)
```

创建：

```text
f2：adder frame
├── k → 7
└── parent → f1
```

执行 `k + n` 时：

```text
k：在 f2 中找到 7
n：f2 中没有 → 在 f1 中找到 10
```

所以：

```python
result == 17
```

### 8.1 为什么外层函数结束后还能找到 n？

因为返回的 `adder` 函数仍然保存着对 `f1` 的引用。只要这个函数还需要该环境，相应的绑定就必须继续存在。

这就是闭包：

```text
闭包 = 函数代码 + 对定义时环境的引用
```

使用记事本比喻：

```text
frame       = 一本记事本
environment = 当前记事本与 parent 记事本组成的查找链
closure     = 函数说明书 + 指向定义时记事本的书签
```

闭包不只是图中的 parent 箭头。它是函数与所需定义环境联系起来的整个组合。

环境图是概念模型；Python 解释器在内存中会使用实际的数据结构保存闭包需要的引用。

---

## 9. 函数组合

函数组合把两个操作连接成一条流水线。

完整代码：

```python
def square(x):
    return x * x


def triple(x):
    return 3 * x


def compose1(f, g):
    def h(x):
        return f(g(x))

    return h


squiple = compose1(square, triple)
result = squiple(5)
```

在 `compose1` frame 中：

```text
f → square
g → triple
```

返回的 `h` 相当于：

```python
def h(x):
    return square(triple(x))
```

调用 `squiple(5)`：

```text
5
↓ triple
15
↓ square
225
```

所以：

```python
result == 225
```

组合顺序很重要：

```python
compose1(square, triple)(5)  # square(triple(5)) → 225
compose1(triple, square)(5)  # triple(square(5)) → 75
```

对于嵌套调用：

```python
f(g(x))
```

必须先得到内层 `g(x)` 的结果，才能调用外层 `f`。

“由内向外”适合描述这种嵌套调用，但不能概括所有 Python 代码的执行规则。

### 9.1 compose1 中的闭包

调用：

```python
combined = compose1(square, triple)
```

会创建 `compose1` frame：

```text
compose1 frame
├── f → square
└── g → triple
```

`h` 在这个 frame 中定义，所以返回的 `h` 是闭包：

```text
h function
├── 代码：return f(g(x))
└── parent → compose1 frame
```

以后调用 `h` 时：

```text
h 调用 frame → compose1 frame → Global frame
```

`x` 在 `h` 调用 frame 中找到，`f` 和 `g` 在 `compose1` frame 中找到。

---

## 10. Lambda 表达式

Lambda 是一个能够产生函数值的表达式：

```python
lambda x: x * x
```

执行这段表达式时得到的是函数，不是平方结果。

必须区分：

```python
lambda x: x * x       # 创建并得到函数值
(lambda x: x * x)(4)  # 调用该函数，得到数字 16
```

### 10.1 Lambda 与 def

下面两种写法的调用行为基本相同：

```python
def square(x):
    return x * x
```

```python
square = lambda x: x * x
```

`def` 会创建函数，并自动把函数绑定到 `square`；函数具有内部名称 `square`。

Lambda 表达式先创建一个函数值，赋值语句再把名称 `square` 绑定到它；函数的内部名称通常显示为 `<lambda>`。

Lambda 冒号后面只能放一个表达式，并且不写 `return`：

```python
lambda x: x + 1
```

大致对应：

```python
def function(x):
    return x + 1
```

Lambda 省略的是 `return` 关键字，不是赋值过程。

普通函数的返回值也不一定需要变量接住：

```python
print(square(4))
```

这里 `square(4)` 的结果直接成为 `print` 的参数。

### 10.2 Lambda 与高阶函数

完整代码：

```python
def apply_twice(f, x):
    return f(f(x))


result = apply_twice(lambda n: n + 1, 5)
```

过程是：

```text
lambda n: n + 1
↓
创建函数值
↓
直接把函数值传给参数 f
↓
f(f(5))
↓
f(6)
↓
7
```

Lambda 没有先获得一个全局名称，但它仍然是一个真实的函数对象。

### 10.3 Lambda 也可以形成闭包

完整代码：

```python
def make_power(n):
    return lambda x: x ** n


square = make_power(2)
result = square(5)
```

环境关系：

```text
make_power frame
├── n → 2
└── parent → Global

lambda function
└── parent → make_power frame

lambda 调用 frame
├── x → 5
└── parent → make_power frame
```

查找：

```text
x：在 lambda 调用 frame 中找到 5
n：在 make_power frame 中找到 2
```

所以：

```python
result = 5 ** 2
result = 25
```

---

## 11. Currying（柯里化）

Currying 把一个接收多个参数的函数，转换成一连串每次只接收一个参数的函数。

普通的双参数调用：

```python
add(10, 5)
```

柯里化后的调用：

```python
curried_add(10)(5)
```

可以先记成：

```text
f(x, y) → curried_f(x)(y)
```

Currying 不负责具体的加法或乘法。它改变的是函数接收参数的方式。

### 11.1 make_adder：从闭包走向 Currying

```python
def make_adder(n):
    return lambda k: n + k
```

调用：

```python
make_adder(2)(3)  # 5
```

分开写：

```python
add_two = make_adder(2)
result = add_two(3)
```

第一次调用：

```text
make_adder(2) → 返回一个函数，这个函数记住 n = 2
```

第二次调用：

```text
add_two(3) → k = 3 → n + k → 5
```

必须区分：

```text
add_two    → 函数值
add_two(3) → 调用表达式，值为 5
```

`make_adder` 展示了分阶段接收参数的结构。`curry2` 会把这个结构推广到任意双参数函数。

### 11.2 curry2：转换双参数函数

先明确要转换的函数：

```python
def add(x, y):
    return x + y
```

`curry2` 的嵌套函数写法：

```python
def curry2(f):
    def g(x):
        def h(y):
            return f(x, y)

        return h

    return g
```

使用：

```python
curried_add = curry2(add)
add_ten = curried_add(10)
result = add_ten(5)
```

结果：

```python
result == 15
```

也可以写成一个连续调用：

```python
curry2(add)(10)(5)  # 15
```

Python 将它理解为：

```python
((curry2(add))(10))(5)
```

各阶段得到的值：

| 表达式 | 参数绑定 | 得到的值 |
|---|---|---|
| `curry2(add)` | `f → add` | 函数 `g` |
| `curry2(add)(10)` | `x → 10` | 函数 `h` |
| `curry2(add)(10)(5)` | `y → 5` | `add(10, 5)` 的结果 `15` |

`g(10)` 是调用表达式；它的返回值是函数 `h`。因此下面两句话需要分清：

```text
过程：调用 g(10)
结果：得到 h 函数
```

### 11.3 curry2 的 environment 与闭包

执行：

```python
curry2(add)(10)(5)
```

第一次调用 `curry2(add)`：

```text
f1：curry2 frame
├── f → add function
└── parent → Global

g function
├── 代码：接收 x，定义并返回 h
└── parent → f1
```

第二次调用 `g(10)`：

```text
f2：g frame
├── x → 10
└── parent → f1

h function
├── 代码：return f(x, y)
└── parent → f2
```

第三次调用 `h(5)`：

```text
f3：h frame
├── y → 5
└── parent → f2
```

执行 `f(x, y)` 时的名称查找：

```text
y：在 f3 中找到 5
x：f3 中没有 → 在 f2 中找到 10
f：f3、f2 中没有 → 在 f1 中找到 add
```

因此：

```text
f(x, y) → add(10, 5) → 15
```

完整 environment 链：

```text
h 调用 frame f3
→ g 调用 frame f2
→ curry2 调用 frame f1
→ Global frame
```

这里连续发生三次用户定义函数调用，所以创建了三个调用 frame。`g` 和 `h` 能保存前面阶段的参数，是因为它们都是闭包。

### 11.4 Lambda 写法

`curry2` 可以压缩成：

```python
curry2 = lambda f: lambda x: lambda y: f(x, y)
```

理解时不要一次读完整行，而要逐层绑定：

```python
curry2(add)
# f = add
# 得到：lambda x: lambda y: add(x, y)
```

```python
curry2(add)(10)
# x = 10
# 得到：lambda y: add(10, y)
```

```python
curry2(add)(10)(5)
# y = 5
# 计算：add(10, 5) → 15
```

可以使用“每传入一个参数，就去掉一层最外部 lambda”来辅助理解，但更准确的说法是：

> 调用当前函数，绑定它的形参，然后得到它返回的下一层函数或最终结果。

### 11.5 make_adder 与 curry2(add) 的关系

```python
def make_adder(n):
    return lambda k: n + k
```

```python
curried_add = curry2(add)
```

它们可以具有相同的调用行为：

```python
make_adder(2)(3)    # 5
curried_add(2)(3)   # 5
```

区别在于：

```text
make_adder    → 专门构造“加 n”的函数
curry2        → 把任意双参数函数转换成两次单参数调用
curry2(add)   → 转换后得到与 make_adder 相同行为的函数
```

Currying 最早由 Moses Schönfinkel 提出，后来由 Haskell Curry 重新发现并推广。

---

## 12. 根据学习过程整理出的常见误区

### 误区一：Lambda 表达式直接得到计算结果

错误理解：

```text
lambda x: x + 1 → 得到数字
```

正确理解：

```text
lambda x: x + 1      → 得到函数
(lambda x: x + 1)(5) → 得到数字 6
```

### 误区二：传递函数时会创建该函数的 frame

错误理解：只要把函数传给高阶函数，就会创建该函数的调用 frame。

正确理解：

```text
传递函数值 → 不创建该函数的调用 frame
真正调用它 → 创建新的调用 frame
```

### 误区三：同名参数会让原来的变量变化

```python
x = 100
f = lambda x: x + 1
result = f(5)
```

这里不是全局 `x` 从 `100` 变成了 `5`，而是存在两个不同的绑定：

```text
Global frame：x → 100
lambda frame：x → 5
```

### 误区四：Frame 会记录整个执行历史

frame 记录局部绑定和 parent，不是逐行运行日志。

### 误区五：Environment 包含所有 frame

environment 只包含当前 frame 以及沿 parent 能到达的 frame。

### 误区六：被谁调用，就能访问谁的局部变量

函数能访问哪些外层 frame，取决于它在哪里定义，不取决于谁调用了它。

### 误区七：闭包就是一条连接线或数据传递记录

闭包是：

```text
函数代码 + 对定义环境的引用
```

图中的 parent 箭头是闭包关系的重要表现，但闭包是整个组合。

### 误区八：普通函数必须用变量接住返回值

返回值可以：

- 绑定给变量；
- 直接作为另一个函数的参数；
- 直接参与其他表达式；
- 不被保存。

```python
result = square(4)
print(square(4))
double(square(4))
square(4)
```

以上写法都可以调用 `square`。

### 误区九：curry2(add) 已经得到加法结果

错误理解：

```text
curry2(add) → 一个数字
```

正确理解：

```text
curry2(add)        → 返回函数 g
curry2(add)(10)    → 返回函数 h
curry2(add)(10)(5) → 返回数字 15
```

### 误区十：g(10) 就是函数 g

必须区分函数值和调用表达式：

```text
g     → 函数值
g(10) → 调用 g；在 curry2 的例子中，返回函数 h
```

因此：

```python
step = g(10)
```

表示 `step` 绑定到 `g(10)` 的返回值 `h`，不是绑定到 `g`。

### 误区十一：Currying 只是从左边删除 lambda 文本

“从左边去掉一层”可以帮助阅读，但真实过程是：

```text
调用最外层函数
→ 把实参绑定到形参
→ 执行函数体
→ 返回下一层函数或最终结果
```

---

## 13. 一页速记版

```text
1. 函数也是值。

2. name 可以绑定数字，也可以绑定函数：
   f → function

3. f 与 f(...) 不同：
   f      得到函数值
   f(...) 调用函数

4. 每次调用用户定义函数都会创建一个新的 frame。

5. frame 保存参数、局部绑定和 parent。

6. environment 是：
   当前 frame → parent → 更外层 parent → Global

7. 名称从当前 frame 开始，沿 parent 查找；找不到则 NameError。

8. 函数的 parent 由定义位置决定，不由调用者决定。

9. 闭包是：
   函数代码 + 对定义环境的引用

10. lambda 表达式产生函数值；调用 lambda 才产生计算结果。

11. f(g(x)) 先计算 g(x)，再把结果传给 f。

12. 高阶函数把行为也当作数据来传递或返回。

13. Currying 改变函数接收参数的形式：
    f(x, y) → curried_f(x)(y)

14. 每次柯里化调用只绑定当前最外层函数的一个参数。

15. curry2(f)(x)(y) 的分组是：
    ((curry2(f))(x))(y)

16. 中间调用返回函数；最后一层调用才得到最终计算结果。
```

---

## 14. 综合代码检查表

看到一段代码时，能够回答：

1. 哪些名称绑定到函数，哪些名称绑定到普通数据？
2. 哪些地方只是创建、传递或返回函数，哪些地方真正调用了函数？
3. 每次函数调用创建的 frame 中有哪些局部绑定？
4. 当前函数查找名称时，它的 parent 链是什么？
5. 一个连续调用表达式应该如何加括号？
6. 每一层调用返回的是函数还是最终数据？
7. Currying 的每个参数分别保存在哪一层 frame 中？

---

## 15. Currying 综合练习

完整代码：

```python
def multiply(x, y):
    return x * y


def curry2(f):
    def g(x):
        def h(y):
            return f(x, y)

        return h

    return g


curried_multiply = curry2(multiply)
times_three = curried_multiply(3)
result = times_three(4)
```

尝试回答：

1. `curry2(multiply)` 返回函数还是数字？
2. `curried_multiply(3)` 返回什么？
3. `f`、`x`、`y` 分别绑定到什么？
4. 三个参数分别位于哪一层调用 frame？
5. 总共发生几次用户定义函数调用？
6. `result` 是多少？

参考答案：

```text
1. 返回函数 g。
2. 返回函数 h；times_three 绑定到 h。
3. f → multiply，x → 3，y → 4。
4. f 在 curry2 frame，x 在 g frame，y 在 h frame。
5. 三次：curry2(multiply)、g(3) 和 h(4)。
6. multiply(3, 4) → 12，所以 result = 12。
```

这段代码与手写的闭包：

```python
def make_multiplier(n):
    return lambda x: n * x
```

具有对应关系：

```python
make_multiplier(3)(4)       # 12
curry2(multiply)(3)(4)      # 12
```
