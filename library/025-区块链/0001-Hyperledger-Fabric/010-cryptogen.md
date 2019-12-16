# cryptogen详解
配置模板文件
```
OrdererOrgs:
  - Name: Orderer
    Domain: example.com
    EnableNodeOUs: false
    Specs:
      - Hostname: orderer
PeerOrgs:
  - Name: Org1
    Domain: org1.example.com
    EnableNodeOUs: false
    CA:
      Hostname: ca # implicitly ca.org1.example.com
      Country: US
      Province: California
      Locality: San Francisco
      OrganizationalUnit: Hyperledger Fabric
      StreetAddress: address for org # default nil
      PostalCode: postalCode for org # default nil
    Specs:
     - Hostname: foo # implicitly "foo.org1.example.com"
       CommonName: foo27.org5.example.com # overrides Hostname-based FQDN set above
       SANS:
         - "bar.{{.Domain}}"
         - "altfoo.{{.Domain}}"
         - "{{.Hostname}}.org6.net"
         - 172.16.10.31
     - Hostname: bar
     - Hostname: baz

    Template:
      Count: 1
      Start: 5 # 默认从0开始
      Hostname: {{.Prefix}}{{.Index}} # default
      SANS:
       - "{{.Hostname}}.alt.{{.Domain}}"
    Users:
      Count: 1 # 生成除管理员外的账户，默认会生成一个管理员账户
```
