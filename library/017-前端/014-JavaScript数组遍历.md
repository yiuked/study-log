JavaScript 中的 `Array` 提供了多种遍历操作，每种方法的用法和适用场景略有不同。以下是常用的遍历方法：

### 1. `forEach()`
对数组的每个元素执行一次指定的函数，适用于只进行简单遍历，不返回任何值。

```javascript
const arr = [1, 2, 3];
arr.forEach((item, index) => {
    console.log(item, index);  // 输出元素和索引
});
```

### 2. `map()`
对数组的每个元素执行指定的操作并返回一个新数组，不改变原数组。

```javascript
const arr = [1, 2, 3];
const newArr = arr.map(item => item * 2);  // [2, 4, 6]
```

### 3. `filter()`
筛选符合条件的元素并返回一个新数组，不改变原数组。

```javascript
const arr = [1, 2, 3, 4];
const evenNumbers = arr.filter(item => item % 2 === 0);  // [2, 4]
```

### 4. `reduce()`
对数组中的每个元素进行累加（或累积）操作，返回累积结果。通常用于计算总和、合并等场景。

```javascript
const arr = [1, 2, 3, 4];
const sum = arr.reduce((accumulator, currentValue) => accumulator + currentValue, 0);  // 10
```

### 5. `some()`
检测数组中是否有元素满足条件，返回 `true` 或 `false`。

```javascript
const arr = [1, 2, 3];
const hasEvenNumber = arr.some(item => item % 2 === 0);  // true
```

### 6. `every()`
检测数组中是否每个元素都满足条件，返回 `true` 或 `false`。

```javascript
const arr = [2, 4, 6];
const allEven = arr.every(item => item % 2 === 0);  // true
```

### 7. `find()`
找到第一个满足条件的元素并返回，不会继续遍历，找不到则返回 `undefined`。

```javascript
const arr = [1, 2, 3, 4];
const firstEven = arr.find(item => item % 2 === 0);  // 2
```

### 8. `findIndex()`
找到第一个满足条件的元素的索引，找不到则返回 `-1`。

```javascript
const arr = [1, 2, 3, 4];
const index = arr.findIndex(item => item % 2 === 0);  // 1
```

### 9. `for...of`
`for...of` 是一种简单的迭代方式，适用于遍历数组和其他可迭代对象（如 `Map`、`Set` 等）。

```javascript
const arr = [1, 2, 3];
for (const item of arr) {
    console.log(item);  // 输出1，2，3
}
```

### 10. `for...in`
遍历数组的可枚举属性，不常用于数组遍历，通常用于对象属性遍历。

```javascript
const arr = [1, 2, 3];
for (const index in arr) {
    console.log(index, arr[index]);  // 输出索引和元素
}
```

### 11. `keys()`, `values()`, `entries()`
这些方法返回一个迭代器，分别用于遍历数组的键（索引）、值和键值对。

```javascript
const arr = ['a', 'b', 'c'];

for (let key of arr.keys()) {
    console.log(key);  // 输出0, 1, 2
}

for (let value of arr.values()) {
    console.log(value);  // 输出 'a', 'b', 'c'
}

for (let [index, value] of arr.entries()) {
    console.log(index, value);  // 输出 [0, 'a'], [1, 'b'], [2, 'c']
}
```

### 总结

- **`forEach()`**：适合无返回值的简单遍历。
- **`map()`**：适合返回新数组的操作。
- **`filter()`**：适合筛选符合条件的元素。
- **`reduce()`**：适合累积运算。
- **`some()` 和 `every()`**：分别适合有条件检查和全条件检查。
- **`find()` 和 `findIndex()`**：适合找到第一个符合条件的元素或索引。