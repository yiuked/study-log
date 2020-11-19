```
github.com/kylelemons/go-gypsy/yaml
```

解析list，格式

```
domains:
	- A
	- B
	- C
```

解析

```
	file, err := yaml.ReadFile("conf.yaml")

	if err != nil {
		panic(err)
		panic("failed to open conf.yaml")
	}

	node,err := yaml.Child(file.Root,"domains")
	if err != nil {
		panic(err)
		panic("failed to parse node")
	}

	domains := node.(yaml.List)
```



