# CS61A Review — Containers, Slicing, Aggregation, Strings, Dictionaries

> 今日学习：5 个小节  
> 目标：理解并能独立应用，而不是只记住语法。

---

# 1. Containers / Box-and-Pointer

## 1.1 Closure Property

如果一种组合数据的方法产生的结果，还能继续用同一种方法参与组合，那么它具有 **closure property（闭包性质）**。

例如：

```python
[1]
[[1]]
[[[1]]]
```

list 组合出来的结果仍然可以作为另一个 list 的元素，因此 list 具有 closure property。

它允许形成：

```text
hierarchical structure（层级结构）
```

例如：

```python
x = [1, [2, [3]], []]
```

可以理解成：

```text
外层 list
├── 1
├── 内层 list
│   ├── 2
│   └── 内层 list
│       └── 3
└── empty list
```

### 我的易错点

一开始容易把 closure property 和 pointer / index / box 混在一起。

正确关系是：

```text
closure property
    ↓
允许 list 嵌套 list
    ↓
形成 hierarchical structure
    ↓
需要 box-and-pointer notation 表示复杂关系
```

---

## 1.2 Object、Name、Reference

```python
a = [1, 2]
```

可以理解成：

```text
name
 a
 │
 │ reference
 ▼
list object
[1, 2]
```

- `a` 是 name
- `[1, 2]` 是 list object
- `reference` = 引用 / 引用关系

### 普通赋值不会复制 list

```python
a = [1, 2]
b = a
```

关系：

```text
a ──┐
    ▼
 [1, 2]
    ▲
b ──┘
```

`a` 和 `b` reference 同一个 object。

所以：

```python
b.append(3)
```

之后：

```python
a == [1, 2, 3]
b == [1, 2, 3]
```

### 我的易错点

不要理解成：

```text
b → a → object
```

更准确是：

```text
a ──┐
    ▼
 object
    ▲
b ──┘
```

两个 name 都引用同一个 object。

---

## 1.3 Index / Box / Pointer

```python
x = [3, [1, 2]]
```

概念图：

```text
x
│
▼
┌─────┬─────┐
│  3  │  ●  │
└─────┴──│──┘
 index0  index1
          │
          ▼
        [1, 2]
```

`index` 表示 list 中的一个元素位置，不代表“一个 index 就是一个 object”。

两个不同 index 也可以 reference 同一个 object：

```python
a = [1, 2]
b = [a, a]
```

此时 `b[0]` 和 `b[1]` 都引用同一个 `a` 所指向的 list object。

---

# 2. Slicing

## 2.1 基本规则

```python
sequence[start:stop]
```

规则：

```text
包含 start
不包含 stop
```

和 `range(start, stop)` 的边界规则一样。

例如：

```python
nums = [2, 4, 6, 8, 10]

nums[1:4]
# [4, 6, 8]
```

## 2.2 省略边界

```python
nums[:3]   # 从开头到 index 3 之前
nums[2:]   # 从 index 2 到结尾
nums[:]    # 全部
```

---

## 2.3 List Slicing 创建新的外层 Object

这是今天最重要的卡点之一。

```python
a = [1, 2]
c = a[:]
```

执行到 `a[:]` 时，根据当时 `a` 的内容创建新的 list object：

```text
a ───► List A [1, 2]

c ───► List B [1, 2]
```

所以：

```python
a.append(3)
```

之后：

```python
a == [1, 2, 3]
c == [1, 2]
```

### 对比

```python
b = a
```

不创建新的 list object：

```text
a ──┐
    ▼
 object
    ▲
b ──┘
```

而：

```python
c = a[:]
```

创建新的外层 list object。

---

## 2.4 Shallow Copy（浅拷贝）

```python
inner = [5]

a = [inner]
b = a[:]
```

`a` 和 `b` 是不同的外层 list object，但它们内部保存的 `inner` reference 仍然指向同一个 object：

```text
a ───► 外层 list A
         │
         ▼
       inner [5]
         ▲
         │
b ───► 外层 list B
```

所以：

```python
inner.append(6)
```

之后：

```python
a == [[5, 6]]
b == [[5, 6]]
```

### 我的易错点

要同时区分：

```text
外层 list 是否同一个 object
```

和：

```text
内部元素是否 reference 同一个 compound object
```

---

# 3. Sequence Aggregation

Aggregation：

```text
很多元素
  ↓
按照某种规则处理
  ↓
得到一个结果
```

## 3.1 `sum`

```python
sum([2, 3, 4])
# 9
```

完整形式：

```python
sum(iterable, start)
```

例如：

```python
sum([2, 3, 4], 10)
# 19
```

概念上：

```text
10 + 2 + 3 + 4
```

---

## 3.2 `max`

```python
max([3, 8, 2])
# 8
```

也可以：

```python
max(3, 8, 2)
# 8
```

---

## 3.3 `max(..., key=...)`

```python
words = ["cat", "elephant", "dog"]

max(words, key=len)
# "elephant"
```

`key` 是 **比较函数 / 评分函数**。

Python 比较：

```text
len("cat")      = 3
len("elephant") = 8
len("dog")      = 3
```

但最后返回的是原始元素：

```python
"elephant"
```

不是：

```python
8
```

### 我的易错点

`key` 不是筛选条件。

更准确：

```text
key(item)
```

决定 item 用什么标准比较，`max` 最后返回原始 item。

---

## 3.4 `all`

```python
all([3, -1, 5])
# True
```

因为这些值都 truthy。

但是：

```python
all([3, 0, 5])
# False
```

因为：

```python
bool(0) == False
```

常见 truthy / falsy：

```python
bool(5)       # True
bool(-1)      # True
bool(0)       # False

bool("hello") # True
bool("")      # False
```

另外：

```python
all([])
# True
```

---

# 4. Strings

String 是对 textual data 的抽象表示。

```python
"hello"
"你好"
"123"
```

注意：

```python
123      # number
"123"    # string
```

## 4.1 字符串写法

```python
'hello'
"hello"
```

通常等价。

三引号可以跨多行：

```python
"""hello
world"""
```

常用于 docstring。

## 4.2 Escape Sequence

```python
"\n"
```

表示 newline。

```python
print("hello\nworld")
```

输出：

```text
hello
world
```

---

## 4.3 String 是 Sequence

```python
s = "computer"
```

index：

```text
0 1 2 3 4 5 6 7
c o m p u t e r
```

所以：

```python
len(s)
# 8
```

## 4.4 String Indexing

```python
s[2]
# "m"
```

结果仍然是 `str`。

Python 在这里没有单独的 `char` 类型。

## 4.5 String Slicing

```python
s = "python"

s[1:4]
# "yth"
```

结果是：

```python
str
```

不是：

```python
['y', 't', 'h']
```

### 我的易错点

固定：

```text
list slicing   → list
string slicing → string
```

---

## 4.6 String 的 `in`

String 可以检查 substring：

```python
"bc" in "abcd"
# True
```

但是：

```python
[2, 3] in [1, 2, 3, 4]
# False
```

list 的 `in` 检查的是：

```text
有没有一个元素 == [2, 3]
```

而不是寻找连续子序列。

---

# 5. Dictionaries

Dictionary 表示：

```text
key → value
```

例如：

```python
numerals = {
    "I": 1,
    "V": 5,
    "X": 10
}
```

lookup：

```python
numerals["V"]
# 5
```

## 5.1 Dictionary vs List

List：

```text
index → value
```

Dictionary：

```text
key → value
```

如果 `0` 不是 key：

```python
numerals[0]
```

会得到 `KeyError`，不是“取第 0 个元素”。

---

## 5.2 Dictionary Lookup 是单向的

```python
numerals["V"]
# 5
```

可以。

但：

```python
numerals[5]
```

不会自动返回 `"V"`。

dictionary 的抽象就是：

```text
key → value
```

---

## 5.3 遍历 Dictionary

```python
for k in d:
```

默认遍历 keys。

如果需要 values：

```python
d.values()
```

例如：

```python
sum(d.values())
```

---

## 5.4 Key 的限制

### Key 不能重复

同一个 key 最多对应一个 value。

如果一个 key 需要对应多个数据，可以让 value 是 list：

```python
{
    7: [14, 21, 28]
}
```

### Key 必须 Hashable

现阶段重点记住：

```text
list       ❌ 不能作为 key
dictionary ❌ 不能作为 key
```

但是 value 可以是 list、dictionary 等复杂对象。

---

# 6. Dictionary Comprehension

基本形式：

```python
{
    key_expression: value_expression
    for name in iterable
    if condition
}
```

例如：

```python
{x: x * 10 for x in range(5) if x % 2 == 0}
```

结果：

```python
{
    0: 0,
    2: 20,
    4: 40
}
```

## 6.1 和 List Comprehension 对比

```python
[x * 2 for x in range(3)]
```

得到 list：

```python
[0, 2, 4]
```

而：

```python
{x: x * 2 for x in range(3)}
```

得到 dictionary：

```python
{
    0: 0,
    1: 2,
    2: 4
}
```

---

# 7. Dictionary + List Comprehension

今天最复杂的结构：

```python
def index(keys, values, match):
    return {
        k: [v for v in values if match(k, v)]
        for k in keys
    }
```

执行思路：

```text
for k in keys
    ↓
当前得到一个 k
    ↓
遍历所有 v in values
    ↓
检查 match(k, v)
    ↓
符合条件的 v 放进 list
    ↓
形成：

k : [符合条件的 v]
```

## 7.1 `k: [...]` 是什么？

它就是普通 dictionary 的：

```text
key : value
```

例如：

```python
{
    7: [35, 42, 49]
}
```

所以：

```python
k: [v for v in values if match(k, v)]
```

表示：

```text
key   = 当前 k
value = 当前 k 对应的结果 list
```

## 7.2 List Comprehension 三部分

```python
[v * 2 for v in values if v > k]
```

拆开：

```text
[v * 2       for v in values       if v > k]
 ↑                  ↑                   ↑
放进结果            遍历来源            筛选条件
```

### 我的易错点

曾把：

```python
v % k == 0
```

写成：

```python
k % v == 0
```

也曾把：

```python
v > k
```

写成：

```python
k > v
```

因此写 comprehension 时最好依次问：

1. 我遍历谁？
2. 什么条件留下？
3. 留下后最终放进去什么？

---

# 8. 今天最重要的执行模型

遇到 object / reference / mutation 题，按照代码执行顺序推演。

```python
a = [1, 2]
b = a
c = a[:]

b.append(3)
```

### 第 1 行

```python
a = [1, 2]
```

创建：

```text
List A = [1, 2]
a → List A
```

### 第 2 行

```python
b = a
```

不创建新 list：

```text
a ──┐
    ▼
 List A
    ▲
b ──┘
```

### 第 3 行

```python
c = a[:]
```

创建：

```text
List B = [1, 2]
c → List B
```

### 第 4 行

```python
b.append(3)
```

修改 List A：

```python
a == [1, 2, 3]
b == [1, 2, 3]
c == [1, 2]
```

---

# 9. 我的掌握状态

## 已经比较稳定

- closure property 的定义
- name / object / reference 的基本关系
- slicing 的边界规则
- `[:stop]`、`[start:]`、`[:]`
- slicing 创建新的外层 sequence value
- `sum`
- `max`
- `max(..., key=...)`
- string indexing / slicing
- string substring `in`
- dictionary key-value lookup
- dictionary comprehension 的整体结构
- dictionary comprehension + nested list comprehension
- comprehension 中 `k` 和 `v` 的来源
- filter condition 和 transformation expression 的区别

## 仍需继续练习

### 1. Aliasing / Mutation

尤其是：

```python
b = a
```

和：

```python
b = a[:]
```

的区别。

以及 shallow copy：

```text
外层 object 不同
内部 compound object 仍可能共享 reference
```

### 2. 跟踪 Sequence 的类型

```text
list slicing   → list
string slicing → string
```

### 3. Truthy / Falsy

尤其：

```python
bool(0) == False
```

所以：

```python
all([1, 0, 3]) == False
```

### 4. 把自然语言条件准确写成 Boolean Expression

```text
v 能被 k 整除
→ v % k == 0

v 大于 k
→ v > k

v 小于 k
→ v < k
```

---

# 10. 自测题（附答案）

## 题 1

```python
a = [1, 2]
b = a
c = a[:]

a.append(3)
```

答案：

```python
a == [1, 2, 3]
b == [1, 2, 3]
c == [1, 2]
```

## 题 2

```python
inner = [5]
a = [inner]
b = a[:]

inner.append(6)
```

答案：

```python
a == [[5, 6]]
b == [[5, 6]]
```

原因：`a` 和 `b` 是不同外层 list，但内部都 reference 同一个 `inner`。

## 题 3

```python
s = "computer"

a = s[1:4]
b = s[2]
```

答案：

```python
a == "omp"
type(a) == str

b == "m"
type(b) == str
```

## 题 4

```python
nums = [3, 0, 5]

a = sum(nums, 2)
b = max(nums)
c = all(nums)
```

答案：

```python
a == 10
b == 5
c == False
```

## 题 5

```python
words = ["cat", "banana", "pear"]

max(words, key=len)
```

答案：

```python
"banana"
```

`len` 是比较标准，`max` 返回原始元素。

## 题 6

实现：

```python
def build(keys, values):
```

要求：

- 每个 `k` 作为 key
- 只保留 `v > k`
- 放进 list 的是 `v + 1`

答案：

```python
def build(keys, values):
    return {
        k: [v + 1 for v in values if v > k]
        for k in keys
    }
```

---

# 11. 下一次学习前的快速复习

不看笔记，先推演：

```python
inner = [1]
a = [inner]
b = a[:]
c = a

inner.append(2)
a.append(3)
```

尝试独立判断：

```text
a =
b =
c =
```

如果能正确解释 object / reference，再继续新的 lecture。
