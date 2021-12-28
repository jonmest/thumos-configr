# Thumos Configr
A simple Python3 class to facilitate easy loading and access to configuration settings using dot-style syntax, with support for Yaml, JSON, TOML and XML. To clarify, dot-style syntax refers to something such as the following:

Example YAML file:
```yaml
configuration:
  mysql:
    host: localhost
    port: 3600
```

Using Configr, the values could be accessed in this way:
```python
cr = Configr("config.yaml")
cr["configuration.mysql.host"]
>> localhost
cr["configuration.port"]
>> 3600
```

However, other characters than the dot can be used as a separator.
```python
cr = Configr("config.yaml", separator="/")
cr["configuration/mysql/host"]
>> localhost
```

It is also possible to set an initial root key, to minimize verbosity when using deep configuration files that may contain settings not pertinent to the script or application you are working on. Take the following example YAML file:
```yaml
this:
  is:
    nothingInteresting: Jimmy With A Law Degree Is Like A Chimp With A Machine Gun.
    really:
      fantastically:
        deep: Is it not?
      absolutely:
        annoying: Indeed
```
```python
cr = Configr("config.yaml", root_key="this.is.really")
cr["fantastically.deep"]
>> Is it not?
cr["absolutely.annoying"]
>> Indeed
```