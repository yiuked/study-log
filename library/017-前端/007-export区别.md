好的，以下是 `export const`、`export function`、`export class` 和 `export default` 四种导出方式的区别：

| 导出方式       | 导入方式                                             | 样例                                            |
| -------------- | ---------------------------------------------------- | ----------------------------------------------- |
| `export const` | 推荐采用解构的方式引入                               | `export const a = 5;`<br>`export const b = {}` |
|                | `import { a, b } from './example.js';`               |                                                 |
| `export function`  | 使用函数名称方式引入：                              | `export function square(x) { return x * x; }`  |
|                | `import { square } from './example.js';`            |                                                 |
| `export class` | 使用类名称方式引入：                                 | `export class Dog { ... }`                      |
|                | `import { Dog } from './example.js';`               |                                                 |
| `export default` | 使用 default 引入，可以通过命名引入（alias）来改名 | `export default MyClass;`                      |
|                | `import MyClass from './example.js';`               |                                                 |

总的来说，四种导出方式具有一定的灵活性和适用场景，采用不同的导出方式具体取决于开发者的需求。例如，如果只需要导出一个值，默认导出 `export default` 方式更为直接和简洁，如果需要导出多个变量，则选择规范导出方式比较合适。