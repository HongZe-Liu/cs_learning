# Assignment and Names

1. Python 中 name 会绑定到 value。

2. = 的右边先计算，再把结果绑定给左边的 name。

3. 再次赋值，就是让 name 重新绑定到另一个 value。

4. 函数也是 value，因此一个函数可以有多个名字。

5. 普通 assignment 不会记住计算公式；function 每次调用都会重新执行函数体。

 ## Discussion

```
f = min
f = max
g, h = min, max
max = g
max(f(2, g(h(1, 5), 3)), 4)
```

### 变化
```
f = min
f = max

g -> min function
h -> max function

max -> min function
```
### 结果
```
f   -> max
g   -> min
h   -> max
max -> min
```