```
# Copyright The OpenTelemetry Authors  
#  
# Licensed under the Apache License, Version 2.0 (the "License");  
# you may not use this file except in compliance with the License.  
# You may obtain a copy of the License at  
#  
#     http://www.apache.org/licenses/LICENSE-2.0  
#  
# Unless required by applicable law or agreed to in writing, software  
# distributed under the License is distributed on an "AS IS" BASIS,  
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  
# See the License for the specific language governing permissions and  
# limitations under the License.  
version: "3.7"  
services:  
  zipkin-collector:  
    image: openzipkin/zipkin-slim:latest  
    ports:  
      - "9411:9411"  
    networks:  
      - example  
  zipkin-client:  
    build:  
      dockerfile: ./Dockerfile  
      context: ../..  
    command:  
      - "/bin/sh"  
      - "-c"  
      - "while ! nc -w 1 -z zipkin-collector 9411; do echo sleep for 1s waiting for zipkin-collector to become available; sleep 1; done && /go/bin/main -zipkin http://zipkin-collector:9411/api/v2/spans"  
    networks:  
      - example  
    depends_on:  
      - zipkin-collector  
networks:  
  example:
```