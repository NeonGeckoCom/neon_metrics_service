# NeonAI Metrics Service
Handles client reported metrics and aggregates data for analysis.

## Request Format
Reported metrics should be in the form of a dictionary. The only required parameter is `name`, any other arbitrary data 
may be included in the request.

>Example Request:
>```json
>{
>  "name": "Metric Name",
>  "arbitrary_data": {},
>  "other_param": "data"
>}
>```

## Response Format
No response is expected.

## Docker Configuration
When running this as a docker container, the `XDG_CONFIG_HOME` envvar is set to `/config`.
A configuration file at `/config/neon/diana.yaml` is required and should look like:
```yaml
MQ:
  port: <MQ Port>
  server: <MQ Hostname or IP>
  users:
    neon_metrics_connector:
      password: <neon_metrics user's password>
      user: neon_metrics
```

For example, if your configuration resides in `~/.config`:
```shell
export CONFIG_PATH="/home/${USER}/.config"
docker run -v ${CONFIG_PATH}:/config neon_metrics_connector
```
> Note: If connecting to a local MQ server, you may need to specify `--network host`