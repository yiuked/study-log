Flexbox 和 CSS Grid 是现代 CSS 布局系统的两大核心，提供了强大的工具来创建复杂的布局。以下是这两种布局的详细规范和关键功能：

### Flexbox（Flexible Box Layout）

**Flexbox** 是一种一维布局模型，专注于在一个方向（行或列）上分配空间和对齐内容。它非常适合用于小规模的布局，如导航栏、工具栏、按钮组等。

#### 关键概念和属性：

- **容器属性**：
  - `display: flex`：定义一个 flex 容器。
  - `flex-direction`：设置主轴的方向。
    - `row`（默认）：主轴为水平方向，从左到右。
    - `row-reverse`：主轴为水平方向，从右到左。
    - `column`：主轴为垂直方向，从上到下。
    - `column-reverse`：主轴为垂直方向，从下到上。
  - `flex-wrap`：设置是否换行。
    - `nowrap`（默认）：不换行。
    - `wrap`：换行，第一行在上方。
    - `wrap-reverse`：换行，第一行在下方。
  - `justify-content`：定义项目在主轴上的对齐方式。
    - `flex-start`（默认）：从主轴起点对齐。
    - `flex-end`：从主轴终点对齐。
    - `center`：居中对齐。
    - `space-between`：两端对齐，项目之间的间隔相等。
    - `space-around`：项目周围的间隔相等。
  - `align-items`：定义项目在交叉轴上的对齐方式。
    - `stretch`（默认）：如果项目未设置高度或设置为 auto，将占满整个容器的高度。
    - `flex-start`：从交叉轴的起点对齐。
    - `flex-end`：从交叉轴的终点对齐。
    - `center`：居中对齐。
    - `baseline`：项目的基线对齐。
  - `align-content`：定义多根轴线的对齐方式。
    - `stretch`（默认）：轴线占满整个交叉轴。
    - `flex-start`：与交叉轴的起点对齐。
    - `flex-end`：与交叉轴的终点对齐。
    - `center`：与交叉轴的中点对齐。
    - `space-between`：轴线之间的间隔平均分布。
    - `space-around`：每根轴线两侧的间隔都相等。

- **项目属性**：
  - `order`：定义项目的排列顺序。数值越小，排列越靠前，默认值为 0。
  - `flex-grow`：定义项目的放大比例，默认为 0，即如果存在剩余空间，也不放大。
  - `flex-shrink`：定义项目的缩小比例，默认为 1，即如果空间不足，该项目将缩小。
  - `flex-basis`：定义在分配多余空间之前，项目占据的主轴空间，默认值为 `auto`。
  - `flex`：是 `flex-grow`, `flex-shrink` 和 `flex-basis` 的简写，默认值为 `0 1 auto`。
  - `align-self`：允许单个项目有与其他项目不一样的对齐方式，可覆盖 `align-items` 属性。默认值为 `auto`。

### CSS Grid Layout

**CSS Grid** 是一种二维布局模型，允许在行和列两个方向上进行布局。它适合于更复杂的布局，如整个网页的布局。

#### 关键概念和属性：

- **容器属性**：
  - `display: grid`：定义一个网格容器。
  - `grid-template-columns`：定义列的数量和宽度。
    ```css
    grid-template-columns: 100px 1fr 2fr;
    ```
  - `grid-template-rows`：定义行的数量和高度。
    ```css
    grid-template-rows: 50px auto 1fr;
    ```
  - `grid-template-areas`：通过命名区域来布局。
    ```css
    grid-template-areas:
      "header header header"
      "sidebar content content"
      "footer footer footer";
    ```
  - `grid-column-gap` 和 `grid-row-gap`：分别定义列间距和行间距。
    ```css
    grid-column-gap: 10px;
    grid-row-gap: 15px;
    ```
  - `gap`：同时定义行间距和列间距。
    ```css
    gap: 10px 15px; /* 行间距为10px，列间距为15px */
    ```

- **项目属性**：
  - `grid-column`：定义项目的起始和结束列。
    ```css
    grid-column: 1 / 3; /* 从第1列跨到第3列（不包括第3列） */
    ```
  - `grid-row`：定义项目的起始和结束行。
    ```css
    grid-row: 2 / 4; /* 从第2行跨到第4行（不包括第4行） */
    ```
  - `grid-area`：定义项目的区域，使用区域名或 `grid-row` 和 `grid-column` 的简写形式。
    ```css
    grid-area: header; /* 使用命名区域 */
    grid-area: 1 / 1 / 2 / 3; /* 使用行列定义 */
    ```
  - `justify-self`：定义项目在单元格内的水平对齐方式。
    ```css
    justify-self: center; /* 水平居中 */
    ```
  - `align-self`：定义项目在单元格内的垂直对齐方式。
    ```css
    align-self: center; /* 垂直居中 */
    ```

### 总结

- **Flexbox** 是一维布局工具，主要用于在一个方向上（行或列）分配空间和对齐内容，适合简单的布局，如导航栏、工具栏等。
- **CSS Grid** 是二维布局工具，允许在行和列两个方向上进行布局，适合复杂的页面布局，如整个网页的布局。

这两种布局工具各有优劣，通常可以根据具体的布局需求选择合适的工具。在某些情况下，Flexbox 和 Grid 可以结合使用，以发挥它们各自的优势。