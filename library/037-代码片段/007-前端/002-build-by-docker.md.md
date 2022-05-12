```
#!/bin/bash  
  
# shellcheck disable=SC2046  
# shellcheck disable=SC2006  
docker run -v $(pwd):/html/src node:14.18.1 sh -c "cd /html/src/ && npm install && npm run-script build"
```

```
#!/bin/bash  
  
# shellcheck disable=SC2046  
# shellcheck disable=SC2006  
docker run -v $(pwd):/html/src node:14.18.1 sh -c "cd /html/src/ && yarn install && yarn build"
```