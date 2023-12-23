在Go中，选择是使用指针还是非指针通常取决于你对数据的需求以及性能和语义的考虑。以下是一些指导原则：

### 使用指针的情况：

1. **需要在函数中修改数据：**
   - 如果你需要在函数中修改一个变量的值，你应该传递该变量的指针。

    ```go
    func modifyValue(value *int) {
        *value = *value * 2
    }

    // 使用示例
    var x = 5
    modifyValue(&x)
    ```

2. **避免复制大对象：**
   - 当你处理大的结构体或对象时，通过传递指针可以避免在函数调用时复制整个对象。

    ```go
    type LargeStruct struct {
        // fields
    }

    func processLargeObject(obj *LargeStruct) {
        // do something with obj
    }

    // 使用示例
    largeObj := LargeStruct{}
    processLargeObject(&largeObj)
    ```

3. **返回动态分配的内存：**
   - 当函数返回一个新分配的对象时，使用指针可以避免在返回之前进行数据复制。

    ```go
    func createObject() *SomeStruct {
        obj := SomeStruct{}
        // 初始化 obj
        return &obj
    }
    ```

### 不使用指针的情况：

1. **小的基本类型：**
   - 对于小的基本类型，直接传递值而不是指针更为简单。

    ```go
    func doubleValue(value int) int {
        return value * 2
    }

    // 使用示例
    result := doubleValue(5)
    ```

2. **不需要修改原始值：**
   - 如果你不需要在函数内修改变量的值，可以直接传递值。

    ```go
    func printValue(value int) {
        fmt.Println(value)
    }

    // 使用示例
    x := 10
    printValue(x)
    ```

3. **值语义更合适：**
   - 如果你更倾向于值语义，即希望确保函数不会修改原始值，使用非指针可能更为合适。

    ```go
    func processImmutable(value SomeStruct) {
        // 不会修改原始值
    }

    // 使用示例
    obj := SomeStruct{}
    processImmutable(obj)
    ```

总的来说，Go的设计哲学是简单而清晰的。使用指针时要小心，确保它是必要的，而不是出于方便或不必要的优化。在大多数情况下，使用值传递是安全的，因为Go会在必要时进行自动复制。